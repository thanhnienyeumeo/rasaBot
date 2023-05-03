import re
from typing import Any, Dict, List, Text
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.shared.nlu.training_data.message import Message
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES
from underthesea import word_tokenize
from rasa.nlu.tokenizers.whitespace_tokenizer import WhitespaceTokenizer
from unicodedata import normalize
@DefaultV1Recipe.register(
    component_types=[DefaultV1Recipe.ComponentType.MESSAGE_TOKENIZER],
    is_trainable=False,
)
class VietnameseTokenizer(Tokenizer):

    # provides = [TOKENS_NAMES[attribute] for attribute in MESSAGE_ATTRIBUTES]
    # @staticmethod
    # def supported_languages() -> Optional[List[Text]]:
    #     #"""Supported languages (see parent class for full docstring)."""
    #     return ["vi"]

    # def __init__(self, component_config: Dict[Text, Any] = None) -> None:
    #     super().__init__(component_config)

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        text = message.get(attribute)
        text = normalize('NFC',text)
        words = word_tokenize( text)
        print(words, text)
        tokens = self._convert_words_to_tokens(words, text)

        return self._apply_token_pattern(tokens)
    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        """Returns the component's default config."""
        return {
            "intent_tokenization_flag": False,
            "intent_split_symbol": "_", 
             "token_pattern": None,
        }