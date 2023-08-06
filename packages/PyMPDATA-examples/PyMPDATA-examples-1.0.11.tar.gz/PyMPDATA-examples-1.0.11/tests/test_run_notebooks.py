# pylint: disable=wrong-import-position
# https://bugs.python.org/issue37373
import sys
if sys.platform == 'win32' and sys.version_info[:2] >= (3, 7):
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import pathlib
import re
import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import pytest


# https://stackoverflow.com/questions/7012921/recursive-grep-using-python
def findfiles(path, regex):
    regObj = re.compile(regex)
    res = []
    for root, _, fnames in os.walk(path):
        for fname in fnames:
            if regObj.match(fname):
                res.append(os.path.join(root, fname))
    return res


@pytest.fixture(params=findfiles(pathlib.Path(__file__).parent.parent.absolute(), r'.*\.(ipynb)$'))
def notebook_filename(request):
    return request.param


def test_run_notebooks(notebook_filename, tmp_path):  # pylint: disable=redefined-outer-name
    with open(notebook_filename, encoding="utf8") as f:
        nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=15*60, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': tmp_path}})
