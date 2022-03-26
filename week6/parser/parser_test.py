"""
Acceptance tests for parser.py

Make sure that this file is in the same directory as parser.py!

"""
from io import StringIO
import os
import sys
from unittest.mock import patch
import pytest as pt
import parser as p

sentences = ["Holmes sat.",
             "I had a little moist red paint in the palm of my hand.",
             "Holmes lit a pipe.",
             "We arrived the day before Thursday.",
             "Holmes sat in the red armchair and he chuckled.",
             "My companion smiled an enigmatical smile.",
             "Holmes chuckled to himself.",
             "She never said a word until we were at the door here.",
             "Holmes sat down and lit his pipe.",
             "I had a country walk on Thursday and came home in a dreadful mess"]


def testPreprocess():
    assert p.preprocess(sentences[0]) == ["holmes", "sat"]
    assert p.preprocess(sentences[5]) == [
        "my", "companion", "smiled", "an", "enigmatical", "smile"]


@pt.mark.parametrize("sentenceNumber", range(1, 11))
def testTwo(sentenceNumber, capfd):
    sentenceDirectory = "./sentences/"
    testArgs = ['parser.py', sentenceDirectory + str(sentenceNumber) + ".txt"]

    with patch("sys.argv", testArgs):
        p.main()
        out, err = capfd.readouterr()
        assert "Grammar does not cover some of the input words" not in out
        assert "Could not parse sentence." not in out


def testHintExmpleOne(capfd):
    testSentence = StringIO('Holmes sat in the armchair.\n')
    pt.MonkeyPatch.setattr('sys.stdin', testSentence)
    # pt.MonkeyPatch.setattr('parser.main', testSentence)

    assert p.main()
    out, err = capfd.readouterr()
    assert "Grammar does not cover some of the input words" not in out
    assert "Could not parse sentence." not in out
