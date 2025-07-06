import tweepy
from dotenv import load_dotenv
import os
import pandas as pd

# carregando apis dentro do .env
load_dotenv()

api_key = os.getenv('API_KEY')
api_key_secret = os.getenv('API_KEY_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')


# passamos a query que tenha "Juliana Marins"
# filtramos por lang:pt para português
# filtramos por -is:retweet para não ter retweets

# inicializamos o client
client = tweepy.Client(bearer_token,api_key,api_key_secret,access_token,access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

query = "juliana marins lang:pt -is:retweet"

# buscamos os tweets | limite mensal de 100 no plano gratuito
all_tweets = []
next_token = None

for _ in range(10):  # Ajuste conforme o limite do seu plano
    try:
        response = client.search_recent_tweets(
            query=query,
            max_results=10,
            tweet_fields=['created_at', 'lang', 'public_metrics'],
            expansions=['author_id'],
            user_fields=['username'],
            next_token=next_token
        )
        if not response.data:
            break  # Não há mais tweets
        tweet_data = response.data
        users = {u['id']: u for u in response.includes['users']}
        for tweet in tweet_data:
            user = users[tweet.author_id]
            all_tweets.append({
                'usuario': user.username,
                'data': tweet.created_at,
                'texto': tweet.text,
                'likes': tweet.public_metrics['like_count'],
                'retweets': tweet.public_metrics['retweet_count']
            })
        next_token = response.meta.get('next_token')
        if not next_token:
            break  # Chegou ao fim dos resultados
    except tweepy.TooManyRequests:
        print("Rate limit atingido. Aguardando 15 minutos...")
        import time
        time.sleep(15 * 60)  # Espera 15 minutos
        continue
    except Exception as e:
        print("Erro:", e)
        break

df = pd.DataFrame(all_tweets)