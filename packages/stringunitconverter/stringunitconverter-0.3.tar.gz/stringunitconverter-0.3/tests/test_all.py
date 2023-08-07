"""
Function unit tests
2022, March 13
"""

import pytest
from pytest import approx

# Code to test
from stringunitconverter import *


@pytest.mark.parametrize('test_input, expected', [
    ('N', '1'),
    ('kN', '(1e3*1)'),
    ('mm', '(1e-3*1)'),
    ('mN', '(1e-3*1)'),
    ('kPa', '(1e3*1)'),
])
def test_unit_to_factor_string(test_input, expected):
    assert unit_to_factor_string(test_input) == expected


@pytest.mark.parametrize('test_input, expected', [
    ('N', 1),
    ('N m', 1),
    ('kN', 1e3),
    ('N^2', 1),
    ('kN^2', 1e6),
    ('1/N', 1),
    ('1/N^2', 1),
    ('1/kN', 1e-3),
    ('1/kN^2', 1e-6),
    ('1/(MN*mm)^2', 1e-6),
    ('% kN m', 1e1),
    ('km ds^-1', 1e3 / 10),
    ('km*ds^-1', 1e3 / 10),
    ('km·ds^-1', 1e3 / 10),
    ('kPa', 1e3),
    ('1/kPa', 1e-3),
    ('1 / kPa', 1e-3),
    (' kPa ', 1e3),
    ('  kPa  ', 1e3),
    ('mm²', 1e-6),
    ('mm³', 1e-9),
])
def test_get_factor(test_input, expected):
    assert get_factor(test_input) == approx(expected)


@pytest.mark.parametrize('test_input', [
    'import',
    'eval("10 + 10")',
])
def test_get_factor_input_protection_01(test_input):
    with pytest.raises(Exception):
        _ = get_factor(test_input)


@pytest.mark.parametrize('test_input, expected', [
    ('eval("10 + 10")', 20),
])
def test_get_factor_input_protection_02(test_input, expected):
    assert get_factor(test_input, unsafe=True) == approx(expected)


@pytest.mark.parametrize('test_input, expected', [
    (('kPa', 'bar'), 1e-2),
    (('Pa', 'N/m^2'), 1),
    (('1/kPa', '1/(N/m^2)'), 1e-3),
    (('25 N·m', 'N·mm'), 25 * 1e3),
])
def test_multiplier(test_input, expected):
    a, b = test_input
    assert multiplier(a, b) == approx(expected)
