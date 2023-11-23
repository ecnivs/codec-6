import pandas as pd
from nltk import word_tokenize
import nltk
import wikipedia

# Download the 'punkt' resource
# nltk.download('punkt')

# Sample data
data = {'Query': ["What is the capital of France?", "Python programming language", "How does photosynthesis work?", "Tell me a joke"]}
df = pd.DataFrame(data)

# Function to detect if a query is a question
def is_question(query):
    words = word_tokenize(query)
    # Check if the first word is a question word
    question_words = ['what', 'who',]
    return words[0].lower() in question_words

def process(query_text):
    if is_question(query_text):
        query_text = query_text.replace("what is", "")
        query_text = query_text.replace("what is the", "")
        query_text = query_text.replace("what are", "")
        query_text = query_text.replace("who is", "")
        query_text = query_text.replace("who are", "")
        return(wikipedia.summary(query_text, sentences=2))
    else:
        return(False)


