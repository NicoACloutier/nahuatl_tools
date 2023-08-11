import typing
import parse, orthography_converter, pos_tagger

ORTHO_DICT = {'modern': orthography_converter.Orthography(uses_c=False, substitutions=orthography_converter.MODERN),
              'classical': orthography_converter.Orthography(uses_c=True, substitutions=orthography_converter.CLASSIC),}

def agglutination_checker(parse_output: tuple[list[str], str], nouns: list[str]) -> list[str]:
    '''
    Check for compound words given a list of initial candidates for the compound.
    Arguments:
        `parse_output: tuple[list[str], str]`: the output of the parsing function applied to a word.
        `nouns: list[str]`: the list of initial candidates for the compound.
    Returns:
        `list[str]`: the list of morphemes in the word, including compounds if any found.
    '''
    lemma_ind = parse_output[0].index(parse_output[1])
    new_lemma, noun = parse.search_prefix(parse_output[1], nouns)
    if noun:
        return parse_output[0][:lemma_ind] + [noun, new_lemma] + parse_output[0][lemma_ind+1:]
    return parse_output[0]

def tokenize_text(text: str, basic: list[str] = [], verb_lemmas: list[str] = [], noun_lemmas: list[str] = [], agglutination_check: bool = False, 
                  convert_ortho: typing.Optional[typing.Union[orthography_converter.Orthography, str]] = None) -> list[list[str]]:
    '''
    Perform the complete tokenization process on a Nahuatl text.
    Arguments:
        `text: str`: the full text to be converted, with spaces in between words.
        `basic: list[str] = []`: a list of basic words not to be parsed at all.
        `verb_lemmas: list[str] = []`: a list of verb lemmas to be used for analysis.
        `noun_lemmas: list[str] = []`: a list of noun lemmas to be used for analysis.
        `agglutination_check: bool = False`: whether or not to check for noun incorporation and compounding. Does not by default.
        `convert_ortho: typing.Optional[typing.Union[orthography_converter.Orthography, str]] = None`: the orthography used to convert text, or the string 'modern' or 'classical' for pre-built orthographies, or `None`, meaning no orthography conversion will occur.
    Returns:
        `list[list[str]]`: a list of lists of morphemes in each word in the text.
    '''
    #convert orthography if applicable
    if isinstance(convert_ortho, str):
        text = ORTHO_DICT[convert_ortho].convert(text)
    elif convert_ortho:
        text = convert_ortho.convert(text)
    
    #do the actual parsing
    words = [word for word in list(set(text.split())) if word not in basic]
    classes = [pos_tagger.is_verb_rb(word, verb_lemmas, noun_lemmas) for word in words]
    parsed_words = [(parse.parse_verb(word) if classes[i] else parse.parse_noun(word)) for i, word in enumerate(words)]
    
    #check for noun incorporation/agglutination if applicable
    if agglutination_check:
        parsed_words = [agglutination_checker(word, noun_lemmas) for word in parsed_words]
    
    #replace words in text
    parsings = {word: parsed_words[i] for i, word in enumerate(words)}
    return [parsings[word][0] for word in text.split()]