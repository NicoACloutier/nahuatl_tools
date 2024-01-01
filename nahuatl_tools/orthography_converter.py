import re

#a substitution that will correctly convert most modern orthographies.
#   Can work with `uses_c=True` or `uses_c=False`.
MODERN = {'k': ['qu'],
          'c': ['ch'],
          'j': ['h'], 
          'q': ['kw', 'ku'],
          'z': ['ts', 'tz'],
          'w': ['u'],
          'L': ['tl'],
         }

#a substitution that will correctly convert the classical orthography.
#   Recommended with `uses_c=True`.
CLASSIC = {'k': ['qu'],
           's': ['z'],
           'z': ['ts'],
           'w': ['hu', 'uh'],
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
        text = re.sub(r'([cjlmpqstwxyz])\1', r'\1', text) #remove double consonants
        return text

#a substitution that will correctly convert back to a modern orthography.
#   Recommended with `uses_c_for_s=False`, `uses_c_for_k=False`, `uses_hu=False`, `uses_cu=False`, and `final_double_l=False`.
REVERSE_MODERN = {'c': 'ch',
                  'q': 'kw',
                  'z': 'tz',
                  'L': 'tl',
                  }

#a substitution that will correctly convert back to the classical orthography
#   Recommended with `uses_c_for_s=True`, `uses_c_for_k=True`, `uses_hu=True`, `uses_cu=True`, and `final_double_l=True`.
REVERSE_CLASSIC = {'c': 'ch',
                   'z': 'ts',
                   's': 'z',
                   'L': 'tl',
                   'j': 'h',
                   }

class ReverseOrthography:
    def __init__(self, uses_c_for_s: bool, uses_c_for_k: bool, uses_hu: bool, uses_cu: bool, final_double_l: bool, substitutions: dict[str, list[str]]) -> None:
        
        '''
        Create a reverse orthography object.
        Arguments:
            `uses_c_for_s: bool`: whether or not the orthography uses the grapheme <c> as the phoneme /s/.
            `uses_c_for_k: bool`: whether or not the orthography uses the grapheme <c> as the phoneme /k/.
            `uses_hu: bool`: whether or not the orthography uses the graphemes <hu> as the phoneme /w/.
            `uses_cu: bool`: whether or not the orthography uses the graphemes <cu> as the phoneme /kʷ/.
            `final_double_l: bool`: whether or not the orthography uses a final double <l> on words ending in <li>.
            `substitutions: dict[str, list[str]]`: the direct substitutions that can be made for the orthography.
        Returns:
            `None`
        '''
        self.uses_c_for_s = uses_c_for_s
        self.uses_c_for_k = uses_c_for_k
        self.uses_hu = uses_hu
        self.uses_cu = uses_cu
        self.final_double_l = final_double_l
        self.substitutions = substitutions
    
    def convert(self, text: str) -> str:
        '''
        Convert a text from the common orthography to an orthography of choice.
        Arguments:
            `text: str`: the text to be converted.
        Returns:
            `str`: the converted text.
        '''
        for substitution in self.substitutions:
            text = text.replace(substitution, self.substitutions[substitution])
        if self.uses_c_for_s:
            text = re.sub('z(?=[ei])', 'c', text)
        if self.uses_hu:
            text = re.sub('w(?=[aeiou])', 'hu', text)
            text = re.sub('(?<=[aeiou])w', 'uh', text)
        if self.uses_cu:
            text = re.sub('q(?=[aeiou])', 'cu', text)
            text = re.sub('(?<=[aeiou])q', 'uc', text)
        if self.uses_c_for_k:
            text = re.sub('k(?=[ei])', 'qu', text)
            text = text.replace('k', 'c')
        if self.final_double_l:
            text = re.sub('li\\b', 'lli', text)
        return text