import sys, typing
from .parse import *

COMMON_SUFFIXES = ['ko', 's']
PLURAL_VERB_PREFIXES = ['ti', 'ti', 'in', 'an']
VERB_ENDINGS = ['owa', 'iya', 'oa', 'ia']

def is_verb_rb(word: str, verb_list: typing.Union[list[str], set[str]], non_verb_list: typing.Union[list[str], set[str]]) -> typing.Optional[bool]:
    '''
    Rules-based algorithm to determine whether a Nahuatl word is a verb.
    Arguments:
        `word: str`: the word to make the determination on.
        `verb_list: typing.Union[list[str], set[str]]`: the list of verb stems.
        `non_verb_list: typing.Union[list[str], set[str]]`: the list of non-verb stems.
    Returns:
        `typing.Optional[bool]`: whether or not the word is a verb. If it cannot be determined, returns `None`.
    '''
    verb_list, non_verb_list = (set(verb_list), set(non_verb_list)) if verb_list is list or non_verb_list is list else (verb_list, non_verb_list)
    noun_morphemes, noun_stem = parse_noun(word)
    verb_morphemes, verb_stem = parse_verb(word)
    noun_stem_pos, verb_stem_pos = noun_morphemes.index(noun_stem), verb_morphemes.index(verb_stem)
    _, absolutive = search_absolutive(word)

    #check for presence in the wordlists
    if noun_stem in non_verb_list and verb_stem not in verb_list:
        return False
    elif noun_stem not in non_verb_list and verb_stem in verb_list:
        return True

    #check for both object and subject prefixes
    temp_word, prefix = search_prefix(word, SUBJECT_PREFIXES_V)
    if prefix:
        _, obj_prefix = search_prefix(temp_word, [item for item in OBJECT_PREFIXES_V if item != 'te' and item != 'La'])
        if obj_prefix:
            return True
    
    if word.startswith('kii') or word.startswith('omo'):
        return True

    #check for an absolutive suffix
    if absolutive:
        return False

    #check for plural ending to verb and plural signifier
    if verb_morphemes[:-1] in NUMBER_SUFFIXES_V and any(prefix in verb_morphemes[:verb_stem_pos] for prefix in PLURAL_VERB_PREFIXES):
        return True

    #check for verb endings and optative prefix
    if verb_morphemes[0] == 'xi' or any(verb_stem.endswith(ending) for ending in VERB_ENDINGS):
        return True

    #check for tense and directional suffixes
    for suffix in TENSE_SUFFIXES_V + DIRECTIONAL_SUFFIXES_V:
        if suffix in verb_morphemes[verb_stem_pos:] and suffix not in COMMON_SUFFIXES:
            return True

    #check for object prefixes
    for prefix in OBJECT_PREFIXES_V:
        if prefix in verb_morphemes[:verb_stem_pos]:
            return True

    #check for both a genitive prefix and suffix (e.g. <yo>, <wa(n)>)
    if any(prefix in noun_morphemes[:noun_stem_pos] for prefix in GENITIVE_PREFIXES_N):
        return False

    if any(suffix in noun_morphemes[noun_stem_pos:] for suffix in DIMINUTIVE_SUFFIXES_N):
        return False

    for prefix in SUBJECT_PREFIXES_V:
        if prefix in verb_morphemes[:verb_stem_pos] and any(suffix in verb_morphemes[verb_stem_pos:] for suffix in COMMON_SUFFIXES):
            return True

    return None