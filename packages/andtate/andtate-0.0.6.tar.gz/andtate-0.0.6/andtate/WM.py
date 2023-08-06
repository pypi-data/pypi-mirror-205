################### Scrape the details like color, dimensions, material etc. Or customer ratings by features ###################
################### P1 ###################

# Only Works on IDLE
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.service import Service

s= Service('C:/web driver/chromedriver_win32/chromedriver.exe')
driver =  webdriver.Chrome(service=s)
url="https://www.amazon.in/s?k=books&crid=FW7RDE7ZO0FO&sprefix=%2Caps%2C241&ref=nb_sb_ss_recent_1_0_recent"
driver.get(url)

#List to store details of books
books= []
prices=[]
ratings=[]

content=driver.page_source
soup= BeautifulSoup(content, 'html.parser')
list = soup.find_all('div', attrs={'class':'sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 sg-col-12-of-24 s-list-col-right'})

for i in list:
    book = i.find("span",attrs={'class':'a-size-medium a-color-base a-text-normal'})
    print(book.text)
    books.append(book.text)
    price = i.find("span",attrs={'class':'a-price-whole'})
    print(price.text)
    prices.append(price.text)
    rating= i.find("span",attrs={'class':'a-icon-alt'})
    print(rating.text)
    ratings.append(rating.text)
driver.close()

df=pd.DataFrame({'Book Nmae':books, 'Price':prices, 'Rating':ratings})
df.to_csv('Books.csv', index=False, encoding='utf-8')


################### Apriori Algorithm implementation in casestudy ###################
################### P3 ###################

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

################### Perform Spam Classifier ###################
################### P4 ###################

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


################### Text Mining Pre-processing using meta information from the Text (Local) ###################
################### P5 ###################

#imports
import string #for some string manipulation task
import nltk # natural language toolkit
from string import punctuation # Solving punctuation problems
from nltk.corpus import stopwords # stop words in sentences
from nltk.stem import WordNetLemmatizer # For stemming the sentence
from nltk.stem import SnowballStemmer # For stemming the sentence
from nltk.corpus import wordnet

def sentence_tokenize(text):
    """
    take string input and return a list of sentences.
    use nltk.sent_tokenize() to split the sentence.
    """
    return nltk.sent_tokenize(text)

def word_tokenize(text):
    """
    :param text:
    :return: list of words
    """
    return nltk.word_tokenize(text)

def to_lower(text):
    """
    :param text:
    :return: list of words
    """
    return text.lower()

def remove_numbers(text):
    """
    take string input and return a clean text without numbers.
    Use regex to discard the numbers.
    """
    output = ''.join(c for c in text if not c.isdigit())
    return output

def remove_punct(text):
    return ''.join(c for c in text if c not in punctuation)

def remove_stopwords(sentence):
    """
    remove all the stop words like "is,the,a, etc."
    """
    stop_words = stopwords.words('english')
    return ' '.join([w for w in nltk.word_tokenize(sentence) if not w in stop_words])

def get_wordnet_pos(word):
    # Map POS tag to first character lemmatize() accepts
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV
                }
    return tag_dict.get(tag,wordnet.NOUN)

def lemmatize(text):
    lemmatizer = WordNetLemmatizer()
    lemmatized_word = [lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(text)]
    return " ".join(lemmatized_word)

def preprocess(text):
    lower_text = to_lower(text)
    sentence_tokens = sentence_tokenize(lower_text)
    word_list = []
    for each_sent in sentence_tokens:
        lemmatizzed_sent = lemmatize(each_sent)
        clean_text = remove_numbers(lemmatizzed_sent)
        clean_text = remove_punct(clean_text)
        clean_text = remove_stopwords(clean_text)
        word_tokens = word_tokenize(clean_text)
        for i in word_tokens:
            word_list.append(i)
    return word_list

fileObject = open("Test.txt","r")
data = fileObject.read()
print("Original Data: ",data)
print("\n")
print("Preprocessed Data = ",preprocess(data))


################### Webpage Pre-processing using meta information from the web pages (Online) ###################
################### P6 ###################

# Only Works on IDLE
#imports
import string #for some string manipulation task
import nltk # natural language toolkit
from string import punctuation # Solving punctuation problems
from nltk.corpus import stopwords # stop words in sentences
from nltk.stem import WordNetLemmatizer # For stemming the sentence
from nltk.stem import SnowballStemmer # For stemming the sentence
from nltk.corpus import wordnet
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

def sentence_tokenize(text):
    """
    take string input and return a list of sentences.
    use nltk.sent_tokenize() to split the sentence.
    """
    return nltk.sent_tokenize(text)

def word_tokenize(text):
    """
    :param text:
    :return: list of words
    """
    return nltk.word_tokenize(text)

def to_lower(text):
    """
    :param text:
    :return: list of words
    """
    return text.lower()

def remove_numbers(text):
    """
    take string input and return a clean text without numbers.
    Use regex to discard the numbers.
    """
    output = ''.join(c for c in text if not c.isdigit())
    return output

def remove_punct(text):
    return ''.join(c for c in text if c not in punctuation)

def remove_stopwords(sentence):
    """
    remove all the stop words like "is,the,a, etc."
    """
    stop_words = stopwords.words('english')
    return ' '.join([w for w in nltk.word_tokenize(sentence) if not w in stop_words])

def get_wordnet_pos(word):
    # Map POS tag to first character lemmatize() accepts
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV
                }
    return tag_dict.get(tag,wordnet.NOUN)

