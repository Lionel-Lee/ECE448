"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import math
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
    predicts = []
    raise Exception("You must implement me")
    return predicts


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
    tags={}
    tag_pairs={}
    tag_word={}
    total_words=0
    unique_words=0
    tag_trans_pair=0
    #pre count 
    for each_sent in train:
        for index in range(0,len(each_sent)):
            word_tag_pair=each_sent[index]
            total_words += 1
            word= word_tag_pair[0]
            tag= word_tag_pair[1]
            #add tag count
            if tag not in tags:
                tags[tag] = 1
            else:
                tags[tag] +=1
            #add tag_words count
            if tag in tag_word:
                if word in tag_word:
                    tag_word[tag][word] +=1
                else:
                    tag_trans_pair +=1
                    tag_word[tag][word] =1
            else:
                tag_trans_pair +=1
                tag_word[tag] = {word : 1}
            #add tag_pairs count
            if (index != (len(each_sent)-1)):
                next_pair=each_sent[index+1]
                next_tag=next_pair[1]
                if tag in tag_pairs:
                    if next_tag in tag_pairs[tag]:
                        tag_pairs[tag][next_tag] +=1
                    else:
                        tag_pairs[tag][next_tag] =1
                else:
                    tag_pairs[tag]={next_tag:1}
    #calculate prob
    #first for tag prob
    k=0.000001
    tag_sum=sum(tags.values())
    for tag in tagset:
        if tag in tags:
            tags[tag]= math.log((tags[tag]+k)/(tag_sum + 16*k))
        else:
            tags[tag]= math.log((k)/(tag_sum + 16*k))
    #for tag_words prob
    for tag in tagset:
        tag_sum=sum(tag_word[tag].values())
        tag_word[tag]['UNKNOWN']=0
        for word in tag_word[tag]:
            tag_word[tag][word]= math.log((tag_word[tag][word]+k)/(tag_sum + (len(tag_word))*k))
    #for tag_pair prob:
    for tag in tag_pairs:
        tag_sum=sum(tag_pairs[tag].values())
        for next_tag in tagset:
            if next_tag in tag_pairs[tag]:
                tag_pairs[tag][next_tag]= math.log((tag_pairs[tag][next_tag]+k)/(tag_sum + (len(tag_pairs[tag])+ 1)*k))
            else:
                tag_pairs[tag][next_tag]= math.log((k)/(tag_sum + (len(tag_pairs[tag]) + 1)*k)) 
    # raise Exception("You must implement me")
    for each_sent in test:
        best_tag=[]
        best_prob=[]
        local_best_tag={}
        local_best_prob={}
        #first column
        for each_tag in tagset:
            local_best_prob[each_tag]=tags[each_tag]
            local_best_tag[each_tag]='st'
        # print(local_best_prob)
        best_tag.append(local_best_tag)
        best_prob.append(local_best_prob)
        for i in range(1,len(each_sent)+1):
            local_best_tag={}
            local_best_prob={}
            for next_tag in tagset:
                temp=float('-inf')
                for tag in tagset:
                    a=best_prob[i-1][tag]
                    b=tag_pairs[tag][next_tag]
                    c=tag_word[next_tag].get(each_sent[i-1],tag_word[next_tag]['UNKNOWN'])
                    if (a+b+c>temp):
                        temp=best_prob[i-1][tag]\
                            +tag_pairs[tag][next_tag]\
                            +tag_word[next_tag].get(each_sent[i-1],tag_word[next_tag]['UNKNOWN'])
                        local_best_prob[next_tag]=a+b+c
                        local_best_tag[next_tag]=tag
            best_tag.append(local_best_tag)
            best_prob.append(local_best_prob)
        temp_ans=[]
        temp_ans.insert(0,(each_sent[len(each_sent)-1],max(best_prob[len(each_sent)],key=best_prob[len(each_sent)].get)))
        curr_tag=best_tag[len(each_sent)][max(best_prob[len(each_sent)],key=best_prob[len(each_sent)].get)]
        for i in range(len(each_sent)-1,0,-1):
            temp_ans.insert(0,(each_sent[i-1],curr_tag))
            curr_tag=best_tag[i][curr_tag]
        predicts.append(temp_ans)
        # print(temp_ans)
        # return predicts
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