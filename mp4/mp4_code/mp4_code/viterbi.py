"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

from collections import Counter

tagset = {'NOUN', 'VERB', 'ADJ', 'ADV',
          'PRON', 'DET', 'IN', 'NUM',
          'PART', 'UH', 'X', 'MODAL',
          'CONJ', 'PERIOD', 'PUNCT', 'TO'}

def baseline(train, test):
    '''
    TODO: implement the baseline algorithm. This function has time out limitation of 1 minute.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
            test data (list of sentences, no tags on the words)
            E.g  [[word1,word2,...][word1,word2,...]]
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''

    predict = []
    num_word = Counter()
    num_tag = Counter()
    num_word_tag = Counter()

    for sentence in train:                          #train
        for word_tag in sentence:
            num_word[word_tag[0]] += 1
            num_tag[word_tag[1]] += 1
            num_word_tag[word_tag] += 1

    most_recent_tag = num_tag.most_common(1)[0][0]
    
    for sentence in test:                           #inference
        sentence_predict = []   
        for word in sentence:
            max_tag = most_recent_tag
            num_max_tag = 0
            for tag in tagset:
                if num_word_tag[(word,tag)] > num_max_tag:
                    num_max_tag = num_word_tag[(word,tag)]
                    max_tag = tag
            sentence_predict.append((word,max_tag))
        predict.append(sentence_predict)    
        
    return predict
    






def viterbi_p1(train, test):
    '''
    TODO: implement the simple Viterbi algorithm. This function has time out limitation for 3 mins.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no tags on the words)
            E.g [[word1,word2...]]
    output: list of sentences with tags on the words
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''

    predicts = []
    raise Exception("You must implement me")
    return predicts

def viterbi_p2(train, test):
    '''
    TODO: implement the optimized Viterbi algorithm. This function has time out limitation for 3 mins.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no tags on the words)
            E.g [[word1,word2...]]
    output: list of sentences with tags on the words
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''


    predicts = []
    raise Exception("You must implement me")
    return predicts