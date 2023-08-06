"""Tests for js_bridge"""

from jy.js_parse import func_name_and_params_pairs
from jy.util import js_files

test01_js_code = js_files['test01']


def test_func_name_and_params_pairs():
    pairs = list(func_name_and_params_pairs(test01_js_code))
    assert pairs == [
        (
            'foo',
            [
                {'name': 'a'},
                {'name': 'b', 'default': 'hello'},
                {'name': 'c', 'default': 3},
            ],
        ),
        (
            'bar',
            [
                {'name': 'green'},
                {'name': 'eggs', 'default': 'food'},
                {'name': 'and', 'default': True},
                {'name': 'ham', 'default': 4},
            ],
        ),
        ('add_one', [{'name': 'x'}]),
        ('with_let', [{'name': 'x'}]),
        ('with_arrow_func', [{'name': 'y'}, {'name': 'z', 'default': 1}]),
        # Note that the name here is dot-separated!
        ('func.assigned.to.nested.prop', [{'name': 'x'}]),
        ('obj', [{'name': 'exports'}]),
    ]

