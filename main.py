import argparse
import json
from pathlib import Path

import excel_input

def get_arguments():
    parser = argparse.ArgumentParser()

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
        bom_rows = excel_input.read_bom(
            file_path=arguments.excel_file,
            sheet_name=arguments.sheet,
        )

        nexar_variables = excel_input.build_nexar_variables(
            bom_rows=bom_rows,
            result_limit=1,
        )

    except (FileNotFoundError, OSError, ValueError) as error:
        print(f"Could not process workbook: {error}")
        return

    print("BOM rows:")
    print(json.dumps(bom_rows, indent=2))

    print("\nNexar variables:")
    print(json.dumps(nexar_variables, indent=2))

main()