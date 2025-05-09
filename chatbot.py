from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

class SaaSFlowChatBot:
    def __init__(self):
        self.chatbot = ChatBot('SaaSFlowBot')
        self.trainer = ChatterBotCorpusTrainer(self.chatbot)

    def train_bot(self):
        self.trainer.train('chatterbot.corpus.english')

    def get_response(self, query):
        return self.chatbot.get_response(query)
