import asyncio
import websockets
import json
import random
import string
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
nltk.download('punkt') # first-time use only
nltk.download('wordnet') # first-time use only

# Ensure nltk data is available
#nltk.data.path.append('/path/to/nltk_data')  # Update this path to where NLTK data is downloaded

lemmer = WordNetLemmatizer()

# Load the corpus
with open('hospital.txt', 'r', encoding='utf8', errors='ignore') as fin:
    raw = fin.read().lower()

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

# Functions for NLP processing
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def greeting(sentence):
    GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
    GREETING_RESPONSES = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me"]
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
    return None

def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf[:-1])
    idx = vals.argsort()[0][-1]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-1]
    sent_tokens.pop()  # Remove the user response from the list of sentences
    if req_tfidf < 0.1:  # Threshold for recognizing a valid response
        robo_response = "I am sorry! I don't understand you"
    else:
        robo_response = sent_tokens[idx]
    return robo_response

async def handler(websocket, path):
    try:
        await websocket.send(json.dumps({"text": "Hello, I'm your voice assistant. How can I help you?", "voice": False}))
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            message_type = data.get('type')
            
            if message_type == 'ping':
                # Ignore ping messages
                continue

            user_response = data['text'].lower()
            is_voice = data['voice']
            
            if user_response in ['bye', 'thanks', 'thank you']:
                await websocket.send(json.dumps({"text": "Bye! Take care..", "voice": is_voice}))
                break
            else:
                greet = greeting(user_response)
                if greet:
                    response_text = greet
                else:
                    response_text = response(user_response)
                print(f"User: {user_response}")
                print(f"Bot: {response_text}")
                await websocket.send(json.dumps({"text": response_text, "voice": is_voice}))
    except websockets.exceptions.ConnectionClosedOK:
        print("Connection closed normally")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed with error: {e}")
    finally:
        print("Connection closed")

# Start the server
start_server = websockets.serve(handler, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
