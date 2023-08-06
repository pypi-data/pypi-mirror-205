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
