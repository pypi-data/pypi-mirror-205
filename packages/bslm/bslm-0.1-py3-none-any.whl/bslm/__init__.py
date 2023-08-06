def mlp():
    s="""
    #MLP Multi layer percepton

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import mean_squared_error, mean_absolute_error,r2_score
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV


df = pd.read_csv('/content/HR.csv')
df.isnull().sum()
LE = LabelEncoder()
df['Departments'] = LE.fit_transform(df['Departments'])
df['salary'] = LE.fit_transform(df['salary'])
scaler = MinMaxScaler()
df_norm = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.25,random_state=105,shuffle=True)


NN = MLPClassifier(hidden_layer_sizes=(10,20),max_iter=200)
NN.fit(x_train,y_train)
predictions = NN.predict(x_test)



plt.plot(NN.loss_curve_)
plt.xlabel("No. of Iterations")
plt.ylabel("Training Error")
plt.title("Traning curve")


print("Confusion Matrix:\n", confusion_matrix(y_test,predictions))
print("\nPerformance Metrics:\n", classification_report(y_test,predictions))


NN1 = MLPClassifier(max_iter=200)
param_grid = [
        {
            'activation' : ['identity', 'logistic', 'tanh', 'relu'],
            'solver' : ['lbfgs', 'sgd', 'adam'],
            'hidden_layer_sizes': [
             (1,),(2,),(3,),(4,),(5,),(6,),(7,),(8,),(9,),(10,),(11,), (12,),(13,),(14,),(15,),(16,),(17,),(18,),(19,),(20,),(21,)
             ]
        }
       ]
clf = RandomizedSearchCV(NN1,param_grid,n_jobs=-1,cv=10)
clf.fit(x_train,y_train)
print("Best Parameters found:",clf.best_params_)
Predictions=clf.predict(x_test)
print("\nConfusion Matrix:\n", confusion_matrix(y_test,predictions))
print("\nPerformance Metrics:\n", classification_report(y_test,predictions))
clf = GridSearchCV(NN1,param_grid,n_jobs=-1,cv=10)
clf.fit(x_train,y_train)
print("Best Parameters found:",clf.best_params_)
Predictions=clf.predict(x_test)
print("\nConfusion Matrix:\n", confusion_matrix(y_test,predictions))
print("\nPerformance Metrics:\n", classification_report(y_test,predictions))

mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y1_test, predictions)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, predictions)
print("Mean Absolute Error: ", np.round(mae, 2))
print("Mean Squared Error: ", np.round(mse, 2))
print("Root Mean Squared Error: ", np.round(rmse, 2))
print("R2_Score: ", np.round(r2, 2))
    """
    print(s)
def ada():
    s="""
    #AdaBoost Classifier

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import  confusion_matrix
from sklearn.ensemble import AdaBoostClassifier


#1. Read the dataset and do necessary preprocessing[data imputation in null values, use encoding techniques to convert categorical to numerical]
df=pd.read_csv('/content/drive/MyDrive/Datasets/income.csv')
df.isnull().sum()


#2. Choose independent variable (X) and dependent variable (Y) from given dataset
x=df.iloc[:,:-1]
y=df.income_level
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.20,random_state=105)


clf_1 = AdaBoostClassifier(n_estimators=100,algorithm='SAMME',random_state=0)
clf_1.fit(x_train,y_train)
y1c_predicted = clf_1.predict(x_test)
clf_1.score(x_test,y_test)


cm_1c = confusion_matrix(y_test,y1c_predicted)
acc_1c=(cm_1c[0][0]+cm_1c[1][1])/np.sum(cm_1c)
pre_1c=cm_1c[0][0]/(cm_1c[0][0]+cm_1c[1][0])
rec_1c=cm_1c[0][0]/(cm_1c[0][0]+cm_1c[0][1])
f1_sc_1c=cm_1c[1][1]/(cm_1c[1][1]+cm_1c[1][0])
met_1c=pd.DataFrame([[cm_1c[0][0],cm_1c[0][1],cm_1c[1][0],cm_1c[1][1],acc_1c,pre_1c,rec_1c,f1_sc_1c]],columns=['TP','FN','FP','TN','Accuracy','Precision','Recall','F1_Score'])
met_1c


clf_2 = AdaBoostClassifier(n_estimators=100,algorithm='SAMME.R',random_state=0)
clf_2.fit(x_train,y_train)
y2c_predicted = clf_2.predict(x_test)
clf_2.score(x_test,y_test)


cm_2c = confusion_matrix(y_test,y2c_predicted)
acc_2c=(cm_2c[0][0]+cm_2c[1][1])/np.sum(cm_2c)
pre_2c=cm_2c[0][0]/(cm_2c[0][0]+cm_2c[1][0])
rec_2c=cm_2c[0][0]/(cm_2c[0][0]+cm_2c[0][1])
f1_sc_2c=cm_2c[1][1]/(cm_2c[1][1]+cm_2c[1][0])
met_2c=pd.DataFrame([[cm_2c[0][0],cm_2c[0][1],cm_2c[1][0],cm_2c[1][1],acc_2c,pre_2c,rec_2c,f1_sc_2c]],columns=['TP','FN','FP','TN','Accuracy','Precision','Recall','F1_Score'])
met_2c
    """
    print(s)

