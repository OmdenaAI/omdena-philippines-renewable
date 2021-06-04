import pandas as pd
import shapely
from shapely import wkt
from shapely.geometry import shape,mapping, Point, Polygon, MultiPolygon
import glob

#Orgdemand is converted from Anastasia geojson to tabula format
orgdem = pd.read_csv('task2_estimate_energy_demand/organizational demand/OrgDemand.csv')
orgdem = orgdem.drop_duplicates().reset_index()
def changename(state):
    if state == 'Fct':
        state='Federal Capital Territory'
    else:
        state
    return state
orgdem['state'] = orgdem['state'].apply(lambda x:changename(x))
points=[]
for lat,lon in zip(orgdem['lat'],orgdem['lon']):
    p = Point(lon,lat)
    points.append(p)
points=pd.DataFrame(points)
points.columns = ['point']
orgdem=orgdem.merge(points, left_index=True, right_index=True, how='left')

orgdem.tail()
clusters = pd.read_excel('clusters_500m/clusters.xlsx')
clusters['geometry'] = clusters['geometry'].apply(wkt.loads)
clusters = clusters.drop(['name','healthcare','school'],axis=1)


orgclus =  clusters.merge(orgdem, left_on='adm1',right_on='state',how='left')   
d = dict(tuple(orgclus.groupby(['state'])))

def coord_in_polygon(geo, point):
    """
    check one point is inside a cluster
    """
    return geo.contains(point)

for state in d:
    org = d[state].reset_index()
    org['in'] = org.apply(lambda x:coord_in_polygon(x['geometry'],x['point']),axis=1)
    org = org[org['in']==True]
    org.to_csv(f'org_{state}.csv',index=False)

df = pd.concat(map(pd.read_csv, glob.glob('org_*.csv')))
del df['level_0']
df = df.reset_index()

#concate organization insider a cluster into one list
organization = df.groupby(['label'])['name'].apply(list).reset_index()
clusters = clusters.merge(organization, on ='label', how='left')

#count number of healthcare/school in a cluster
org_type = df[['label','type','name']]
org_type = org_type.groupby(['label', 'type']).count().reset_index()

org_type = org_type.pivot(index='label',
       columns='type',values="name").reset_index()

clusters = clusters.merge(org_type, on = 'label',how='left')
clusters = clusters.drop(['healthcare', 'school'],axis=1)

clusters['healthcare'] = clusters['healthcare'].fillna(0)
clusters['school'] = clusters['school'].fillna(0)
clusters.to_excel('clusters_500m/clusters.xlsx',index=False)