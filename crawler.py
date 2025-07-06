import snscrape.modules.twitter as sntwitter

# passamos a query que tenha "Juliana Marins"
# a data que ocorreu o incidente da queda foi em 21/06

query = "juliana marins since:2025-06-21 until:2025-07-05"
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    print(tweet.content)
    if i >= 10:
        break