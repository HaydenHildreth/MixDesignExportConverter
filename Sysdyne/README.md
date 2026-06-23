sysdyne_convert_mixes.py

author Hayden Hildreth

version 1.2.0

revision date 06/23/2026


Convert sysdyne's mix design XLSX export into a format importable into Keystone.

Input format (XLSX, header on row 3, data from row 4):

  Each mix+plant combination begins with a row where 'Item Code' is populated.
  
  Subsequent ingredient rows have NaN in 'Item Code' and inherit the current mix context.
  
  Columns of interest:
  
    Item Code                     - Mix design code
    
    Description                   - Mix design description (col B in output)
    
    Location                      - Plant number, appended to mix code in col A
    
    Constituent Short Description - Ingredient name
    
    Quantity                      - Amount
    
    Unit of Measure               - Unit (ga -> GL, others uppercased)

  The input file also contains a secondary sheet ('Sheet1') with a list of mix codes
  
  (in column A, rows 14-211) that are highlighted yellow via a conditional formatting
  
  rule. This script reads that list and re-applies yellow highlighting to any matching
  
  rows in the output.

Output format (6 columns, matching Keystone import spec):

  Column A (col 0): Mix code + product_separator + plant number + plant_separator
  
  Column B (col 1): Mix Description
  
  Column C (col 2): Ingredient name
  
  Column D (col 3): (empty)
  
  Column E (col 4): Amount  (2 decimal places)
  
  Column F (col 5): Unit (LB / OZ / GL)

  Output is written as .xlsx so cell fill colors are supported.

Usage:
  python newvendor_convert_mixes.py [input.xlsx] [output.xlsx] [plant_separator] [product_separator]

Defaults (used if script is run without parameters at runtime):

  input             = original_format.xlsx
  
  output            = output_converted.xlsx
  
  plant_separator   = ""
  
  product_separator = ""

Arguments:

  plant_separator   - String appended to the very end of the mix code in col A.
  
                      Matches the convention used in command_convert_mixes.py and
                      
                      mpaq_convert_mixes.py.
                      
  product_separator - String inserted between the Item Code and the plant number
  
                      from the Location column.
                      
                      Example: product_separator="-" -> "100SLHP-01"
                      
                      If omitted, the plant number is still appended with no
                      
                      separator: "100SLHP01"

Notes:

  - Ingredients with a zero or blank quantity are skipped.
  - Unit 'ga' is normalized to 'GL' to match Keystone convention; all units uppercased.
  - Each unique Item Code + Location combination becomes its own group in the output.
  - Rows whose Item Code appears in the highlight list (Sheet1 col A) are written
    with a yellow background, matching the original file's conditional formatting.
