# mpaq_convert_mixes.py

author Hayden Hildreth

version 0.1.2

revision date 05/22/2026

Convert MPAQ's mix design CSV export into a format importable into Keystone.

Input format (CSV, one mix per row):
* MixId          - Mix ID code
* Name           - Mix design name
* WATER GALLONS  - Water amount (gallons)
* Agg1ID / Agg1Target  } repeating group (up to 6 aggregates)
* Cem1ID / Cem1Target  } repeating group (up to 3 cements)
* Adm1ID / Adm1Target  } repeating group (up to 8 admixtures)
  
Unit assumptions (MPAQ stores no explicit unit per ingredient):
* Aggregates   -> LB
* Cements      -> LB
* Admixtures   -> OZ
* Water        -> GL

Output format (5 columns, matching Keystone import spec):
* Column A (col 0): Mix Design Name
* Column B (col 1): Ingredient name
* Column C (col 2): (empty)
* Column D (col 3): Amount  (3 decimal places)
* Column E (col 4): Unit (LB / OZ / GL)

Usage:
  ```python mpaq_convert_mixes.py [input.csv] [output.xls] [plant_separator]```

Defaults (used if script is run without parameters at runtime):
* input           = mpaq_export.csv
* output          = mpaq_converted.xls
* plant_separator = ""
