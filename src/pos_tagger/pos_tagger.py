import sys
from .. import parse

def is_verb_rb(word: str, verb_list: list[str], non_verb_list: list[str]) -> bool:
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
	_, absolutive = parse.search_absolutive(word)

	#check for presence in the wordlists
	if noun_lemma in non_verb_list and verb_lemma not in verb_list:
		return False
	elif noun_lemma not in non_verb_list and verb_lemma in verb_list:
		return True

	#check for an absolutive suffix
	if absolutive:
		return False

	#check for verb endings
	if verb_lemma.endswith('oa') or verb_lemma.endswith('ia') or verb_morphemes[0] == 'xi':
		return True

	for suffix in parse.TENSE_SUFFIXES_V + parse.DIRECTIONAL_SUFFIXES_V:
		if suffix in verb_morphemes:
			return True

	return False