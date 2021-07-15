import pandas as pd
clusters = pd.read_excel('clusters_500m/clusters.xlsx')
clusters['noorg'] = clusters['healthcare']+clusters['school']
clusters = clusters[clusters['ongrid']==0]
clusters['r_dens'] = clusters['density'].rank()
clusters['r_org'] = clusters['noorg'].rank()
clusters['r_pvout'] = clusters['mean_relative_pv_output'].rank()
clusters['r_sum']=clusters['r_dens']+clusters['r_org']+clusters['r_pvout']
clusters['score'] = clusters['r_sum'].rank(method='dense',ascending=False)
clusters = clusters.sort_values(by='score')
clusters = clusters.drop(['r_dens','r_org','r_pvout','r_sum'],axis=1)
clusters.to_excel('clusters_500m/clusters.xlsx')