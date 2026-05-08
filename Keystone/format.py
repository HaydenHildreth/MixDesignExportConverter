import cbc_import as cbc

# All plants config
all_plant_cfg = {'plant_sep': '-', 'ing_cls': 'IN', 'co_cls': 'CO'}

# Plant specific config
filepath1 = r'C:\Path To File\cbc-mix-exp.txt'
filepath2 = r'C:\Path To File 2\cbc-mix-exp.txt'

plant_1_cfg = {'cbc_mix_exp': filepath1, 'plant_no': '01', 'co_sls_gl': '4000-01'}
plant_2_cfg = {'cbc_mix_exp': filepath2, 'plant_no': '02', 'co_sls_gl': '4000-02'}

plants = [plant_1_cfg, plant_2_cfg]
for x in plants:
    cls = cbc.KeystoneMixImport(x['cbc_mix_exp'], True)
    cls.plant_sep = all_plant_cfg['plant_sep']
    cls.plant_no = x['plant_no']
    cls.ing_cls = all_plant_cfg['ing_cls']
    cls.co_cls = all_plant_cfg['co_cls']
    cls.co_sls_gl = x['co_sls_gl']

    # Takes argument ftype = 'sql' to output to sql file instead of txt.
    cls.sql_to_file()
    #cls.sql_to_file(ftype='sql')
