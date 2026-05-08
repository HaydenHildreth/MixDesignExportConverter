import sys
import pandas as pd
import re


def clean_csv(line_lst: list):
    """
    :param line_lst: cbc-mix-exp.txt.readlines()
    :return: List of corrected lines to write to file
    """
    new_lines = []
    for x in line_lst:
        # Remove any trailing commas
        if x[-1] == ',':
            x = x[:-1]
        line_index = line_lst.index(x)
        line_split = x.split(',')
        if len(line_split) >= 71:
            print('Columns mismatch at line: ' + str(line_index + 1) + f' - Expected 70, got {len(line_split)}')
            if line_split[2] not in ['False', 'True']:
                print('WARNING: Extra comma(s) detected in Mix ID or Mix Desc!')
                if x.index(',False,'):
                    metric_pos = x.index(',False,')
                elif x.index(',True,'):
                    metric_pos = x.index(',True,')
                else:
                    exit('Field "metric" not found - check file integrity.')
                # First comma SHOULD be correct.
                incorrect_str = x[x.index(',') + 1:metric_pos]
                correct_str = incorrect_str.replace(',', ' ')
                x = x.replace(incorrect_str, correct_str)
                print(f'Removed commas: {incorrect_str.replace(',','[,]')}')
        # Update to formatted line
        new_lines.append(x)
    return new_lines