def agg():
    s="""
    #agglomerative Clustering

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score, davies_bouldin_score


# Pre-process the data and fill the missing values and apply normalization
df = pd.read_csv('CC GENERAL.csv')
df.head()


# Apply label encoding to convert the categorical values to numerical values
LE = LabelEncoder()
df['CUST_ID'] = LE.fit_transform(df['CUST_ID'])
df.head()


x=df.iloc[:,:-1]
x.head()


# Plot the dendrogram
dendrogram = sch.dendrogram(sch.linkage(x, method="ward",metric="euclidean"))
plt.show()


# Implement agglomerative and divisive clustering algorithms to cluster the
#given data for different distance metrics (Euclidean, Manhattan etc,) and
#linkage functions (single, complete, average, wards)
Agglo = AgglomerativeClustering(n_clusters=3,affinity='euclidean',linkage = 'ward')
Agglo1 = AgglomerativeClustering(n_clusters=3,affinity='manhattan',linkage = 'complete')
Agglo2 = AgglomerativeClustering(n_clusters=3,affinity='l1',linkage = 'average')
Agglo3 = AgglomerativeClustering(n_clusters=3,affinity='l2',linkage = 'single')
Agglo.fit(x)
Agglo1.fit(x)
Agglo2.fit(x)
Agglo3.fit(x)
labels=Agglo.labels_
labels1=Agglo1.labels_
labels2=Agglo2.labels_
labels3=Agglo3.labels_



score1 = silhouette_score(x,Agglo.labels_,metric='euclidean')
score2 = silhouette_score(x,Agglo1.labels_,metric='manhattan')
score3 = silhouette_score(x,Agglo2.labels_,metric='l1')
score4 = silhouette_score(x,Agglo3.labels_,metric='l2')
score1,score2,score3,score4



dscore1 = davies_bouldin_score(x,Agglo.labels_)
dscore2 = davies_bouldin_score(x,Agglo1.labels_)
dscore3 = davies_bouldin_score(x,Agglo2.labels_)
dscore4 = davies_bouldin_score(x,Agglo3.labels_)
dscore1,dscore2,dscore3,dscore4
    """
    print(s)
