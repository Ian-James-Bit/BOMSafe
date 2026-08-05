import nexar
import json
import sort

def main():
    mpn = input("Enter an MPN: ").strip()

    if not mpn:
        print("You must enter an MPN.")
        return

    supplier_name = input("Enter a supplier name: ").strip()

    if not supplier_name:
        print("You must enter a supplier name.")
        return

    try:
        access_token = nexar.get_access_token()

        data = nexar.get_part_offers(access_token=access_token,mpn=mpn)

        # debugging: print the raw Nexar response to the console.
        # print("\nRAW NEXAR RESPONSE:")
        # print(json.dumps(data, indent=2))
        
    except RuntimeError as error:
        print(f"Nexar request failed: {error}")
        return

    supplier_results = sort.get_supplier_stock_and_pricing(nexar_data=data,supplier_name=supplier_name)

    if not supplier_results:
        print(
            f"No stock or pricing data was returned "
            f"for supplier '{supplier_name}'."
        )

        returned_suppliers = sort.get_returned_supplier_names(data)

        print("Suppliers returned by Nexar:")

        if returned_suppliers:
            for supplier in returned_suppliers:
                print(f"- {supplier}")
        else:
            print("- No suppliers were returned.")
            return

    print(json.dumps(supplier_results, indent=2))

main()