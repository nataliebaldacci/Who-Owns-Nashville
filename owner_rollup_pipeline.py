#!/usr/bin/env python3
"""Owner dedupe + rollup pipeline for Who Owns Nashville.

Replicates the linking methodology of Hangen & O'Brien (2024, Housing Studies,
"Linking Landlords to Uncover Ownership Obscurity") and Shelton & Seymour
(2024, Annals AAG, "Horizontal Holdings"), adapted to Davidson County sources:

  Stage 0  extract current corporate/trust owners from the ownership history
  Stage 1  rigorous name + address cleaning and standardization
  Stage 2  exact matches on cleaned name (collapses spelling variants)
  Stage 3  probabilistic matches: char 3-gram TF-IDF cosine >= 0.85
  Stage 4  shared NON-HUB mailing addresses (the Horizontal Holdings rule:
           service addresses - registered-agent mills, C/O tax reps, shared
           PO Boxes - are non-informative and never link owners)
  Stage 5  TN Secretary of State: principal-office / mailing addresses of the
           resolved entity (registered-agent addresses excluded entirely)
  Stage 6  shared PEOPLE from landlord-registration case_people (owner-side
           roles only; property managers and billing contacts never link)
  Stage 7  connected components -> owner groups; canonical labels prefer the
           existing curated parent names (Ownership_Rollup canon_parent)

Inputs (data/rollup_inputs/): ownership_history_flattened.csv.xz,
TNSOS_Resolved_STEMS_20260714.xlsx, landlord_registration_people_flattened.csv.xz,
Ownership_Rollup_CURRENT_Corporate_20260711.csv
Outputs: Owner_Rollup_Linked_<date>.csv, Owner_Groups_Summary_<date>.csv,
and stage-by-stage counts on stdout (for the methodology log).
"""
import re, sys, json, collections
import numpy as np
import pandas as pd

BASE='data/rollup_inputs/'
STAMP='20260715'

# ---------------------------------------------------------------- cleaning --
SUFFIX_FIX=[(r'\bL\s*L\s*C\b','LLC'),(r'\bL\s*L\s*P\b','LLP'),(r'\bL\s*P\b','LP'),
 (r'\bLLLC\b','LLC'),(r'\bCORPORAITON\b','CORPORATION'),(r'\bCRP\b','CORP'),
 (r'\bINCORPORATED\b','INC'),(r'\bINCORP\b','INC'),(r'\bCOMPANY\b','CO'),
 (r'\bLIMITED\b','LTD'),(r'\bPARTNERSHIPS?\b','PARTNERSHIP'),
 (r'\bASSOCIATION\b','ASSOC'),(r'\bTRUSTEES?\b','TRUSTEE')]
DROP_SUFFIX=re.compile(r'\b(LLC|LLP|LP|INC|CORP|CORPORATION|CO|LTD|GP|PLLC|PC|TRUST|TR|PARTNERSHIP|ASSOC)\b\.?$')

def clean_name(s):
    s=str(s or '').upper()
    s=re.sub(r'[^A-Z0-9& ]',' ',s)
    s=re.sub(r'\s+',' ',s).strip()
    for pat,rep in SUFFIX_FIX: s=re.sub(pat,rep,s)
    return s

def stem_name(s):
    """cleaned name with trailing org suffixes iteratively stripped"""
    s=clean_name(s); prev=None
    while s!=prev:
        prev=s; s=DROP_SUFFIX.sub('',s).strip()
    return s

ADDR_FIX=[(r'\bPOST OFFICE BOX\b','PO BOX'),(r'\bP\s*O\s*BOX\b','PO BOX'),
 (r'\bSUITE\b','STE'),(r'\bSUIT\b','STE'),(r'#','STE '),(r'\bAVENUE\b','AVE'),
 (r'\bSTREET\b','ST'),(r'\bDRIVE\b','DR'),(r'\bROAD\b','RD'),(r'\bBOULEVARD\b','BLVD'),
 (r'\bPARKWAY\b','PKWY'),(r'\bPLACE\b','PL'),(r'\bLANE\b','LN'),(r'\bCOURT\b','CT'),
 (r'\bNORTH\b','N'),(r'\bSOUTH\b','S'),(r'\bEAST\b','E'),(r'\bWEST\b','W'),
 (r'\bFLOOR\b','FL'),(r'\bFLR\b','FL')]
