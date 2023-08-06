import argparse
import doctest
from doctest import DocTestParser
from parsimonious import Grammar
from pathlib import Path
import pandas as pd
import re
import tempfile

from nlpia2.text_processing.re_patterns import RE_URL_WITH_SCHEME, RE_URL_SIMPLE  # noqa
from nlpia2.constants import SRC_DATA_DIR

RE_TEXT_LINE = r"^[A-Z_\*][-A-Za-z\ 0-9 :\";',!@#$%^&*()_+-={}<>?,.\/]+"
RE_TITLE_LINE = r"^[=]+[A-Za-z0-9\ \-?!,]+"
RE_MARKUP_LINE = r"^[\[][A-Za-z0-9,\ ]+[\]]"
RE_CODE_OR_OUTPUT = r"^(>>>|\.\.\.|[a-z0-9\-\+]+|\(|[\ ]+).*"
RE_CODE_COMMENT=r"^[<].*"
RE_METADATA = r"^[:].*"
RE_EMPTY_LINE = r"^[ \t]*$"
RE_FIGURE_NAME=r"^[\.].*"
RE_SEPARATOR=r"^(\-\-\-\-|====)[\-=]*\s*"
RE_COMMENT=r"^(\\\\|\/\/).*"

from nlpia2 import MANUSCRIPT_DIR

MANUSCRIPT_DIR = MANUSCRIPT_DIR or Path.home() / 'code/tangibleai/nlpia-manuscript/manuscript/adoc'
DATA_DIR = SRC_DATA_DIR

assert DATA_DIR.is_dir()

MANUSCRIPT_DIR = SRC_DATA_DIR / 'book_adoc'

assert MANUSCRIPT_DIR.is_dir()

DEFAULT_FILENAME = 'Chapter-01_Machines-that-can-read-and-write-NLP-overview'
DEFAULT_FILEPATH = MANUSCRIPT_DIR / DEFAULT_FILENAME
DEFAULT_LINES_FILENAME = 'nlpia_lines.csv'
DEFAULT_OPTIONFLAGS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE


def extract_blocks(filepath=Path('data/tests/test.adoc'), grammarpath=Path('data/grammars/adoc.ppeg')):
    filepath, grammarpath = Path(filepath), Path(grammarpath)
    g = Grammar(grammarpath.open().read())
    ast = g.parse(filepath.open().read())
    return ast

def extract_lines(text=DEFAULT_FILEPATH, with_meta=True):
    filepath, filename = '', ''
    if (isinstance(text, Path) or len(text) < 1024) and Path(text).is_file():
        filepath = Path(text)
        filename = filepath.name
        text = filepath.read_text(encoding='utf-8')

    lines = []
    for i, line in enumerate(text.splitlines()):
        lines.append(dict(
         line_text=line,
         line_number=i,
         filename=filename,
         is_text=(re.match(RE_TEXT_LINE, line) is not None),
         is_empty=(re.match(RE_EMPTY_LINE, line) is not None),
         is_code_or_output=(re.match(RE_CODE_OR_OUTPUT, line) is not None),
         is_title=(re.match(RE_TITLE_LINE, line) is not None),
         is_metadata=(re.match(RE_METADATA, line) is not None),
         is_code_comment=(re.match(RE_CODE_COMMENT, line) is not None),
         is_markup=(re.match(RE_MARKUP_LINE, line) is not None),
         is_figure_name=(re.match(RE_FIGURE_NAME, line) is not None),
         is_separator=(re.match(RE_SEPARATOR, line) is not None),
         is_comment=(re.match(RE_COMMENT, line) is not None)
            )
        )
    return lines


def extract_code_lines(filepath=DEFAULT_FILEPATH, with_metadata=True):
    """ Extract lines of Python using DocTestParser, return list of strs """
    expressions = extract_expressions(filepath=filepath)
    if with_metadata:
        return [vars(ex) for ex in expressions]
    return [ex.source for ex in expressions]


def extract_expressions(filepath=DEFAULT_FILEPATH):
    """ Use doctest.DocTestParser to find lines of Python code in doctest format """
    text = Path(filepath).open('rt').read()
    dtparser = DocTestParser()
    return dtparser.get_examples(text)


