import typing, re

#verb morphemes
NEGATION_PREFIXES_V = ['ax'] #prefixes used for negation
TENSE_PREFIXES_V = ['o'] #past tense prefix.
SUBJECT_PREFIXES_V = ['ni', 'ti', 'in', 'xi'] #prefixes used to mark subjects
REFLEXIVE_PREFIXES_V = ['no', 'mo'] #prefixes used to mark reflexives
OBJECT_PREFIXES_V = ['nec', 'miz', 'tec', 'kin', 'ki', 'k', 'j', 'te', 'La'] #prefixes used to mark objects

DIRECTIONAL_SUFFIXES_V = ['ti', 'to', 'ki', 'ko'] #suffixes used to mark directionals
NUMBER_TENSE_SUFFIXES_V = ['j', 'k', 'se', 's'] #suffixes used to mark tense and number

#noun morphemes
GENITIVE_PREFIXES_N = ['no', 'mo', 'to', 'inin', 'ini', 'in', 'i', 'imo'] #prefixes used to mark possession

ABSOLUTIVE_SUFFIXES_N = {'tli': 'tli', 'tl': 'tl', '(?<=[l])i': 'i', '(?!<=[z])in': 'in'} #suffixes used to mark the absolutive (uses RegEx)
PLURAL_SUFFIXES_N = ['mej', 'me', 'wan', 'wa'] #suffixes used to mark the plural
DIMINUTIVE_SUFFIXES_N = ['zin', 'zi'] #suffixes used to mark the diminutive

def search_prefix(word: str, prefixes: list[str]) -> tuple[str, typing.Optional[str]]:
	'''
	Search a word for a prefix among a list of mutually exclusive prefixes.
	Arguments:
		`word: str`: the word to find prefixes in.
		`prefixes: list[str]`: a list of mutually exclusive prefixes to search for.
	Returns:
		`tuple[str, typing.Optional[str]]`: modified string without found prefix and prefix found, or unmodified string and `None` if none found.
	'''
	for prefix in prefixes:
		if word.startswith(prefix):
			word = word[len(prefix):]
			return word, prefix
	return word, None

def search_suffix(word: str, suffixes: typing.Union[list[str], dict[str, str]], use_regex: bool = False) -> tuple[str, typing.Optional[str]]:
	'''
	Search a word for a suffix among a list of mutually exclusive suffixes.
	Arguments:
		`word: str`: the word to find suffixes in.
		`suffixes: typing.Union[list[str], dict[str, str]]`: list of mutually exclusive suffixes to find, or dict with RegEx keys/plain values if RegEx used.
		`use_regex: bool = False`: whether to use regex for the suffixes.
	Returns:
		`tuple[str, typing.Optional[str]]`: modified string without found suffix and suffix found, or unmodified string and `None` if none found.
	'''
	search = (lambda word, suffix: bool(re.search(f'{suffix}$', word))) if use_regex else (lambda word, suffix: word.endswith(suffix))
	for suffix in suffixes:
		if search(word, suffix):
			used_suffix = suffixes[suffix] if use_regex else suffix
			ind = len(word) - len(used_suffix)
			word = word[:ind]
			return word, used_suffix
	return word, None

def search_absolutive(noun: str) -> tuple[str, typing.Optional[str]]:
	'''
	Search for an absolutive suffix in a noun.
	Arguments:
		`noun: str`: the noun to search in.
	Returns:
		`tuple[str, typing.Optional[str]]`: if absolutive present, tuple of noun w/out absolutive and absolutive. Otherwise, tuple of `noun` and `None`.
	'''
	return search_suffix(noun, ABSOLUTIVE_SUFFIXES_N, use_regex=True)

def lemmatize_word(word: str, prefixes: list[list[str]], suffixes: list[list[str]]) -> str:
	'''
	Return the lemma of a word.
	Arguments:
		`word: str`: the word to gloss.
		`prefixes: list[list[str]]`: a list of lists of mutually exclusive prefixes in order of appearance from beginning.
		`suffixes: list[list[str]]`: a list of lists of mutually exclusive suffixes in order of appearance from end.
	Returns:
		`str`: the lemma of the word.
	'''
	for prefix_list in prefixes:
		word, _ = search_prefix(word, prefix_list)
	for suffix_list in suffixes:
		word, _ = search_suffix(word, suffix_list)
	return word

def lemmatize_noun(noun: str) -> str:
	'''
	Lemmatize a noun.
	Arguments:
		`noun: str`: the noun to lemmatize.
	Returns:
		`str`: the lemma of the noun.
	'''
	noun, absolutive = search_absolutive(noun)
	return noun if absolutive else lemmatize_word(noun, [GENITIVE_PREFIXES_N], [PLURAL_SUFFIXES_N, DIMINUTIVE_SUFFIXES_N])

def parse_word(word: str, prefixes: list[list[str]], suffixes: list[list[str]]) -> list[str]:
	'''
	Split a word into its component morphemes.
	Arguments:
		`word: str`: the word to gloss.
		`prefixes: list[list[str]]`: a list of lists of mutually exclusive prefixes in order of appearance from beginning.
		`suffixes: list[list[str]]`: a list of lists of mutually exclusive suffixes in order of appearance from end.
	Returns:
		`list[str]`: the list of morphemes in the word.
	'''
	morphemes = []
	for prefix_list in prefixes:
		word, prefix = search_prefix(word, prefix_list)
		if prefix:
			morphemes.append(prefix)

	found_suffixes = []
	for suffix_list in suffixes:
		word, suffix = search_suffix(word, suffix_list)
		if suffix:
			found_suffixes.append(suffix)

	morphemes.append(word)
	morphemes += found_suffixes[::-1]
	return morphemes

def parse_verb(verb: str) -> list[str]:
	'''
	Parse a verb for morphemes.
	Arguments:
		`verb: str`: the verb to be parsed.
	Returns:
		`list[str]`: a list of morphemes in the verb.
	'''
	return parse_word(verb, [NEGATION_PREFIXES_V, SUBJECT_PREFIXES_V, REFLEXIVE_PREFIXES_V, OBJECT_PREFIXES_V], 
					  [DIRECTIONAL_SUFFIXES_V, NUMBER_TENSE_SUFFIXES_V])

def parse_noun(noun: str) -> list[str]:
	'''
	Parse a noun for morphemes.
	Arguments:
		`noun: str`: the noun to be parsed.
	Returns:
		`list[str]`: the list of morphemes in the noun.
	'''
	noun, absolutive = search_absolutive(noun)
	return [noun, absolutive] if absolutive else parse_word(noun, [GENITIVE_PREFIXES_N], [PLURAL_SUFFIXES_N, DIMINUTIVE_SUFFIXES_N])