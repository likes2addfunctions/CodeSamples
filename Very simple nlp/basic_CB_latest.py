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

start = time.time()
datafile = "c:/users/g/desktop/data/train.csv"        

def get_stmt_cat(stmt):
    for k in range(num_of_cats-1):
        for synonym in (transformed_keys[k]):
                try:
                    if synonym > 1:
                        if stmt.index(synonym):
                            return cat_vects[k]
                except:
                    1
    else:
        return cat_vects[-1]

def validate(j, print_flag):
    if print_flag == 1:
        print("validating")
    out_preds = []
    for stmt in TS:
        out_preds.append(list(sess.run(y, {curr_in: [stmt]}))[0])
    OP = np.array(out_preds)
    if print_flag == 1:
        outs  = []
        for t in range(valid_print_size):
            outs.append(OP[t])
            rept = []
            for num in OP[t]:
                rept.append(float(f'{num:.2f}'))
            print ("p", rept, TR[t])
            
#            print (TS[t])
#            print (TR[t])
        print ("")
    correct_prediction = tf.equal(tf.argmax(out_pred, 1), tf.argmax(out_cat, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    Acc = sess.run(accuracy, feed_dict={out_pred: OP, out_cat: TR})    
    now = time.time()
    if print_flag == 1:
        print ("time :" , now - start, ":", "validation complete with", Acc, "accuracy after", j, "epochs." )    
        print (" ")
    return Acc

def pad_stmt(stmt):
    if len(stmt) > M:
        return np.array(stmt[:M])
    while len(stmt) < M:
        stmt.append(0)
    return np.array(stmt)

def make_stmts(convo):
    stmts = []
    last_stmt = []
    while max(convo) > 0:
        try:
            change_index = convo.index(transformed_tokens[0])
            stmts.append(pad_stmt(convo[:change_index]))
            convo = convo[change_index+1 :]
        except:
            last_stmt.append(convo[0])
            convo = convo[1:]
                
    stmts.append(pad_stmt(last_stmt))
    return stmts

def make_batch(preped_data):
    prepared_data = np.array(random.sample(preped_data, 1000))    
    trans_stmts = []
    for convo in prepared_data:
        stmts = make_stmts(convo.tolist())
        for x in stmts[:-1]:
            trans_stmts.append(x) 
            
    TS = trans_stmts
    #print(TS[0])
    TR = []
    for stmt in trans_stmts:
        TR.append(get_stmt_cat(stmt.tolist()))
    return [TS,TR]

def print_w_time(printstr):
    now = time.time()
    print ("time:" , now - start, "- " + printstr )

sess = tf.Session()

key_list = [["cpu", "processor", "print", "printer", "ram", "memory", "fan", "fans", "HD", "hard drive"],
            ["driver", "drivers", "apt", "apt-get", "update", "os", "operating system", "bios"],
            ["ty", "thank", "thanks","thank you", "bye", "later", "welcome", "your welcome", "you're welcome"]]
num_of_cats = len(key_list)+1
hot_ind = list(range(num_of_cats))
cat_vects = sess.run(tf.one_hot(hot_ind, num_of_cats, 1))

#### m = max number of tokens per conversation
m = 2000
#### M = max number of words per speaker turn
M = 50

###
valid_print_size = 30
  
vocab_processor = tf.contrib.learn.preprocessing.VocabularyProcessor(m, min_frequency = 1)

with open (datafile, encoding ="utf8") as traindata:
    next(traindata)
    total_convos = 0
    convos = [convo for convo in traindata]
    
preped_data = list(vocab_processor.fit_transform(convos))



user_change_tokens = ["__eot__", "__eou__,", "__eou__\"", "__eou__"]
transformed_tokens = [list(vocab_processor.transform([user_change_token]))[0][0] for user_change_token in user_change_tokens] 
transformed_keys = []
for cat in key_list:
    transformed_cat = [list(vocab_processor.transform([synonym]))[0][0] for synonym in cat]
    transformed_keys.append(transformed_cat)

print (transformed_keys)

newbatch = make_batch(preped_data)
TS = newbatch[0]
TR = newbatch[1]
vocab_dict = vocab_processor.vocabulary_._mapping    

dict_len = len(vocab_dict)

curr_in = tf.placeholder(tf.float32)
out_cat = tf.placeholder(tf.float32)
out_pred = tf.placeholder(tf.float32)
A = tf.Variable(np.random.random_sample((M,num_of_cats)) + .1, dtype=tf.float32)
d = tf.Variable(np.random.random([1,num_of_cats]) + .1, dtype=tf.float32)

y = tf.nn.softmax(tf.matmul(curr_in,A)+d)

cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=out_cat, logits=y)

optimizer = tf.train.AdadeltaOptimizer()
train = optimizer.minimize(cross_entropy)

init = tf.global_variables_initializer()
sess.run(init)

Accs = []
    
epochs = 500

for k in range(epochs):
    print_w_time("beginning training")
    for j in range(1000):
        sess.run(train, feed_dict={curr_in: TS, out_cat: TR})
    print_w_time("making batch")
    newbatch = make_batch(preped_data)
    TS = newbatch[0]
    TR = newbatch[1]
    if k%10 == 0:
        Acc = validate(k,1)
        Accs.append(Acc)
        ps = str(k) + " epochs complete, making new batch"
        print_w_time(ps)
        fig = plt.figure()
        plt.plot(Accs)
        plt.show()
        fig.savefig("Accuracies.png")
        plt.close()
        
Acc = validate(k,1)
Accs.append(Acc)
print (Accs)
fig = plt.figure()
plt.plot(Accs)
plt.show()
fig.savefig("Accuracies.png")
plt.close()        
        


