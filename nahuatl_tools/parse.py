import typing, re

VOWELS = ['a', 'e', 'i', 'o', 'u']

#verb morphemes
NEGATION_PREFIXES_V = ['ax'] #prefixes used for negation
TENSE_PREFIXES_V = ['o'] #past tense prefix
SUBJECT_PREFIXES_V = ['ni', 'ti', 'an', 'xi'] #prefixes used to mark subjects
REFLEXIVE_PREFIXES_V = ['no', 'mo'] #prefixes used to mark reflexives
OBJECT_PREFIXES_V = ['nec', 'miz', 'tec', 'kin', 'mec', 'ki', 'k', 'j', 'te', 'La'] #prefixes used to mark objects
COMMON_PREFIXES_V = ['nel'] #common semantic prefixes
DIRECTIONAL_PREFIXES_V = ['wal', 'on'] #directional prefixes

NUMBER_SUFFIXES_V = ['j'] #suffixes used to mark number
DIRECTIONAL_SUFFIXES_V = ['ti', 'to', 'toya', 'ki', 'ko', 'koya'] #suffixes used to mark directionals
TENSE_SUFFIXES_V = ['se', 's', 'yaya', 'ktok', 'jtok', 'k', 'ke', 'ya'] #suffixes used to mark tense or aspect
CAUSATIVE_SUFFIXES_V = ['ltia', 'lti', 'ti'] #suffixes used to mark the causative
OPTATIVE_PLURAL_SUFFIXES_V = ['ka', 'kan'] #optative plural suffixes

#noun morphemes
GENITIVE_PREFIXES_N = ['no', 'mo', 'to', 'inin', 'ini', 'in', 'i', 'imo'] #prefixes used to mark possession
DIMINUTIVE_PREFIXES_N = ['pil'] #prefixes used to mark the diminutive

ABSOLUTIVE_SUFFIXES_N = {'(?<!=[aeiou])Li': 'Li', '(?<=[aeiou])L': 'L', '(?<=[l])i': 'i', '(?!<=[z])in': 'in'} #suffixes used to mark the absolutive (uses RegEx)
PLURAL_SUFFIXES_N = ['mej', 'me'] #suffixes used to mark the plural
GENITIVE_SUFFIXES_N = ['wan', 'wa', 'yo'] #suffixes used with the genitive
DIMINUTIVE_SUFFIXES_N = ['zizin', 'zinzin', 'zin', 'zizi', 'zi', 'pil'] #suffixes used to mark the diminutive

def search_prefix(word: str, prefixes: typing.Union[list[str], dict[str, str]]) -> tuple[str, typing.Optional[str]]:
    '''
    Search a word for a prefix among a list of mutually exclusive prefixes.
    Arguments:
        `word: str`: the word to find prefixes in.
        `prefixes: typing.Union[list[str], dict[str, str]]`: a list of mutually exclusive prefixes to search for, or dict with RegEx keys/plain values if RegEx used.
    Returns:
        `str`: modified string without found prefix or original string if none found.
        `typing.Optional[str]`: prefix found or `None` if none found.
    '''
    use_regex = isinstance(prefixes, dict)
    search = (lambda word, prefix: bool(re.search(f'^{prefix}', word))) if use_regex else (lambda word, prefix: word.startswith(prefix))
    for prefix in prefixes:
        if search(word, prefix):
            used_prefix = prefixes[prefix] if use_regex else prefix
            word = word[len(used_prefix):]
            return word, used_prefix
    return word, None

