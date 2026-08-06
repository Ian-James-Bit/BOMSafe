# holds functions for sorting to get stock and pricing information and normalizing data recieved from Nexar API 
from typing import Any

#Normalize a supplier name by removing spaces and punctuation.
def normalize_supplier_name(supplier_name):
    normalized_supplier = ""

    for character in supplier_name.casefold():
        if character.isalnum():
            normalized_supplier += character

    return normalized_supplier

#get supplier stock and pricing using a supplier name.
def get_supplier_stock_and_pricing(nexar_data,supplier_name):
    requested_supplier = normalize_supplier_name(supplier_name)
    results: list[dict[str, Any]] = []

    match_groups = nexar_data.get("supMultiMatch") or []

    for match_group in match_groups:
        parts = match_group.get("parts") or []

        for part in parts:
            sellers = part.get("sellers") or []

            for seller in sellers:
                company = seller.get("company") or {}
                returned_name = company.get("name") or ""

                if normalize_supplier_name(returned_name) != requested_supplier:
                    continue

                offers = seller.get("offers") or []

                for offer in offers:
                    pricing = []

                    for price in offer.get("prices") or []:
                        pricing.append(
                            {
                                "quantity": price.get("quantity"),
                                "unit_price": price.get("convertedPrice"),
                                "currency": price.get("convertedCurrency"),
                            }
                        )

                    results.append(
                        {
                            "stock": offer.get("inventoryLevel"),
                            "pricing": pricing,
                        }
                    )

    return results

# Return the supplier names thats in a Nexar response
def get_returned_supplier_names(nexar_data):
    supplier_names: list[str] = []

    match_groups = nexar_data.get("supMultiMatch") or []

    for match_group in match_groups:
        for part in match_group.get("parts") or []:
            for seller in part.get("sellers") or []:
                company = seller.get("company") or {}
                name = company.get("name")

                if name and name not in supplier_names:
                    supplier_names.append(name)

    return supplier_names