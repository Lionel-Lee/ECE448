"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import math

from collections import Counter
import math

tagset = {'NOUN', 'VERB', 'ADJ', 'ADV',
          'PRON', 'DET', 'IN', 'NUM',
          'PART', 'UH', 'X', 'MODAL',
          'CONJ', 'PERIOD', 'PUNCT', 'TO'}

tagarray = ['NOUN', 'VERB', 'ADJ', 'ADV',
          'PRON', 'DET', 'IN', 'NUM',
          'PART', 'UH', 'X', 'MODAL',
          'CONJ', 'PERIOD', 'PUNCT', 'TO']

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

    num_word = Counter()
    num_tag = Counter()
    num_word_tag = Counter()

    for sentence in train:                          #train
        for word_tag in sentence:
            num_word[word_tag[0]] += 1
            num_tag[word_tag[1]] += 1
            num_word_tag[word_tag] += 1

    most_recent_tag = num_tag.most_common(1)[0][0]

    predict = []    
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
    num_word = Counter()
    num_tag = Counter()
    num_word_tag = Counter()
    num_tag_tag = Counter()
    num_init_tag = Counter()

    total_sentences = 0
    total_words = 0
    for sentence in train:                          #train
        num_init_tag[sentence[0][1]] += 1
        total_sentences += 1
        total_words += len(sentence)
        for i in range(len(sentence)):
            word_tag = sentence[i]
            num_word[word_tag[0]] += 1
            num_tag[word_tag[1]] += 1
            num_word_tag[word_tag] += 1
            if not i==0:
                prev_word_tag = sentence[i-1]
                num_tag_tag[(prev_word_tag[1],word_tag[1])] += 1

    kindsofwords = len(num_word)
    k = 0.00001
    predict = []
    for sentence in test:                           #inference
        sentence_predict = []  
        trellis = []
        for _ in range(len(sentence)):
            prob_prev = []         
            for _ in range(16):
                prob_prev.append([0.0, -1])         #one of 16 entries in tag_prob_prev 
                                                    # = (probability, previous_tag_idx)
            trellis.append(prob_prev)           #3D trellis ==> [N][16][2]

        for word_idx in range(len(sentence)):
            cur_word = sentence[word_idx]
            if (word_idx == 0):                 #initial probabilities
                for tag_idx in range(16):
                    trellis[word_idx][tag_idx][0] = math.log((num_init_tag[tagarray[tag_idx]] + k)/(total_sentences+k*16))
                    # p1 = math.log((num_tag[tagarray[tag_idx]] + k)/(total_words+k*(kindsofwords+1)))
                    # p2 = math.log((num_word_tag[(sentence[word_idx],tagarray[tag_idx])] + k)/(num_tag[tagarray[tag_idx]]+k*(kindsofwords+1)))
                    # trellis[word_idx][tag_idx][0] = p1 + p2
            else:
                for tag_idx in range(16):
                    prev_idx = -1
                    max_prob = float("-inf")
                    for prev_tag_idx in range(16):
                        prev_prob = trellis[word_idx-1][prev_tag_idx][0]
                        cur_tag = tagarray[tag_idx]
                        prev_tag = tagarray[prev_tag_idx]
                        trans_prob = math.log((num_tag_tag[(prev_tag,cur_tag)]+k)/(num_tag[prev_tag]+k*16))
                        emission_prob = math.log((num_word_tag[(cur_word,cur_tag)]+k)/(num_tag[cur_tag]+k*(1+kindsofwords)))
                        cur_prob = prev_prob + trans_prob + emission_prob

                        if cur_prob > max_prob:
                            prev_idx = prev_tag_idx
                            max_prob = cur_prob
                    trellis[word_idx][tag_idx][1] = prev_idx
                    trellis[word_idx][tag_idx][0] = max_prob
        #back trace
        max_prob = float("-inf")
        max_tag_idx = -1
        for tag_idx in range(16):
            if trellis[-1][tag_idx][0] > max_prob:
                max_prob = trellis[-1][tag_idx][0]
                max_tag_idx = tag_idx
        for i in range(len(sentence)-1,-1,-1):
            sentence_predict.append((sentence[i], tagarray[max_tag_idx]))
            max_tag_idx = trellis[i][max_tag_idx][1]
        predict.append(sentence_predict[::-1])
    return predict


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