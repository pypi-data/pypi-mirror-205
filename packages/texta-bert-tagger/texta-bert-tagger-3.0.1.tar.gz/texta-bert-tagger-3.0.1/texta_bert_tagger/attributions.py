import os
import torch
import numpy as np
from copy import deepcopy
from string import punctuation
from typing import List, Tuple, NoReturn
from collections import defaultdict
from captum.attr import visualization as viz
from captum.attr import LayerConductance, LayerIntegratedGradients

class BertConnector:
    def __init__(self, loaded_bert_tagger):
        self.__bert_tagger = loaded_bert_tagger
        self.__model_input = self.__set_input()
        self.__lig = LayerIntegratedGradients(self.__model_output, self.__model_input)
        self.__tokenizer = self.__bert_tagger.load_tokenizer()
        self.__device = self.__bert_tagger.device.type
        self.__new_word_start_char = self.__set_new_word_start_char()

    @property
    def tokenizer(self):
        return self.__tokenizer

    @property
    def bert_tagger(self):
        return self.__bert_tagger

    @property
    def lig(self):
        return self.__lig

    @property
    def new_word_start_char(self):
        return self.__new_word_start_char

    @property
    def device(self):
        return self.__device


    def __model_output(self, inputs):
        return self.__bert_tagger.model(inputs)[0]

    def __set_input(self):
        try:
            model_input = self.__bert_tagger.model.bert.embeddings
        except:
            model_input = self.__bert_tagger.model.roberta.embeddings
        return model_input

    def __set_new_word_start_char(self) -> str:
        """ Finds and sets the character(s) used for marking
        the beginnings of new words.
        """
        # NB! Has to be a nicer way to retrieve this!
        first_chars = defaultdict(int)
        for token in list(self.__tokenizer.get_vocab().keys()):
            if len(token) > 1 and token[0] == token[1]:
                first_chars[token[:2]]+=1
            else:
                first_chars[token[0]]+=1
        fc = list(first_chars.items())
        fc.sort(key= lambda x: x[1], reverse=True)
        new_word_start_char = fc[0][0] # probably

        # Log start / continuation char as the algorithm for detecting it is hacky and
        # thus it might be sometimes detected incorrectly
        logger_msg = f"BERT Tokenizer: Word start or continuation char is: {new_word_start_char}"
        self.__bert_tagger._print(logger_msg)
        if self.__bert_tagger.logger: self.__bert_tagger.logger.info(logger_msg)

        return new_word_start_char


    def is_beginning_of_new_word(self, token: str) -> bool:
        """ Checks if token denotes the beginning of a new word or not.
        """
        if self.__new_word_start_char != "##":
            if (
                token in self.__tokenizer.all_special_tokens or
                token.startswith(self.__new_word_start_char) or
                token in punctuation
            ):
                return True
        else:
            if (
                token in self.__tokenizer.all_special_tokens or
                not token.startswith(self.__new_word_start_char) or
                token in punctuation
            ):
                return True
        return False


