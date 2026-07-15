#!/usr/bin/env python3
"""Aggregate the 206k framework homes into owner counts per geography
(tracts, block groups, communities, council districts, subdivisions) via
point-in-polygon, joined with ACS 2020-2024 context (SF tenure + DP04).
Output: owner_counts_geo.json for Owner_Counts_Choropleth.html."""
import json, re
import pandas as pd
from shapely.geometry import shape, Point
from shapely.strtree import STRtree

U='/root/.claude/uploads/6ba4e66d-6ed7-5650-bff1-8b675f5eb8ef/'
fw=pd.read_parquet(U+'d65a6f13-Nashville_Framework_Homes_CANONICAL_20260707_ENTITYFLAG.parquet',
 columns=['lat','lon','owner_type_canonical','flag_nonowner_occupant','flag_out_of_state','owner_category'])
fw=fw.dropna(subset=['lat','lon'])
fw=fw[(fw.lat.between(35.9,36.5))&(fw.lon.between(-87.2,-86.3))]
pts=[Point(lo,la) for la,lo in zip(fw['lat'],fw['lon'])]
corp=((fw['owner_type_canonical']=='Entity')|(fw['owner_type_canonical']=='Bank-Lender')).values
trust=(fw['owner_type_canonical']=='Trust').values
noo=fw['flag_nonowner_occupant'].astype(bool).values
oos=fw['flag_out_of_state'].astype(bool).values
inst=(fw['owner_category']=='Long-term \u2014 National SFR').values   # the identified 350+ institutional operators
print('framework points:',len(pts))

acs_tr=pd.read_parquet(U+'61119b48-ACS_Framework_SF_Tenure_Tract_20202024.parquet')
acs_bg=pd.read_parquet(U+'4f58bc8b-ACS_Framework_SF_Tenure_BlockGroup_20202024.parquet')
acs_tr['t6']=acs_tr['GEOID'].astype(str).str[-6:]
acs_bg['k']=acs_bg['GEOID'].astype(str).str[-7:]
tr_acs={r['t6']:{'renter_share':round(r['pct_sf_renter_occ'],1),'sf_units':int(r['sf_total_units'])} for _,r in acs_tr.iterrows() if pd.notna(r['pct_sf_renter_occ']) and pd.notna(r['sf_total_units'])}
bg_acs={r['k']:{'renter_share':round(r['pct_sf_renter_occ'],1),'sf_units':int(r['sf_total_units'])} for _,r in acs_bg.iterrows() if pd.notna(r['pct_sf_renter_occ']) and pd.notna(r['sf_total_units'])}

def simplify(geom,tol):
    g=geom.simplify(tol,preserve_topology=True)
    return json.loads(json.dumps(g.__geo_interface__),parse_float=lambda x:round(float(x),5))

def agg(geofile,label,namefn,tol,acsfn=None,minpts=0):
    d=json.load(open(geofile))
    geoms=[];metas=[]
    for f in d['features']:
        try:g=shape(f['geometry'])
        except:continue
        geoms.append(g);metas.append(f['properties'])
    tree=STRtree(geoms)
    counts=[dict(n=0,corp=0,trust=0,noo=0,oos=0,inst=0) for _ in geoms]
    # assign each point to the first polygon containing it
    for i,p in enumerate(pts):
        for j in tree.query(p):
            if geoms[j].contains(p):
                c=counts[j];c['n']+=1
                if corp[i]:c['corp']+=1
                if trust[i]:c['trust']+=1
                if noo[i]:c['noo']+=1
                if oos[i]:c['oos']+=1
                if inst[i]:c['inst']+=1
                break
    feats=[]
    for g,m,c in zip(geoms,metas,counts):
        if c['n']<minpts:continue
        nm=namefn(m)
        row={'name':nm,'geom':simplify(g,tol),**c}
        if acsfn:
            a=acsfn(m)
            if a:row['acs']=a
        feats.append(row)
    print(f'{label}: {len(feats)} areas, {sum(f["n"] for f in feats):,} homes assigned')
    return feats

out={}
out['tract']=agg('Davidson_Institutional_Pct_by_Tract.geojson','tracts',
    lambda m:'Tract '+str(m.get('TRACTCE')),0.0004,
    lambda m:tr_acs.get(str(m.get('TRACTCE'))))
out['bg']=agg('institutional_by_blockgroup.geojson','block groups',
    lambda m:'Block group '+str(m.get('bg'))[-7:],0.0004,
    lambda m:bg_acs.get(str(m.get('bg'))[-7:]))
out['community']=agg('institutional_by_community.geojson','communities',
    lambda m:str(m.get('city') or m.get('zip')),0.0006)
out['council']=agg('Davidson_Institutional_by_CouncilDistrict.geojson','council districts',
    lambda m:'District '+str(m.get('district'))+(' — '+m['member'] if m.get('member') else ''),0.0005)
out['subdivision']=agg('Subdivisions_shapes.geojson','subdivisions',
    lambda m:str(m.get('NAME')),0.0003,minpts=25)
json.dump(out,open('owner_counts_geo.json','w'),separators=(',',':'))
import os
print('owner_counts_geo.json: %.1f MB'%(os.path.getsize('owner_counts_geo.json')/1e6))
