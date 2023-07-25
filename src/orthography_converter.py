import re

#a substitution that will correctly convert most modern orthographies
MODERN = {'j': ['h'], 
		  'k': ['qu'],
		  'q': ['kw', 'ku'],
		  'z': ['ts', 'tz'],
		  'w': ['u'],
		  'L': ['tl'],
		 }

#a substitution that will correctly convert the classical orthography
CLASSIC = {'k': ['qu'],
		   's': ['z'],
		   'z': ['ts'],
		   'w': ['hu', 'uh', 'u'],
		   'L': ['tl'],
		  }

class Orthography:
	'''
	Defines a Nahuatl orthography and has methods to convert text from this orthography to the common orthography.
	The common orthography uses one grapheme for every phoneme, does not use double letters. 
	The vowels are all the same as their IPA equivalents, and the consonants are as follows:
		/tʃ/: <c> (unvoiced postalveolar affricate)
		/h/: <j> (unvoiced glottal fricative)
		/k/: <k> (unvoiced velar plosive)
		/l/: <l> (voiced lateral approximant)
		/tɬ/: <L> (unvoiced lateral affricate)
		/m/: <m> (voiced bilabial nasal)
		/n/: <n> (voiced alveolar nasal)
		/p/: <p> (unvoiced bilabial plosive)
		/kʷ/: <q> (unvoiced labialized velar plosive)
		/s/: <s> (unvoiced alveolar approximant)
		/t/: <t> (unvoiced alveolar plosive)
		/w/: <w> (voiced bilabial approximant)
		/ʃ/: <x> (unvoiced postalveolar fricative)
		/j/: <y> (voiced palatal approximant)
		/c/: <z> (unvoiced alveolar affricate)
	This orthography is not meant to be used for actual writing, it is just useful to have a one-to-one orthography for processing.

	Instance variables:
		`self.uses_c: bool`: whether or not the orthography uses the grapheme <c> as the phonemes /k/ and /s/.
		`self.has_doubles: bool`: hether or not the orthography has repeated graphemes representing a single morpheme.
		`self.substitutions: dict[str, list[str]]`: direct substitutions. Keys are graphemes in common orthography, values are list of reps in other.
	'''

	def __init__(self, uses_c: bool, substitutions: dict[str, list[str]]) -> None:
		'''
		Create an orthography object.
		Arguments:
			`uses_c: bool`: whether or not the orthography uses the grapheme <c> as the phonemes /k/ and /s/.
			`substitutions: dict[str, list[str]]`: the direct substitutions that can be made for the orthography.
		Returns:
			`None`
		'''
		self.uses_c = uses_c
		self.substitutions = substitutions

	def c_convert(self, text: str) -> str:
		'''
		Convert the instances of the grapheme <c> in a text with the proper phonemes.
		Arguments:
			`text: str`: the text to be converted.
		Returns:
			`str`: the converted text.
		'''
		text = re.sub('c(?=[ie])', 's', text)
		text = re.sub('c(?=[oa])', 'k', text)
		text = text.replace('cu', 'q')
		text = text.replace('cz', 's')
		text = text.replace('c', 'k')
		return text.replace('kh', 'c')

	def convert(self, text: str) -> str:
		'''
		Convert a text to the common orthography.
		Arguments:
			`text: str`: the text to be converted.
		Returns:
			`str`: the converted text.
		'''
		text = self.c_convert(text.lower()) if self.uses_c else text.lower()
		for phoneme in self.substitutions:
			for grapheme in self.substitutions[phoneme]:
				text = text.replace(grapheme, phoneme)
		text = re.sub(r'([cjlmnpqstwxyz])\1', r'\1', text) #remove double consonants except <l>
		return text