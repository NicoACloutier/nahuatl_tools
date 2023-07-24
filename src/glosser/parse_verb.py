import typing

NEGATION_PREFIXES = ['ax']
SUBJECT_PREFIXES = ['ni', 'ti', 'in', 'xi']
REFLEXIVE_PREFIXES = ['no', 'mo']
OBJECT_PREFIXES = ['nec', 'miz', 'tec', 'kin', 'ki', 'k', 'j', 'te', 'La']

DIRECTIONAL_LIST = ['ti', 'to', 'ki', 'ko']
NUMBER_TENSE_LIST = ['j', 'k', 'se', 's']

def search_prefix(word: str, prefixes: list[str]) -> tuple[str, typing.Optional[str]]:
	'''Search a word for a prefix among a list of mutually exclusive prefixes.'''
	for prefix in prefixes:
		if word.startswith(prefix):
			word = word[word.index(prefix)+len(prefix):]
			return word, prefix
	return word, None

def search_suffix(word: str, suffixes: list[str]) -> tuple[str, typing.Optional[str]]:
	'''Search a word for a suffix among a list of mutually exclusive suffixes.'''
	for suffix in suffixes:
		if word.endswith(suffix):
			word = word[:word.index(suffix)]
			return word, suffix
	return word, None

def parse_verb(verb: str) -> list[str]:
	'''Split a verb into its component morphemes.'''
	morphemes = []
	for prefix_list in [NEGATION_PREFIXES, SUBJECT_PREFIXES, REFLEXIVE_PREFIXES, OBJECT_PREFIXES]:
		verb, prefix = search_prefix(verb, prefix_list)
		if prefix:
			morphemes.append(prefix)

	suffixes = []
	for suffix_list in [DIRECTIONAL_LIST, NUMBER_TENSE_LIST]:
		verb, suffix = search_suffix(verb, suffix_list)
		if suffix:
			suffixes.append(suffix)

	morphemes.append(verb)
	morphemes += suffixes[::-1]
	return morphemes