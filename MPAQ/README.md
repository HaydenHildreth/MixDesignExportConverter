mpaq_convert_mixes.py
author  Hayden Hildreth
version 0.1.0
revision date 05/19/2026

Convert MPAQ's mix design CSV export into the flat, row-per-ingredient
format that can be imported into Keystone.

MPAQ stores every ingredient as a numeric ID (Agg1ID, Cem1ID, Adm1ID, …)
so you must supply a lookup file that maps those IDs to ingredient names.
A sample lookup CSV is shown in the Usage section below.

Output columns:
  Column A (col 0): Mix Design Name  (MixId value, uppercased)
  Column B (col 1): Ingredient name  (from lookup, or auto-generated)
  Column C (col 2): Unit             (LB for agg/cem/water, OZ for admixtures)
  Column D (col 3): Amount           (formatted to 3 decimal places)

Usage:
  python mpaq_convert_mixes.py [input.csv] [output.xlsx] [lookup.csv] [plant_separator]

Arguments:
  input.csv         – MPAQ mix design export  (default: mpaq_export.csv)
  output.xlsx       – Desired output file      (default: mpaq_converted.xlsx)
  lookup.csv        – Ingredient ID lookup     (default: mpaq_lookup.csv)
  plant_separator   – Optional suffix appended to every mix/ingredient name
                      (default: "")

Lookup file format (CSV, no header required, columns = ID, Name):
  1,SAND 2
  2,1 STONE
  3,PEASTONE
  ...

  Separate lookups per material type are supported via an optional third
  column containing the type abbreviation (AGG, CEM, ADM).  If the third
  column is absent the same table is used for all types:
  1,AGG,SAND 2
  1,CEM,HEIDELBERG
  1,ADM,AIRALON

  If no lookup file exists (or a particular ID is not found) the script
  falls back to auto-generated names like AGG_1, CEM_2, ADM_3 so the
  output is still usable.

Water:
  WaterTarget is always written as a WATER / LB row when the value is
  non-zero.  MPAQ stores water separately from the numbered ingredient
  slots so no lookup entry is needed.

Units:
  Aggregates   -> LB
  Cementitious -> LB
  Water        -> LB
  Admixtures   -> OZ  (industry convention; override via lookup if needed)
