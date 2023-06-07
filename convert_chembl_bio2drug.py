import pandas as pd
import pymysql

# 连接MySQL数据库
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='***passwd***',
                       db='chembl_31',
                       charset='utf8mb4')

# 查询数据
sql = '''
SELECT td.chembl_id AS target_chembl_id, td.pref_name AS target_name, td.target_type, td.organism,
       cs.molregno, cs.canonical_smiles, a.standard_type, a.standard_relation, a.standard_value, a.standard_units,
       a.pchembl_value, a.activity_comment
FROM target_dictionary td
LEFT JOIN target_components tc ON td.tid = tc.tid
LEFT JOIN assays s ON td.tid = s.tid
LEFT JOIN activities a ON s.assay_id = a.assay_id
LEFT JOIN compound_structures cs ON a.molregno = cs.molregno
LEFT JOIN organism o ON td.organism = o.tax_id
WHERE o.scientific_name IN ('Mycobacterium tuberculosis', 'Plasmodium falciparum')
'''

df = pd.read_sql(sql, conn)

# 保存数据到CSV文件
df.to_csv('pathogen_inhibitors.csv', index=False)

# 关闭数据库连接
conn.close()
