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