def extract_urls_from_text(text=DEFAULT_FILEPATH, with_meta=True):
    """ Find all URLs in the file at filepath, return a list of dicts with urls """
    filepath, filename = '', ''
    if (isinstance(text, Path) or len(text) < 1024) and Path(text).is_file():
        filepath = Path(text)
        filename = filepath.name
        text = filepath.read_text(encoding='utf-8')
    urls = []
    for i, line in enumerate(text.splitlines()):
        for k, match in enumerate(re.finditer(RE_URL_SIMPLE, line)):
            urls.append(dict(
                scheme=match.group('scheme_type') or '',
                url=match.group('url') or '',
                url_path=match.group('path') or '',
                tld=match.group('tld') or '',
                line_number=i,
                url_number=k,
                line_text=line,
                filepath=str(filepath),
                filename=filename
            ))
    return urls


def extract_lists_from_files(input_dir=MANUSCRIPT_DIR, glob='*.adoc',
                             extractor=extract_urls_from_text, with_meta=True):
    """ Find all URLs in files at input_dir, return a list of dicts with urls """
    outputs = []
    for p in input_dir.glob(glob):
        df = extractor(filepath=p, with_meta=with_meta)
        outputs.append(df)
    return outputs


extract_lists = extract_lists_from_files


def extract_url_lists_from_files(input_dir=MANUSCRIPT_DIR, glob='*.adoc',
                                 extractor=extract_urls_from_text, with_meta=True):
    """ Find all URLs in files at input_dir, return a list of dicts with urls """
    outputs = []
    for p in input_dir.glob(glob):
        df = extractor(p, with_meta=with_meta)
        outputs.append(df)
    return outputs


extact_url_lists = extract_url_lists_from_files


def extract_urls(texts=MANUSCRIPT_DIR, glob='*.adoc', with_meta=True):
    if (isinstance(texts, Path) or len(texts) < 1024):
        if Path(texts).is_file():
            return extract_urls_from_text(text=texts, with_meta=with_meta)
        elif Path(texts).is_dir():
            glob = glob or '*'
            return extract_url_lists_from_files(
                input_dir=texts, glob='*.adoc', with_meta=with_meta)
    return extract_urls_from_text(text=texts, with_meta=with_meta)


def extract_urls_df(filepath=DEFAULT_FILEPATH, with_meta=True):
    """ Use regex to extract URLs from text file, return DataFrame with url column """
    urls = extract_urls_from_text(filepath=filepath, with_meta=with_meta)
    df = pd.DataFrame(urls, index=[
        f"{u['line_number']}-{u['url_number']}" for u in urls])
    df['filename'] = filepath.name
    df['filepath'] = str(filepath)
    return df

def extract_lines_df(filepath=DEFAULT_FILEPATH, with_meta=True):
    lines = extract_lines(text=filepath, with_meta=with_meta)
    df = pd.DataFrame(lines)
    return df


def expressions_to_doctests(expressions, prompt='>>> ', ellipsis='... ', comment=''):
    # expressions = extract_expressions(filepath=filepath)

    prompt = prompt or ''
    if prompt and prompt[-1] != ' ':
        prompt += ' '
    if not isinstance(prompt, str):
        prompt = '>>> '

    ellipsis = ellipsis or ''
    if ellipsis and ellipsis[-1] != ' ':
        ellipsis += ' '
    if not isinstance(ellipsis, str):
        ellipsis = '... '

    comment = comment or ''
    if not isinstance(comment, str):
        comment = '# '
    if comment and comment[-1] != ' ':
        comment += ' '
    blocks = ['']

    for exp in expressions:
        lines = exp.source.splitlines()
        if exp.source.strip() and len(lines) == 1:
            blocks[-1] += prompt + exp.source
        else:
            blocks[-1] += prompt + lines[0] + '\n'
            for line in lines[1:]:
                blocks[-1] += ellipsis + lines[0] + '\n'

        if exp.want:
            blocks[-1] += comment + exp.want
            blocks.append('')