def clean_addr(s):
    s=str(s or '').upper()
    s=re.sub(r'[^A-Z0-9# ]',' ',s)
    s=re.sub(r'\s+',' ',s).strip()
    for pat,rep in ADDR_FIX: s=re.sub(pat,rep,s)
    s=re.sub(r'\s+',' ',s).strip()
    return s

CORP_PAT=re.compile(r'\b(LLC|LLP|LP|INC|CORP|CORPORATION|CO|LTD|GP|PLLC|HOLDINGS?|PROPERTIES|REALTY|INVESTMENTS?|FUND|PARTNERS?|VENTURES?|HOMES|RENTALS?|CAPITAL|BORROWER|PROPCO|ASSETS?|EQUITY|GROUP|DEVELOPMENT|BUILDERS?|CONSTRUCTION|ENTERPRISES?|SOLUTIONS)\b')
TRUST_PAT=re.compile(r'\b(TRUST|TRUSTEE|TR|LIVING TR|REV TR|REVOCABLE)\b')
GOV_PAT=re.compile(r'\b(METRO|METROPOLITAN GOVERNMENT|STATE OF|HOUSING AUTH|UNITED STATES|BOARD OF|COUNTY OF)\b')
def is_entity(nm):
    n=clean_name(nm)
    return bool(n) and not GOV_PAT.search(n) and bool(CORP_PAT.search(n) or TRUST_PAT.search(n))

# service / agent hub markers: these addresses never link owners
AGENT_PAT=re.compile(r'C/?O|RYAN LLC|RYAN TAX|CORPORATION SERVICE|C T CORP|CT CORP|REGISTERED AGENT|NATIONAL REGISTERED|UNITED AGENT|COGENCY|INCORP SERVICES|CSC\b|LEGALINC|NORTHWEST REGISTERED|PARACORP|2908 POSTON AVE|800 S GAY ST')

# ---------------------------------------------------------------- stage 0 ---
print('=== Stage 0: extract current corporate/trust owners ===')
oh=pd.read_csv(BASE+'ownership_history_flattened.csv.xz',low_memory=False,
    usecols=['ParcelID','Owner1_Name','Owner1_Address','Owner1_City','Owner1_State','Owner1_Zip'])
oh=oh.dropna(subset=['Owner1_Name'])
oh['is_ent']=oh['Owner1_Name'].map(is_entity)
ent=oh[oh['is_ent']].copy()
print(f'parcels with current owner: {len(oh):,} | corporate/trust-owned: {len(ent):,}')
ent['name_clean']=ent['Owner1_Name'].map(clean_name)
ent['stem']=ent['Owner1_Name'].map(stem_name)
ent['addr_clean']=(ent['Owner1_Address'].fillna('')+' '+ent['Owner1_City'].fillna('')+' '
                   +ent['Owner1_State'].fillna('')+' '+ent['Owner1_Zip'].fillna('').astype(str)).map(clean_addr)
raw_owner_addr=ent.groupby(['Owner1_Name','Owner1_Address']).size()
print(f'unique raw (name,address) owners: {len(raw_owner_addr):,}')

# owner universe: one node per cleaned name
nodes=ent.groupby('name_clean').agg(parcels=('ParcelID','nunique'),
    stem=('stem','first'),
    raw_names=('Owner1_Name',lambda s:sorted(set(s))[:5]),
    addrs=('addr_clean',lambda s:sorted(set(a for a in s if a))[:6])).reset_index()
print(f'Stage 1-2 (clean + exact name): {ent["Owner1_Name"].nunique():,} raw names -> {len(nodes):,} cleaned owners')

# union-find over node indices
parent=list(range(len(nodes)))
def find(a):
    while parent[a]!=a: parent[a]=parent[parent[a]]; a=parent[a]
    return a
def union(a,b):
    ra,rb=find(a),find(b)
    if ra!=rb: parent[max(ra,rb)]=min(ra,rb)
idx_of={n:i for i,n in enumerate(nodes['name_clean'])}
comp_parcels={i:int(nodes['parcels'].iat[i]) for i in range(len(nodes))}
def union_guarded(a,b,cap=300):
    ra,rb=find(a),find(b)
    if ra==rb: return False
    if comp_parcels[ra]>cap and comp_parcels[rb]>cap: return False   # both large: needs review, not auto-merge
    union(ra,rb); r=find(ra)
    comp_parcels[r]=comp_parcels.get(ra,0)+comp_parcels.get(rb,0)
    return True
