#!/usr/bin/env python3
"""Reconcile the pipeline's linked owner groups against the curated FINAL
entity-to-parent table (authoritative). For every pipeline group:

  CONFIRMED  every FINAL-parented member agrees on one parent, and the
             pipeline linked nothing else - independent methods agree
  EXTENDS    the group ties additional unparented names to a FINAL family -
             candidate additions for the curated crosswalk (review queue)
  CONFLICT   the group spans two or more different FINAL parents - either a
             pipeline false-positive or a real hidden connection (review!)
  UNLABELED  no member appears in the FINAL curated set

Outputs: Owner_Rollup_RECONCILED_<date>.csv (per owner name),
Rollup_Review_Queue_<date>.csv (EXTENDS + CONFLICT groups only).
"""
import re, collections
import pandas as pd

STAMP='20260715'
def clean_name(s):
    s=str(s or '').upper()
    s=re.sub(r'[^A-Z0-9& ]',' ',s)
    s=re.sub(r'\s+',' ',s).strip()
    for pat,rep in [(r'\bL\s*L\s*C\b','LLC'),(r'\bL\s*L\s*P\b','LLP'),(r'\bL\s*P\b','LP'),
      (r'\bLLLC\b','LLC'),(r'\bINCORPORATED\b','INC'),(r'\bCOMPANY\b','CO'),(r'\bLIMITED\b','LTD')]:
        s=re.sub(pat,rep,s)
    return s

link=pd.read_csv(f'Owner_Rollup_Linked_{STAMP}.csv')
e2p=pd.read_csv('data/rollup_inputs/FINAL_Entity_to_Parent_20260714.csv.xz',low_memory=False)
par=e2p[e2p['parent_operator'].notna()&(e2p['parent_operator']!='')].copy()
par['key']=par['canon_name'].map(clean_name)
parent_of=dict(zip(par['key'],par['parent_operator']))
attrib_of=dict(zip(par['key'],par['attribution_source']))
print(f'FINAL curated: {len(parent_of):,} entities -> {par["parent_operator"].nunique()} parents')

link['final_parent']=link['owner_name_clean'].map(parent_of)
link['final_attrib']=link['owner_name_clean'].map(attrib_of)
hit=link['final_parent'].notna().sum()
print(f'pipeline names matched to FINAL entities: {hit:,} of {len(link):,}')

rows=[];queue=[]
for gid,g in link.groupby('group_id'):
    parents=sorted(set(g['final_parent'].dropna()))
    n_par=g['final_parent'].notna().sum()
    if not parents: status='UNLABELED'; label=g['group_name'].iat[0]
    elif len(parents)>1: status='CONFLICT'; label=parents[0]
    elif n_par==len(g): status='CONFIRMED'; label=parents[0]
    else: status='EXTENDS'; label=parents[0]
    for _,r in g.iterrows():
        rows.append({'owner_name_clean':r['owner_name_clean'],'group_id':gid,
            'group_label':label,'final_parent':r['final_parent'] if pd.notna(r['final_parent']) else '',
            'status':status,'owner_parcels':r['owner_parcels'],
            'attribution':r['final_attrib'] if pd.notna(r['final_attrib']) else ('pipeline-link' if status in('EXTENDS','CONFLICT') and pd.isna(r['final_parent']) else '')})
    if status in ('EXTENDS','CONFLICT'):
        newly=g[g['final_parent'].isna()]
        queue.append({'group_id':gid,'status':status,
            'parents':' | '.join(parents),
            'curated_members':int(n_par),'new_members':int(len(g)-n_par),
            'new_parcels':int(newly['owner_parcels'].sum()),
            'new_names':'; '.join(newly['owner_name_clean'].head(10))})

out=pd.DataFrame(rows)
out.to_csv(f'Owner_Rollup_RECONCILED_{STAMP}.csv',index=False)
q=pd.DataFrame(queue).sort_values(['status','new_parcels'],ascending=[True,False])
q.to_csv(f'Rollup_Review_Queue_{STAMP}.csv',index=False)

st=out.groupby('status').agg(names=('owner_name_clean','nunique'),parcels=('owner_parcels','sum'))
print('\nreconciliation:')
print(st.to_string())
print(f"\nreview queue: {len(q):,} groups ({(q.status=='CONFLICT').sum()} conflicts, {(q.status=='EXTENDS').sum()} extensions)")
print('\nBiggest EXTENDS (pipeline adds names to a curated family):')
print(q[q.status=='EXTENDS'].head(10)[['parents','curated_members','new_members','new_parcels','new_names']].to_string(index=False,max_colwidth=70))
print('\nCONFLICTS (two curated parents linked together - inspect):')
print(q[q.status=='CONFLICT'].head(10)[['parents','curated_members','new_members','new_names']].to_string(index=False,max_colwidth=70))
