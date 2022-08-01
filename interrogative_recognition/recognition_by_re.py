# -*- coding: utf-8 -*-

import re


def is_interrogative(text):
    
    if re.findall(r'.*请问.*', text):
        return True
    if re.findall(r'.+[?？吗].*', text):
        return True
    if re.findall(r'.*怎么(?![这]).*', text):
        return True
    if re.findall(r'.*[呢么嘛]$', text):
        return True
    if re.findall(r'.*哪里|哪些|怎么|如何|什么.*', text):
        return True
    if re.findall(r'(\w)[不没](\1)', text):
        return True
    return False