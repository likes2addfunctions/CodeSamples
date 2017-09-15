 # -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 12:29:08 2017

@author: g
"""


import tensorflow as tf

import numpy as np

import time

import matplotlib.pyplot as plt

import random

fig = plt.figure()

start = time.time()
datafile = "c:/users/g/desktop/data/test.csv"
validfile = "c:/users/g/desktop/data/valid.csv"


def clean_stmt(stmt):
    end_tokens = ["__eou__\"", "__eot__", "__eou__,", "__eou__"]
    for token in end_tokens:
        stmt = stmt.replace(token, "")
    return stmt

def prep_data_long(data):
    utts = []
    replys = []
    for convostr in data:
        while len(convostr) > 6:
            ends1 = []
            ends2 = []
            end_tokens = ["__eot__", "__eou__,", "__eou__\""]
            for token in end_tokens:
                if convostr.find(token) > -1:
                    ends1.append(convostr.find(token))
            if len (ends1) == 0:
                eot1 = -1
            else:
                eot1 = min(ends1)
            current_utt = clean_stmt(convostr[1:eot1])
            convostr = convostr[(eot1 + 7):]
            for token in end_tokens:
                if convostr.find(token) > -1:
                    ends2.append(convostr.find(token))
            if len (ends2) == 0:
                eot2 = -1
            else:
                eot2 = min(ends2)
            next_utt = clean_stmt(convostr[:eot2])
            if len(current_utt) > 0:
                utts.append(current_utt)    
                if eot2 > -1:
                    replys.append(next_utt)
                else:
                    replys.append("__eoc__")               
    prepared_data =  [utts,replys]
    return prepared_data

def get_vocab(df):
    utts = []
    replys = []
    with open(df, encoding = "utf8") as data:
        for convostr in data:
            if len(convostr.split()) < 500:
                while len(convostr) > 6:
                    ends1 = []
                    ends2 = []
                    end_tokens = ["__eot__", "__eou__,", "__eou__\""]
                    for token in end_tokens:
                        if convostr.find(token) > -1:
                            ends1.append(convostr.find(token))
                    if len (ends1) == 0:
                        eot1 = -1
                    else:
                        eot1 = min(ends1)
                    current_utt = clean_stmt(convostr[1:eot1])
                    convostr = convostr[(eot1 + 7):]
                    for token in end_tokens:
                        if convostr.find(token) > -1:
                            ends2.append(convostr.find(token))
                    if len (ends2) == 0:
                        eot2 = -1
                    else:
                        eot2 = min(ends2)
                    next_utt = clean_stmt(convostr[:eot2])
                    if len(current_utt) > 0:
                        utts.append(current_utt)    
                        if eot2 > -1:
                            replys.append(next_utt)
                        else:
                            replys.append("__eoc__")
        data.close()
    vocab = utts
    return vocab

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
        #print (mat)
        n = L - len(list(sess.run(mat)))
        if n > 0:
            paddings = [[0,n],[0,0]]
            mat = tf.pad(mat,paddings, "CONSTANT")
        if n < 0:
            mat = tf.cast(np.array(list(sess.run(mat))[:L]), dtype=tf.float32)
        padded_mats.append(mat)
    return(padded_mats)


def get_stmt_cat(stmt):
    if stmt == "":
        return cat_vects[0]
    for k in range(num_of_cats-2):
        if stmt.find(key_list[k+1]) > -1:
            return cat_vects[k+1]
    else:
        return cat_vects[-1]

def format_batch_data(pre_data):
    in_list = []
    out_list = []
    for k in range(len(pre_data[0])):
        #print(pre_data[0][k])
        stmt = trans_stmt(pre_data[0][k]) 
        #print (pre_data[0][entrypt])
        P = pad_mats([stmt], max_conv_length)
        in_point = sess.run(tf.matmul(E,P[0])+f)
        outcat = get_stmt_cat(pre_data[1][k])
        in_list.append(in_point[0])
        out_list.append(outcat)
    in_batch = np.array(in_list)
    out_batch = np.array(out_list)
    return (in_batch, out_batch)

def validate(j, print_flag):
    if print_flag == 1:
        print("validating")
    out_preds = []
    for stmt in valid_batch[0]:
        out_preds.append(list(sess.run(y, {curr_in: [stmt]}))[0])
    OP = np.round(np.array(out_preds),3)
    if print_flag == 1:
        outs  = []
        for t in range(20):
            outs.append(OP[t])
            print (OP[t], valid_batch[1][t])
            #print(set(outs))
    correct_prediction = tf.equal(tf.argmax(out_pred, 1), tf.argmax(out_cat, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    Acc = sess.run(accuracy, feed_dict={out_pred: OP, out_cat: np.array(valid_batch[1])})    
    now = time.time()
    if print_flag == 1:
        print ("time :" , now - start, ":", "validation complete with", Acc, "accuracy after epoch", j )    
        print (" ")
    return Acc

sess = tf.Session()

key_list = ["cpu","apt","thank","_eoc_","print", "ram", "HD"]
num_of_cats = len(key_list)+1
hot_ind = list(range(num_of_cats))
cat_vects = sess.run(tf.one_hot(hot_ind, num_of_cats, 1))

prepared_data = get_vocab(datafile)
valid_data = get_vocab(validfile)

#### m = max number of characters per word
m = 20
  
vocab_processor = tf.contrib.learn.preprocessing.VocabularyProcessor(m, min_frequency = 10)

vocab_processor.fit(prepared_data + valid_data)

vocab_dict = vocab_processor.vocabulary_._mapping    

dict_len = len(vocab_dict)
print (dict_len, "words learned")

max_conv_length = max(len(stmt.split()) for stmt in prepared_data + valid_data)
max_conv_length = 200
        
print ("max utt length", max_conv_length)

curr_in = tf.placeholder(tf.float32)
out_cat = tf.placeholder(tf.float32)
out_pred = tf.placeholder(tf.float32)
A = tf.Variable(np.random.random_sample((m,num_of_cats)) + .1, dtype=tf.float32)
d = tf.Variable(np.random.random([1,num_of_cats]) + .1, dtype=tf.float32)
E = tf.constant(np.random.random_sample([1,max_conv_length]) + .1, dtype=tf.float32)
f = tf.constant(np.random.random_sample([1,m]) + .1, dtype=tf.float32)

y = tf.nn.softmax(tf.matmul(curr_in,A) + d)
#z = tf.matmul(curr_in,A) + b

cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=out_cat, logits=y)
#zcross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=out_pred, logits=z)

optimizer = tf.train.AdadeltaOptimizer()
train = optimizer.minimize(cross_entropy)

init = tf.global_variables_initializer()
sess.run(init)
#ztrain = optimizer.minimize(zcross_entropy)
print ("error defined")



Accs = []

validsize = 10
trainsize = 25

def make_valid_batch():
    with open (validfile, encoding ="utf8") as vdata:
        next(vdata)
        convos = [convo for convo in vdata]
        batch = random.sample(convos,validsize)
        now = time.time()
        print ("time:" , now - start, "- formatting validation batch")
        valid_batch = format_batch_data(prep_data_long(batch))
        return valid_batch
    vdata.close()

valid_batch = make_valid_batch()

with open (datafile, encoding ="utf8") as traindata:
    next(traindata)
    convos = [convo for convo in traindata]
    for k in range(100):
        batch = random.sample(convos,trainsize)
        now = time.time()
        print ("time:" , now - start, "- formatting training batch")
        train_batch = format_batch_data(prep_data_long(batch))
        now = time.time()
        print ("time:" , now - start, "- training")
        for p in range (1000):
            sess.run(train, feed_dict={curr_in: train_batch[0], out_cat: train_batch[1]})        
        if (k+1) % 2 == 0:
            Acc = validate(k,1)
        else:
            Acc = validate(k,0)
        if (k+1)%20 == 0:
            valid_batch = make_valid_batch()
        Accs.append(Acc)
        now = time.time()

Acc = validate(k,1)
Accs.append(Acc)
print (Accs)
    

plt.plot(Accs)
plt.show()
fig.savefig("Accuracies.png")
plt.close()
        
        


