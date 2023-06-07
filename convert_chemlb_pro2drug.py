#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import pymysql

# 连接MySQL数据库
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='passwd',
                       db='chembl_32',
                       charset='utf8mb4')

# 查询数据
sql = '''
SELECT m.molregno AS molregno, 
m.chembl_id AS compound_chembl_id,
td.pref_name AS target_name,
cs.accession AS protein_accession,
cs.sequence AS protein_sequence,
td.target_type,   
s.canonical_smiles,   
r.compound_key,  
a.description AS assay_description,   
act.standard_type,   
act.standard_relation,   
act.standard_value,   
act.standard_units,   
act.activity_comment 
FROM compound_structures s
RIGHT JOIN molecule_dictionary m ON s.molregno = m.molregno 
JOIN compound_records r ON m.molregno = r.molregno  
JOIN docs d ON r.doc_id = d.doc_id 
JOIN activities act ON r.record_id = act.record_id
JOIN assays a ON act.assay_id = a.assay_id 
JOIN target_dictionary td ON a.tid = td.tid 
JOIN target_components tc ON td.tid = tc.tid
JOIN component_sequences cs ON tc.component_id = cs.component_id
AND td.target_type = 'SINGLE PROTEIN' 
AND act.standard_type = 'IC50' 
AND act.standard_units = 'nM';
'''

df = pd.read_sql(sql, conn)

# 保存数据到CSV文件
df.to_csv('protein_inhibitors.csv', index=False)

# 关闭数据库连接
conn.close()


