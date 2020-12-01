"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import math
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
    # Assign smoothing factor (as suggested on piazza)
    # Assign smoothing factor (as suggested on piazza)
    '''
    k = 1e-5

    # Dictionary to keep count of occurrence
    words = Counter()  # (word, count)
    tags = Counter()  # (tag, count)
    word_to_tag = Counter()  # ((word, tag), count)
    prev_and_cur = Counter()  # ((cur, prev), count)
    init_tag = Counter()  # (first_word_of_sentence, count)

    # Train Data
    for sentence in train:
        # increment first word of sentence's tag
        init_tag[sentence[0][1]] += 1
        max_idx = len(sentence) - 1
        pair_idx = 0
        for pair in sentence:
            cur_word = pair[0]
            cur_tag = pair[1]

            # Increment word, tag, (word, tag) count
            words[cur_word] += 1
            tags[cur_tag] += 1
            word_to_tag[(cur_word, cur_tag)] += 1

            # Increment (cur,next) count
            if pair_idx + 1 < max_idx:
                prev_and_cur[(cur_tag, sentence[pair_idx + 1][1])] += 1
            pair_idx += 1

    # Dictionaries to keep probabilities of each type:
    trans_prob = {}  # Transmission Probability
    init_prob = {}  # Initial Probability

    # Calculate the Transmission and Initial Probabilities
    # Formulas given on piazza
    for cur_tag in tags:
        for prev_tag in tags:
            n = prev_and_cur[(prev_tag, cur_tag)] + k
            d = tags[prev_tag] + k * len(tags)
            trans_prob[(cur_tag, prev_tag)] = math.log(n / d)

        n = init_tag[cur_tag] + k
        d = sum(init_tag.values()) + k * len(tags)
        init_prob[cur_tag] = math.log(n / d)

    predicts = []
    # Develop Data:
    for sentence in test:
        # algorithm from page 11 of https://web.stanford.edu/~jurafsky/slp3/8.pdf
        viterbi = {}
        backpointer = {}
        first_word = sentence[0]

        # Initialization
        for cur_tag in tags:
            n = word_to_tag[(first_word, cur_tag)] + k
            d = tags[cur_tag] + k * len(words)
            emission_prob = math.log(n / d)

            viterbi[(cur_tag, 0)] = init_prob[cur_tag] + emission_prob
            backpointer[(cur_tag, 0)] = 0

        # Recursion
        best_path_max = {}
        max_time_step = range(len(sentence))
        max_len = len(sentence) - 1
        for t in max_time_step:
            if t is 0:
                continue
            for cur_tag in tags:
                # get max probability of previous time step
                prob = {}
                for prev_tag in tags:
                    n = word_to_tag[(sentence[t], cur_tag)] + k
                    d = tags[cur_tag] + k * len(words)
                    emission_prob = math.log(n / d)
                    prob[prev_tag] = trans_prob[(cur_tag, prev_tag)] + emission_prob + viterbi[(prev_tag, t - 1)]

                # get max prob from previous time step
                viterbi[(cur_tag, t)] = max(prob.values())

                # get key tag of the maximum into back pointer
                # https://www.geeksforgeeks.org/python-get-key-with-maximum-value-in-dictionary/
                backpointer[(cur_tag, t)] = (max(prob, key=prob.get), t - 1)

        # Termination step:
        # get the list of best probs for each tag at max_len
        for cur_tag in tags:
            best_path_max[(cur_tag, max_len)] = viterbi[(cur_tag, max_len)]

        best_path = []
        # Get index of the best probability
        bestpathpointer = max(best_path_max, key=best_path_max.get)
        # follows backpointer[] to states back in time
        while bestpathpointer != 0:
            best_path.insert(0, bestpathpointer[0])
            bestpathpointer = backpointer[bestpathpointer]

        predicted_sentence = []
        for idx in max_time_step:
            predicted_sentence.append((sentence[idx], best_path[idx]))

        predicts.append(predicted_sentence)
    return predicts
    '''


    k = 1e-5

    # initialization
    words = Counter()
    tags = Counter()
    word_tag = Counter() # ((word, tag),count)
    curr_next = Counter() # ((current tag, next tag), count)
    init_tag = Counter() # (initial tag of a sentence, count)

    # train data
    for sentence in train:
        # update initial word tag
        init_tag[sentence[0][1]] += 1
        max_idx = len(sentence) - 1
        pair_idx = 0
        for pair in sentence:
            # update words, tags and word_tag
            curr_word = pair[0]
            curr_tag = pair[1]
            words[curr_word] += 1
            tags[curr_tag] += 1
            word_tag[(curr_word, curr_tag)] += 1

            # update prev_curr
            if pair_idx + 1 < max_idx:
                curr_next[(curr_tag, sentence[pair_idx + 1][1])] += 1
                pair_idx += 1

     # calculate initial and transmission probability
    init_prob = {}
    tran_prob = {}
    # smoothing
    for next_tag in tags:
        # transmission
        for curr_tag in tags:
            nominator = curr_next[(curr_tag, next_tag)] + k
            denominator = tags[curr_tag] + k * len(tags)
            tran_prob[(next_tag, curr_tag)] = math.log(nominator / denominator)
        # initial
        nominator = init_tag[next_tag] + k
        denominator = sum(init_tag.values()) + k * len(tags)
        init_prob[next_tag] = math.log(nominator / denominator)

    # test data
    predicts = []
    # initialization
    for sentence in test:
        viterbi = {}
        backpointer = {}
        init_word = sentence[0]
        for curr_tag in tags:
            # update initial word tag
            nominator = word_tag[init_word, curr_tag] + k
            denominator = tags[curr_tag] + len(words) * k
            emiss_prob = math.log(nominator / denominator)

            viterbi[(curr_tag, 0)] = init_prob[curr_tag] + emiss_prob
            backpointer[(curr_tag, 0)] = 0

        # Recursion
        best_path_max = {}
        max_time_step = range(len(sentence))
        max_len = len(sentence) - 1
        for t in max_time_step:
            if t is 0:
                continue
            for cur_tag in tags:
                # get max probability of previous time step
                prob = {}
                for prev_tag in tags:
                    n = word_tag[(sentence[t], cur_tag)] + k
                    d = tags[cur_tag] + k * len(words)
                    emission_prob = math.log(n / d)
                    prob[prev_tag] = tran_prob[(cur_tag, prev_tag)] + emission_prob + viterbi[(prev_tag, t - 1)]

                # get max prob from previous time step
                viterbi[(cur_tag, t)] = max(prob.values())

                # get key tag of the maximum into back pointer
                # https://www.geeksforgeeks.org/python-get-key-with-maximum-value-in-dictionary/
                backpointer[(cur_tag, t)] = (max(prob, key=prob.get), t - 1)


        # # recursion
        # best_path_max = {}
        # max_time_idx = len(sentence) - 1
        # max_timestep = range(len(sentence))
        # for timestep in max_timestep:
        #     if timestep == 0:
        #         continue
        #     for next_tag in tags:
        #         prob = {}
        #         for curr_tag in tags:
        #             # smoothing
        #             nominator = word_tag[sentence[timestep], curr_tag] + k
        #             denominator = tags[next_tag] + len(words) * k
        #             emiss_prob = math.log(nominator / denominator)
        #             prob[curr_tag] = trans_prob[(next_tag, curr_tag)] + emiss_prob + viterbi[(curr_tag, timestep - 1)]
        #
        #         # get max prob from previous time step
        #         viterbi[(next_tag, timestep)] = max(prob.values())
        #         # get max parameter from previous time step
        #         backpointer[(next_tag, timestep)] = (max(prob, key=prob.get), timestep - 1)


        # termination
        best_path = []
        for curr_tag in tags:
            best_path_max[(curr_tag, max_len)] = viterbi[(curr_tag, max_len)]
        # set initial pointer
        best_path_pointer = max(best_path_max, key = best_path_max.get)
        while best_path_pointer != 0:
            best_path.insert(0, best_path_pointer[0])
            best_path_pointer = backpointer[best_path_pointer]

        predict_sentence = []
        for time in max_time_step:
            predict_sentence.append((sentence[time], best_path[time]))
        predicts.append(predict_sentence)
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