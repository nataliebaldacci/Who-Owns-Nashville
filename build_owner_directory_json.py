#!/usr/bin/env python3
"""Assemble owner_directory.json for the Owner Directory page:
owners (with reconciled status + FINAL parent), addresses, agents.
Runs after owner_rollup_pipeline.py / reconcile_final_rollup.py /
build_won_directory.py."""
import json, re, collections
import pandas as pd

STAMP='20260715'
def slugify(s):
    return re.sub(r'[^a-z0-9]+','-',str(s or '').lower()).strip('-')[:90]

rec=pd.read_csv(f'Owner_Rollup_RECONCILED_{STAMP}.csv')
owners_tbl=pd.read_csv('won_owners.csv')
addr_tbl=pd.read_csv('won_addresses.csv')
agents_tbl=pd.read_csv('won_agents.csv')

# group-level: label, parent, status, parcels, members
grp=collections.OrderedDict()
for _,r in rec.iterrows():
    g=grp.setdefault(int(r['group_id']),{'label':r['group_label'],'status':r['status'],
        'parent':'','parcels':0,'members':[]})
    g['parcels']+=int(r['owner_parcels'])
    g['members'].append(r['owner_name_clean'])
    if isinstance(r.get('final_parent'),str) and r['final_parent']: g['parent']=r['final_parent']
addr_slugs=dict(zip(owners_tbl['id'],owners_tbl['address_slugs'].fillna('')))

owners=[]
for gid,g in grp.items():
    slugs=[s.strip() for s in str(addr_slugs.get(gid,'')).split(',') if s.strip()][:12]
    owners.append([gid,g['parent'] or g['label'],g['parent'],g['status'],g['parcels'],
                   g['members'] if len(g['members'])>1 else [],slugs])
owners.sort(key=lambda o:-o[4])

addresses=[]
for _,r in addr_tbl.iterrows():
    ids=[int(x) for x in str(r['owner_ids']).split(',') if x.strip().isdigit()]
    addresses.append([r['slug'],r['address'],1 if r['hub_flag']=='HUB' else 0,ids])

agents=[]
for _,r in agents_tbl.iterrows():
    ids=[int(x) for x in str(r['owner_ids']).split(',') if x.strip().isdigit()]
    agents.append([r['agent'],r.get('kind') or '',ids])

out={'built':'2026-07-15','owners':owners,'addresses':addresses,'agents':agents}
json.dump(out,open('owner_directory.json','w'),separators=(',',':'))
import os
print('owners:',len(owners),'| addresses:',len(addresses),'| agents:',len(agents))
print('owner_directory.json: %.1f MB'%(os.path.getsize('owner_directory.json')/1e6))