def apr():
    s="""
    # Apriori

import pandas as pd
import warnings
warnings.filterwarnings('ignore')


df=pd.read_csv("/content/drive/MyDrive/Datasets/Shop1.csv")
t_df = df.Item.str.split(",")
df.head()


def count_item(t_df):
  count_ind_item = {}
  for row in t_df:
    for i in range(len(row)):
      if row[i] in count_ind_item.keys():
        count_ind_item[row[i]] += 1
      else:
        count_ind_item[row[i]] = 1
  data = pd.DataFrame(list(count_ind_item.items()),columns = ['item_sets','supp_count'])
  return data

def prune(data,supp):
  df=data[data.supp_count>=supp]
  return df
list_of_items=list(prune(count_item(t_df),2).item_sets)


def join(list_of_items,count):
  itemsets = []
  i=1
  for entry in list_of_items:
    proceding_items = list_of_items[i:]
    for item in proceding_items:
      if type(item) is str:
        if entry!= item:
          tuples = (entry,item)
          itemsets.append(tuples)
      else:
        tuples=set(entry).union(item)
        if(len(tuples)==count):
          itemsets.append(tuple(sorted(tuples)))
    i = i+1
  return itemsets
itemsets=join(list_of_items,2)
itemsets1=join(itemsets,3)


def count_itemset(t_df,itemsets):
  count_item = {}
  for item_set in itemsets:
    count_item[item_set] = 0
    set_A = set(item_set)
    for row in t_df:
      set_B = set(row)
      if set_B.intersection(set_A) == set_A:
        if item_set in count_item.keys():
          count_item[item_set] +=1
        else:
          count_item[item_set] = 1
    data = pd.DataFrame(list(count_item.items()),columns = ['item_sets','supp_count'])
    return data
df=count_itemset(t_df,itemsets1)
df


ind=count_item(t_df)
confidence=pd.DataFrame(columns=['item_set','confidence'])
for row in df.item_sets:
  for i in range(len(row)):
    for j in range(len(row)):
      if i!=j and j>i:
        tuples=(row[i],row[j])
        value1=df[df.item_sets==row].supp_count
        d=set(row).difference(set(tuples))
        value2=ind[ind.item_sets==list(d)[0]].supp_count
        value3=count_itemset(t_df,[tuples]).supp_count
        conf=round(int(value1)/int(value2)*100,2)
        st=(tuple(d),'->',tuples)
        new_row={'item_set':st,'confidence':conf}
        confidence=confidence.append(new_row,ignore_index=True)
        conf=round(int(value1)/int(value3)*100,2)
        st=(tuples,'->',tuple(d))
        new_row={'item_set':st,'confidence':conf}
        confidence=confidence.append(new_row,ignore_index=True)
confidence
    """
    print(s)
def dap():
    s="""
    1. Read the data
import pandas as pd
df = pd.read_csv('/content/Stores1b.csv')
df.info()

2. Calculate the % of missing values in the columns
null = (df.isnull().sum() / len(df)) * 100
null[null > 0]

3. Replace missing value with mean for the numerical column, if the % of missing value
is less than 10%. (Use temporary data frame & inplace=True)
q3 = df.copy()
for i in range(len(missing)):
if missing[i] < 10:
q3[missing.index[i]].fillna(value=q3[missing.index[i]].mean, inplace=True)
m3 = q3.isnull().sum()/q3.shape[0]*100
m3

4. Perform the interpolation using nearest method to estimate the missing values for the
numerical column, if the % of missing value is less than 10%. (Use temporary data
frame)
q4 = df.copy()
for i in range(len(missing)):
if missing[i] < 10 and missing[i] != 0:
q4[missing.index[i]].interpolate(method='nearest', inplace=True)
m4 = q4.isnull().sum()/q4.shape[0]*100

5. Perform the mode imputation for a categorical data, if the % of missing value is less
than 10%. (Use temporary data frame & inplace=True)
q5 = df.copy()
m5 = df.isnull().sum()/df.shape[0]*100
print("Before mode imputaion\n",m5)
for i in range(len(missing)):
if missing[i] < 10:
q5[missing.index[i]].fillna(q5[missing.index[i]].mode(), inplace=True)
m5 = q5.isnull().sum()/q5.shape[0]*100
print("\After mode imputaion\n",m4)

6. Drop the columns with more than 10% missing values and display the size (Use
temporary data frame & inplace=True)
print(df.shape)
a=df.drop(df.loc[:,df.isnull().sum()/len(df) > 0.10],axis=1)
a.shape

7. Drop the rows with outlier Z-score value > 3 for “Quantity” and display the size. (Use
temporary data frame & inplace=True)
from scipy import stats
q7 = df.copy()
q7["ZScore"] = stats.zscore(q7["Quantity"])
drop = q7[q7['ZScore'] > 3].index
print("Length before:", len(q7))
q7.drop(drop, inplace=True)
print("Length after:", len(q7))

8. Find the % of duplicate rows with all columns having same value.
q8 = df.copy()
n = len(q8)
duplicate = q8[q8.duplicated()]
x = len(duplicate)
print("Duplicate %: " + str((x/n)*100) + "%")

9. Find the % of duplicate rows based on some specific columns ['Customer','Product
line','Age','Gender'] having same value. Drop the duplicates and display the size. (Use
temporary data frame & inplace=True)
df6=df.copy()
print(df6.shape)
print(df6[['Customer','Product line','Age','Gender']].duplicated().sum()/len(df6)*100)
df6.drop_duplicates(subset=['Customer','Product line','Age','Gender'], inplace=True)
df6.shape

10. Perform the min-max normalization for a numerical feature 'Age' using Python code
and analyze the values in scatter plot.
import matplotlib.pyplot as plt
q8r=df['Age'].copy()
mymin=q8r.min()
mymax=q8r.max()
newq8r=[]
for i in q8r:
i=(i-mymin)/(mymax-mymin)
newq8r.append(i)
q8=pd.DataFrame(newq8r,columns =['Age'])
print(q8)
plt.scatter(q8,newq8r)

11. Perform the Z-score normalization for a numerical feature 'Age' using Python code and
analyze the values in scatter plot.
from sklearn.preprocessing import StandardScaler, LabelEncoder
q11 = df.copy()
q11["ZScore"] = st.zscore(q11["Age"])
scaler = StandardScaler()
fit = scaler.fit_transform(q11[['ZScore']])
plt.scatter(q11.Age, q11.ZScore)

12. Perform the label encoding for a categorical feature ‘Payment’ using Python code
q12 = df.copy()
label = LabelEncoder()
df['Encoding'] = label.fit_transform(df['Payment'])
df[['Payment', 'Encoding']].head()

13. Perform the one-hot encoding for a categorical feature ‘Payment’ using Python code
q10r=df.copy()
one_hot_encoded_data = pd.get_dummies(q10r, columns = ['Payment'])
one_hot_encoded_data
    """
    print(s)
