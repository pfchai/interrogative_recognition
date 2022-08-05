# -*- coding: utf-8 -*-

import os
import pickle
import argparse

# import jieba
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

from dataset import C3Dataset, Cmrc2018Dataset


def load_data(is_delete_end_punctuation=False):
    examples, labels = [], []

    dataset = C3Dataset(is_delete_end_punctuation=is_delete_end_punctuation)
    _examples, _labels = dataset.load_data()
    examples.extend(_examples)
    labels.extend(_labels)

    dataset = Cmrc2018Dataset(is_delete_end_punctuation=is_delete_end_punctuation)
    _examples, _labels = dataset.load_data()
    examples.extend(_examples)
    labels.extend(_labels)

    assert len(examples) == len(labels)
    return examples, labels


def load_pickle(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)


def save_pickle(obj, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f)


def make_vectorizer(examples, vectorizer_name, save_path):
    if vectorizer_name.lower() == 'tfidf':
        vectorizer = TfidfVectorizer(
            token_pattern=r"(?u)\b\w+\b",
            max_features=5000)
    elif vectorizer_name.lower() == 'bow':
        vectorizer = CountVectorizer(
            token_pattern=r"(?u)\b\w+\b",
            max_features=5000)
    else:
        raise

    vectorizer.fit(examples)

    name = 'vectorizer_' + vectorizer_name + '.pickle'
    save_pickle(vectorizer, os.path.join(save_path, name))
    return vectorizer


def run(args):
    examples, labels = load_data(args.delete_end_punctuation)
    document = [' '.join(example.split()) for example in examples]
    print('加载数据完成，共加载 {} 条数据'.format(len(examples)))

    if args.do_train_vectorizer:
        vectorizer = make_vectorizer(document, args.vectorizer, args.model_path)
    else:
        name = 'vectorizer_' + args.vectorizer + '.pickle'
        vectorizer = load_pickle(os.path.join(args.model_path, name))

    print('vectorizer 训练/加载 完成')

    vec_x = vectorizer.transform(examples)
    print('数据向量化完成')

    x_train, x_val, y_train, y_val = train_test_split(vec_x, labels, test_size=0.2, shuffle=True, random_state=42)

    if args.do_train:
        if args.classifier == 'svm':
            classifier = LinearSVC()
        elif args.classifier == 'dt':
            classifier = DecisionTreeClassifier()
        elif args.classifier == 'ada_boost':
            classifier = AdaBoostClassifier(random_state=2022)
        # 集成学习
        # elif args.classifier == 'ensemble':
            # classifier = VotingClassifier(estimators=[('svc', clf1), ('tree', clf2), ('ada', clf3)])

    print('开始训练')
    classifier.fit(x_train, y_train)
    print('训练完成')

    val_pre = classifier.predict(x_val)
    print(classification_report(y_val, val_pre))

    if args.do_train:
        name = args.classifier + '.pickle'
        save_pickle(classifier, os.path.join(args.model_path, name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='机器学习模型判断句子是否为疑问句')
    parser.add_argument('--vectorizer', default='tfidf', help='文本特征')
    parser.add_argument('--do_train_vectorizer', default=False, action='store_true')
    parser.add_argument('--classifier', default='dt', help='分类器')
    parser.add_argument('--model_path', default='./models', help='模型保存路径')
    parser.add_argument('--do_train', default=False, action='store_true')

    parser.add_argument('--delete_end_punctuation', default=True, type=bool)
    args = parser.parse_args()

    run(args)
