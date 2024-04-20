#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np


# In[5]:


import warnings
warnings.filterwarnings('ignore')


# In[7]:


DATA_FILE='criteo_attribution_dataset.tsv.gz'
df_Criteo_Attribution = pd.read_csv(DATA_FILE, sep='\t', compression='gzip')


# In[8]:


df_Criteo_Attribution.head()


# In[9]:


df_Criteo_Attribution.tail()


# In[10]:


df_Criteo_Attribution['day'] = np.floor(df_Criteo_Attribution.timestamp / 86400.).astype(int)
df_Criteo_Attribution['conversion_day'] = np.floor(df_Criteo_Attribution.conversion_timestamp / 86400.).astype(int)


# In[11]:


df_Criteo_Attribution


# In[22]:


df_Criteo_Attribution['jid'] = df_Criteo_Attribution['uid'].map(str) + '_' + df_Criteo_Attribution['conversion_id'].map(str)


# In[23]:


df_Criteo_Attribution.head()


# In[25]:


df_Criteo_Attribution.shape


# In[28]:


df_Criteo_Attribution['uid'].nunique()


# In[29]:


df_Criteo_Attribution['campaign'].nunique()


# In[30]:


df_Criteo_Attribution['gap_click_sale'] = -1
df_Criteo_Attribution.loc[df_Criteo_Attribution.conversion == 1, 'gap_click_sale'] = df_Criteo_Attribution.conversion_day - df_Criteo_Attribution.day


# In[31]:


df_Criteo_Attribution


# In[32]:


df_Criteo_Attribution.tail()


# In[40]:


grouped = df_Criteo_Attribution.groupby(['jid']).count()


# In[41]:


grouped


# In[44]:


grouped = df_Criteo_Attribution.groupby(['jid'])['uid'].count()


# In[45]:


grouped


# In[46]:


grouped = df_Criteo_Attribution.groupby(['jid'])['uid'].count().reset_index(name="count")


# In[47]:


grouped


# In[48]:


df_Criteo_Attribution = df_Criteo_Attribution[df_Criteo_Attribution['jid'].isin( grouped[grouped['count'] >= 2]['jid'].values )]


# In[49]:


df_Criteo_Attribution


# In[50]:


journey_counts=df_Criteo_Attribution.groupby(['jid'])['uid'].count()


# In[51]:


journey_counts


# In[53]:


journey_counts_reset=journey_counts.reset_index(name="count")


# In[54]:


journey_counts_reset


# In[56]:


journey_counts_reset.groupby(['count']).count().rename(columns={'jid': 'number_of_jid'})


# In[57]:


grouped = df_Criteo_Attribution.groupby(['jid'])['uid'].count().reset_index(name="count")
df_Criteo_Attribution = df_Criteo_Attribution[df_Criteo_Attribution['jid'].isin( grouped[grouped['count'] >= 2]['jid'].values )]


# In[58]:


df_Criteo_Attribution.groupby(['jid'])['uid'].count().reset_index(name="count").groupby(['count']).count()


# In[62]:


counts = df_Criteo_Attribution.groupby(['jid'])['uid'].count().reset_index(name="count").groupby(['count']).count().reset_index()
hist_x = counts['count']
hist_y = counts['jid']
plt.plot(hist_x, hist_y, label='all journeys')

plt.xlabel('Journey length (number of touchpoints)')
plt.ylabel('Fraction of journeys')
plt.show()


# In[63]:


def journey_length_histogram(df):
    counts = df.groupby(['jid'])['uid'].count().reset_index(name="count").groupby(['count']).count()
    return counts.index, counts.values / df.shape[0]

hist_x, hist_y = journey_length_histogram(df_Criteo_Attribution)

plt.plot(range(len(hist_x)), hist_y, label='all journeys')
plt.yscale('log')
plt.xlim(0, 200)
plt.xlabel('Journey length (number of touchpoints)')
plt.ylabel('Fraction of journeys')
plt.show()


# In[64]:


def journey_length_hist(df):
    counts = df.groupby(['jid'])['uid'].count().reset_index(name="count").groupby(['count']).count()
    return counts.index, counts.values / df.shape[0]

hist_x, hist_y = journey_length_hist(df_Criteo_Attribution[df_Criteo_Attribution.conversion==1])

plt.plot(range(len(hist_x)), hist_y, label='all journeys')
plt.yscale('log')
plt.xlim(0, 120)
plt.xlabel('Journey length (number of touchpoints)')
plt.ylabel('Fraction of journeys')
plt.show()


# In[ ]:




