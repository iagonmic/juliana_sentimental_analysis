import tweepy
from dotenv import load_dotenv
import os
import pandas as pd
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
saidas_dir = os.path.join(script_dir, '..', 'saidas')
os.makedirs(saidas_dir, exist_ok=True)

load_dotenv()

api_key = os.getenv('API_KEY')
api_key_secret = os.getenv('API_KEY_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key,
    consumer_secret=api_key_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

query = "juliana marins lang:pt -is:retweet"

all_tweets = []
next_token = None

for _ in range(10):  # Limite de chamadas (ajuste conforme seu plano)
    try:
        response = client.search_recent_tweets(
            query=query,
            max_results=10, 
            tweet_fields=['created_at', 'author_id', 'lang', 'public_metrics'],
            expansions=['author_id'],
            next_token=next_token
        )

        if not response.data:
            break  
        users = {}
        if response.includes and hasattr(response.includes, 'users'):
            users = {u.id: u for u in response.includes.users}

        for tweet in response.data:
            user = users.get(tweet.author_id)
            all_tweets.append({
                'usuario': user.username if user else 'desconhecido',
                'data': tweet.created_at,
                'texto': tweet.text,
                'likes': tweet.public_metrics['like_count'],
                'retweets': tweet.public_metrics['retweet_count']
            })

        next_token = response.meta.get('next_token')
        if not next_token:
            break

    except tweepy.TooManyRequests:
        print("Rate limit atingido. Aguardando 15 minutos...")
        time.sleep(15 * 60)
        continue
    except Exception as e:
        print("Erro:", e)
        break

df = pd.DataFrame(all_tweets)
output_path = os.path.join(saidas_dir, 'tweets_juliana_marins.csv')
df.to_csv(output_path, index=False)
print(f"Arquivo salvo com sucesso em: {output_path}")