# v0.3
# 5/8/2026
class KeystoneMixImport:
    def __init__(self, cbc_mix_exp: str, run_full: bool):
        """
        :param cbc_mix_exp: Filepath to cbc-mix-exp.txt
        :param run_full: Default: False; True: Runs all functions with defaults and outputs import SQL. MUST be
        True for .sql_to_file()
        """
        # ------------
        # Initialize Parameters
        # ------------

        self.cbc_mix_exp = cbc_mix_exp
        self.root = self.cbc_mix_exp[:self.cbc_mix_exp.rindex('\\')+1]
        self.fname = self.cbc_mix_exp[self.cbc_mix_exp.rindex('\\')+1:self.cbc_mix_exp.rindex('.')]
        self.run_full = run_full

        # ------------
        # Properties
        # ------------

        self.formatted = False
        if self.formatted is True:
            self.df = pd.read_csv(cbc_mix_exp, index_col=False)
        else:
            self.df = None

        # Updated using @property plant_id below
        self.plant_sep, self.plant_no = '', ''

        self.ing_cls = 'IN'
        self.co_cls = 'CO'
        self.co_sls_gl = ''

        # ------------
        # Constants
        # ------------

        self.HEADER = "mix,desc,metric,slump,yield,air,time,max,price,wname1,wtar1,wname2,wtar2,wname3,wtar3,wname4,wtar4,aname1,atar1,aname2,atar2,aname3,atar3,aname4,atar4,aname5,atar5,aname6,atar6,aname7,atar7,aname8,atar8,cname1,ctar1,cname2,ctar2,cname3,ctar3,cname4,ctar4,cname5,ctar5,cname6,ctar6,xname1,xtar1,xname2,xtar2,xname3,xtar3,xname4,xtar4,xname5,xtar5,xname6,xtar6,xname7,xtar7,xname8,xtar8,xname9,xtar9,xname10,xtar10,xname11,xtar11,xname12,xtar12\n"
        self.COLUMNS = self.HEADER.split(',')
        self.ING_NAME_COLS = {
            # Aggregate
            'A': ('aname1', 'aname2', 'aname3', 'aname4', 'aname5', 'aname6', 'aname7', 'aname8'),
            # Cement
            'C': ('cname1', 'cname2', 'cname3', 'cname4', 'cname5', 'cname6'),
            # Water
            'W': ('wname1', 'wname2', 'wname3', 'wname4'),
            # Admix
            'X': ('xname1', 'xname2', 'xname3', 'xname4', 'xname5', 'xname6', 'xname7', 'xname8', 'xname9', 'xname10',
                  'xname11', 'xname12')
        }
        self.ING_TAR_COLS = {
            'A': ('atar1', 'atar2', 'atar3', 'atar4', 'atar5', 'atar6', 'atar7', 'atar8'),
            'C': ('ctar1', 'ctar2', 'ctar3', 'ctar4', 'ctar5', 'ctar6'),
            'W': ('wtar1', 'wtar2', 'wtar3', 'wtar4'),
            'X': ('xtar1', 'xtar2', 'xtar3', 'xtar4', 'xtar5', 'xtar6', 'xtar7', 'xtar8', 'xtar9', 'xtar10', 'xtar11',
                  'xtar12')
        }
        # May need to account for /C in future
        self.UMS = {
            "X": 'OZ',
            "C": 'LB',
            "F": 'LB',
            "A": 'LB',
            "W": 'GL'
        }

    @property
    def plant_id(self):
        # '-', '01' -> '-01'
        if self.plant_sep == '' or self.plant_no == '':
            return 'NULL'
        return self.plant_sep + self.plant_no
    def format_cbc_exp(self):
        """
        :param out_name: Optional - output filename
        :return: Nothing - output is new file
        """
        # --------
        # Prepare input & output files
        # --------

        if self.plant_no != 'NULL':
            newfile = self.root + self.fname + f'_PLT_{self.plant_no}_COPY.txt'
        else:
            newfile = self.root + self.fname + '_COPY.txt'

            # Don't overwrite original file
            if self.cbc_mix_exp == newfile:
                sys.exit('Output file matches input - change filename')
        try:
            with open(self.cbc_mix_exp, 'r') as f:
                lines = f.readlines()
                f.close()
            # Update header line from batch export
            lines[0] = self.HEADER
        except Exception as e:
            exit(f'Error replacing header in cbc-mix-exp.txt - check filename, permissions:\n"{e}"')
        # --------
        # Cleaning function
        # --------
        try:
            new_lines = clean_csv(lines)
            # Write to file
            with open(newfile, 'w+') as f:
                f.writelines(new_lines)
                f.close()
                print(f'Wrote cleaned file to {newfile}')
                self.formatted = True

            # update df with cleaned file.

            self.df = pd.read_csv(newfile, index_col=False)
        except Exception as e:
            exit(f'Error writing to {newfile}:\n"{e}"')

    def get_ing_names(self, ing_type: str) -> list:
        """
        Takes set of columns from DF containing mix designs and flattens to one column w/ unique values
        Used by gen_ing_products_sql()
        :param ing_type: Ingredient type code - A, C, W, X
        :return: List of unique ingredient names.
        """
        flat_series = (pd.Series(self.df[list(self.ING_NAME_COLS[ing_type])]
                                 # Remove null values from ingredient list
                                 .replace(".", None)
                                 .values.flatten())
                       .drop_duplicates().reset_index(drop=True))
        ret_list = flat_series.tolist()
        try:
            ret_list.pop(ret_list.index(None))
            return ret_list
        except ValueError:
            return ret_list

    def gen_ing_products_sql(self, prod_cls: str) -> list[str]:
        """
        Generate SQL queries for inserting ingredients into ARTPROD
        :param: prod_cls: Product Class code
        :return: List of SQL queries for inserting ingredients
        """
        if self.df is None:
            exit('self.df not defined. Check result of format_cbc_exp()')
        ing_dict = {
            'A': self.get_ing_names('A'),
            'C': self.get_ing_names('C'),
            'W': self.get_ing_names('W'),
            'X': self.get_ing_names('X')
        }
        sql_list = []
        ing_updates = ['-----CORRECTED INGREDIENTS-----\n==============================\n']
        for x in ing_dict:
            ing_type = x
            ing_list = ing_dict[x]
            for prod_base in ing_list:
                # Remove quotation marks and whitespace
                prod_base_new = prod_base.replace("'", "").strip().upper()
                if prod_base_new != prod_base:
                    print(f"Corrected '{prod_base}' to '{prod_base_new}'")
                    self.df = self.df.replace(prod_base, prod_base_new)
                    ing_updates.append("'"+ prod_base + "' --> '" + prod_base_new + "'\n")
                if self.plant_id != 'NULL':
                    prod_code = prod_base_new + self.plant_id
                else:
                    prod_code = prod_base_new
                l1 = f"""INSERT INTO artprod (product_code, base_product, description_1, plant_no, product_class, product_type, ingredient_type, sellable_flag, unit_of_measure)\n """
                l2 = f"""SELECT '{prod_code}', '{prod_base_new}', '{prod_base_new}', '{self.plant_no}', '{prod_cls}', 'I', '{ing_type}', 'N', '{self.UMS[ing_type]}' FROM artloc\n """
                l3 = f"""WHERE loc_id = 0 AND NOT EXISTS (SELECT 1 FROM artprod WHERE product_code = '{prod_code}') AND NOT EXISTS (SELECT 1 FROM artprod WHERE base_product = '{prod_base_new}' AND plant_no = '{self.plant_no}');\n """
                l4 = f"""UPDATE artprod SET product_code='{prod_code}', base_product='{prod_base_new}', product_type = 'M', unit_of_measure='CY' WHERE EXISTS (SELECT 1 FROM artprod WHERE base_product IN ('{prod_base_new}','{prod_code}') AND plant_no = '{self.plant_no}') AND NOT EXISTS (SELECT 1 FROM artprod WHERE product_code = '{prod_code}');\n"""
                sql_list.append(l1 + l2 + l3 + l4)

        with open(self.root + f'PLT_{self.plant_no}_Corrected_Ings.txt', 'w+') as f:
            f.writelines(ing_updates)
            f.close()

        return sql_list

    def gen_mix_products_sql(self, prod_cls: str, sales_gl: str):
        mix_df = self.df.loc[:, ['mix', 'desc']]
        ins_sql_list = ["CREATE TABLE TMP_SNO(SNO INTEGER); DELETE FROM TMP_SNO; INSERT INTO TMP_SNO (SNO) SELECT session_no FROM CCP_SESSION_BEGIN('ADMIN', 'Insert Mix Structure', '127.0.0.1', '5.x.x'); COMMIT;"]
        mix_updates = ['-----CORRECTED MIXES-----\n=========================\n']
        for row in mix_df.itertuples():
            prod_base = row.mix
            prod_desc = row.desc.replace("'", "")
            # Remove quotation marks and whitespace
            prod_base_new = prod_base.replace("'", "").strip().upper()
            if prod_base_new != prod_base:
                print(f"Corrected '{prod_base}' to '{prod_base_new}'")
                self.df = self.df.replace(prod_base, prod_base_new)
                mix_updates.append("'" + prod_base + "' --> '" + prod_base_new + "'\n")
            if self.plant_id != 'NULL':
                prod_code = prod_base_new + self.plant_id
            else:
                prod_code = prod_base_new

            l1 = f"""INSERT INTO artprod (product_code, base_product, description_1, plant_no, product_class, product_type, sellable_flag, unit_of_measure, sales_gl) SELECT '{prod_code}', '{prod_base_new}', '{prod_desc}', '{self.plant_no}', '{prod_cls}', 'M', 'Y', 'CY', '{sales_gl}' FROM artloc\n """
            l2 = f"""WHERE loc_id = 0 AND NOT EXISTS (SELECT 1 FROM artprod WHERE product_code = '{prod_code}') AND NOT EXISTS (SELECT 1 FROM artprod WHERE base_product = '{prod_base_new}' AND plant_no = {self.plant_no});\n """
            l3 = f"""UPDATE artprod SET product_code='{prod_code}', base_product='{prod_base_new}', product_type = 'M', unit_of_measure='CY' WHERE EXISTS (SELECT 1 FROM artprod WHERE base_product IN ('{prod_base_new}', '{prod_code}') AND plant_no = '{self.plant_no}') AND NOT EXISTS (SELECT 1 FROM artprod WHERE product_code = '{prod_code}');\n """
            l4 = f"""DELETE FROM artprstr WHERE assy_product_code='{prod_code}';\n"""
            ins_sql_list.append(l1 + l2 + l3 + l4)

        with open(self.root + f'PLT_{self.plant_no}_Corrected_Mixes.txt', 'w+') as f:
            f.writelines(mix_updates)
            f.close()

        return ins_sql_list

    def gen_mix_design_sql(self):
        # Splits fields into atar1 --> (atar, 1)
        def split_field_name(field_name):
            match = re.match(r'^(.*?)(\d+)$', field_name)
            if match:
                return match.group(1), int(match.group(2))  # (prefix, number)
            return field_name, None

        name_cols = []
        tar_cols = []

        # Need to get the individual columns broken down to iterate over
        for x in self.ING_NAME_COLS:
            col_list = list(map(split_field_name, self.ING_NAME_COLS[x]))
            name_cols.extend(col_list)
        for x in self.ING_TAR_COLS:
            col_list = list(map(split_field_name, self.ING_TAR_COLS[x]))
            tar_cols.extend(col_list)

        df = self.df
        tr_no = 1
        sql_list = []

        bad_vals = ['.', 0, '', None]

        # Generate sql for mix structure in each row, iterated for each ingredient/amount.
        for row in df.itertuples():
            assy_prod = row.mix
            for i, d in zip(name_cols, tar_cols):

                name_fld = str(i[0] + str(i[1]))
                tar_fld = str(d[0] + str(d[1]))
                # Only SKIP empty fields since we do not iterate by ordinal number (xtar1 comes after atar3 etc.)
                if getattr(row, name_fld) in bad_vals or getattr(row, tar_fld) in bad_vals:
                    continue
                # Integrity check -- aname1 = atar1, below checks a = a, 1 = 1, etc.
                if i[1] != d[1] or i[0][0] != d[0][0]:
                    exit(f'Index mismatch when generating SQL for {name_fld}, {tar_fld} -- check file integrity')

                # Assemble dictionary - {name, value}
                comp_dict = {name_fld: getattr(row, name_fld), tar_fld: getattr(row, tar_fld)}

                # Construct ingredient name & mix name w/ plant id
                ing_name = comp_dict[name_fld]

                if self.plant_id != 'NULL':
                    ing_name = comp_dict[name_fld] + self.plant_id
                    assy_prod = row.mix + self.plant_id

                # Sequencing is done via field ending id num -- ex: atar3 is seq 3 for aggregates
                # Current sequence order - A,C,W,X
                u_of_m = self.UMS[i[0][0].upper()]
                insert = 'INSERT INTO artprstr (session_no, trans_no, sequence_code, assy_product_code, comp_product_code, qty_assembly, comp_ums, imported_flag, last_change_datetime, last_change_user) \n'
                values = f"VALUES ( (SELECT SNO FROM TMP_SNO), {tr_no}, {i[1]}, UPPER('{assy_prod}'), UPPER('{ing_name}'), {comp_dict[tar_fld]}, UPPER('{u_of_m}'), 'Y', CAST('TODAY' AS TIMESTAMP), 'HIT');\n"""
                sql_list.append(insert + values)
                tr_no += 1
        return sql_list

    def sql_to_file(self, ftype='txt'):
        """
        :param ftype: Output Filetype -- txt or sql
        :return:
        """
        def write_to_file(file_name, func_name):
            work_path = self.root
            try:
                with open(work_path + file_name, 'w+') as f:
                    f.writelines(func_name)
                    f.close()
                    print(f'Results saved to {work_path + file_name} successfully.\n')
            except Exception as e:
                print(f'Error writing {file_name} to {work_path}: {e}\n')
            return None
        print(f'========= Plant{self.plant_id} Import =========\n --- START ---')
        print('--- Formatting batch file ---')
        self.format_cbc_exp()
        print('--- Writing SQL for Ingredients -> ARTPROD ---\n')
        write_to_file(f'PLT_{self.plant_no}_SQL_Ing_Prods.{ftype}', self.gen_ing_products_sql(prod_cls=self.ing_cls))
        print('--- Writing SQL for Mixes -> ARTPROD ---\n')
        write_to_file(f'PLT_{self.plant_no}_SQL_Mix_Prods.{ftype}', self.gen_mix_products_sql(prod_cls=self.co_cls, sales_gl=self.co_sls_gl))
        print('--- Writing SQL for Mix Design --> ARTPRSTR ---\n')
        write_to_file(f'PLT_{self.plant_no}_SQL_Mix_Structure.{ftype}', self.gen_mix_design_sql())
        print(f' =========== END =========== ')
        return
