import re
from pathlib import Path
import logging
import pkg_resources

# TODO: move constants.py->constants/__init__.py and constants_*.py to constants/*.py
from .constants_stopwords import NLTK_STOPWORDS_ENGLISH, STOPWORDS, STOPWORDS_DICT  # noqa
from .constants_uri_schemes import URI_SCHEMES, uri_schemes_iana  # noqa

log = logging.getLogger(__name__)

PKG_DIR = Path(__file__).absolute().resolve().parent
SRC_DATA_DIR = PKG_DIR / 'data'
PKG_NAME = PKG_DIR.name
SRC_DIR = PKG_DIR.parent if PKG_DIR.parent != PKG_NAME else PKG_NAME
REPO_DIR = SRC_DIR.parent

MANUSCRIPT_DIR = SRC_DATA_DIR / 'manuscript'
ADOC_DIR = MANUSCRIPT_DIR / 'adoc'
IMAGES_DIR = MANUSCRIPT_DIR / 'images'

HOME_DIR = Path.home().resolve().absolute()
DATA_DIR_NAME = '.nlpia2-data'
DATA_DIR = PKG_DIR / DATA_DIR_NAME
if not DATA_DIR.is_dir():
    DATA_DIR = REPO_DIR / DATA_DIR_NAME
if not DATA_DIR.is_dir():
    DATA_DIR = HOME_DIR / DATA_DIR_NAME
    # try/except this and use tempfiles python module as backup
    DATA_DIR.mkdir(parents=True, exist_ok=True)

LOG_DIR = Path(DATA_DIR) / 'log'
CONSTANTS_DIR = Path(DATA_DIR) / 'constants'
HISTORY_PATH = Path(DATA_DIR) / 'history.yml'
Path(LOG_DIR).mkdir(exist_ok=True)
Path(CONSTANTS_DIR).mkdir(exist_ok=True)

QUESTIONWORDS = set('who what when were why which how'.split() + ['how come', 'why does', 'can i', 'can you', 'which way'])
QUESTION_STOPWORDS = QUESTIONWORDS | set(STOPWORDS)

SPECIAL_PUNC = {
    "—": "-", "–": "-", "_": "-", '”': '"', "″": '"', '“': '"', '•': '*', '−': '-',
    "’": "'", "‘": "'", "´": "'", "`": "'", '،': ',',
    '\u200b': ' ', '\xa0': ' ', '„': '', '…': ' ... ', '\ufeff': '',
}




def get_version():
    """ Look within setup.cfg for version = ... and within setup.py for __version__ = """
    version = '0.0.0'
    try:
        return pkg_resources.get_distribution(PKG_NAME)
    except Exception as e:
        log.error(e)
        log.warning(f"Unable to find {PKG_NAME} version so using {version}")
    return version

    # setup.cfg will not exist if package install in site-packages
    with (REPO_DIR / 'setup.cfg').open() as fin:
        for line in fin:
            matched = re.match(r'\s*version\s*=\s*([.0-9abrc])\b', line)
            if matched:
                return (matched.groups()[-1] or '').strip()


__version__ = get_version()



# canonical data directory to share data between nlpia2 installations
HOME_DATA_DIR = HOME_DIR / DATA_DIR_NAME
if not HOME_DATA_DIR.is_dir():
    HOME_DATA_DIR.mkdir(parents=True, exist_ok=True)

REPO_DATA_DIR, DATA_DIR = DATA_DIR, HOME_DATA_DIR

# DONE: create nlpia2/init.py
# DONE: add maybe_download() to init.py
# TODO: all required data files up to chapter07
# TODO: add list of all required data files to init.py
# TODO: ensure all files are in HOME_DATA_DIR (DATA_DIR is just a subset)
# TODO: move DATA_DIR constant to data.py
# DATA_FILENAMES = dict(
#     DATA_DIR
# )

if __name__ == '__main__':
    assert MANUSCRIPT_DIR.is_dir()
    assert ADOC_DIR.is_dir()