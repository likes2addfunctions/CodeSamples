 # -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 12:29:08 2017

@author: g
"""

import csv

import tensorflow as tf

import numpy as np

import math

import time

import random

start = time.time()
datafile = "c:/users/g/desktop/data/train.csv"
validfile = "c:/users/g/desktop/data/valid.csv"

def prep_data(df):
    utts = []
    replys = []
    with open(df, encoding="utf8") as data:
        next(data)
        for convostr in data:
            while len(convostr) > 6:
                eou = convostr.find("__eou__")
                eot = convostr.find("__eot__")
                current_utt = convostr[:eou].replace("__eot__", "")
                convostr = convostr[(eou + 8):]
                eou2 = convostr.find("__eou__")
                next_utt = convostr[:eou2].replace("__eot__", "")
#                print("eou:", eou)
#                print("eot:", eot)
#                print("Curr urr:", current_utt)
#                print("next_utt:", next_utt)
                utts.append(current_utt)
                if (eot < eou) and (eot > -1):
                    replys.append(next_utt)
                else:
                    replys.append("")
                
    prepared_data =  [utts,replys]
    return prepared_data

def trans_stmt(stmt):
    transformed_stmt = tf.cast(np.array(list(vocab_processor.fit_transform(stmt))), 
                               tf.float32)
    return transformed_stmt

def clean_decode(raw_decode):
    print("decoding")
    clean_ans = ""
    for entry in raw_decode:
        word = entry[:entry.find("<UNK>")].replace(" " , "")
        clean_ans = clean_ans + word + " "
    return clean_ans
              
def pad_mats(matlst, max_conv_length):
    L = max_conv_length
    padded_mats = []
    for mat in matlst:
        n = L - len(list(sess.run(mat)))
        if n > 0:
            paddings = [[0,n],[0,0]]
            mat = tf.pad(mat,paddings, "CONSTANT")
        if n < 0:
            mat = tf.cast(np.array(list(sess.run(mat))[:L]), dtype=tf.float32)
        padded_mats.append(mat)
    return(padded_mats)

def get_stmt_cat(stmt):
    if stmt.find("?") > 0:
        return (0,1,0)
    if stmt.find("apt-get") > 0:
        return (1,0,0)
    else:
        return (0,0,1)



prepared_data = prep_data(datafile)


### Prepare vocab processor
max_document_length = 15
  
vocab_processor = tf.contrib.learn.preprocessing.VocabularyProcessor(
        max_document_length,
        min_frequency = 20)

vocab_processor.fit(prepared_data[0])

vocab_dict = vocab_processor.vocabulary_._mapping    

dict_len = len(vocab_dict)
print (dict_len, "words learned")


sess = tf.Session()


max_conv_length = max(len(stmt.split()) for stmt in prepared_data[0])
print ("max utt length", max_conv_length)

m = max_document_length
num_of_cats = 3
curr_in = tf.placeholder(tf.float32)
out_cat = tf.placeholder(tf.float32)
out_pred = tf.placeholder(tf.float32)
A = tf.Variable(2* np.random.random_sample((m,num_of_cats))-1, dtype=tf.float32)
d = tf.Variable(np.random.random([1,num_of_cats]), dtype=tf.float32)
E = tf.Variable(2 * np.random.random_sample([1,max_conv_length]) - 1, dtype=tf.float32)

init = tf.global_variables_initializer()
sess.run(init)

y = tf.nn.softmax(tf.matmul(curr_in,A) + d)
cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=out_cat, logits=y)
optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(cross_entropy)
print ("error defined")

def make_batch_data(pre_data, size):
    in_list = []
    out_list = []
    for k in range(size):
        entrypt = random.randrange(len(pre_data[0]))
        stmt = trans_stmt(pre_data[0][entrypt]) 
        P = pad_mats([stmt], max_conv_length)
        in_point = sess.run(tf.matmul(E,P[0]))
        outcat = get_stmt_cat(pre_data[1][entrypt])
        in_list.append(in_point[0])
        out_list.append(outcat)
    in_batch = np.array(in_list)
    out_batch = np.array(out_list)
    return (in_batch, out_batch)
    
valid_data = prep_data(validfile)

for j in range(500):
    batch = make_batch_data(prepared_data,100)
    print("training")
    sess.run(train, feed_dict={curr_in: batch[0], out_cat: batch[1]})     


    if j%20 == 0:
        print("validating")
        valid_batch = make_batch_data(valid_data, 50)
        out_preds = []
        for stmt in valid_batch[0]:
            out_preds.append(list(sess.run(y, {curr_in: [stmt]}))[0])
        OP = np.array(out_preds)
        print (OP[:10])
        correct_prediction = tf.equal(tf.argmax(out_pred, 1), tf.argmax(out_cat, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        A = sess.run(accuracy, feed_dict={out_pred: OP, out_cat: np.array(valid_batch[1])})    
        now = time.time()
        print ("time :" , now - start, ":", "validation complete with", A, "accuracy on epoch", j)
        
        print (" ")\
    

        
        


