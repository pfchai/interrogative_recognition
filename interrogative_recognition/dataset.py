# -*- coding: utf-8 -*-

import os
import re
import json
from itertools import zip_longest


def split_sentence(sentence):
    ret = []
    items = re.split(r'([？。！?.!])', sentence)
    for t, p in zip_longest(items[::2], items[1::2], fillvalue=''):
        ret.append(t + p)
    return ret


class DatasetBase():

    def __init__(self, **kwargs):
        self.is_delete_end_punctuation = kwargs.get('is_delete_end_punctuation', False)
        self.tag2id = {
            'declarative_sentence': 0,
            'interrogative_sentence': 1,
        }

    def clean_sentence(self, sentence):
        if self.is_delete_end_punctuation:
            sentence = re.sub(r'[？。！?.!]$', '', sentence)
        return sentence


class C3Dataset(DatasetBase):

    def __init__(self, **kwargs):
        super(C3Dataset, self).__init__(**kwargs)

    def _load_data(self, file):
        data, label = [], []

        with open(file, 'r', encoding='utf-8') as f:
            samples = json.load(f)
            for sample in samples:
                [context, questions] = sample[:2]
                for reply in context:
                    for sentence in split_sentence(reply.split('：', 1)[-1]):
                        if len(sentence) < 2:
                            continue
                        data.append(self.clean_sentence(sentence))
                        if sentence[-1] in ("?", "？"):
                            label.append(self.tag2id['interrogative_sentence'])
                        else:
                            label.append(self.tag2id['declarative_sentence'])

                data.append(self.clean_sentence(questions[0]['question']))
                label.append(self.tag2id['interrogative_sentence'])

        assert len(data) == len(label)
        return data, label

    def load_data(self):
        data, label = [], []

        file_type = '.json'
        data_dir = '../data/c3'
        for file in os.listdir(data_dir):
            if os.path.splitext(file)[-1] == file_type:
                _data, _label = self._load_data(os.path.join(data_dir, file))
                data.extend(_data)
                label.extend(_label)

        return data, label


class Cmrc2018Dataset(DatasetBase):

    def __init__(self, **kwargs):
        super(Cmrc2018Dataset, self).__init__(**kwargs)

    def _load_data(self, file):
        data, label = [], []

        with open(file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            samples = json_data['data']
            for sample in samples:
                for paragraph in sample['paragraphs']:
                    for context in paragraph['context']:
                        for sentence in split_sentence(context):
                            if len(sentence) < 2:
                                continue
                            data.append(self.clean_sentence(sentence))
                            if sentence[-1] in ("?", "？"):
                                label.append(self.tag2id['interrogative_sentence'])
                            else:
                                label.append(self.tag2id['declarative_sentence'])

                    for question in paragraph['qas']:
                        data.append(self.clean_sentence(question['question']))
                        label.append(self.tag2id['interrogative_sentence'])

        assert len(data) == len(label)
        return data, label

    def load_data(self):
        data, label = [], []

        file_type = '.json'
        data_dir = '../data/cmrc2018_public'
        for file in os.listdir(data_dir):
            if os.path.splitext(file)[-1] == file_type:
                _data, _label = self._load_data(os.path.join(data_dir, file))
                data.extend(_data)
                label.extend(_label)

        return data, label


if __name__ == '__main__':
    dataset = C3Dataset()
    data, label = dataset.load_data()
    print(len(data))
    print(data[:10])
    print(label[:10])

    dataset = Cmrc2018Dataset()
    data, label = dataset.load_data()
    print(len(data))
    print(data[:10])
    print(label[:10])
