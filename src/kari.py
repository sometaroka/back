#!/usr/bin/env python3
import MeCab
m = MeCab.Tagger(
    "-Ochasen ")
print(m.parse("取れなかったんだ"))