def eda():
    s="""
    import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

1. Read the data
df=pd.read_csv('/content/drive/MyDrive/ML(dataset)/Stores.csv')
df.info()

2. Display the first and last 5 rows
pd.concat([df.head(),df.tail()])

3. Display the number of rows and columns
print("The number of rows: ",len(df.index))
print("The number of columns: ",len(df.columns)

4. Display the number of categorical and numerical columns
col=df.select_dtypes('number').columns
#print(col)
col2=df.select_dtypes('object').columns
#print(col2)
print("Number of Categorical columns: ",len(col2))
print("Number of numerical columns: ",len(col)

5. For numerical columns, display the min, max and mean
df.describe().loc[['min','max','mean']]

6. Display the columns with null values
print("The columns with null values are: ")
for i in df.columns:
if(df[i].isnull().sum()):
print(i)

7. Calculate the 5 number summary for “age” column and correlate with box plot (Python
code)
q1=25/100*50+1
q2=50/100*50+1
q3=75/100*50+1
l=x.min()
h=x.max()
print("The five summary detalis are")
print("q1:",float(q1)+math.ceil(q1)/2)
print("q3:",float(q3)+math.ceil(q3)/2)
print("minimum:",l)
print("maximum:",h)
print("median:",x.median())
plt.boxplot(df['Age'])
# df['Age'].describe()

8. Display the row index along with outlier values and Z-score for the column
“Guarantee_Period” and verify with box plot (Python code)
print("Outliers are:")
mean=df['Quantity'].mean()
std=df['Quantity'].std()
for i in df['Quantity']:
zscore=(i-mean)/std
if(zscore>3):
print(i)
print(zscore)
plt.boxplot(df['Quantity'])

9. Find the correlation for the input features Age, Price, Quarterly_Tax, Weight
df1= df[['Age','Price','Tax','Quarterly_Tax','Rating']]
df1.corr().style.background_gradient()

10. Display the feature pairs with high positive correlation and high negative correlation
values for the given input features (Python code)
c=corr.columns
for i in corr:
for j in corr:
if corr[i][j] > 0.60 and corr[i][j] < 1:
print(corr[i][j])

11. Display the feature pairs that have correlation value greater than 70% for the given
input features (Python code)
import seaborn as sns
sns.kdeplot(data=df,x='Tax')
q=df['Tax'].skew()
q
if q >0 :
print('positive skew')
else:
print("negative skew")

12. Analyze the skewness of the feature using plot distribution graph for the “cc” column
and display whether the feature is right skew, left skew or no skew (Python code)
plt.bar(df['City'],df.index)

13. Perform univariate analysis for categorical variable “Fuel_Type” using bar plot with
counts of observations.
sns.swarmplot(data=df, x="Rating")
sns.violinplot(data = df["Rating"] )

14. Perform univariate analysis for continuous variable “Age” using swarm plot and violin
plot
plt.scatter(df['Tax'],df['cogs'])
plt.xlabel('Tax')
plt.ylabel('cogs')
plt.show()

15. Display the scatter plot to show the relationship between two continuous variables
“Age” and “Price”
sns.boxplot(data=df,x='Gender',y='Age')

16. Perform a bivariate analysis between categorical variable and continuous variable of
“Fuel_Type” and “Age” using categorical box plot
crosstb = pd.crosstab(df.Gender, df.Customer)
barplot = crosstb.plot.bar(rot=0)
plt.show()

17. Perform a bivariate analysis between two categorical variables “Fuel_Type” and
“Gears” using crosstab and count plot
18. Perform a multivariate analysis between input features “Age”, “Price”, “KM”,
“Weight” using pair plot with respect to Fuel_Type as hue.
sns.pairplot(df[['Age','City', 'Price', 'Tax', 'Rating','cogs']],hue="City")
    """
    print(s)
