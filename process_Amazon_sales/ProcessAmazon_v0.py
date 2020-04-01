### Python Modules ###
######################

import pandas as pd  # Data Processing
import numpy as np  # Linear Algebra
import re  # Regular Expressions
from datetime import datetime
import os  # Interaction with paths to read input and write output
from pandas.errors import ParserError
import sys  # Minimally used for exceptions

### Constants ###
#################
# Save here any mapping objects

MAP_COLUMN_NAMES = {

    # Notes on MAP_COLUMN_NAMES constant:
    # This constant is a dictionary of values to define a relationship between the column names in different languages
    # to be able to process the data consistently.

    "English": {
        "date/time": "date",
        "quantity": "units_sold",
        "product sales": "sales_revenue",
        "shipping credits": "shipping_fees",
        "promotional rebates": "promotions",
        "postage credits": "shipping_fees",
    },

    "French": {
        "date/heure": "date",
        "quantité": "units_sold",
        "ventes de produits": "sales_revenue",
        "crédits d'expédition": "shipping_fees",
        "Rabais promotionnels": "promotions",
        "type": "type",
        "frais de vente": "selling fees",
        "Frais Expédié par Amazon": "fba fees",
        "autres frais de transaction": "other transaction fees",
        "autre": "other",
    },

    "Spanish": {
        "fecha y hora": "date",
        "cantidad": "units_sold",
        "ventas de productos": "sales_revenue",
        "abonos de envío": "shipping_fees",
        "devoluciones promocionales": "promotions",
        "tipo": "type",
        "tarifas de venta": "selling fees",
        "tarifas de Logística de Amazon": "fba fees",
        "tarifas de otras transacciones": "other transaction fees",
        "otro": "other",
        "descripción": "description",
    },

    "Italian": {
        "Data/Ora:": "date",
        "Quantità": "units_sold",
        "Vendite": "sales_revenue",
        "Sconti promozionali": "promotions",
        "Accrediti per le spedizioni": "shipping_fees",
        "SKU": "sku",
        "Tipo": "type",
        "Commissioni di vendita": "selling fees",
        "Costi del servizio Logistica di Amazon": "fba fees",
        "Altri costi relativi alle transazioni": "other transaction fees",
        "Altro": "other",
        "Descrizione": "description",
    },

    "German": {
        "Datum/Uhrzeit": "date",
        "Menge": "units_sold",
        "Umsätze": "sales_revenue",
        "Rabatte aus Werbeaktionen": "promotions",
        "Gutschrift für Versandkosten": "shipping_fees",
        "SKU": "sku",
        "Typ": "type",
        "Beschreibung": "description",
        "Verkaufsgebühren": "selling fees",
        "Gebühren zu Versand durch Amazon": "fba fees",
        "Andere Transaktionsgebühren": "other transaction fees",
        "Andere": "other",
    },
}


MAP_PARENT = {

    # Notes on MAP_PARENT constant:
    # This constant is a dictionary of values to define a relationship between the Amazon child SKU's (Stock Keeping Units) and their parent SKU's.
    # The Amazon reports do not include the parent SKU's and grouping the products by parent SKU was one of my client's request.

    # Fill out with required parent/child SKU's
    # I personally used Regex patterns to extract them for documents
    # that my client provided instead of typing this constant manually
    'PARENT_SKU_1': 'CHILD_SKU_1',
    'PARENT_SKU_2': 'CHILD_SKU_2',

}

MAP_NAME = {

    # Notes on MAP_NAME constant:
    # This constant is a dictionary of values to define a relationship between the Amazon parent SKU's (Stock Keeping Units) and their product names.
    # This was used to simplify the reporting and map the product names.

    # Fill out with required values
    # I personally used Regex patterns to extract them for documents
    # that my client provided instead of typing this constant manually
    'PARENT_SKU_1': 'PRODUCT_NAME_1',
    'PARENT_SKU_2': 'PRODUCT_NAME_2',
}


US_STATES = {
    # This dictionary is not required in this script. I used it for future reporting/visualizations in dashboards.
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}

### Functions ###
#################


