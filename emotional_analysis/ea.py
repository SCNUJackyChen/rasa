from enum import IntEnum
from typing import Dict, Optional, Text, Any, List

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.nlu import utils

import nltk
# from nltk.classify import NaiveBayesClassifier
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os


from rasa.shared.nlu.constants import (
    TEXT,
    INTENT,
    TEXT_TOKENS,
    FEATURE_TYPE_SENTENCE,
    FEATURE_TYPE_SEQUENCE,
)

SENTIMENT_MODEL_FILE_NAME = "sentiment_classifier.pkl"

@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER], is_trainable=True
)
class SentimentAnalyzer(GraphComponent):
    """A custom sentiment analysis component"""
    name = "sentiment"
    provides = ["entities"]
    requires = ["tokens"]
    defaults = {}
    language_list = ["en"]
    print('initialised the class')


    def __init__(
        self,
        model_storage: ModelStorage,
        resource: Resource,
        training_artifact: Optional[Dict],
    ) -> None:
        # Store both `model_storage` and `resource` as object attributes to be able
        # to utilize them at the end of the training
        self._model_storage = model_storage
        self._resource = resource


    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ):
        return cls(model_storage, resource, training_artifact=None)

    def train(self, training_data: TrainingData) -> Resource:
        """Load the sentiment polarity labels from the text
           file, retrieve training tokens and after formatting
           data train the classifier."""
        pass



        # with open('labels.txt', 'r') as f:
        #     labels = f.read().splitlines()


        # training_data = training_data.training_examples #list of Message objects
        # tokens = [list(map(lambda x: x.text, t.get('tokens'))) for t in training_data]
        # processed_tokens = [self.preprocessing(t) for t in tokens]
        # labeled_data = [(t, x) for t,x in zip(processed_tokens, labels)]
        # self.clf = NaiveBayesClassifier.train(labeled_data)






    def convert_to_rasa(self, value, confidence):
        """Convert model output into the Rasa NLU compatible output format."""


        entity = {"value": value,
                  "confidence": confidence,
                  "entity": "sentiment",
                  "extractor": "sentiment_extractor"}


        return entity
        


    # def process_training_data(self, tokens: TrainingData) -> TrainingData:
    #     """Create bag-of-words representation of the training examples."""
        
    #     return ({word: True for word in tokens})




    def process(self, messages: List[Message]) -> List[Message]:
        """Retrieve the tokens of the new message, pass it to the classifier
            and append prediction results to the message class."""
        message = messages[0]
        
        sid = SentimentIntensityAnalyzer()
        res = sid.polarity_scores(message.get(TEXT))
        key, value = max(res.items(), key=lambda x: x[1])
        entity = self.convert_to_rasa(key, value)

        message.set("sentiments", [entity], add_to_output=True)        

        return [message]
        # if not self.clf:
        #     # component is either not trained or didn't
        #     # receive enough training data
        #     entity = None
        # else:
        #     tokens = [t.text for t in messages.get("tokens")]
        #     tb = self.preprocessing(tokens)
        #     pred = self.clf.prob_classify(tb)


        #     sentiment = pred.max()
        #     confidence = pred.prob(sentiment)


        #     entity = self.convert_to_rasa(sentiment, confidence)


        #     messages.set("entities", [entity], add_to_output=True)




    def persist(self, file_name, model_dir):
        """Persist this model into the passed directory."""
        pass
        # classifier_file = os.path.join(model_dir, SENTIMENT_MODEL_FILE_NAME)
        # utils.json_pickle(classifier_file, self)
        # return {"classifier_file": SENTIMENT_MODEL_FILE_NAME}


    # @classmethod
    # def load(
    #     cls,
    #     config: Dict[Text, Any],
    #     model_storage: ModelStorage,
    #     resource: Resource,
    #     execution_context: ExecutionContext,
    #     model_dir=None,
    #     **kwargs: Any,
    # ) -> GraphComponent:
    #     file_name = config.get("classifier_file")
    #     classifier_file = os.path.join(model_dir, file_name)
    #     return utils.json_unpickle(classifier_file)

if __name__ == "__main__" :
    sid = SentimentIntensityAnalyzer()
    res = sid.polarity_scores("I am very happy")
    key, value = max(res.items(), key=lambda x: x[1])
    print(key, value)