def lemmatize(text):
    lemmatizer = WordNetLemmatizer()
    lemmatized_word = [lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(text)]
    return " ".join(lemmatized_word)

def preprocess(text):
    lower_text = to_lower(text)
    sentence_tokens = sentence_tokenize(lower_text)
    word_list = []
    for each_sent in sentence_tokens:
        lemmatizzed_sent = lemmatize(each_sent)
        numbers_removed = remove_numbers(lemmatizzed_sent)
        punctuation_removed = remove_punct(numbers_removed)
        stopwords_removed = remove_stopwords(punctuation_removed)
        word_tokens = word_tokenize(stopwords_removed)
        for i in word_tokens:
            word_list.append(i)
    return word_list

s = Service('C:WebDrivers/chromedriver.exe')
s.start()
driver = webdriver.Chrome(service=s)
url="https://link.springer.com/chapter/10.1007/978-981-13-9364-8_26"
driver.get(url)
content = driver.page_source
soup = BeautifulSoup(content,'html.parser')
text = soup.get_text()
print("\nOriginal Data: ",text.replace(" ",""))
print("\n")
print("Preprocessed Data = ",preprocess(text))


################### Develop a basic crawler for the web search for user defined keywords. ###################
################### P7 ###################

from bs4 import BeautifulSoup
import requests
pages_crawled = []
def crawler(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text,"html.parser")
    links = soup.find_all("a")
    for link in links:
        if "href" in link.attrs:
            if link["href"].startswith("/wiki") and ":" not in link["href"]:
                if link["href"] not in pages_crawled:
                    print(link["href"])
                    new_link = f"https://www.wikipedia.org{link['href']}"
                    pages_crawled.append(link["href"])
                    try:
                        with open("E:/data.csv","a") as file:
                            file.write(f'{soup.title.text};{soup.h1.text};{link["href"]}\n')
                        crawler(new_link)
                    except:
                         continue
crawler("https://en.wikipedia.org/wiki/Web_crawler")                        

################### deep search implementation to detect plagiarism in documents online. ###################
################### P8 ###################

import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

student_files = [doc for doc in os.listdir() if doc.endswith('.txt')]
student_notes =[open(File).read() for File in student_files]

vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
similarity = lambda doc1,doc2:cosine_similarity([doc1, doc2])

vectors = vectorize(student_notes)
s_vectors = list(zip(student_files, vectors))

def check_plagiarism():
    plagiarism_results = set()
    global s_vectors
    for student_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((student_a,text_vector_a))
        del new_vectors[current_index]
        for student_b , text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a,text_vector_b)[0][1]
            student_pair = sorted((student_a, student_b))
            score = (student_pair[0],student_pair[1],sim_score)
            plagiarism_results.add(score)
        return plagiarism_results

for data in check_plagiarism():
    print(data)

################### Sentiment analysis for reviews by customers and visualize the same ###################
################### P9 ###################


# Collab Only
import nltk
nltk.download('vader_lexicon')
nltk.download('movie_reviews')
nltk.download('punkt')

from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
sia = SIA()
sia.polarity_scores("This restaurant was great, but I'm not sure if I'll go there again")

text= "I just got a call from my boss - does he realise it's Saturday?"
sia.polarity_scores(text)

text= "I just got a call from my boss - does he realise it's Saturday? :)"
sia.polarity_scores(text)

text= "I just got a call from my boss - does he realise it's Saturday? 🙂"
sia.polarity_scores(text)

#TextBLOB

from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer

blob  = TextBlob("This restaurant was great, but I'm not sure if I'll go there again")
print(blob.sentiment)

blobber = Blobber(analyzer=NaiveBayesAnalyzer())
blob = blobber("This restaurant was great, but I'm not sure if I'll go there again")
print(blob.sentiment)

import pandas as pd
pd.set_option("display.max_colwidth", 200)
df = pd.DataFrame({'content': [
    "I love love love this kitten",
    "I hate hate hate hate this society",
    "I'm not sure how I feel about you",
    "Did you see teh game yesterday?",
    "The package was delivered late and the content were broken",
    "Trashy television shows are some of my favorites",
    "I'm seeing a Kubrick film tomorrow, I hear not so great things about it",
    "I find chirping birds irritating, but I know I'm not the only one."
]
                   })

print(df)

import pandas as pd
pd.set_option("display.max_colwidth", 200)
df = pd.DataFrame({'content': [
    "I love love love this kitten",
    "I hate hate hate hate this society",
    "I'm not sure how I feel about you",
    "Did you see teh game yesterday?",
    "The package was delivered late and the content were broken",
    "Trashy television shows are some of my favorites",
    "I'm seeing a Kubrick film tomorrow, I hear not so great things about it",
    "I find chirping birds irritating, but I know I'm not the only one."
]
                   })

print(df)

def get_scores(content):
  blob = TextBlob(content)
  nb_blob = blobber(content)
  sia_scores = sia.polarity_scores(content)

  return pd.Series({
      'content': content,
      'textblob': blob.sentiment.polarity,
      'textblob_bayes':nb_blob.sentiment.p_pos -  nb_blob.sentiment.p_neg,
      'nltk' : sia_scores['compound']
  })
  
scores = df.content.apply(get_scores)

scores.style.background_gradient(cmap = 'RdYlGn', axis=None, low=0.4, high=0.4)