# DATA PROCESSING
# def read_data(path_of_files):
def read_data(file):
    """
    Converts Amazon csv monthly data into a DataFrame object.
    It skips any rows that do not contain any values -description rows

    Args:
        folder where csv files are stored

    Returns:
        Data in DataFrame format
    """
    is_read = False
    skr = 0
    min_cols = 21
    max_cols = 27

    while not is_read:
        try:
            df = pd.read_csv(file, skiprows=skr, thousands=",")
            n_cols = len(df.columns)
            if n_cols >= min_cols and n_cols <= max_cols:
                is_read = True
            else:
                skr += 1
        except ParserError:
            skr += 1
            is_read = False
    language = data_language(df)
    print("Read Data: {}".format(file))
    print("Number of Rows: {}".format(n_cols))
    print("Language of csv file: {}".format(language))

    # Reading DataFrame again after determining the language to avoid conflicts with thousands punctuation
    if language == "English":
        return df
    else:
        df = pd.read_csv(file, skiprows=skr, decimal=",")
        return df


def actual_sold(row):
    """Changes value of units_sold if the transaction is not an order
    This function is used in process_data function
    Args:
        row: row from DataFrame
    returns:
        Actual units sold for row (negative if return)
    """
    if row["type"] == "Order":
        actual_sold_units = row["units_sold"]
    elif row["type"] == "Refund":
        actual_sold_units = -row["units_sold"]
    else:
        actual_sold_units = 0
    return actual_sold_units


def calc_reimbursement(row):
    """Determines whether the "other" cost comes from a reimbursement
    Args:
        row: row from DataFrame
    returns:
        "other" costs for refunds
    """
    if row["type"] == "Refund" or row["type"] == "Adjustment":
        reimbursement_cost = row["other"]
    else:
        reimbursement_cost = 0
    return reimbursement_cost


def translate_order_types(column, language):
    """
    Translates values of Order and Refund to English
    returns:
        pandas Series with Order and Refund translated
    """
    if language == "French":
        return column.str.replace("Commande", "Order")\
            .str.replace("Remboursement", "Refund")
    elif language == "Spanish":
        return column.str.replace("Pedido", "Order")\
            .str.replace("Reembolso", "Refund")
    elif language == "Italian":
        return column.str.replace("Ordine", "Order")\
            .str.replace("Rimborso", "Refund")
    elif language == "German":
        return column.str.replace("Bestellung", "Order")\
            .str.replace("Erstattung", "Refund")
    else:
        return column


def data_language(df):
    """Returns the language of the read DataFrame"""
    if "date/time" in df.columns:
        return "English"
    elif "date/heure" in df.columns:
        return "French"
    elif "fecha y hora" in df.columns:
        return "Spanish"
    elif "Data/Ora:" in df.columns:
        return "Italian"
    elif "Datum/Uhrzeit" in df.columns:
        return "German"


def map_parent_sku(string):
    for key, value in MAP_PARENT.items():
        if isinstance(value, str):
            if key in string:
                return value


def process_data(df):
    """Cleans DataFrame so we can perform analytics on it

    Args:
        df: read DataFrame

    Returns:
        Clean data in DataFrame format
    """
    df_clean = df.copy()

    # modify column names based on language
    # returns language of csv file to map column names
    language = data_language(df)
    df_clean.rename(columns=MAP_COLUMN_NAMES.get(language), inplace=True)

    # create amazon_fees column - client request
    df_clean["amazon_fees"] = df_clean[['selling fees', 'fba fees',
                                        'other transaction fees']].sum(axis=1)  # sum/consolidate 3 columns
    df_clean.drop(['selling fees', 'fba fees', 'other transaction fees'],
                  axis=1, inplace=True)  # remove 3 columns

    """
    IMPORTANT NOTE: In order to make this function work for all languages, 
    I deactivated the convert_to_datetime feature below for now.
    """
    # # convert date column to datetime format with only date
    # df_clean.iloc[:,0] = pd.to_datetime(df_clean.iloc[:,0]).dt.date

    # # add period column - YYYY-MM, will become handy to group by month
    # df_clean["period"] = pd.to_datetime(df_clean.loc[:,"date"]).dt.to_period("M")
    """convert_to_datetime ends here"""

    df_clean["parent_sku"] = df_clean["sku"]\
        .astype("str")\
        .apply(map_parent_sku)
    # this will add a column product_name to our DataFrame
    df_clean["product_name"] = df_clean["parent_sku"].map(MAP_NAME)

    # add The Stanford Sleeping Book to product_name
    df_clean["product_name"] = df_clean.apply(add_product_sleep_book, axis=1)

    # Translate types of order in order to determine the actual units sold
    df_clean["type"] = translate_order_types(df_clean["type"], language)

    # calculate actual sold values -using actual_sold(row)
    df_clean["actual_units_sold"] = df_clean.apply(actual_sold, axis=1)

    # calculate actual sold values -using calc_reimbursementa(row)
    df_clean["reimbursements"] = df_clean.apply(calc_reimbursement, axis=1)

    # clean order state column - ONLY US
    try:
        df_clean["order state"] = df_clean["order state"].str.upper()
        # using replace instead map allows us to keep values that are not US states
        df_clean["order state"] = df_clean["order state"].replace(US_STATES)
        df_clean["order state"] = df_clean["order state"].str.title()
    except:
        pass
    return df_clean


