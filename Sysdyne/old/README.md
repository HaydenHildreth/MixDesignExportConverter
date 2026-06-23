# sysdyne_convert_mixes.py

Program name: sysdyne_convert_mixes.py

Author: Hayden Hildreth

Version: 0.1.0

Last revision date: 04/14/2026

Reason:

This program should be used to convert Sysdyne's mix design listing (export) into a nice and readable format which can then be imported into Keystone.

Input format:
* Each row is one mix design. Columns of interest:
    * Code: Mix design name
        * MaterialName1 / MaterialAmount1 / MaterialUnit1  } repeating group
        * MaterialName2 / MaterialAmount2 / MaterialUnit2  } up to 16 materials
    
Output:
  * Excel Column A (col 0): Mix Design Name
  * Excel Column B (col 1): Ingredient name
  * Excel Column C (col 2): Unit (LB / OZ / etc.)
  * Excel Column D (col 3): Amount

Usage:

  ```python sysdyne_mix_listing.py [input.xlsx] [output.xlsx] [plant_separator]```

Defaults (these are used if script is ran without parameters at runtime):
* input  = sysdyne_export.xlsx
* output = sysdyne_export_converted.xlsx
* plant_separator = ""