def count_groups(): return len({find(i) for i in range(len(nodes))})
def top_components(k=3):
    from collections import Counter
    c=Counter(find(i) for i in range(len(nodes)))
    return [n for _,n in sorted(((v,v) for v in c.values()),reverse=True)[:k]]

# stems: same stem -> same owner family
stem_groups=collections.defaultdict(list)
for i,s in enumerate(nodes['stem']):
    if s: stem_groups[s].append(i)
for g in stem_groups.values():
    for j in g[1:]: union(g[0],j)
print(f'after stem linking: {count_groups():,} groups | largest: {top_components()}')

# ---------------------------------------------------------------- stage 3 ---
print('=== Stage 3: fuzzy 3-gram cosine >= 0.85 (Hangen & O\'Brien) ===')
from sklearn.feature_extraction.text import TfidfVectorizer
names=nodes['stem'].where(nodes['stem'].str.len()>=4,nodes['name_clean']).tolist()
vec=TfidfVectorizer(analyzer='char_wb',ngram_range=(3,3),min_df=1)
X=vec.fit_transform(names)
Xn=X.multiply(1/np.sqrt(X.multiply(X).sum(axis=1))).tocsr()
fuzzy_pairs=0
CH=2000
for start in range(0,Xn.shape[0],CH):
    sims=(Xn[start:start+CH]@Xn.T).tocoo()
    for r,c,v in zip(sims.row,sims.col,sims.data):
        i=start+r
        if c<=i or v<0.85: continue
        union(i,c); fuzzy_pairs+=1
print(f'fuzzy pairs linked: {fuzzy_pairs:,} | groups now: {count_groups():,} | largest: {top_components()}')

# ---------------------------------------------------------------- stage 4 ---
print('=== Stage 4: shared non-hub deed mailing addresses ===')
addr_names=collections.defaultdict(set)
for nm,ac in zip(ent['name_clean'],ent['addr_clean']):
    if ac and len(ac)>8: addr_names[ac].add(nm)
hub=set()
addr_stems={}
for a,nm in addr_names.items():
    stems={nodes['stem'].iat[idx_of[n]] for n in nm}
    addr_stems[a]=stems
    if AGENT_PAT.search(a): hub.add(a)
    elif a.startswith('PO BOX') and len(stems)>=6: hub.add(a)
    elif len(stems)>=12: hub.add(a)          # heavy sharing: attorney/manager/service hub
print(f'addresses: {len(addr_names):,} | flagged as non-informative hubs: {len(hub):,}')
linked=0
for a,nm in addr_names.items():
    # conservative: only small clusters link (2-8 distinct stems); big shared
    # addresses are far more likely service/manager hubs than one owner
    if a in hub or not (2<=len(addr_stems[a])<=8): continue
    ids=[idx_of[n] for n in nm]
    for j in ids[1:]:
        if union_guarded(ids[0],j): linked+=1
print(f'address links applied: {linked:,} | groups now: {count_groups():,} | largest: {top_components()}')

# ---------------------------------------------------------------- stage 5 ---
print('=== Stage 5: TN SOS principal/mailing addresses (agents excluded) ===')
sos=pd.read_excel(BASE+'TNSOS_Resolved_STEMS_20260714.xlsx')
sos['stem_clean']=sos['input_owner'].map(stem_name)
sos_addr_names=collections.defaultdict(set)
matched_sos=0
for _,r in sos.iterrows():
    s=r['stem_clean']
    hit=[i for i in stem_groups.get(s,[])]
    if not hit:
        # fall back: exact cleaned-name match
        i=idx_of.get(clean_name(r['input_owner']))
        hit=[i] if i is not None else []
    if not hit: continue
    matched_sos+=1
    for fld in ('principal_office_address','mailing_address'):
        a=clean_addr(r.get(fld))
        if a and len(a)>8 and not AGENT_PAT.search(a):
            for i in hit: sos_addr_names[a].add(i)
linked=0
for a,ids in sos_addr_names.items():
    ids=list(ids)
    for j in ids[1:]:
        if find(ids[0])!=find(j): linked+=1
        union(ids[0],j)
print(f'SOS stems matched to owner universe: {matched_sos:,} of {len(sos):,}')
print(f'SOS address links applied: {linked:,} | groups now: {count_groups():,} | largest: {top_components()}')

