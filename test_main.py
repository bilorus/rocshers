import json
import sys
from contextlib import contextmanager
from io import StringIO
from unittest.mock import patch, MagicMock

import main


@contextmanager
def replace_stdin(target):
    orig = sys.stdin
    sys.stdin = target
    yield
    sys.stdin = orig


def test_get_links_notlink():
    with replace_stdin(StringIO("not a link\n\n")):
        assert main.get_links() == []


def test_get_links_different_input():
    inp = 'https://www.google.com/\nhttp://www.yandex.ru\nnot a link\n\n'
    with replace_stdin(StringIO(inp)):
        test_case = main.get_links()
        assert test_case == ['https://www.google.com/', 'http://www.yandex.ru']
        assert len(test_case) == 2


def test_get_links_empty():
    with replace_stdin(StringIO("\n\n")):
        assert main.get_links() == []


@patch('main.requests')
def test_get_links_allow_methods(mock_requests):

    mock_requests.get('https://www.google.com/').status_code = 200
    mock_requests.post('https://www.google.com/').status_code = 300
    mock_requests.put('https://www.google.com/').status_code = 405
    mock_requests.delete('https://www.google.com/').status_code = 405
    mock_requests.head('https://www.google.com/').status_code = 405
    mock_requests.options('https://www.google.com/').status_code = 405
    mock_requests.patch('https://www.google.com/').status_code = 405

    # mock_requests.return_value = mock_response

    answer = {"https://www.google.com/": {"GET": 200, "POST": 300}}

    assert main.get_links_allow_methods(['https://www.google.com/']) == json.dumps(answer, indent=4)
