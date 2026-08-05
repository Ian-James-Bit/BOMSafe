import nexar
import json

def main():
    mpn = input("Enter an MPN: ").strip()

    if not mpn:
        print("You must enter an MPN.")
        return

    try:
        access_token = nexar.get_access_token()

        data = nexar.get_part_offers(
            access_token=access_token,
            mpn=mpn,
        )

    except RuntimeError as error:
        print(f"Nexar request failed: {error}")
        return

    # Temporarily print the returned JSON in a readable format.
    print(json.dumps(data))

main()