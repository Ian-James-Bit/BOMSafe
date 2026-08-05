from typing import Any

#sort data to get supplier stock and pricing from a Nexar supMultiMatch response using a supplier name.
def get_supplier_stock_and_pricing(nexar_data: dict[str, Any],supplier_name: str):
    requested_supplier = supplier_name.strip().casefold()
    results: list[dict[str, Any]] = []

    match_groups = nexar_data.get("supMultiMatch") or []

    for match_group in match_groups:
        parts = match_group.get("parts") or []

        for part in parts:
            sellers = part.get("sellers") or []

            for seller in sellers:
                company = seller.get("company") or {}
                returned_name = company.get("name") or ""

                if returned_name.strip().casefold() != requested_supplier:
                    continue

                offers = seller.get("offers") or []

                for offer in offers:
                    pricing = []

                    for price in offer.get("prices") or []:
                        pricing.append(
                            {
                                "quantity": price.get("quantity"),
                                "unit_price": price.get(
                                    "convertedPrice"
                                ),
                                "currency": price.get(
                                    "convertedCurrency"
                                ),
                            }
                        )

                    results.append(
                        {
                            "stock": offer.get("inventoryLevel"),
                            "pricing": pricing,
                        }
                    )

    return results

def get_returned_supplier_names(
    nexar_data: dict[str, Any],
) -> list[str]:
    """Return the supplier names present in a Nexar response."""

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