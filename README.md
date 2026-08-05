# BOMSafe
BOMSafe is a Python command-line tool that reads an electronic Bill of Materials (BOM) from Excel, retrieves supplier stock and pricing through the Nexar Supply API, and creates a new results workbook with the new data attached.

Features:
Reads .xlsx BOM files
Supports multiple supplier columns
Queries each unique MPN once
Retrieves supplier stock and quantity pricing
Matches supplier names despite capitalization or punctuation differences
Saves the completed workbook and raw Nexar response
Can reuse a saved response without making another API call

Setup:
git clone https://github.com/Ian-James-Bit/BOMSafe.git
cd BOMSafe
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

On Windows, activate the environment with:
.venv\Scripts\Activate.ps1

Copy .env.example to .env and add your Nexar credentials:
NEXAR_CLIENT_ID=your_client_id
NEXAR_CLIENT_SECRET=your_client_secret

Excel Format:
The workbook must contain:
One MPN column
At least one supplier or distributor column

Example:
MPN
Supplier 1
Supplier 2
1726480102
Mouser
DigiKey

Common headings such as MPN, Manufacturer Part Number, Supplier 1, and Distributor 1 are supported.

Usage:
Process the active worksheet: python main.py uploads/customer_bom.xlsx

Process a specific worksheet:python main.py uploads/customer_bom.xlsx --sheet BOM

Reuse a saved Nexar response:python main.py uploads/customer_bom.xlsx \ --sheet BOM \ --response-file output/customer_bom_nexar_response.json

Output:
BOMSafe creates:

output/customer_bom_results.xlsx
output/customer_bom_nexar_response.json

The results workbook keeps the original data and adds columns such as:

Supplier 1 Stock
Supplier 1 Pricing
Supplier 2 Stock
Supplier 2 Pricing

License

MIT License