def fcm():
    s="""
    #Fuzzy_c_means

!pip install fuzzy-c-means

import numpy as np
import pandas as pd
from fcmeans import FCM
from sklearn.model_selection  import train_test_split
import matplotlib.pyplot as plt
from sklearn import datasets
from scipy.stats import pearsonr
n_samples=5000



df =   pd.read_csv("/content/Iris..csv")
x=df.iloc[:,1:4]
y=df.Species
x_train,y_train,x_test,y_test = train_test_split(x,y,test_size=0.25,random_state=105,shuffle=True)


plt.figure(figsize=(5,5))
plt.scatter(x_train.iloc[:,0].head(20),y_train.iloc[:,1].head(20),alpha=1)
plt.show()



x=np.array(x_train)
fcm= FCM(n_clusters=3)
fcm.fit(x)
#outputs
fcm_centers = fcm.centers
fcm_labels  = fcm.predict(x)
fcm_labels
fcm.partition_coefficient


#plot results
f,axes = plt.subplots(1,2,figsize=(15,5))
axes[0].scatter(x[:,0],x[:,1],alpha=1)
axes[1].scatter(x[:,0],x[:,1],c=fcm_labels,alpha=1)
axes[1].scatter(fcm_centers[:,0],fcm_centers[:,1],marker = "+",s=500,c='r')
    """
    print(s)
def lr():
    s="""
    import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

Linear Regression

#1.Read CSV data into pandas dataframe object
df = pd.read_csv("/content/drive/MyDrive/Datasets/Prostate_Cancer.csv")
df.head()
y = df['diagnosis_result']
le = LabelEncoder()
df['diagnosis_result'] = le.fit_transform(y)
df.columns


#2.Do necessary preprocessing
df_sc = StandardScaler()
df_sc = df_sc.fit_transform(df)
df_sc = pd.DataFrame(df_sc, columns =['id', 'diagnosis_result', 'radius', 'texture', 'perimeter', 'area',
       'smoothness', 'compactness', 'symmetry', 'fractal_dimension'])


#3.Choose independent variable (X) and dependent variable (Y) from given dataset
X = df_sc.radius
Y = df_sc.fractal_dimension

#4.Find the bo and b1 values to get Ypredicted
x_mean = np.mean(X)
y_mean = np.mean(Y)
num=0
den=0
for i in range(len(X)):
  num+=(X[i]-x_mean)*(Y[i]-y_mean)
  den+=(X[i]-x_mean)**2
  b1=num/den
b0=y_mean-(b1*x_mean)
y_pred = b0 + b1*X
print('Intercept: ',b0 ,'Slope: ',b1 , '\n')
print("Y_pred \n",y_pred)


#5.After getting Ypred, calculate the SSE (sum of squared error)
se = 0
for i in range(len(Y)):
  se += (Y[i]-y_pred[i])**2
print("Sum of squared error: ",se)


#6.Calculate the RMSE (Root Mean Square Error) value
rmse = math.sqrt(se/len(Y))
print("Sum of squared error: ",rmse)

#7.Calculate the coefficient of determination (r2) r-square
st = 0
for i in range(len(Y)):
  st += (Y[i]-y_mean)**2
r2 = 1-(se/st)
print("R-Square: ",r2)


#8.Plot regression line along with the given data points
plt.scatter(X,Y)
plt.plot(X,y_pred)

#9.Predict the output for a given input value
x_in = float(input())
print("Output: ",(b0+b1*x_in))
    """
    print(s)
