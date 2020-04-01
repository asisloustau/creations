# Process Amazon Sales Script

This script will process the Amazon monthly sales reports contained in the input csv files and output a monthly report per processed sheet and product, values:

- `product_name`
- `actual_units_sold`
- `sales_revenue`
- `shipping_fees`
- `promotions`
- `amazon_fees`
- `reimbursements`

This script is adjusted to my client's needs, but could be useful for any other sellers.
  
### Requirements

- Python 3.6 or higher
- pandas==1.0.1
- numpy==1.18.1
- XlsxWriter==1.2.7

### How to use ProcessAmazon_v0 script ###
1. Modify following constants in ProcessAmazon_v0.py:<br>
    1.1 `MAP_PARENT`: Dictionary of values to define a relationship between the Amazon child SKU's (Stock Keeping Units) and their parent SKU's.<br>
    1.2 `MAP_NAME`: Dictionary of values to define a relationship between the Amazon parent SKU's (Stock Keeping Units) and their product names.

2. Move to the app's root folder on the terminal.


3. Place your csv files in the `input` directory

4. Run the script by typing or pasting this in your terminal:<br>
`python3 ProcessAmazon.py`

5. This will create a folder named `output` with an Excel sheet with one tab per csv processed.

### Notes:
Your working directory should contain following files/directories:

- `input` directory: store Amazon's csv files to be processed in there.
- `ProcessAmazon_v0.py`: This is the Python script that you are executing. I compacted it to a single file for ease of use.
- This `README` :)