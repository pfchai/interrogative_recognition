# -*- coding: utf-8 -*-

from interrogative_recognition.recognition_by_re import is_interrogative


# 使用正则的方式识别
def recognition_by_re():
    text = '最近身体还好吗？'
    recognition_result = '是' if is_interrogative(text) else '不是'
    print('句子"{}" => {}疑问句'.format(text, recognition_result))

    text = '今天天气不错'
    recognition_result = '是' if is_interrogative(text) else '不是'
    print('句子"{}" => {}疑问句'.format(text, recognition_result))


if __name__ == "__main__":
    recognition_by_re()