def logr():
    s="""
    Logistic Regression

import numpy as nm  
import matplotlib.pyplot as plt 
import pandas as pd  

#reading data
df = pd.read_csv('/content/drive/MyDrive/Datasets/Algerian_forest_fires_dataset_UPDATE.csv')
df.columns
dfcpy = df.copy()
y = dfcpy['Classes']
le = LabelEncoder()
dfcpy['Classes'] = le.fit_transform(y)
df

#Assigning var and testing and training
x= dfcpy.iloc[:, :-1].values  
y= dfcpy.iloc[:,-1].values  
from sklearn.model_selection import train_test_split  
x_train, x_test, y_train, y_test= train_test_split(x, y, test_size= 0.25, random_state=0)  

#preprocessing using standard scaler
st_x= StandardScaler()    
x_train= st_x.fit_transform(x_train)    
x_test= st_x.transform(x_test)  

#logistic regression
from sklearn.linear_model import LogisticRegression  
classifier = LogisticRegression()  
classifier.fit(x_train, y_train) 
y_pred= classifier.predict(x_test) 

#cm
from sklearn.metrics import confusion_matrix  
cm= confusion_matrix(y_test,y_pred)  
cm
import seaborn as sns
sns.heatmap(cm, annot=True)


from sklearn.metrics import accuracy_score as acc
acc(y_test,y_pred)


from sklearn.metrics import precision_score as pre
pre(y_test,y_pred)


from sklearn.metrics import recall_score as re
re(y_test,y_pred)


pre = tp/(tp+fp)
acc = (tp+tn)/(tn+fp+fn+tp)
recall = tp/(tp+fn)

print(f'Presision: {pre}')
print(f'Accuracy: {acc}')
print(f'Recall: {recall}')
    """
    print(s)
def mlr():
    s="""
    Multi-Linear Regression


#1.Read CSV data into pandas dataframe object
df = pd.read_csv("/content/drive/MyDrive/Datasets/Prostate_Cancer.csv")
df.head()
y = df['diagnosis_result']
le = LabelEncoder()
df['diagnosis_result'] = le.fit_transform(y)
df.columns

#2.Do necessary preprocessing
df_sc = StandardScaler()
df_sc = df_sc.fit_transform(df)
df_sc = pd.DataFrame(df_sc, columns =['id', 'diagnosis_result', 'radius', 'texture', 'perimeter', 'area',
       'smoothness', 'compactness', 'symmetry', 'fractal_dimension'])

#3.Choose independent variables (X1,X2 ….) and dependent variable (Y) from given
#dataset
X1 = df_sc.radius
X2 = df_sc.texture
Y1 = df_sc.fractal_dimension

#4.Print values of y-intercept and independent variable coefficients
x1_mean = np.mean(X1)
x2_mean = np.mean(X2)
y1_mean = np.mean(Y1)
num1=0
num2=0
den1=0
den2= 0
for i in range(len(Y1)):
  num1+=(X1[i]-x_mean)*(Y1[i]-y1_mean)
  num2+=(X2[i]-x_mean)*(Y1[i]-y1_mean)
  den1+=(X1[i]-x1_mean)**2
  den2+=(X2[i]-x2_mean)**2
b1=num1/den1
b2=num2/den2
b0=y1_mean-(b1*x1_mean)-(b2*x2_mean)

print('Intercept: ',b0 ,'Slope 1 : ',b1 ,'Slope 2 : ',b2 , '\n')


#5.Find the Ypred
y1_pred = b0 + b1*X1 + b2*X2
print("Y_pred \n",y1_pred)

#6.Calculate the SSE (sum of squared error)and RMSE (Root Mean Square Error) value
se1 = 0
for i in range(len(Y)):
  se1 += (Y1[i]-y1_pred[i])**2
print("Sum of squared error: ",se1)

#7.Calculate the coefficient of determination (r2) r-square
st1 = 0
for i in range(len(Y1)):
  st1 += (Y1[i]-y1_mean)**2
r21 = 1-(se1/st1)
print("R-Square: ",r21)

#8.Plot the scatter graph of Yactual and Ypredicted
plt.scatter(Y1,y1_pred)

#9.Predict the output for a given input values
x1_in = float(input())
x2_in = float(input())
print("Output: ",(b0+b1*x1_in+b2*x2_in))
    """
    print(s)
