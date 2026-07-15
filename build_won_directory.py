#!/usr/bin/env python3
"""Build Who-Owns-Atlanta-style directory tables for Nashville, plus a
Nashville <-> Atlanta shared-address crosswalk.

Outputs (WOA schema, so the same site patterns apply):
  won_owners.csv     id, name, member_names, parcels, address_slugs
  won_addresses.csv  slug, address, owner_ids, owner_names, hub_flag
  won_agents.csv     slug, agent, kind (case person / SOS registered agent), owner_ids
  won_atl_crosswalk.csv  shared mailing addresses between Nashville owner
                         groups and Who Owns Atlanta owners

Runs after owner_rollup_pipeline.py (uses its Owner_Rollup_Linked output).
"""
import re, collections
import pandas as pd

BASE='data/rollup_inputs/'
STAMP='20260715'

def slugify(s):
    s=re.sub(r'[^a-z0-9]+','-',str(s or '').lower()).strip('-')
    return s[:90]

# reuse the pipeline's cleaning
import importlib.util
def clean_addr(s):
    import re as _re
    s=str(s or '').upper()
    s=_re.sub(r'[^A-Z0-9# ]',' ',s); s=_re.sub(r'\s+',' ',s).strip()
    for pat,rep in [(r'\bPOST OFFICE BOX\b','PO BOX'),(r'\bP\s*O\s*BOX\b','PO BOX'),
      (r'\bSUITE\b','STE'),(r'#','STE '),(r'\bAVENUE\b','AVE'),(r'\bSTREET\b','ST'),
      (r'\bDRIVE\b','DR'),(r'\bROAD\b','RD'),(r'\bBOULEVARD\b','BLVD'),(r'\bPARKWAY\b','PKWY'),
      (r'\bPLACE\b','PL'),(r'\bLANE\b','LN'),(r'\bCOURT\b','CT'),(r'\bNORTH\b','N'),
      (r'\bSOUTH\b','S'),(r'\bEAST\b','E'),(r'\bWEST\b','W'),(r'\bFLOOR\b','FL')]:
        s=_re.sub(pat,rep,s)
    return _re.sub(r'\s+',' ',s).strip()
def clean_name(s):
    import re as _re
    s=str(s or '').upper(); s=_re.sub(r'[^A-Z0-9& ]',' ',s); s=_re.sub(r'\s+',' ',s).strip()
    return s
AGENT_PAT=re.compile(r'C/?O|RYAN LLC|RYAN TAX|CORPORATION SERVICE|C T CORP|CT CORP|REGISTERED AGENT|NATIONAL REGISTERED|UNITED AGENT|COGENCY|INCORP SERVICES|CSC\b|LEGALINC|NORTHWEST REGISTERED|PARACORP|2908 POSTON AVE|800 S GAY ST')

# ---- Nashville owner groups + their addresses --------------------------------
link=pd.read_csv(f'Owner_Rollup_Linked_{STAMP}.csv')
oh=pd.read_csv(BASE+'ownership_history_flattened.csv.xz',low_memory=False,
    usecols=['ParcelID','Owner1_Name','Owner1_Address','Owner1_City','Owner1_State','Owner1_Zip'])
oh['name_clean']=oh['Owner1_Name'].map(clean_name)
oh['addr_clean']=(oh['Owner1_Address'].fillna('')+' '+oh['Owner1_City'].fillna('')+' '
                  +oh['Owner1_State'].fillna('')+' '+oh['Owner1_Zip'].fillna('').astype(str)).map(clean_addr)
name2group=dict(zip(link['owner_name_clean'],link['group_id']))
gname=dict(zip(link['group_id'],link['group_name']))
oh['group_id']=oh['name_clean'].map(name2group)
ohg=oh.dropna(subset=['group_id']).copy()
ohg['group_id']=ohg['group_id'].astype(int)

# owners table
own_rows=[]
addr_owner=collections.defaultdict(set)
for gid,g in ohg.groupby('group_id'):
    addrs=sorted({a for a in g['addr_clean'] if a and len(a)>8})
    slugs=[slugify(a) for a in addrs][:12]
    for a in addrs: addr_owner[a].add(gid)
    own_rows.append({'id':gid,'name':gname[gid],
        'member_names':link[link.group_id==gid]['owner_name_clean'].nunique(),
        'parcels':g['ParcelID'].nunique(),
        'address_slugs':', '.join(slugs)})
