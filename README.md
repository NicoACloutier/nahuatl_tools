`nahuatl_tools`: a selection of tools for Nahuatl NLP, designed to be fast, simple, and easy to use. It has no library dependencies other than those included in base Python. All code files have fully documented functions for ease of use. Download with `pip`: `pip install nahuatl_tools`

For all features of `nahuatl_tools`, it is expected that the text be in an orthography designed for a one-to-one phoneme to grapheme conversion. For automatic orthography conversion, see `nahuatl_tools/orthography_converter.py`. The wordlists are also written with this orthography.

Features:
- Morphological segmentation (see `nahuatl_tools/parse.py`)
- Stemming (see `nahuatl_tools/parse.py`)
- Part-of-speech tagging (see `nahuatl_tools/pos_tagger.py`)
- Full text tokenization/morpheme segmentation pipeline, including optional orthography conversion (see `nahuatl_tools/tokenizer.py`)
- Wordlists and lists of stems (see `wordlists/`)
- Morpheme glosser (see `nahuatl_tools/gloss.py`)

For questions, suggestions, or anything else, email `nicocloutier1@gmail.com`.