def search_suffix(word: str, suffixes: typing.Union[list[str], dict[str, str]]) -> tuple[str, typing.Optional[str]]:
    '''
    Search a word for a suffix among a list of mutually exclusive suffixes.
    Arguments:
        `word: str`: the word to find suffixes in.
        `suffixes: typing.Union[list[str], dict[str, str]]`: list of mutually exclusive suffixes to find, or dict with RegEx keys/plain values if RegEx used.
    Returns:
        `str`: modified string without found suffix or original string if none found.
        `typing.Optional[str]`: suffix found or `None` if none found.
    '''
    use_regex = isinstance(suffixes, dict)
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
        `str`: noun without absolutive if absolutive present, otherwise initial noun.
        `typing.Optional[str]`: absolutive if present otherwise `None`.
    '''
    return search_suffix(noun, ABSOLUTIVE_SUFFIXES_N)

def search_genitive(noun: str) -> tuple[str, typing.Optional[str]]:
    '''
    Search for a gentive prefix in a noun.
    Arguments:
        `noun: str`: the noun to search in.
    Returns:
        `str`: noun without geniitive if genitive present, otherwise initial noun.
        `typing.Optional[str]`: genitive if present otherwise `None`.
    '''
    return search_prefix(noun, GENITIVE_PREFIXES_N)

def parse_word(word: str, prefixes: list[list[str]], suffixes: list[list[str]], stems: typing.Optional[set[str]] = None) -> tuple[list[str], str]:
    '''
    Split a word into its component morphemes.
    Arguments:
        `word: str`: the word to gloss.
        `prefixes: list[list[str]]`: a list of lists of mutually exclusive prefixes in order of appearance from beginning.
        `suffixes: list[list[str]]`: a list of lists of mutually exclusive suffixes in order of appearance from end.
        Optional:
        `stems: typing.Optional[set[str]] = None`: a set of stems to check for.
    Returns:
        `list[str]`: the list of morphemes in the word.
        `str`: the stem of the word.
    '''
    morphemes = []
    for prefix_list in prefixes:
        word, prefix = search_prefix(word, prefix_list)
        if prefix:
            morphemes.append(prefix)
        if stems and word in stems:
            morphemes.append(word)
            return morphemes, word

    found_suffixes = []
    for suffix_list in suffixes:
        word, suffix = search_suffix(word, suffix_list)
        if suffix:
            found_suffixes.append(suffix)
        if stems and word in stems:
            morphemes.append(word)
            morphemes += found_suffixes[::-1]
            return morphemes, word

    morphemes.append(word)
    morphemes += found_suffixes[::-1]
    return morphemes, word

def join_on_illegal_sequence(morphemes: list[str], stem: str) -> tuple[list[str], str]:
    '''
    Join a stem with the previous morpheme if that stem begins with two consonants.
    Arguments:
        `morphemes: list[str]`: a list of morphemes in the word.
        `stem: str`: the stem of the word.
    Returns:
        `list[str]`: the morphemes after joining the stem on illegal sequences.
        `str`: the stem after being joined on illegal sequences.
    '''
    if len(stem) == 0 or (stem[0] not in VOWELS and (len(stem) == 1 or stem[1] not in VOWELS)):
        stem_index = morphemes.index(stem)
        if stem_index == 0:
            return morphemes, stem
        stem = morphemes[stem_index-1] + stem
        morphemes = morphemes[:stem_index-1] + [stem,] + morphemes[stem_index+1:]
    return morphemes, stem

def parse_verb(verb: str, stems: typing.Optional[set[str]] = None) -> tuple[list[str], str]:
    '''
    Parse a verb for morphemes.
    Arguments:
        `verb: str`: the verb to be parsed.
        Optional:
        `stems: typing.Optional[set[str]] = None`: a set of stems to check for.
    Returns:
        `list[str]`: a list of morphemes in the verb.
        `str`: the stem of the verb.
    '''
    morphemes, stem = parse_word(verb, [NEGATION_PREFIXES_V, TENSE_PREFIXES_V, SUBJECT_PREFIXES_V], [], stems=stems)
    new_morphemes, stem = parse_word(stem, [REFLEXIVE_PREFIXES_V, OBJECT_PREFIXES_V, COMMON_PREFIXES_V, DIRECTIONAL_PREFIXES_V], 
                      [NUMBER_SUFFIXES_V, DIRECTIONAL_SUFFIXES_V, TENSE_SUFFIXES_V, CAUSATIVE_SUFFIXES_V] + ([OPTATIVE_PLURAL_SUFFIXES_V,] if morphemes[0] == 'xi' else []), stems=stems)
    morphemes = morphemes[:-1] + new_morphemes
    return join_on_illegal_sequence(morphemes, stem)

def stem_verb(verb: str, stems: typing.Optional[set[str]] = None) -> str:
    '''
    Stem a verb.
    Arguments:
        `verb: str`: the verb to stem.
        Optional:
        `stems: typing.Optional[set[str]] = None`: a set of stems to check for.
    Returns:
        `str`: the stem of the verb.
    '''
    return parse_verb(verb, stems=stems)[1]

def parse_noun(noun: str, stems: typing.Optional[set[str]] = None) -> tuple[list[str], str]:
    '''
    Parse a noun for morphemes.
    Arguments:
        `noun: str`: the noun to be parsed.
        Optional:
        `stems: typing.Optional[set[str]] = None`: a set of stems to check for.
    Returns:
        `list[str]`: the list of morphemes in the noun.
        `str`: the stem of the noun.
    '''
    cut_noun, absolutive = search_absolutive(noun)
    if not absolutive:
        _, genitive = search_genitive(noun)
        suffixes = [DIMINUTIVE_SUFFIXES_N, GENITIVE_SUFFIXES_N] if genitive else [PLURAL_SUFFIXES_N, DIMINUTIVE_SUFFIXES_N]
        return join_on_illegal_sequence(*parse_word(noun, [SUBJECT_PREFIXES_V, GENITIVE_PREFIXES_N, DIMINUTIVE_PREFIXES_N], suffixes, stems=stems))
    else:
        morphemes, stem = parse_word(cut_noun, [SUBJECT_PREFIXES_V, DIMINUTIVE_PREFIXES_N], [DIMINUTIVE_SUFFIXES_N], stems=stems)
        return join_on_illegal_sequence(morphemes + [absolutive,], stem)

def stem_noun(noun: str, stems: typing.Optional[set[str]] = None) -> str:
    '''
    Stem a noun.
    Arguments:
        `noun: str`: the noun to stem.
        Optional:
        `stems: typing.Optional[set[str]] = None`: a set of stems to check for.
    Returns:
        `str`: the stem of the noun.
    '''
    return parse_noun(noun, stems=stems)[1]