#!/usr/bin/python
# -*- coding: ISO-8859-9 -*-

import os
import time
import nltk
import sys
import re
import logging
from TurkishStemmer import TurkishStemmer
from zemberek import (

        TurkishMorphology,
        TurkishTokenizer,
        TurkishSpellChecker,
        TurkishSentenceExtractor,
        TurkishSentenceNormalizer

)

absolute_path = os.getcwd() + "/data/train"
stop_words = []


class Category:

    def __init__(self, name, training_path, testing_path):
        self.name = name
        self.training_path = training_path
        self.testing_path = testing_path
        self.training_files = []
        self.testing_files = []
        self.file_contents = []
        self.tokenized_file_contents = []
        self.stemmed_words = []
        self.finalized_words = []
        self.f

    def check_directories(self):

        path = os.getcwd()

        print("Current working directory '{}'".format(path))
        # time.sleep(1)
        print("Checking folder training and testing folders for '{}'...".format(self.name))
        # time.sleep(1)
        print(os.listdir())
        # time.sleep(1)

        if not os.path.exists(self.training_path):
            print("'{}' folder doesn't exist".format(self.training_path))
        else:
            print("'{}' folder exists".format(self.training_path))

        if not os.path.exists(self.testing_path):
            print("'{}' folder doesn't exist".format(self.testing_path))
        else:
            print("'{}' folder exists".format(self.testing_path))

    def import_training_files(self):

        # Get the list of all files in directory tree at given path
        self.files = getListOfFiles(absolute_path)

        # Print the files
        for elem in self.files:
            print(elem)
        print("****************")

    def parse_imported_files(self):

        logger = logging.getLogger(__name__)

        print("There are {} files in the directory...".format(len(self.files)))
        content = ""
        # sort lines
        for i in range(len(self.files)):
            FileName = (self.files[i])
            # print(FileName)
            with open(FileName, encoding="iso-8859-9") as f:
                content = f.read()

                content = re.sub("\W+", ' ', content)
                content = re.sub("\d", '', content)
                content = content.lower()
                content = content.split()
                # content = [x.strip() for x in content]
                # print(content)
                # self.file_contents.append(content)
                self.file_contents.extend(content)
        # print(self.filecontents)

        self.file_contents = list(filter(None, self.file_contents))

        # print(self.file_contents)

        """for i in range(len(self.filecontents)):
            print(type(self.filecontents[i]))"""

        # sorts the contents
        self.file_contents.sort()

        # print(self.file_contents)
        print("unfiltered word count: ", len(self.file_contents))

        # adds plain words
        ordered_tokens = set()
        for word in self.file_contents:
            if word not in ordered_tokens:
                ordered_tokens.add(word)
                self.tokenized_file_contents.append(word)

        # print(self.tokenized_file_contents)
        print("tokenized word count: ", len(self.tokenized_file_contents))

        # remove stopwords
        stopwordremovedlist = []
        for word in self.tokenized_file_contents:
            if word in stop_words:
                self.tokenized_file_contents.remove(word)
                stopwordremovedlist.append(word)
                # print(word)

        # print(self.tokenized_file_contents)

        # print(stopwordremovedlist)
        print("removed word count: ", len(stopwordremovedlist))
        print("filtered word count: ", len(self.tokenized_file_contents))

        stemmer = TurkishStemmer()
        for word in self.tokenized_file_contents:
            stemmedWord = stemmer.stem(word)
            self.stemmed_words.append(stemmedWord)
        print("stemlenmiş kelime sayısı: ", len(self.stemmed_words))
        print(self.stemmed_words)
        self.finalized_words = set(self.stemmed_words)

        morphology = TurkishMorphology.create_with_defaults()

        """start = time.time()
        sc = TurkishSpellChecker(morphology)
        logger.info(f"Spell checker instance created in: {time.time() - start} s")

        start = time.time()
        for word in self.finalized_words:
            print(word + " = " + ' '.join(sc.suggest_for_word(word)))
        logger.info(f"Spells checked in: {time.time() - start} s")"""


        # print(self.stemmed_words)
        print("stemlenip temizlenmiş kelime sayısı: ", len(self.finalized_words))
        print(self.finalized_words)

        """ tokenizer = TurkishTokenizer.DEFAULT

        for word in self.finalized_words:
            tokens = tokenizer.tokenize(word)
            for token in tokens:
                print('Content = ', token.content)
                print('Type = ', token.type_.name)
                print('Start = ', token.start)
                print('Stop = ', token.end, '\n')"""

        """for word in self.finalized_words:
            results = morphology.analyze(word)
            for result in results:
                print(result)
            print("\n")"""

    def vsm_print(self):
        print(self.finalized_words)

    def import_testing_files(self):

        try:
            os.chdir(self.testing_path)

        except:
            print("da")


def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

if __name__ == '__main__':

    FileName = "stop-words_TUR.txt"

    stemmer = TurkishStemmer()
    word = stemmer.stem("eleme")
    print(word)

    with open(FileName) as f:
        words = f.read()
        words = words.split()
        stop_words.extend(words)
        print(type(words))
        print(stop_words)

    economy = Category("ekonomi", "train/ekonomi", "test/ekonomi")
    economy.check_directories()
    economy.import_training_files()
    economy.parse_imported_files()
    economy.vsm_print()

    print("anan")
    print(sys.getdefaultencoding())
    print(sys.getfilesystemencoding())
    print(sys.stdout.encoding)