def rfc():
    s="""
    #rfc

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import  confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier


#1. Read the dataset and do necessary preprocessing[data imputation in null values, use encoding techniques to convert categorical to numerical]
df=pd.read_csv('/content/drive/MyDrive/Datasets/income.csv')
df.isnull().sum()


#2. Choose independent variable (X) and dependent variable (Y) from given dataset
x=df.iloc[:,:-1]
y=df.income_level
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.20,random_state=3)




model_1 = RandomForestClassifier(criterion='gini',max_features='sqrt')
model_1.fit(x_train,y_train)
y1_predicted = model_1.predict(x_test)
model_1.score(x_test,y_test)


cm_1 = confusion_matrix(y_test,y1_predicted)
acc_1=(cm_1[0][0]+cm_1[1][1])/np.sum(cm_1)
pre_1=cm_1[0][0]/(cm_1[0][0]+cm_1[1][0])
rec_1=cm_1[0][0]/(cm_1[0][0]+cm_1[0][1])
f1_sc_1=cm_1[1][1]/(cm_1[1][1]+cm_1[1][0])
met_1=pd.DataFrame([[cm_1[0][0],cm_1[0][1],cm_1[1][0],cm_1[1][1],acc_1,pre_1,rec_1,f1_sc_1]],columns=['TP','FN','FP','TN','Accuracy','Precision','Recall','F1_Score'])
met_1


model_2 = RandomForestClassifier(criterion='gini',max_features='log2')
model_2.fit(x_train,y_train)
y2_predicted = model_2.predict(x_test)
model_2.score(x_test,y_test)


cm_2 = confusion_matrix(y_test,y2_predicted)
acc_2=(cm_2[0][0]+cm_2[1][1])/np.sum(cm_2)
pre_2=cm_2[0][0]/(cm_2[0][0]+cm_2[1][0])
rec_2=cm_2[0][0]/(cm_2[0][0]+cm_2[0][1])
f1_sc_2=cm_2[1][1]/(cm_2[1][1]+cm_2[1][0])
met_2=pd.DataFrame([[cm_2[0][0],cm_2[0][1],cm_2[1][0],cm_2[1][1],acc_2,pre_2,rec_2,f1_sc_2]],columns=['TP','FN','FP','TN','Accuracy','Precision','Recall','F1_Score'])
met_2



model_3 = RandomForestClassifier(criterion='entropy',max_features='sqrt')
model_3.fit(x_train,y_train)
y3_predicted = model_3.predict(x_test)
model_3.score(x_test,y_test)


cm_3 = confusion_matrix(y_test,y3_predicted)
acc_3=(cm_3[0][0]+cm_3[1][1])/np.sum(cm_3)
pre_3=cm_3[0][0]/(cm_3[0][0]+cm_3[1][0])
rec_3=cm_3[0][0]/(cm_3[0][0]+cm_3[0][1])
f1_sc_3=cm_3[1][1]/(cm_3[1][1]+cm_3[1][0])
met_3=pd.DataFrame([[cm_3[0][0],cm_3[0][1],cm_3[1][0],cm_3[1][1],acc_3,pre_3,rec_3,f1_sc_3]],columns=['TP','FN','FP','TN','Accuracy','Precision','Recall','F1_Score'])
met_3



model_4 = RandomForestClassifier(criterion='log_loss',max_features=None)
model_4.fit(x_train,y_train)
y4_predicted = model_4.predict(x_test)
model_4.score(x_test,y_test)


cm_4 = confusion_matrix(y_test,y4_predicted)
acc_4=(cm_4[0][0]+cm_4[1][1])/np.sum(cm_4)
pre_4=cm_4[0][0]/(cm_4[0][0]+cm_4[1][0])
rec_4=cm_4[0][0]/(cm_4[0][0]+cm_4[0][1])
f1_sc_4=cm_4[1][1]/(cm_4[1][1]+cm_4[1][0])
met_4=pd.DataFrame([[cm_4[0][0],cm_4[0][1],cm_4[1][0],cm_4[1][1],acc_4,pre_4,rec_4,f1_sc_4]],columns=['TP','FN','FP','TN','Accuracy','Precision','Recall','F1_Score'])
met_4
    """
    print(s)
