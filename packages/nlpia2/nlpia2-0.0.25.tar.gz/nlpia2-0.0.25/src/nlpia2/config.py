# nlpia2.config.py
from pathlib import Path

try:
    MODULE_DIR = Path(__file__).resolve().absolute().parent
    DATA_DIR = MODULE_DIR / 'data'
    BASE_DIR = MODULE_DIR.parent
    if BASE_DIR.name == 'src':
        BASE_DIR = MODULE_DIR.parent
except NameError:
    BASE_DIR = DATA_DIR = Path.cwd()
    MODULE_DIR = None

assert DATA_DIR.is_dir()

MANUSCRIPT_DIR = Path.home() / 'code/tangibleai/nlpia-manuscript/manuscript/adoc'
DEFAULT_FILENAME = 'Chapter 03 -- Math with Words (TF-IDF Vectors).adoc'
DEFAULT_FILEPATH = MANUSCRIPT_DIR / DEFAULT_FILENAME
# DEFAULT_DOCTEST_OPTIONFLAGS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
