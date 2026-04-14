# command_convert_mixes.py

Program name: command_convert_mixes.py

Author: Hayden Hildreth

Version: 0.1.4

Last revision date: 04/08/2026

Reason:

This program should be used to convert CommandAlkon's commandBATCH mix design listing (export) into a nice and readable format which can then be imported into Keystone.

Output:
* Excel Column A (col 0): Mix Design Name
* Excel Column B (col 1): Ingredient name
* Excel Column C (col 2): Unit (LB / OZ / etc.)
* Excel Column D (col 3): Amount 

Usage:

  ```python convert_mix_listing.py [input.xls] [output.xls] [plant_separator]```

Defaults (these are used if script is ran without parameters at runtime):
* input  = MixListing.xls
* output = MixListingEdit_converted.xls
* plant_separator = ""