def extract_goodreads_quotes(text):
    """ Regexes used in Sublime to turn goodreads copypasta text into yaml entries in quotes.yml

    Example output:
      https://gitlab.com/tangibleai/nlpia2/-/tree/main/src/nlpia2/data/quotes.yml
    Example input (copy text in browser):
      https://www.goodreads.com/author/quotes/5780686.Liu_Cixin
    Crawler can start with search for author/keyword quotes:
      https://www.goodreads.com/quotes/search?q=Chiang
    """
    resub_pairs = dict(
        unicode_quotes=[r'[“”]', r'"'],
        unicode_appostrophes=[r'[‘’]', r"'"],
        quote_text=[r'― ([^,]+),([-!?\w\d ]+)',
                    r'''
  author: \1
  source: Good Reads
  book: \2
'''],
        likes=[
            r'''

(\d*) likes
Like
(".*)
''',
            r'''

-
  text: \2
  likes: \1
'''],

    )
    for name, (pattern, replacement) in resub_pairs.items():
        text = re.sub(pattern, replacement, text)
    return text


re_codeblock_source = r'[ ]*\[[ ]*source\s*,[ ]*python[ ]*\][ ]*'
re_ipython_shabang = r'([>]{2,3}|[.]{2,3})?[ ]*[!].*'
re_codeblock_horizontal_line = r'[ ]*[-]{2,80}[ ]*'


def test_file(filepath=DEFAULT_FILEPATH, skip=0, adoc=True,
              cleanup=True,  # whether to remove the temporary adoc file containing preprocessed code blocks
              optionflags=DEFAULT_OPTIONFLAGS,
              name=None,
              verbose=False,
              package=None,
              module_relative=False,
              **kwargs):
    if name is None:
        name = filepath.name
    if package:
        module_relative = True
    if not module_relative:
        assert filepath.is_file()
    if adoc:
        # Insert blank line before '----' at end of adoc code block for doctests
        with filepath.open() as fin:
            lines = fin.readlines()
            newlines = []
            # blocks the command line and the running of doctests
            ignore_line_prefixes = [
                '>>> !firefox',
                '>>> displacy.serve(',
                '>>> spacy.cli.download(',
            ]
            ignore_linepair_prefixes = [
                '>>> %timeit',
            ]
            ignore_nextline = False
            for i, (line, nextline) in enumerate(zip(lines[:-1], lines[1:])):
                if i < skip:
                    continue
                # skip ignore_prefixes lines:
                if any((line.lower().lstrip().startswith(p) for p in ignore_line_prefixes)):
                    line = '\n'

                if ignore_nextline:
                    line = '\n'
                    ignore_nextline = False
                if any((line.lower().lstrip().startswith(p) for p in ignore_linepair_prefixes)):
                    line = '\n'
                    ignore_nextline = True
                # remove nonpython shell commands (shabangs) !
                # line = re.match(r'(>[2,3]|[.]{3})?\s*!.*', '', line)

                # remove comment hash at begging of return value (e.g. '# 42')
                # line = re.sub(r'^#\s+', '', line)

                # rstrip EOL footnotes/comments (e.g. '  # <1>')
                line = re.sub(r'[ ]+#[ ]+<\d+>[ ]*', '', line)

                newlines.append(line)

                # insert newline before '----' at end of code block
                if nextline.startswith('----'):
                    # print(f'line: {len(newlines)}')
                    # print(repr(line))
                    # print(f'nextline: {len(newlines)+1}')
                    # print(repr(nextline))
                    if not re.match(re_codeblock_source, line):
                        newlines.append('\n')
                    # check for inline adoc code block comments (callout bubbles)
            # for loop finishes one early, so append the last line of text
            newlines.append(lines[-1])
        fp, filepath = tempfile.mkstemp(text=True, suffix='.adoc')
        filepath = Path(filepath)
        print(filepath)
        with filepath.open('wt') as fout:
            fout.writelines(newlines)
    results = doctest.testfile(str(filepath),
                               name=name,
                               module_relative=module_relative, package=package,
                               optionflags=optionflags, verbose=verbose,
                               **kwargs)
    if results.failed > 0:
        fp, pyfilepath = tempfile.mkstemp(text=True, suffix='.py')
        extract_code_file(filepath=filepath, destfile=pyfilepath)
        print(f"You can find the doctests in {pyfilepath}")
    if cleanup:
        filepath.unlink()
    else:
        print(f"You can find the preprocessed adoc text in {filepath}")
    return results


def extract_code_file(filepath=DEFAULT_FILEPATH, destfile=None):
    filepath = Path(filepath)
    destfile = Path(destfile) if destfile else filepath.with_suffix('.adoc.py')
    if destfile.is_dir():
        destfile = destfile / filepath.with_suffix('.adoc.py').name
    lines = extract_code_lines(filepath=filepath, with_metadata=False)
    if destfile:
        with Path(destfile).open('wt') as fout:
            fout.writelines(lines)
    return ''.join(lines)


