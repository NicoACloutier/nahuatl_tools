import re

MODERN = {'j': ['h'], 
		  'k': ['qu'],
		  'q': ['kw', 'ku'],
		  'z': ['ts', 'tz'],
		  'w': ['u'],
		  'L': ['tl'],
		 }

CLASSIC = {'k': ['qu'],
		   's': ['z'],
		   'z': ['ts'],
		   'w': ['hu', 'uh', 'u'],
		   'L': ['tl'],
		  }

class Orthography:
	def __init__(self, uses_c: bool, substitutions: dict[str, list[str]]):
		'''Create an orthography object.'''
		self.uses_c = uses_c
		self.substitutions = substitutions

	def c_convert(self, text: str) -> str:
		'''Convert the instances of the grapheme `c` in a text with the proper phonemes.'''
		text = re.sub('c(?=[ie])', 's', text)
		text = re.sub('c(?=[oa])', 'k', text)
		text = text.replace('cu', 'q')
		text = text.replace('cz', 's')
		text = text.replace('c', 'k')
		return text.replace('kh', 'c')

	def convert(self, text: str) -> str:
		'''Convert a text to the common orthography.'''
		text = self.c_convert(text.lower()) if self.uses_c else text.lower()
		for phoneme in self.substitutions:
			for grapheme in self.substitutions[phoneme]:
				text = text.replace(grapheme, phoneme)
		text = re.sub(r'([cjklmnpqstwxyz])\1', r'\1', text) #remove double consonants
		return text