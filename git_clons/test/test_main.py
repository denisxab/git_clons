import pytest
from git_clons.logic import getconf_, sync_, cmd_, getlog_


def test_getconf():
    user_name = 'denisxab'
    token = None #"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"
    outfile = '/media/denis/dd19b13d-bd85-46bb-8db9-5b8f6cf7a825/MyProject/PycharmProjects/git_clons/git_clons/test/gitconf.json'
    getconf_(user_name, outfile, token)


def test_sync():
    a = 1
    assert a == 1, 'Ошибка !!!'
