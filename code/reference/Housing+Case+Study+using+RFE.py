#!/usr/bin/env python
# coding: utf-8

# ## Model Selection using RFE (Housing Case Study)

# ### Importing and Understanding Data

# In[1]:


# Supress Warnings

import warnings
warnings.filterwarnings('ignore')


# In[2]:


import pandas as pd
import numpy as np


# In[3]:


# Importing Housing.csv
housing = pd.read_csv('Housing.csv')


# In[4]:


# Looking at the first five rows
housing.head()


# ### Data Preparation

# In[5]:


# List of variables to map

varlist =  ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']

# Defining the map function
def binary_map(x):
    return x.map({'yes': 1, "no": 0})

# Applying the function to the housing list
housing[varlist] = housing[varlist].apply(binary_map)


# In[6]:


# Check the housing dataframe now

housing.head()


# ### Dummy Variables

# The variable `furnishingstatus` has three levels. We need to convert these levels into integer as well. For this, we will use something called `dummy variables`.

# In[7]:


# Get the dummy variables for the feature 'furnishingstatus' and store it in a new variable - 'status'

status = pd.get_dummies(housing['furnishingstatus'])

# Check what the dataset 'status' looks like
status.head()


# Now, you don't need three columns. You can drop the `furnished` column, as the type of furnishing can be identified with just the last two columns where — 
# - `00` will correspond to `furnished`
# - `01` will correspond to `unfurnished`
# - `10` will correspond to `semi-furnished`

# In[8]:


# Let's drop the first column from status df using 'drop_first = True'
status = pd.get_dummies(housing['furnishingstatus'], drop_first = True)

# Add the results to the original housing dataframe
housing = pd.concat([housing, status], axis = 1)

# Now let's see the head of our dataframe.
housing.head()


# In[9]:


# Drop 'furnishingstatus' as we have created the dummies for it
housing.drop(['furnishingstatus'], axis = 1, inplace = True)

housing.head()


# ## Splitting the Data into Training and Testing Sets

# In[10]:


from sklearn.model_selection import train_test_split

# We specify this so that the train and test data set always have the same rows, respectively

df_train, df_test = train_test_split(housing, train_size = 0.7, test_size = 0.3, random_state = 100)


# ### Rescaling the Features 
# 
# We will use MinMax scaling.

# In[11]:


from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()


# In[12]:


# Apply scaler() to all the columns except the 'yes-no' and 'dummy' variables
num_vars = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking','price']

df_train[num_vars] = scaler.fit_transform(df_train[num_vars])

df_train.head()


# ### Dividing into X and Y sets for the model building

# In[13]:


y_train = df_train.pop('price')
X_train = df_train


# ## Building our model
# 
# This time, we will be using the **LinearRegression function from SciKit Learn** for its compatibility with RFE (which is a utility from sklearn)

# ### RFE
# Recursive feature elimination

# In[14]:


# Importing RFE and LinearRegression
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression


# In[15]:


# Running RFE with the output number of the variable equal to 10
lm = LinearRegression()
lm.fit(X_train, y_train)

rfe = RFE(lm, 10)             # running RFE
rfe = rfe.fit(X_train, y_train)


# In[16]:


list(zip(X_train.columns,rfe.support_,rfe.ranking_))


# In[17]:


col = X_train.columns[rfe.support_]
col


# In[18]:


X_train.columns[~rfe.support_]


# ### Building model using statsmodel, for the detailed statistics

# In[19]:


# Creating X_test dataframe with RFE selected variables
X_train_rfe = X_train[col]


# In[20]:


# Adding a constant variable 
import statsmodels.api as sm  
X_train_rfe = sm.add_constant(X_train_rfe)


# In[21]:


lm = sm.OLS(y_train,X_train_rfe).fit()   # Running the linear model


# In[22]:


#Let's see the summary of our linear model
print(lm.summary())


# `Bedrooms` is insignificant in presence of other variables; can be dropped

# In[23]:


X_train_new = X_train_rfe.drop(["bedrooms"], axis = 1)


# Rebuilding the model without `bedrooms`

# In[24]:


# Adding a constant variable 
import statsmodels.api as sm  
X_train_lm = sm.add_constant(X_train_new)


# In[25]:


lm = sm.OLS(y_train,X_train_lm).fit()   # Running the linear model


# In[26]:


#Let's see the summary of our linear model
print(lm.summary())


# In[27]:


X_train_new.columns


# In[28]:


X_train_new = X_train_new.drop(['const'], axis=1)


# In[29]:


# Calculate the VIFs for the new model
from statsmodels.stats.outliers_influence import variance_inflation_factor

vif = pd.DataFrame()
X = X_train_new
vif['Features'] = X.columns
vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif['VIF'] = round(vif['VIF'], 2)
vif = vif.sort_values(by = "VIF", ascending = False)
vif


# ## Residual Analysis of the train data
# 
# So, now to check if the error terms are also normally distributed (which is infact, one of the major assumptions of linear regression), let us plot the histogram of the error terms and see what it looks like.

# In[30]:


y_train_price = lm.predict(X_train_lm)


# In[31]:


# Importing the required libraries for plots.
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[32]:


# Plot the histogram of the error terms
fig = plt.figure()
sns.distplot((y_train - y_train_price), bins = 20)
fig.suptitle('Error Terms', fontsize = 20)                  # Plot heading 
plt.xlabel('Errors', fontsize = 18)                         # X-label


# ## Making Predictions

# #### Applying the scaling on the test sets

# In[33]:


num_vars = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking','price']

df_test[num_vars] = scaler.transform(df_test[num_vars])


# #### Dividing into X_test and y_test

# In[34]:


y_test = df_test.pop('price')
X_test = df_test


# In[35]:


# Now let's use our model to make predictions.

# Creating X_test_new dataframe by dropping variables from X_test
X_test_new = X_test[X_train_new.columns]

# Adding a constant variable 
X_test_new = sm.add_constant(X_test_new)


# In[36]:


# Making predictions
y_pred = lm.predict(X_test_new)


# ## Model Evaluation

# In[37]:


# Plotting y_test and y_pred to understand the spread.
fig = plt.figure()
plt.scatter(y_test,y_pred)
fig.suptitle('y_test vs y_pred', fontsize=20)              # Plot heading 
plt.xlabel('y_test', fontsize=18)                          # X-label
plt.ylabel('y_pred', fontsize=16)                          # Y-label

