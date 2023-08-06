# nlpia2.__init__.py
from pathlib import Path

try:
    DATA_DIR = Path(__file__).parent / 'data'
except NameError:
    DATA_DIR = Path.cwd()

assert DATA_DIR.is_dir()

MANUSCRIPT_DIR = Path.home() / 'code/tangibleai/nlpia-manuscript/manuscript/adoc'
DEFAULT_FILENAME = 'Chapter 03 -- Math with Words (TF-IDF Vectors).adoc'
DEFAULT_FILEPATH = MANUSCRIPT_DIR / DEFAULT_FILENAME
# DEFAULT_DOCTEST_OPTIONFLAGS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
