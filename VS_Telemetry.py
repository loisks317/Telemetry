import string
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

###############
# for first time use uncomment this 
#
# read in data

data=pd.read_csv('VS_Extensions_RTVS_1week_correct.csv')
data=data.drop(['MacAddressHash1'], axis=1)
# now we need to parse out Extensions Used
df=data.groupby('MacAddressHash').agg(lambda x: ' , '.join(set(x))).reset_index()

# split the strings in Extensions used and expand 
df2 = df.ExtensionsUsed.str.split(' , ', expand=True)
df2 = pd.get_dummies(df2, prefix='', prefix_sep='')
df2 = df2.groupby(df2.columns, axis=1).sum()
newdf=pd.concat([df, df2], axis=1)
colNames=list(set(newdf.columns.values) - set(['MacAddressHash',  'ExtensionsUsed']))
newdf.drop([col for col, val in newdf[colNames].sum().iteritems() if val < 10], axis=1, inplace=True)       
###########

# GITHUB! 

# low and high
cc=newdf#.drop(['ExtensionsUsed'])
cc.loc['Total']= pd.Series(cc[cc.columns.values[2:]].sum(), index = [cc.columns.values[2:]])

carr=np.array(cc.loc['Total'])
clab=np.array(cc.columns.values[2:])
#clab2=[i.lstrip(' ') for i in clab]
#clab3=[i.rstrip(' ') for i in clab2]

slist=sorted(zip(carr[2:], clab))
numbers = list(zip(*slist))[0]
tool = list(zip(*slist))[1]

fig=plt.figure()
ax=fig.add_subplot(111)   
plt.subplots_adjust(left=0.65)
ax.barh(np.arange(15), numbers[-15:])
plt.yticks(np.arange(15), tool[-15:]) 
ax.set_xlabel('Number of Users over a Week')
ax.set_ylabel('Other Extensions Used')
plt.savefig('RTVS_extensions_python_1wk.png')