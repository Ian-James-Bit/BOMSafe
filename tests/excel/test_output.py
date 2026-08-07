import json
from pathlib import Path

import pytest
from openpyxl import load_workbook
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter

from src.excel import input
from src.excel import output
from src.nexar.utilities import sort

@pytest.fixture
def path(): 
    return "uploads/final_bomsafe_test.xlsx"

@pytest.fixture
def supplier_results():
    return [
        {
            "stock": 14948,
            "pricing": [
                {"quantity": 1, "unit_price": 0.8, "currency": "USD"},
                {"quantity": 10, "unit_price": 0.686, "currency": "USD"},
            ],
        }
    ]

@pytest.fixture
def multiple_supplier_results():
    return [
        {
            "stock": 14948,
            "pricing": [
                {"quantity": 1, "unit_price": 0.8, "currency": "USD"},
                {"quantity": 10, "unit_price": 0.686, "currency": "USD"},
            ],
        },
        {
            "stock": 7296,
            "pricing": [
                {"quantity": 1, "unit_price": 0.85, "currency": "USD"},
                {"quantity": 10, "unit_price": 0.719, "currency": "USD"},
            ],
        },
    ]

@pytest.fixture
def nexar_variables():
    return {
    "queries": [
            {
                "mpn": "1726480102",
                "start": 0,
                "limit": 1,
            }
        ]
    }

@pytest.fixture
def nexar_data():
    return json.load("output/final_bomsafe_test_nexar_response.json")

def test_format_stock(supplier_results, multiple_supplier_results):
    assert output.format_stock(supplier_results) == "14948"
    assert output.format_stock(multiple_supplier_results) == "Offer 1: 14948\nOffer 2: 7296"

def test_format_pricing(supplier_results, multiple_supplier_results):
    assert output.format_pricing(supplier_results) == ("1+: 0.8 USD; 10+: 0.686 USD")
    assert output.format_pricing(multiple_supplier_results) == (
        "Offer 1: 1+: 0.8 USD; 10+: 0.686 USD\n"
        "Offer 2: 1+: 0.85 USD; 10+: 0.719 USD"
    )

# def test_build_match_groups_by_mpn(nexar_data,nexar_variables):
#     assert output.build_match_groups_by_mpn(nexar_data,nexar_variables) == 