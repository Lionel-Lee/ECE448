# TextClassifier.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Dhruv Agarwal (dhruva2@illinois.edu) on 02/21/2019

"""
You should only modify code within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import math
class TextClassifier(object):
    def __init__(self):
        """Implementation of Naive Bayes for multiclass classification

        :param lambda_mixture - (Extra Credit) This param controls the proportion of contribution of Bigram
        and Unigram model in the mixture model. Hard Code the value you find to be most suitable for your model
        """
        # self.count_class={}
        # self.word_count_per_class={}
        # self.class_word_total={}
        # self.prob_class={}
        # self.word_prob_per_class={}
        # self.lambda_mixture = 0.0
        # self.diff_words={}
        # self.word_total=0.0
        # self.p_words={}
        self.count_word={}
        self.prob_word={}
        self.class_count={}
        self.prob_class={}
        self.lambda_mixture = 0.0
    def fit(self, train_set, train_label):
        """
        :param train_set - List of list of words corresponding with each text
            example: suppose I had two emails 'i like pie' and 'i like cake' in my training set
            Then train_set := [['i','like','pie'], ['i','like','cake']]

        :param train_labels - List of labels corresponding with train_set
            example: Suppose I had two texts, first one was class 0 and second one was class 1.
            Then train_labels := [0,1]
        """
        length=len(train_label)
        for i in range(1,15):
            self.class_count[i] = 0.0
            self.prob_class[i] = 0.0
        for sets, label in zip(train_set,train_label):
            for word in sets:
                if word not in self.count_word:
                    self.count_word[word]={}
                    self.prob_word[word]={}
                    for i in range(1,15):
                        self.count_word[word][i]=0.0
                        self.prob_word[word][i]=0.0
                    self.count_word[word][label] += 1.0
                else:
                     self.count_word[word][label] += 1.0
                self.class_count[label] += 1.0
        sum = 0
        for label in range(1,15):
            sum=sum+self.class_count[label]
        print(sum)
        for label in range(1,15):
            self.prob_class[label]=math.log(self.class_count[label]/sum)
        # use to print top 20 words each of class
        # for i in range(1,15):
        #     top={}
        #     for key in self.count_word.keys():
        #         # print(key)
        #         top[key]= self.count_word[key][i]
        #     # sorted(top,reverse=True)
        #     print("In class",i,", the top 20 words are:")
        #     counter=0
        #     for j in sorted(top.items(), key = lambda kv:(kv[1], kv[0]),reverse=True):
        #         counter += 1
        #         print(j,end="")
        #         if counter == 20:
        #             break
        #     print(" ")
                
        k=0.5
        for label in range(1,15):
            for word in self.count_word.keys():
                self.prob_word[word][label]=math.log((self.count_word[word][label]+k)/(self.class_count[label]+14 * k))
        

    def predict(self, x_set, dev_label,lambda_mix=0.0):
        """
        :param dev_set: List of list of words corresponding with each text in dev set that we are testing on
              It follows the same format as train_set
        :param dev_label : List of class labels corresponding to each text
        :param lambda_mix : Will be supplied the value you hard code for self.lambda_mixture if you attempt extra credit

        :return:
                accuracy(float): average accuracy value for dev dataset
                result (list) : predicted class for each text
        """
    
        accuracy = 0.0
        result = []
        count = 0.0
        for sets, label in zip(x_set,dev_label):
            max_prob=-999999.0
            max_class=0
            count += 1.0
            for each_label in range(1,15):
                # temp=0
                temp=self.prob_class[each_label]
                for word in sets:
                    if word in self.prob_word:
                        temp += self.prob_word[word][each_label]
                if temp > max_prob:
                    max_class=each_label
                    max_prob=temp
            if max_class == label:
                accuracy += 1.0
            # print(max_class)
            result.append(max_class)
        # TODO: Write your code here
        accuracy = accuracy / count
        return accuracy,result















