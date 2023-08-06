import numpy as np
import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

#Load Dataset
df = pd.read_csv('/content/spam.csv', encoding='latin-1')

#Keep only necessary columns
df =  df[['v2', 'v1']]

#Rename columns
df.columns = ['SMS','Type']

#Let's process the text data
#Instantiate count vectorizer
countvec = CountVectorizer(ngram_range = (1,4), stop_words='english', strip_accents='unicode', max_features=1000)

#Create bag of words
bow = countvec.fit_transform(df.SMS)

#Prepare training data
X_train = bow.toarray()
y_train = df.Type.values

#Instantiate classifier
mnb = MultinomialNB()

#Train the classifier/ fit the model
mnb.fit(X_train, y_train)

#Testing
text= countvec.transform(['free gifts for all'])
print(mnb.predict(text))