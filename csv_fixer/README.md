# csv File Fixer


With this script you will be able to normalize CSV files that are delimited by different values. Run following script in your terminal to use it:

`$ python3 fix_csv.py --in-delimiter="|" --in-quote="'" [csv_to_fix.csv] [fixed_csv_to_create.csv]`

Notes:

  - `--in-delimiter="|"`: OPTIONAL; `"|"` is the default value. If used, replace `"|"` for existing delimiter -i.e. `"/"`.

  - `--in-quote="'"`: OPTIONAL; `"'"` is the default value. If used, replace `"'"` for existing quote character -i.e. `"."`.

  - `[csv_to_fix.csv]`; REQUIRED; name of the existing csv to be normalized.

  - `[fixed_csv_to_create.csv]`; REQUIRED; name of the fixed csv to be created.

*Inspired by Python Morsels*
