import tweepy
from random import choice
import keys
import answers

class TweetListener(tweepy.StreamListener):
    """Stream que verifica se tem tweets novos"""
    def __init__(self, api):
        self.api = api

    def on_status(self, tweet):
        if from_creator(tweet):
            print(tweet.text)

            resposta = "@tartaponei "
            
            if hasattr(tweet, 'extended_entities') == False:
                #SE FOR TWEET PEDINDO COISA PRA VIDEO:
                if True in [i in tweet.text for i in answers.palavras]:
                    if True in ["pessoa" in tweet.text]: #se tiver pedindo uma pessoa
                        opcao = choice(answers.opcoes_sugestao_pessoa) #escolhe uma resposta aleatória das opções
                        resposta += opcao
                    else:
                        opcao = choice(answers.opcoes_sugestao_generica) #escolhe uma resposta aleatória das opções
                        resposta += opcao
                #SE FOR TWEET GENERICO:
                else:
                    opcao = choice(answers.opcoes_generica) #escolhe uma resposta aleatória das opções
                    resposta += opcao
            else:
                #SE FOR UMA IMAGEM:
                if True in [media['type'] == 'photo' for media in tweet.extended_entities['media']]:
                    opcao = choice(answers.opcoes_imagem) #escolhe uma resposta aleatória das opções
                    resposta += "bela imagem " + opcao

                #SE FOR UMA VIDEO:
                elif True in [media['type'] == 'video' for media in tweet.extended_entities['media']]:
                    opcao = choice(answers.opcoes_video) #escolhe uma resposta aleatória das opções
                    resposta += "belo video " + opcao

            self.api.update_status(resposta, in_reply_to_status_id=str(tweet.id)) #responde o tweet em questão


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

    id = str(api.get_user("tartaponei").id) #pega o id do usuário

    #listener pra ver se tem tweet novo
    listener = TweetListener(api)
    stream = tweepy.Stream(api.auth, listener)
    stream.filter(follow=[id], is_async=True, ) #procura os tweets e executa o on_status()

if __name__ == "__main__":
    main()