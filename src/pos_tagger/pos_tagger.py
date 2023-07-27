import sys, typing
from .. import parse

def is_verb_rb(word: str, verb_list: list[str], non_verb_list: list[str]) -> typing.Optional[bool]:
	'''
	Rules-based algorithm to determine whether a Nahuatl word is a verb.
	Arguments:
		`word: str`: the word to make the determination on.
		`verb_list: list[str]`: the list of verb lemmas.
		`non_verb_list: list[str]`: the list of non-verb lemmas.
	Returns:
		`bool`: whether or not the word is a verb.
	'''
	noun_morphemes, noun_lemma = parse.parse_noun(word)
	verb_morphemes, verb_lemma = parse.parse_verb(word)
	noun_lemma_pos, verb_lemma_pos = noun_morphemes.index(noun_lemma), verb_morphemes.index(verb_lemma)
	_, absolutive = parse.search_absolutive(word)

	#check for presence in the wordlists
	if noun_lemma in non_verb_list and verb_lemma not in verb_list:
		return False
	elif noun_lemma not in non_verb_list and verb_lemma in verb_list:
		return True

	#check for both object and subject prefixes
	temp_word, prefix = parse.search_prefix(word, parse.SUBJECT_PREFIXES_V)
	if prefix:
		_, obj_prefix = parse.search_prefix(temp_word, parse.OBJECT_PREFIXES_V)
		if obj_prefix:
			return True

	#check for an absolutive suffix
	if absolutive:
		return False

	#check for verb endings
	if verb_lemma.endswith('oa') or verb_lemma.endswith('ia') or verb_morphemes[0] == 'xi':
		return True

	#check for tense and directional suffixes
	for suffix in parse.TENSE_SUFFIXES_V + parse.DIRECTIONAL_SUFFIXES_V:
		if suffix in verb_morphemes[verb_lemma_pos:] and suffix != 'ko':
			return True

	#check for object prefixes
	for prefix in parse.OBJECT_PREFIXES_V:
		if prefix in verb_morphemes[:verb_lemma_pos]:
			return True

	#check for both a genitive prefix and suffix (e.g. <yo>, <wa(n)>)
	if any(prefix in noun_morphemes[:noun_lemma_pos] for prefix in parse.GENITIVE_PREFIXES_N):
		return False

	if any(suffix in noun_morphemes[noun_lemma_pos:] for suffix in parse.DIMINUTIVE_SUFFIXES_N):
		return False

	return None