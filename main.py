import argparse
from pathlib import Path

import src.excel.input as input
import src.excel.output as output
import src.nexar.nexar as nexar
import json

# reads the options and file path you type when running the program in the terminal.
# EX: python main.py uploads/bom.xlsx --sheet BOM
def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--response-file",
        type=Path,
        help="Use a previously saved Nexar JSON response instead of calling the API.",
    )

    parser.add_argument(
        "excel_file",
        type=Path,
        help="Path to the Excel BOM file.",
    )

    parser.add_argument(
        "--sheet",
        help="Optional worksheet name.",
    )

    return parser.parse_args()


def main():
    arguments = get_arguments()

    try:
        bom_rows = input.read_bom(
            file_path=arguments.excel_file,
            sheet_name=arguments.sheet,
        )

        nexar_variables = input.build_nexar_variables(bom_rows=bom_rows,result_limit=1)

        if arguments.response_file:
            with arguments.response_file.open(
                "r",
                encoding="utf-8",
            ) as response_file:
                nexar_data = json.load(response_file)

        else:
            access_token = nexar.get_access_token()

            nexar_data = nexar.get_part_offers(access_token=access_token,variables=nexar_variables)

            response_file = (Path("output")/ f"{arguments.excel_file.stem}_nexar_response.json")

            response_file.parent.mkdir(parents=True,exist_ok=True,)

            with response_file.open("w",encoding="utf-8",) as saved_response:
                json.dump(
                    nexar_data,
                    saved_response,
                    indent=2,
                )

            print(f"Saved Nexar response: {response_file}")

        output_file = (Path("output")/ f"{arguments.excel_file.stem}_results.xlsx")

        created_file = output.write_bom_results(
            input_file=arguments.excel_file,
            output_file=output_file,
            nexar_data=nexar_data,
            nexar_variables=nexar_variables,
            sheet_name=arguments.sheet,
        )

    except (
        FileNotFoundError,
        OSError,
        RuntimeError,
        ValueError,
    ) as error:
        print(f"Could not process BOM: {error}")
        return

    print(f"Created results file: {created_file}")


main()