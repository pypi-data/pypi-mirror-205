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