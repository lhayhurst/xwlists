#!/usr/bin/python -u
# -*- coding: utf-8 -*-

def decode(text):
    if text is None:
        return ""
    return text.decode( 'ascii', 'ignore')