def calculate_month(df):
    columns_to_show = ['product_name', 'actual_units_sold', 'sales_revenue',
                       'shipping_fees', 'promotions', 'amazon_fees', 'reimbursements', ]

    product_results = df[columns_to_show]\
        .groupby("product_name")\
        .sum()\
        .round(2).T
    product_results
    return product_results


# BELOW FUNCTIONS: NOT IMPLEMENTED YET #
"""NOTES FOR PROFIT ESTIMATE
- Profit Per Unit (PPU) = (Total Amazon + CPU * Units Sold) / Units Sold
- Cost Per Unit (CPU) = Comes from client, varies month to month -> Define what to do to input it. 
For the previous months we could just add a mapping constant with each product, month, year and CPU -see below
- Ads Per Unit (APU) = Units Sold / Advertising
- Profit Estimate = PPU * Units Sold
"""

# we can use this data structure to store/parse previous costs per unit from excel sheet - or do it manually, that might be a lot.

# MOVE COST_PER_UNIT TO CONSTANTS
# Use datetime format for dates for easier processing
COST_PER_UNIT = {
    "product_name": {
        "YYYY-MM": 1,  # Change keys to datetime format
        "YYYY-MM2": 2
    }
}


def cost_per_unit(sku, date):
    """
    Looks for the CPU stored for the input product and date -this function will be used in the layout callbacks

    Args:
        sku: Product SKU children in string format
        date: Date in datetime format
    Returns:
        CPU as float (stored in COST_PER_UNIT)
    """
    return COST_PER_UNIT[sku][date]


def ads_per_unit(units_sold, ads_cost):
    """
    Ads Per Unit (APU) = Units Sold / Advertising Costs

    Args:
        units_sold: Actual Units Sold for one particular sku within a period selected -i.e. monthly
        ads_cost: Advertising Costs for one particular sku within a period selected -i.e. monthly
    Returns:
        APU as float
    """
    return ads_cost / units_sold


def profit_per_unit(total_amazon, units_sold, sku, date):
    """
    Profit Per Unit (PPU) = (Total Amazon + CPU * Units Sold) / Units Sold
    """
    return (total_amazon + cost_per_unit(sku, date) * units_sold) / units_sold


### Script ###
##############

# define name for input directory
INPUT_DIR = "input"
# adding 1 for / character. This variable will be used to slice INPUT_DIR/
n_chars_dir = len(INPUT_DIR) + 1

# define name for output directory
OUTPUT_DIR = "output"


if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

try:
    data_paths = [INPUT_DIR + "/" + csv for csv in os.listdir(INPUT_DIR)]
except:
    sys.exit(
        "input directory not found. Please create a folder named input and add csv files.")

if not data_paths:
    print("No files were found. Make sure you added csv files to your input directory")
else:
    print("Files found:")
    for i in data_paths:
        print(i)
    print("Note: Amazon csv data placed in /{} will be processed and saved in /{}".format(INPUT_DIR, OUTPUT_DIR))

    dataframes_list = []
    for csv_file in data_paths:
        dataframes_list.append(read_data(csv_file))

    processed_data = dict()
    print("Processing data...")
    for df, path in zip(dataframes_list, data_paths):
        processed_data.setdefault(
            path[n_chars_dir:],  # this eliminates INPUT_DIR/
            process_data(df)
        )

    with pd.ExcelWriter(OUTPUT_DIR + '/output.xlsx', mode='w', engine='xlsxwriter') as writer:
        for key, df in processed_data.items():
            sheet_name = key[:-4]
            results = calculate_month(df)
            results.to_excel(writer, sheet_name=sheet_name, startrow=1)

            # SHEET FORMATTING -could be wrapped in function
            worksheet = writer.sheets[sheet_name]
            workbook = writer.book

            title_format = workbook.add_format({'bold': True})

            worksheet.write(
                0, 0, 'Amazon Monthly Report for {}'.format(sheet_name))
            worksheet.set_row(0, 15, title_format)
            worksheet.set_column('A:A', 25)
            worksheet.set_column(1, len(results.columns), 10)
    print("Data successfully processed and saved in {}/output.xlsx".format(OUTPUT_DIR))
