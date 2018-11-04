# This is a VERY SIMPLE NLP constructed from UBUNTU corpus data.

# The progran predicts the category of respone to a given statement.
# categories are composed of (loosely) synonomious words:
# The default categories are softare, hardware, thanks and other.

# This nlp is based on ubuntu corpus data which consists of MULTI-USER,
# UNSTRUCTURED conversations. There is a large amount of randomnness in
# preducting the next statment.

# It isn't hard to structure conversations if the data set you generate 
# includes user IDs. 

# I have UNPLUBISHED solutions to the following issues... and more.

# Caterogies are not optimally defined.
# The number of categories is limited by construction and is easy to adjust
 
# Categories are defined by a set of key words and would perform better if 
# better defined. Simple expamples include:
    # Category key words can be editted through the variable key_list
    # Categories can be representd as context vectors in a multilayer network

# this network only considers the immediately previous statement
    #better results would be obtained by taking into account more history
    
# this network does not suggest a statement only a category
    # It would be easy to give a suggested statement given key words found

import tensorflow as tf

import numpy as np

import time

import matplotlib.pyplot as plt

import random

start = time.time()
datafile = "c:/users/g/desktop/data/train.csv"        

def get_stmt_cat(stmt):
    
    ### returns the statement category vector based on which category shows up FIRST in statement
    
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
    
    ### validation function, takes an epoch number (j) and print_flag
    ### uses global variables VS, VR
    
    if print_flag == 1:
        print("validating")
    out_preds = []
    for stmt in VS:
        out_preds.append(list(sess.run(y, {curr_in: [stmt]}))[0])
    OP = np.array(out_preds)
    if print_flag == 1:
        outs  = []
        for t in range(valid_print_size):
            outs.append(OP[t])
            rept = []
            for num in OP[t]:
                rept.append(float(f'{num:.2f}'))
            print (rept, VR[t])
        print ("")
    correct_prediction = tf.equal(tf.argmax(out_pred, 1), tf.argmax(out_cat, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    Acc = sess.run(accuracy, feed_dict={out_pred: OP, out_cat: VR})    
    now = time.time()
    if print_flag == 1:
        print ("time :" , now - start, ":", "validation complete with", Acc, "accuracy after", j, "epochs." )    
        print (" ")
    return Acc

def pad_stmt(stmt):
    
    ### forces stmt vectors to have uniform length.
    
    if len(stmt) > M:
        return np.array(stmt[:M])
    while len(stmt) < M:
        stmt.append(0)
    return np.array(stmt)

def make_stmts(convo):
    
    ### splits conversation string into user turns
    
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

def make_batch(preped_data, batch_size):
    
    ## formats data for training
    
    prepared_data = np.array(random.sample(preped_data, batch_size))    
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
    
    # prints with elapesed time
    
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

### number of examples to be printed after validation.
valid_print_size = 30

### extract conversation strings from data file
with open (datafile, encoding ="utf8") as traindata:
    next(traindata)
    total_convos = 0
    convos = [convo for convo in traindata]
  
### instantiate vocab processor and transform dataset
### Each statement is transformed into a vector of length m
vocab_processor = tf.contrib.learn.preprocessing.VocabularyProcessor(m, min_frequency = 1)
preped_data = list(vocab_processor.fit_transform(convos))
print (len(preped_data))
valid_data = []
for k in range(int(len(preped_data)/10)):
    valid_data.append(preped_data.pop(random.randrange(len(preped_data))))
print (len(preped_data))
#preped_data = prep_data[(len(prep_data)/10):]
vocab_dict = vocab_processor.vocabulary_._mapping  
dict_len = len(vocab_dict)

### These tokens are specific to the format of the Ubuntu Corpus
### and may be changed for other data sets.
user_change_tokens = ["__eot__", "__eou__,", "__eou__\"", "__eou__"]
transformed_tokens = [list(vocab_processor.transform([user_change_token]))[0][0] for user_change_token in user_change_tokens] 
transformed_keys = []
for cat in key_list:
    transformed_cat = [list(vocab_processor.transform([synonym]))[0][0] for synonym in cat]
    transformed_keys.append(transformed_cat)

print (transformed_keys)

### define variables and placeholders
curr_in = tf.placeholder(tf.float32)
out_cat = tf.placeholder(tf.float32)
out_pred = tf.placeholder(tf.float32)
A = tf.Variable(np.random.random_sample((M,num_of_cats)) + .1, dtype=tf.float32)
d = tf.Variable(np.random.random([1,num_of_cats]) + .1, dtype=tf.float32)

### define neural network
y = tf.nn.softmax(tf.matmul(curr_in,A)+d)

### define error and optimizer
cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=out_cat, logits=y)
optimizer = tf.train.AdadeltaOptimizer()
train = optimizer.minimize(cross_entropy)

### instantiate variables
init = tf.global_variables_initializer()
sess.run(init)

###
batch_size = 1000
epochs = 10000

### list of accuracies for reporting
Accs = []

### create training batch
newbatch = make_batch(preped_data, batch_size)
TS = newbatch[0]
TR = newbatch[1]

validbatch = make_batch(valid_data, batch_size)
VS = validbatch[0]
VR = validbatch[1]


### train loop
for k in range(epochs):
    print_w_time("beginning training")
    for j in range(batch_size):
        sess.run(train, feed_dict={curr_in: TS, out_cat: TR})
    print_w_time("making batch")
    
    Acc = validate(k,0)
    Accs.append(Acc)
    newbatch = make_batch(preped_data, batch_size)
    TS = newbatch[0]
    TR = newbatch[1]
    validbatch = make_batch(valid_data, batch_size)
    VS = validbatch[0]
    VR = validbatch[1]
    
    ### print validation results on regular intervals.
    if k%10 == 0:
        Acc = validate(k,1)
        Accs.append(Acc)
        fig = plt.figure()
        plt.plot(Accs)
        plt.show()
        fig.savefig("Accuracies.png")
        plt.close()
        
Acc = validate(k,1)
Accs.append(Acc)
fig = plt.figure()
plt.plot(Accs)
plt.show()
fig.savefig("Accuracies.png")
plt.close()        
        


