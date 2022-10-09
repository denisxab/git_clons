import pathlib
import pytest
from git_clons.logic import getconf_, sync_, cmd_, getlog_

path_sync = pathlib.Path(__file__).parent / "dataset"
path_conf = path_sync / "gitconf.json"


def test_getconf():
    user_name = 'denisxab'
    token = "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"
    outfile = path_conf
    getconf_(user_name, outfile, token)


def test_sync():
    sync_(path_conf, path_sync)

