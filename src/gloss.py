import typing
from .parse import *
from .pos_tagger import *

class Verb():
    '''
    A morphological verb representation in Nahuatl.
    Instance variables:
        `self.word: str`: the string representation of the word in full. 
        `self.morphemes: list[str]`: the morphemes in the word.
        `self.prefix_index: int`: an index used internally for prefix searching.
        `self.suffix_index: int`: an index used internally for suffix searching. 
        `self.plural: bool`: whether the subject/agent of the verb is plural. 
        `self.negative: bool`: whether the verb is negative. 
        `self.tense: typing.Optional[str]`: the tense of the verb. 
        `self.optative: bool`: whether the verb is in the second person optative (does not count use of "ma" as an external third/first person optative marker).
        `self.person: int`: the person of the subject/agent of the verb, could be `1`, `2`, or `3`.
        `self.reflexive: bool`: whether the verb is reflexive.
        `self.object: typing.Optional[str]`: gives the object information on the verb, see the constant `OBJECT_MATCHER` defined in the `Verb` class for structure. 
        `self.impersonal: typing.Optional[bool]`: `True` if there is an impersonal prefix ("te" or "La"/"tla"), `False` if there is an object prefix but it's personal, `None` otherwise.
        `self.direction: typing.Optional[str]`: `'towards'` if the verb has the "wal" prefix, `'away'` if it has the "on" prefix, and `None` otherwise.
    '''
    SUBJECT_MATCHER = {'s-ni': 1, 's-ti': 2, 'p-ti': 1, 'p-an': 2} #matches subject markers and numbers
    OBJECT_MATCHER = {'nec': '1-singular', 'miz': '2-singular', 'tec': '1-plural', 'kin': '3-plural', 'mec': '2-plural', 
                      'ki': '3-singular', 'k': '3-singular', 'j': '3-singular', 'te': 'impersonal-person', 'La': 'impersonal-nonperson'} #matches object markers

    def __init__(self, word: str) -> None:
        '''
        Initialize a verb.
        Arguments:
            `word: str`: the string representation of the verb.
        Returns:
            `None`
        '''
        self.word = word
        self.morphemes = parse_verb(word)[1]
        self.prefix_index, self.suffix_index = 0, len(self.morphemes)-1
        self.plural = self.search_plural()
        self.get_negative().get_past_prefix().get_subject_person().get_reflexive().get_object().get_direction()
    
    def search_plural(self) -> bool:
        '''
        Search for a plural ending in a verb.
        Arguments:
            `None`
        Returns:
            `bool`: `True` if there is a plural marker, `False` otherwise.
        '''
        if len(self.morphemes) >= 1 and self.morphemes[0] == 'xi':
            return self.morphemes[-1] in OPTATIVE_PLURAL_SUFFIXES_V
        return self.morphemes[-1] == 'j'
    
    #prefix searching methods
    def get_negative(self) -> Verb:
        '''
        Get the negative prefix if present, write information to the `self.negative` instance variable.
        Arguments:
            `None`
        Returns:
            `Verb`: the `Verb` object this method was called on.
        '''
        if self.morphemes[self.prefix_index] in NEGATION_PREFIXES_V:
            self.negative = True
            self.prefix_index += 1
        else:
            self.negative = False
        return self
    
    def get_past_prefix(self) -> Verb:
        '''
        Get the past prefix if present, write information to the `self.tense` instance variable.
        Arguments:
            `None`
        Returns:
            `Verb`: the `Verb` object this method was called on.
        '''
        if self.morphemes[self.prefix_index] in TENSE_PREFIXES_V:
            self.tense = 'past'
            self.prefix_index += 1
        else:
            self.tense = None
        return self
    
    def get_subject_person(self) -> Verb:
        '''
        Get the subject prefix if present, write information to the `self.person` and `self.optative` instance variables.
        Arguments:
            `None`
        Returns:
            `Verb`: the `Verb` object this method was called on.
        '''
        if self.morphemes[self.prefix_index] == 'xi':
            self.optative = True
            self.person = 2
            self.prefix_index += 1
        elif f'{"p" if self.plural else "s"}-{self.morphemes[self.prefix_index]}' in SUBJECT_MATCHER:
            self.person = SUBJECT_MATCHER[f'{"p" if self.plural else "s"}-{self.morphemes[self.prefix_index]}']
            self.optative = False
            self.prefix_index += 1
        else:
            self.optative = False
            self.person = 3
        return self
    
    def get_reflexive(self) -> Verb:
        '''
        Get the reflexive prefix if present, write information to the `self.reflexive` instance variable.
        Arguments:
            `None`
        Returns:
            `Verb`: the `Verb` object this method was called on.
        '''
        if (self.person == 1 and self.morphemes[self.prefix_index] == 'no') or self.morphemes[self.prefix_index] == 'mo':
            self.reflexive = True
            self.prefix_index += 1
        else:
            self.reflexive = False
        return self
    
    def get_object(self) -> Verb:
        '''
        Get the object prefix if present, write information to the `self.object` and `self.impersonal` instance variables.
        Arguments:
            `None`
        Returns:
            `Verb`: the `Verb` object this method was called on.
        '''
        if self.morphemes[self.prefix_index] in OBJECT_MATCHER:
            self.object = OBJECT_MATCHER[self.morphemes[self.prefix_index]]
            self.prefix_index += 1
            self.impersonal = self.object.startswith('impersonal')
        else:
            self.object = None
            self.impersonal = None
        return self
    
    def get_direction(self) -> Verb:
        '''
        Get the direction prefix if present, write information to the `self.direction` instance variable.
        Arguments:
            `None`
        Returns:
            `Verb`: the `Verb` object this method was called on.
        '''
        if self.morphemes[self.prefix_index] in DIRECTIONAL_PREFIXES_V:
            self.direction = 'towards' if self.morphemes[self.prefix_index] == 'wal' else 'away'
            self.prefix_index += 1
        else:
            self.direction = None
        return self
    
class Noun():
    def __init__(self, word: str) -> None:
        self.word = word
        self.morphemes = parse_noun(word)[1]
        self.prefix_index, self.suffix_index = 0, len(self.morphemes)-1

class Other():
    def __init__(self, word: str) -> None:
        self.word = word
        self.morphemes = [word,]

def make_word(word: str) -> tuple[typing.Union[Verb, Noun, Other], typing.Optional[bool]]:
    is_verb = is_verb_rb(word)
    if is_verb == None:
        return Other(word), None
    elif is_verb:
        return Verb(word), True
    else:
        return Noun(word), False