# ---------------------------------------------------------------- stage 6 ---
print('=== Stage 6: shared people from landlord-registration case_people ===')
lp=pd.read_csv(BASE+'landlord_registration_people_flattened.csv.xz',low_memory=False)
OWNER_ROLES={'Property Owner','Permit Owner','Ps - Landlord Owner','Ps - Landlord Co-Owner','Owner'}
person_entities=collections.defaultdict(set)   # person name -> entity node ids
ent_hits=set()
for _,row in lp.iterrows():
    ents,people=set(),set()
    cand=[row.get('ownerName'),row.get('applicant')]+[row.get(f'P{k}_name') for k in range(1,8)]
    roles=[None,None]+[row.get(f'P{k}_role') for k in range(1,8)]
    addrs=[None,None]+[row.get(f'P{k}_address1') for k in range(1,8)]
    for nm,role,padr in zip(cand,roles,addrs):
        pa=clean_addr(padr) if isinstance(padr,str) else ''
        if not isinstance(nm,str) or not nm.strip(): continue
        if is_entity(nm):
            i=idx_of.get(clean_name(nm))
            if i is None:
                g=stem_groups.get(stem_name(nm))
                i=g[0] if g else None
            if i is not None: ents.add(i)
        elif role in OWNER_ROLES:            # explicit owner-side roles only
            p=clean_name(nm)
            if len(p)>=7 and ' ' in p: people.add(p+' @ '+pa)
    if ents:
        ent_hits.update(ents)
        for p in people: person_entities[p].update(ents)
person_entities={p:ids for p,ids in person_entities.items() if 2<=len(ids)<=10}
linked=0
for p,ids in person_entities.items():
    ids=list(ids)
    for j in ids[1:]:
        if union_guarded(ids[0],j): linked+=1
print(f'registration cases scanned: {len(lp):,} | entities seen in cases: {len(ent_hits):,}')
print(f'linking people (2-30 entities each): {len(person_entities):,} | people links applied: {linked:,}')
print(f'groups now: {count_groups():,} | largest: {top_components()}')

# ---------------------------------------------------------------- stage 7 ---
print('=== Stage 7: groups + canonical labels ===')
canon=pd.read_csv(BASE+'Ownership_Rollup_CURRENT_Corporate_20260711.csv')
canon_by_name={clean_name(r['BEST_PARENT']):r['BEST_PARENT'] for _,r in canon.iterrows() if r['source']=='canon_parent'}
groups=collections.defaultdict(list)
for i in range(len(nodes)): groups[find(i)].append(i)
rows=[];summ=[]
for gid,(root,members) in enumerate(sorted(groups.items(),key=lambda kv:-sum(nodes['parcels'].iat[i] for i in kv[1]))):
    total=sum(nodes['parcels'].iat[i] for i in members)
    label=None
    for i in members:
        c=canon_by_name.get(nodes['name_clean'].iat[i])
        if c: label=c;break
    if not label:
        best=max(members,key=lambda i:nodes['parcels'].iat[i])
        label=nodes['raw_names'].iat[best][0]
    for i in members:
        rows.append({'owner_name_clean':nodes['name_clean'].iat[i],'stem':nodes['stem'].iat[i],
            'raw_examples':'; '.join(nodes['raw_names'].iat[i][:3]),
            'group_id':gid,'group_name':label,'owner_parcels':int(nodes['parcels'].iat[i])})
    summ.append({'group_id':gid,'group_name':label,'member_names':len(members),
        'review':'REVIEW' if len(members)>=40 else '',
        'parcels':int(total),
        'sample_members':'; '.join(sorted({nodes['name_clean'].iat[i] for i in members})[:8])})
out=pd.DataFrame(rows); sm=pd.DataFrame(summ)
out.to_csv(f'Owner_Rollup_Linked_{STAMP}.csv',index=False)
sm.to_csv(f'Owner_Groups_Summary_{STAMP}.csv',index=False)
multi=sm[sm['member_names']>1]
print(f'final owner groups: {len(sm):,} (from {len(nodes):,} cleaned owners; {ent["Owner1_Name"].nunique():,} raw names)')
print(f'groups with 2+ linked names: {len(multi):,} covering {multi["parcels"].sum():,} parcels')
print('\nTop 15 groups:')
print(sm.head(15).to_string(index=False,max_colwidth=80))