def slp():
    s="""
    import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
df= pd.read_csv('penguins.csv')
df.head()

#1. Read the dataset and do necessary preprocessing [data imputation in null values, use
# encoding techniques to convert categorical to numerical]
df=df.iloc[:,1:]
y=df['species']
le=LabelEncoder()
df['species'] = le.fit_transform(y)
df['sex'] = le.fit_transform(df['sex'])
df['island'] = le.fit_transform(df['island'])
sc = StandardScaler()
sc = sc.fit_transform(df)
df=df.fillna(df.median())
#2. Determine the number of epochs which have minimum error [0/0.1/0.2]
input_dim =7
learning_rate = 0.1
weights=np.random.rand(input_dim)
x= np.asarray(df.iloc[:, :7])
y=np.asarray(df.iloc[:, 7:])
n=len(x[:,0])
err=[]

for epoch in range(9):
    e=0
    for data in range (0, n):
        os=np.sum(np.multiply(x[data,:],weights))
        if os<0:
            ov=0
        else:
            ov=1
        error=y[data]-ov
        e+=abs(error)
        for i in range(0,input_dim):
            weights[i]+=learning_rate*error*x[data,i]
    err.append(e[0])
index = 0
for i in range(1, len(err)):
    if err[i] < err[index]:
        index = i
print("Epoch with minimum error:", index)
# 3. Display final weight of each attribute which have minimum error.
for epoch in range(5):
    for data in range(n):
        os = np.sum(np.multiply(x[data,:], weights))
        if os < 0:
            ov = 0
        else:
            ov = 1
        
        error = y[data] - ov
        
        for i in range(input_dim):
            weights[i] += learning_rate * error * x[data, i]
    if epoch != index: continue
    for d in range(len(weights)):
        print("Weight " + str(d+1) + ":", np.round(weights[d], 2))
# 4. Plot the convergence of error for each iteration.
import matplotlib.pyplot as plt
plt.plot(err)
plt.title("Convergence of error")
plt.xlabel("Epoch")
plt.ylabel("Error rate")
    """
    print(s)
def som():
    s="""
    #som

!pip install minisom

#1 Load the given dataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder,MinMaxScaler
from minisom import MiniSom
from sklearn.metrics import silhouette_score, davies_bouldin_score
df=pd.read_csv('/content/drive/MyDrive/Iris (1).csv')
df.head()


#2 Conduct the pre-processing steps, if required
df.isnull().sum()


LE = LabelEncoder()
df['Species'] = LE.fit_transform(df['Species'])
df.head()


#3 Remove the target variable, if available in the dataset
x=df.iloc[:,:-1]
y=df['Species']
x.head()


#4 Plot the datapoints using scatter plots.
plt.scatter(df['SepalLengthCm'],df['PetalLengthCm'])
plt.scatter(df['SepalWidthCm'],df['PetalWidthCm'])


#5 Apply SOM clustering approach and cluster the datapoints into N number of clusters. Determine the optimal number of clusters.
def som_ini(ipt1,ipt2):
  data=df.values
  som_shape = (ipt1, ipt2)

  som = MiniSom(som_shape[0], som_shape[1], data.shape[1], sigma=0.5, learning_rate=0.5)

  max_iter = 1000
  q_error = []
  t_error = []

  for i in range(max_iter):
      rand_i = np.random.randint(len(data))
      som.update(data[rand_i], som.winner(data[rand_i]), i, max_iter)
      q_error.append(som.quantization_error(data))
      t_error.append(som.topographic_error(data))

  plt.plot(np.arange(max_iter), q_error, label='quantization error')
  plt.plot(np.arange(max_iter), t_error, label='topographic error')
  plt.ylabel('Quantization error')
  plt.xlabel('Iteration index')
  plt.legend()
  plt.show()

  labels = np.array([som.winner(x) for x in data])
  winner_coordinates = np.array([som.winner(x) for x in data]).T
  cluster_index = np.ravel_multi_index(winner_coordinates, som_shape)
  plt.figure(figsize=(7,5))
  for c in np.unique(cluster_index):
      plt.scatter(data[cluster_index == c, 0],
                  data[cluster_index == c, 1], label='cluster='+str(c), alpha=.7)
  for centroid in som.get_weights():
      plt.scatter(centroid[:, 0], centroid[:, 1], marker='x', 
                  s=10, linewidths=20, color='k')
  plt.legend();
  return np.array(labels)


X=som_ini(1,3)


db_score=davies_bouldin_score(X,y)
db_score


score1 = silhouette_score(X,y,metric='manhattan')
score1
    """
    print(s)