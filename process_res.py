import pandas as pd
from nltk import word_tokenize
import nltk

# Download the 'punkt' resource
# nltk.download('punkt')

# Sample data
data = {'Query': ["What is the capital of France?", "Python programming language", "How does photosynthesis work?", "Tell me a joke"]}
df = pd.DataFrame(data)

# Function to detect if a query is a question
def is_question(query):
    words = word_tokenize(query)
    # Check if the first word is a question word
    question_words = ['what', 'when', 'where', 'who', 'whom', 'which', 'whose', 'why', 'how', 'is', 'are', 'do', 'does', 'did', 'can', 'could', 'should', 'would', 'will', 'am', 'was', 'were', 'has', 'have', 'had', 'may', 'might', 'must', 'shall', 'should']
    return words[0].lower() in question_words

# Apply the function to the 'Query' column
if is_question("hello"):
    print("True")
else:
    print("False")