def extract_lists_from_files(input_dir=MANUSCRIPT_DIR, glob='*.adoc',
                             extractor=extract_urls_from_text, with_meta=True):
    outputs = []
    for p in input_dir.glob(glob):
        df = extractor(filepath=p, with_meta=with_meta)
        outputs.append(df)
    return outputs


def extract_files(
        input_dir=MANUSCRIPT_DIR, output_dir=None, glob='*.adoc',
        extractor=extract_code_file, suffix='.adoc.py'):
    """ Run an extractor on all the text (default=adoc) files in a directory returnning the extracted file paths """
    output_paths = []
    for p in input_dir.glob(glob):
        destfile = (output_dir / p.name).with_suffix(suffix)
        print(f"{p} => {destfile}")
        code = extractor(filepath=p)
        with destfile.open('wt') as fout:
            fout.write(code)
        output_paths.append(destfile)
    return output_paths


def extract_url_dfs_from_files(
        adocdir=MANUSCRIPT_DIR, destdir=None,
        glob='*.adoc', suffix='.adoc.py'):
    adocdir = Path(adocdir)
    dfs = extract_dfs_from_files(
        extractor=extract_urls_df,
        input_dir=adocdir, output_dir=destdir, glob=glob,
        suffix=suffix)
    return dfs

def extract_big_line_df_from_files(
        adocdir=MANUSCRIPT_DIR, destdir=None,
        glob='*.adoc', suffix='.adoc.py'):
    adocdir = Path(adocdir)
    output = []
    for p in adocdir.glob(glob):
        lines = extract_lines(text=p)
        output.extend(lines)
    df = pd.DataFrame(output)

    # for each line, see if we know what its type is
    one_hot_columns = [col for col in df.columns if col.startswith('is_')]
    df['num_types'] = df[one_hot_columns].sum(axis=1)
    df['is_type_defined'] = df[one_hot_columns].sum(axis=1) > 0

    return df

def extract_dfs_from_files(
        input_dir=MANUSCRIPT_DIR, output_dir=None, glob='*.adoc',
        extractor=extract_urls_df, suffix='.adoc.py'):
    outputs = []
    for p in input_dir.glob(glob):
        df = extractor(filepath=p)
        outputs.append(df)
    return outputs


def extract_code_files(adocdir=MANUSCRIPT_DIR, destdir=None, glob='*.adoc', suffix='.adoc.py'):
    adocdir = Path(adocdir)
    if destdir is None:
        destdir = adocdir.parent / 'py'
    destdir = Path(destdir)
    destdir.mkdir(exist_ok=True)
    destpaths = extract_files(extractor=extract_code_file,
                              input_dir=adocdir, output_dir=destdir,
                              glob=glob, suffix=suffix)
    return destpaths


def parse_args(
        description='Transcoder for doctest-formatted code blocks in asciidoc/txt files to py, or ipynb code blocks',
        input_help='Path to asciidoc or text file containing doctest-format code blocks',
        output_help='Path to new py file created from code blocks in INPUT',
        format_help='Output file format or type (md, py, ipynb, python, or notebook)'):

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        '--input', type=Path, default=None,
        help=input_help
    )
    parser.add_argument(
        '--output', type=Path, default=None,
        help=output_help,
    )
    parser.add_argument(
        '--format', type=str, default='py', help=format_help
    )
    return vars(parser.parse_args())


if __name__ == '__main__':
    args = parse_args()
    if args['input']:
        if Path(args['input']).is_dir():
            results = extract_code_files(adocdir=args['input'])
        else:
            results = extract_code_file(filepath=args['input'])
    else:
        if input('Extract lines from all manuscript/adoc files? ').lower()[0] == 'y':
            result_df = extract_big_line_df_from_files()
            result_df.to_csv(DEFAULT_LINES_FILENAME)
        if input('Extract python from all manuscript/adoc files? ').lower()[0] == 'y':
            results = extract_code_files()
            print(results)
        if input('Extract urls from all manuscript/adoc files? ').lower()[0] == 'y':
            results = extract_urls()
            urls = []
            for u in results:
                urls.extend(u)
            df_urls = pd.DataFrame(urls)
            print(df_urls)