owners=pd.DataFrame(own_rows).sort_values('parcels',ascending=False)
owners.to_csv('won_owners.csv',index=False)

# addresses table
addr_rows=[]
for a,gids in addr_owner.items():
    addr_rows.append({'slug':slugify(a),'address':a,
        'owner_ids':', '.join(str(g) for g in sorted(gids)),
        'owner_names':'; '.join(sorted({gname[g] for g in gids})[:8]),
        'n_owner_groups':len(gids),
        'hub_flag':'HUB' if (AGENT_PAT.search(a) or len(gids)>=12 or (a.startswith('PO BOX') and len(gids)>=6)) else ''})
addresses=pd.DataFrame(addr_rows).sort_values('n_owner_groups',ascending=False)
addresses.to_csv('won_addresses.csv',index=False)

# agents table: SOS registered agents + case people (documentation, not linking)
ag=collections.defaultdict(lambda:{'kind':'','owners':set()})
sos=pd.read_excel(BASE+'TNSOS_Resolved_STEMS_20260714.xlsx')
for _,r in sos.iterrows():
    nm=clean_name(r.get('registered_agent_name'))
    if not nm or nm in ('NAN','NONE','NULL') or len(nm)<4: continue
    gid=name2group.get(clean_name(r['input_owner']))
    if gid is None: continue
    ag[nm]['kind']='SOS registered agent'; ag[nm]['owners'].add(int(gid))
lp=pd.read_csv(BASE+'landlord_registration_people_flattened.csv.xz',low_memory=False)
ENT=re.compile(r'\b(LLC|LP|INC|CORP|TRUST|GP|LTD|HOLDINGS|PROPERTIES|HOMES)\b')
for _,row in lp.iterrows():
    ents=set()
    for c in ['ownerName','applicant']+[f'P{k}_name' for k in range(1,8)]:
        v=row.get(c)
        if isinstance(v,str) and ENT.search(v.upper()):
            gid=name2group.get(clean_name(v))
            if gid is not None: ents.add(int(gid))
    if not ents: continue
    for k in range(1,8):
        v=row.get(f'P{k}_name'); role=row.get(f'P{k}_role')
        if isinstance(v,str) and not ENT.search(v.upper()) and isinstance(role,str):
            nm=clean_name(v)
            if len(nm)>=7 and ' ' in nm:
                ag[nm]['kind']=ag[nm]['kind'] or ('case person: '+role)
                ag[nm]['owners'].update(ents)
agents=pd.DataFrame([{'slug':slugify(k),'agent':k,'kind':v['kind'],
    'n_owner_groups':len(v['owners']),
    'owner_ids':', '.join(str(x) for x in sorted(v['owners'])[:40])}
    for k,v in ag.items() if v['owners']]).sort_values('n_owner_groups',ascending=False)
agents.to_csv('won_agents.csv',index=False)

# ---- Nashville <-> Atlanta shared-address crosswalk ---------------------------
woa=pd.read_csv('/root/.claude/uploads/6ba4e66d-6ed7-5650-bff1-8b675f5eb8ef/0be1cddc-woa_addresses.csv')
woa['addr_clean']=woa['address'].map(clean_addr)
woa_by_addr={r['addr_clean']:r for _,r in woa.iterrows() if isinstance(r.get('owner_names'),str) and r['owner_names']}
cross=[]
for a,gids in addr_owner.items():
    w=woa_by_addr.get(a)
    if w is None: continue
    cross.append({'address':a,
        'nashville_owner_groups':'; '.join(sorted({gname[g] for g in gids})[:6]),
        'nashville_parcels':int(ohg[ohg['addr_clean']==a]['ParcelID'].nunique()),
        'atlanta_owners':w['owner_names'],
        'hub_flag':'HUB' if AGENT_PAT.search(a) else ''})
cw=pd.DataFrame(cross).sort_values('nashville_parcels',ascending=False)
cw.to_csv('won_atl_crosswalk.csv',index=False)

print(f'won_owners.csv:    {len(owners):,} owner groups')
print(f'won_addresses.csv: {len(addresses):,} addresses ({int((addresses.hub_flag=="HUB").sum()):,} hubs)')
print(f'won_agents.csv:    {len(agents):,} agents/people')
print(f'won_atl_crosswalk.csv: {len(cw):,} addresses shared with Who Owns Atlanta')
print('\nTop shared Nashville-Atlanta addresses:')
print(cw.head(12).to_string(index=False,max_colwidth=60))
