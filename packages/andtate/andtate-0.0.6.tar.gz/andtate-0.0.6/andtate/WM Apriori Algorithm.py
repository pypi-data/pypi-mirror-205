import pandas as pd
from apyori import apriori

df= pd.read_csv("/content/transaction.csv",header =None)

print("Display Statistics: ")
print("================================================================================")
print(df.describe())

print("\nShape: ",df.shape)
database=[]
for i in range(0,30):
    database.append([str(df.values[i,j]) for j in range(0,6)])
arm_rules=apriori(database,min_support=0.5,min_confidence=0.7,min_lift=1.2)
arm_results=list((arm_rules))

print("\nNo. of rule(s):",len(arm_results))
print("\nResults:")
print("================================================================================")
print(arm_results)