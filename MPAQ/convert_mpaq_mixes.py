"""
mpaq_convert_mixes.py
author Hayden Hildreth
version 0.1.2
revision date 05/22/2026

Convert MPAQ's mix design CSV export into a format importable into Keystone.

Input format (CSV, one mix per row):
  MixId          - Mix ID code
  Name           - Mix design name
  WATER GALLONS  - Water amount (gallons)
  Agg1ID / Agg1Target  } repeating group (up to 6 aggregates)
  Cem1ID / Cem1Target  } repeating group (up to 3 cements)
  Adm1ID / Adm1Target  } repeating group (up to 8 admixtures)

Unit assumptions (MPAQ stores no explicit unit per ingredient):
  Aggregates   -> LB
  Cements      -> LB
  Admixtures   -> OZ
  Water        -> GL

Output format (5 columns, matching Keystone import spec):
  Column A (col 0): Mix Design Name
  Column B (col 1): Ingredient name
  Column C (col 2): (empty)
  Column D (col 3): Amount  (3 decimal places)
  Column E (col 4): Unit (LB / OZ / GL)

Usage:
  python mpaq_convert_mixes.py [input.csv] [output.xls] [plant_separator]

Defaults (used if script is run without parameters at runtime):
  input           = mpaq_export.csv
  output          = mpaq_converted.xls
  plant_separator = ""
"""

import sys
import pandas as pd
import xlwt

INPUT           = sys.argv[1] if len(sys.argv) > 1 else "mpaq_export.csv"
OUTPUT          = sys.argv[2] if len(sys.argv) > 2 else "mpaq_converted.xls"
PLANT_SEPARATOR = sys.argv[3] if len(sys.argv) > 3 else ""

# CONSTANTS
MAX_AGG = 6
MAX_CEM = 3
MAX_ADM = 8


def parse_mixes(path):
    """
    Read MPAQ CSV into a list of mix dicts:
      {
        'name': str,
        'ingredients': [(name, amount_str, unit), ...]
      }
    Skips ingredients where the ID is empty or the target amount is zero.
    Ingredient order: Aggregates -> Cements -> Admixtures -> Water.
    """
    df = pd.read_csv(path, dtype=str)

    mixes = []

    for _, row in df.iterrows():
        mix_name = str(row.get("Name", "")).strip()
        if not mix_name or mix_name == "nan":
            continue

        ingredients = []

        # --- Aggregates (LB) ---
        for n in range(1, MAX_AGG + 1):
            mat_id  = row.get(f"Agg{n}ID",     None)
            mat_amt = row.get(f"Agg{n}Target", None)

            if pd.isna(mat_id) or str(mat_id).strip() == "" or str(mat_id).strip() == "nan":
                continue

            try:
                amount_f = float(mat_amt) if not pd.isna(mat_amt) else 0.0
            except (ValueError, TypeError):
                amount_f = 0.0

            if amount_f == 0.0:
                continue

            ingredients.append((str(mat_id).strip(), f"{amount_f:.3f}", "LB"))

        # --- Cements (LB) ---
        for n in range(1, MAX_CEM + 1):
            mat_id  = row.get(f"Cem{n}ID",     None)
            mat_amt = row.get(f"Cem{n}Target", None)

            if pd.isna(mat_id) or str(mat_id).strip() == "" or str(mat_id).strip() == "nan":
                continue

            try:
                amount_f = float(mat_amt) if not pd.isna(mat_amt) else 0.0
            except (ValueError, TypeError):
                amount_f = 0.0

            if amount_f == 0.0:
                continue

            ingredients.append((str(mat_id).strip(), f"{amount_f:.3f}", "LB"))

        # --- Admixtures (OZ) ---
        for n in range(1, MAX_ADM + 1):
            mat_id  = row.get(f"Adm{n}ID",     None)
            mat_amt = row.get(f"Adm{n}Target", None)

            if pd.isna(mat_id) or str(mat_id).strip() == "" or str(mat_id).strip() == "nan":
                continue

            try:
                amount_f = float(mat_amt) if not pd.isna(mat_amt) else 0.0
            except (ValueError, TypeError):
                amount_f = 0.0

            if amount_f == 0.0:
                continue

            ingredients.append((str(mat_id).strip(), f"{amount_f:.3f}", "OZ"))

        # --- Water (GAL -> LB) ---
        water_gal_raw = row.get("WATER GALLONS", None)
        try:
            water_gal = float(water_gal_raw) if not pd.isna(water_gal_raw) else 0.0
        except (ValueError, TypeError):
            water_gal = 0.0

        if water_gal > 0.0:
            ingredients.append(("WATER", f"{water_gal:.3f}", "GL"))

        if ingredients:
            mixes.append({"name": mix_name, "ingredients": ingredients})

    return mixes


def write_output(mixes, path):
    """
    Write mixes to a .xls file matching the Keystone import format:
      Col A: Mix name  |  Col B: Ingredient  |  Col C: (empty)  |  Col D: Amount  |  Col E: Unit
    """
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Sheet1")

    out_row = 0

    for mix in mixes:
        name = (mix["name"] + PLANT_SEPARATOR).upper()

        for (ingredient, amount, unit) in mix["ingredients"]:
            ws.write(out_row, 0, name)
            ws.write(out_row, 1, ingredient.upper())
            # Column C intentionally left empty (col index 2)
            ws.write(out_row, 3, float(amount))
            ws.write(out_row, 4, unit)
            out_row += 1

    wb.save(path)
    print(f"Written {out_row} rows across {len(mixes)} mixes -> {path}")


if __name__ == "__main__":
    print(f"Parsing {INPUT} ...")
    mixes = parse_mixes(INPUT)
    print(f"Found {len(mixes)} mix designs.")
    if PLANT_SEPARATOR:
        print(f"Using plant separator: {repr(PLANT_SEPARATOR)}")
    write_output(mixes, OUTPUT)
