from collections import defaultdict
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

def extra(train,test):
    '''
    TODO: implement improved viterbi algorithm for extra credits.
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
    num_tag_tag = Counter()
    num_init_tag = Counter()
    scale=Counter()
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
    k = 0.13
    for each in num_word_tag:
        if (num_word_tag[each] == 1):
            scale[each[1]] +=1
    scale_sum=sum(scale.values())
    for each in tagset:
        if each not in scale:
            scale[each] = 0
        scale[each] = (scale[each] + k )/ (scale_sum+k*16)
    
    # for each in scale:
        
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
                #     if tagarray[tag_idx] in num_init_tag:
                #         trellis[word_idx][tag_idx][0] = math.log((num_init_tag[tagarray[tag_idx]] + k)/(total_sentences+k*16))
                #     else:
                #         trellis[word_idx][tag_idx][0] = math.log(k/(total_sentences+k*16)) 
                    p1 = math.log((num_tag[tagarray[tag_idx]] + k)/(total_words+k*(kindsofwords+1)))
                    p2 = math.log((num_word_tag[(sentence[word_idx],tagarray[tag_idx])] + k)/(num_tag[tagarray[tag_idx]]+k*(kindsofwords+1)))
                    trellis[word_idx][tag_idx][0] = p1 + p2
            else:
                for tag_idx in range(16):
                    prev_idx = -1
                    max_prob = float("-inf")
                    for prev_tag_idx in range(16):
                        prev_prob = trellis[word_idx-1][prev_tag_idx][0]
                        cur_tag = tagarray[tag_idx]
                        prev_tag = tagarray[prev_tag_idx]
                        trans_prob = math.log((num_tag_tag[(prev_tag,cur_tag)]+k)/(num_tag[prev_tag]+k*16))
                        # print(cur_tag,scale[cur_tag])
                        emission_prob = math.log((num_word_tag[(cur_word,cur_tag)]+scale[cur_tag]*k)/(num_tag[cur_tag]+scale[cur_tag]*k*(1+kindsofwords)))
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


    predicts = []
    raise Exception("You must implement me")
    return predicts