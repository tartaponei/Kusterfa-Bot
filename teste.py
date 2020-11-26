import tweepy
import keys
#id do maicon: 3120745861
#id meu: 853281780807368705

class TweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api

    def on_status(self, status):
        if from_creator(status):
            print(status.text)
            #print(status.id)

            self.api.update_status("@tartaponei respondi", in_reply_to_status_id=str(status.id))

def from_creator(status):
    """ Verifica se o tweet foi realmente feito pelo user mencionado"""
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True

def main():
    #colocando as credenciais
    auth = tweepy.OAuthHandler(keys.keys['consumer_key'], keys.keys['consumer_secret'])
    auth.set_access_token(keys.keys['access_token'], keys.keys['access_token_secret'])

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) #lance de wait tem a ver com esperar se o limite de rate exceder

    # tweet = api.user_timeline("maiconkusterk")[0]
    # print(tweet.text)

    #listener pra ver se tem tweet novo
    listener = TweetListener(api)
    stream = tweepy.Stream(api.auth, listener)
    stream.filter(follow=['853281780807368705'], is_async=True, ) #procura os tweets e executa o on_status()

if __name__ == "__main__":
    main()