class Attributions:
    """ For finding and visualizing attributions by using layer integrated gradients.
    """
    def __init__(self, bert_connector: BertConnector, text: str, target_class = None, round_digits: int = 3):
        self.__bc = bert_connector
        self.__tokenizer = self.__bc.tokenizer
        self.__bert_tagger = self.__bc.bert_tagger
        self.__lig = self.__bc.lig
        self.__new_word_start_char = self.__bc.new_word_start_char
        self.__device = self.__bc.device
        self.__text = text
        self.__pred_class = None
        self.__target_class = target_class
        self.__round_digits = round_digits

        self.__input_ids = []
        self.__baseline_input_ids = []
        self.__tokens = []
        self.__token_attributions = []
        self.__delta = None
        self.__words = []
        self.__word_attributions = []
        self.__words_and_attributions = []
        self.__tokens_and_attributions = []


        # set input ids, baseline input ids and tokens:
        self.__set_input_and_baseline(text)

        # set attributions and delta
        self.__set_attributions()

    @property
    def text(self):
        return self.__text

    @property
    def target_class(self):
        return self.__target_class

    @property
    def predicted_class_int(self):
        return self.__pred_class

    @property
    def predicted_class_str(self):
        return self.__bert_tagger.config.label_reverse_index.get(self.__pred_class)

    @property
    def word_attributions(self) -> List[dict]:
        if not self.__words_and_attributions:
            self.__convert_to_words()

        word_attrs_dict_list = [
            {"token": w, "score": round(a, self.__round_digits)}
            for w, a in self.__words_and_attributions
        ]
        return word_attrs_dict_list


    @property
    def token_attributions(self) -> List[dict]:
        token_attrs_dict_list = [
            {"token": w, "score": round(a, self.__round_digits)}
            for w, a in self.__tokens_and_attributions
        ]
        return token_attrs_dict_list


    def __zip(self, l1: list, l2: list) -> List[tuple]:
        zipped = list(zip(l1, l2))
        return zipped

    def __set_input_and_baseline(self, text: str) -> NoReturn:
        baseline_token_id = self.__tokenizer.pad_token_id
        sep_token_id = self.__tokenizer.sep_token_id
        cls_token_id = self.__tokenizer.cls_token_id

        text_ids = self.__tokenizer.encode(
            text,
            max_length = self.__bert_tagger.config.max_length,
            truncation = True,
            add_special_tokens = False
        )

        input_ids = [cls_token_id] + text_ids + [sep_token_id]
        token_list = self.__tokenizer.convert_ids_to_tokens(input_ids)

        baseline_input_ids = [cls_token_id] + [baseline_token_id] * len(text_ids) + [sep_token_id]

        self.__input_ids = torch.tensor([input_ids], device = self.__device)
        self.__baseline_input_ids = torch.tensor([baseline_input_ids], device = self.__device)
        self.__tokens = token_list


    def __set_attributions(self) -> NoReturn:
        pred_class_indx = torch.argmax(self.__bert_tagger.model(self.__input_ids)[0]).cpu().numpy()
        self.__pred_class = int(pred_class_indx)

        if self.__target_class == None:
            target = self.__pred_class
        else:
            target = self.__target_class

        attributions, delta = self.__lig.attribute(
                inputs = self.__input_ids,
                baselines = self.__baseline_input_ids,
                return_convergence_delta = True,
                internal_batch_size = 1,
                target = target
        )

        # summarize attributions
        attributions = attributions.sum(dim=-1).squeeze(0)
        attributions = attributions / torch.norm(attributions)

        # Remove special start and end tokens
        self.__tokens = self.__tokens[1:-1]
        attributions = attributions[1:-1]


        self.__token_attributions = attributions
        self.__delta = delta

        self.__tokens_and_attributions = self.__zip(
            self.__tokens,
            [float(t) for t in self.__token_attributions]
        )


    def __convert_to_words(self) -> NoReturn:
        """ Expands attributions from tokens to words.
        """
        if not self.__words:
            words = []
            word_attrs = []

            word_buf = []
            attr_buf = []

            for i in range(len(self.__tokens)):
                token_ = self.__tokens[i]
                attr_ = self.__token_attributions[i].cpu()

                if i > 0 and self.__bc.is_beginning_of_new_word(token_):
                    word = "".join(word_buf)
                    attr = np.sum(attr_buf)

                    words.append(word)
                    word_attrs.append(attr)

                    word_buf = []
                    attr_buf = []

                word_buf.append(token_.strip(self.__new_word_start_char))
                attr_buf.append(attr_)

            if word_buf:
                word = "".join(word_buf)
                attr = np.sum(attr_buf)

                words.append(word)
                word_attrs.append(attr)

            self.__words = words
            self.__word_attributions = np.array(word_attrs)

            self.__words_and_attributions = self.__zip(
                    self.__words,
                    self.__word_attributions
                )


    def __get_probability(self, pred_class: str, round_digits: int = 5) -> float:
        pred_indx = self.__bert_tagger.config.label_index.get(pred_class)

        with torch.no_grad():
            outputs = self.__bert_tagger.model(self.__input_ids)

        logits = outputs.get("logits")

        # Move logits and labels to CPU
        logits = logits.detach().cpu()
        probabilities = [logits.softmax(1).numpy().flatten()]
        probability = round(probabilities[0][pred_indx], round_digits)
        return probability


    def get_top_attributions(self,
                             threshold: float = 0.0,
                             words: bool = False,
                             ignore_special_tokens: bool = True
                            ) -> List[Tuple[str, float]]:
        """ Returns all the words/tokens with their attribution scores,
        if they exceed the given threshold.
        """
        if words:
            if not self.__words:
                self.__convert_to_words()

            zipped = self.__words_and_attributions

        else:
            zipped = self.__tokens_and_attributions

        zipped = deepcopy(zipped)
        zipped.sort(key=lambda x: x[1], reverse=True)

        if ignore_special_tokens:
            zipped = [
                (w, a) for w, a in zipped
                if w not in self.__tokenizer.all_special_tokens
            ]

        top_attributions = [
            {"token": w, "score": a} for w, a in zipped
            if a >= threshold
        ]
        return top_attributions


    def visualize(self, true_class: int, pred_class: str = "", words: bool = False) -> NoReturn:
        """ Visualize attributions.
        """
        if words and not self.__words:
            self.__convert_to_words()

        attributions = self.__word_attributions if words else self.__token_attributions
        raw_inputs = self.__words if words else self.__tokens

        if not pred_class:
            pred_class = self.predicted_class_str

        pred_prob = self.__get_probability(pred_class)


        score_vis = viz.VisualizationDataRecord(
                word_attributions = attributions,
                pred_prob = pred_prob,
                pred_class = pred_class,
                true_class = true_class,
                attr_class = self.__text,
                attr_score = attributions.sum(),
                raw_input_ids = raw_inputs,
                convergence_score = self.__delta
        )
        viz.visualize_text([score_vis])
