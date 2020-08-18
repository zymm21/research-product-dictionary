#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 11:51:55 2020

@author: qingji
"""
import math
def split(txt):
    s = ''
    lst = []
    for i in txt:
        if i not in '.?!':
            s += i
        else:
            lst += [str(s)]
            s = ''
          
    new_lst = []
  
    for n in lst:
        if n[0] == ' ':
            n = n[1:]
            new_lst += [str(n)]
        else:
            new_lst += [str(n)]           
    return new_lst
          
          
#part1
def clean_text(txt):
    clean = ''
    for letter in txt:  # for each character
        if letter.isalpha() or letter.isspace():  # if it is alphanumeric or space
            clean += letter  # keep it
    return clean.lower().split(' ')  # return list of words

def stem(s):
    if s.endswith('y'):
        s=s[:-1]+'i'
        return s
    if s.endswith('ies'):
        s=s[:-2]
        return s
    if s.endswith('e'):
        s=s[:-1]
        return s
    if s.endswith('ing'):
        s=s[:-3]
        return s
    if s.endswith('s'):
        s=s[:-1]
        return s
    if s.endswith('ed'):
        s=s[:-2]
        return s
    if s.endswith('tion'):
        s=s[:-3]+'e'
        return s


def compare_dictionaries(d1, d2):
    """return their log similarity score. """
    score = 0
    total = 0
    for i in d1:
        total += d1[i]
    for i in d2:
        if i in d1:
            score += d2[i] * math.log(d1[i] / total)
        else:
            score += d2[i] * math.log(0.5 / total)
    return score



class TextModel:
    def __init__(self, model_name):  # Constructor
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.first_word = {}

    def __repr__(self):
        # Construct string
         s = 'text model name: ' + self.name + '\n'
         s += ' number of words: ' + str(len(self.words)) + '\n'
         s += ' number of word lengths: ' + str(len(self.word_lengths))
         s += ' number of stems: ' + str(len(self.stems)) + '\n'
         s += ' number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
         return s

    def add_string(self, s):
        for char in s:
            if char == '.':
                index = s.index('.')
                one_sentence = s[:index]
                length = len(one_sentence.split(' '))
                if length not in self.sentence_lengths:
                    self.sentence_lengths[length] = 1
                else:
                    self.sentence_lengths[length] += 1
        
        words = clean_text(s)
        
        for w in words:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1

        for w in words:
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            else:
                self.word_lengths[len(w)] += 1

        for w in words:
            w = stem(w)
            if w not in self.stems:
                self.stems[w] = 1
            else:
                self.stems[w] +=1
                
    def add_file(self, filename):
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()  # get text
        self.add_string(text)  # add string
        
   
        
#part2        
    def sample_file_write(filename):
        d = {'test': 1, 'foo': 42}   # Create a sample dictionary.
        f = open(filename, 'w')      # Open file for writing.
        f.write(str(d))              # Writes the dictionary to the file.
        f.close()                    # Close the file.
    
    def sample_file_read(filename):
        f = open(filename, 'r')    # Open for reading.
        d_str = f.read()           # Read in a string that represents a dict.
        f.close()
        d = dict(eval(d_str))      # Convert the string to a dictionary.
        print("Inside the newly-read dictionary, d, we have:")
        print(d)
        
       
    def save_model(self):
        f1 = open((self.name + '_' + 'words'), 'w')
        f2 = open((self.name + '_' + 'word_lengths'), 'w')
        f3 = open((self.name + '_' + 'stems'), 'w')
        f4 = open((self.name + '_' + 'sentence_lengths'), 'w')
        f5 = open(self.name + '_' + 'self.first_word' + '.txt', 'w')
    
        f1.write(str(self.words))
        f2.write(str(self.word_lengths))
        f3.write(str(self.stems))
        f4.write(str(self.sentence_lengths))
        f5.write(str(self.first_word))
        
        f1.close()
        f2.close()
        f3.close()
        f4.close()
        f5.close()
        
    def read_model(self):
        f1 = open((self.name + '_' + 'words'), 'r')
        f2 = open((self.name + '_' + 'word_lengths'), 'r')
        f3 = open((self.name + '_' + 'stems'), 'r')
        f4 = open((self.name + '_' + 'sentence_lengths'), 'r')
        f5 = open(self.name + '_' + 'self.first_word' + '.txt', 'r')    # Open for reading.
        
        dict_str1 = f1.read()
        dict_str2 = f2.read()
        dict_str3 = f3.read()
        dict_str4 = f4.read()
        dict_str5 = f5.read()  
        
        f1.close()
        f2.close()
        f3.close()
        f4.close()
        f5.close()
        
        self.words = eval(dict_str1)
        self.word_lengths = eval(dict_str2)
        self.stems = eval(dict_str3)
        self.sentence_lengths = eval(dict_str4)
        self.first_word = eval(dict_str5)




    def similarity_scores(self, other):
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        first_word_score = compare_dictionaries(other.first_word, self.first_word)
        score_lst = [word_score, word_lengths_score, stems_score, sentence_lengths_score, first_word_score]
        return score_lst

    def classify(self, source1, source2):
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for source1 : ', scores1)
        print('scores for source2 : ', scores2)
        sim1 = 0
        sim2 = 0
        if scores1[0] > scores2[0]:
            sim1 += 1
        else:
            sim2 += 1
        if scores1[1] > scores2[1]:
            sim1 += 1
        else:
            sim2 += 1
        if scores1[2] > scores2[2]:
            sim1 += 1
        else:
            sim2 += 1
        if scores1[3] > scores2[3]:
            sim1 += 1
        else:
            sim2 += 1
        if scores1[4] > scores2[4]:
            sim1 += 1
        else:
            sim2 += 1
        if sim1 > sim2:
            print(self.name, 'is more likely to have come from', source1.name)
        else:
            print(self.name, 'is more likely to have come from', source2.name)


def test():
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)


def run_tests():
    source1 = TextModel('rowling')
    source1.add_file('rowling_source_text.txt')

    source2 = TextModel('shakespeare')
    source2.add_file('shakespeare_source_text.txt')

    new1 = TextModel('wr100')
    new1.add_file('wr100_source_text.txt')
    new1.classify(source1, source2)
    
    source3 = TextModel('New York Times')
    source3.add_file('New York Times_source_text.txt')

    source4 = TextModel('Wall Street Journal')
    source4.add_file('Wall Street Journal_source_text.txt')

    new2 = TextModel('Boston Globe')
    new2.add_file('Boston Globe_source_text.txt')
    new2.classify(source3, source4)   

    source5 = TextModel('Sheldon Cooper')
    source5.add_file('Sheldon Cooper_text.txt')

    source6 = TextModel('Barney Stinson')
    source6.add_file('Barney Stinson_source_text.txt')

    new3 = TextModel('Bart Simpson')
    new3.add_file('Bart Simpson_source_text.txt')
    new3.classify(source5, source6)  
    
    source7 = TextModel('Twain')
    source7.add_file('Twain_text.txt')

    source8 = TextModel('O.Henry')
    source8.add_file('O.Henry_source_text.txt')

    new4 = TextModel('arthistory')
    new4.add_file('arthistory_source_text.txt')
    new4.classify(source7, source8)  
    


















