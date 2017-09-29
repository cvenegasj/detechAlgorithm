from __future__ import print_function

import tensorflow as tf
from tensorflow.contrib import rnn
import detech_data as dd

from matplotlib import pyplot as plt
import numpy as np


detech = dd.read_data_sets('/home/bregy/Desktop/detechAlgorithm/core/predictor/model/testOut')

learning_rate = 0.001
training_steps = 5000
batch_size = 100
display_step = 100

num_input = 80 # Por definir, depende de la forma de la imagen
timesteps = 60
num_hidden = 120
num_classes = 4 #Etapas de preulcera

X = tf.placeholder("float", [None, timesteps, num_input])
Y = tf.placeholder("float", [None, num_classes])

weights = {'out': tf.Variable(tf.random_normal([2*num_hidden, num_classes]))}
biases = {'out': tf.Variable(tf.random_normal([num_classes]))}


def BiRNN(x, weights, biases):
    x = tf.unstack(x, timesteps, 1)

    lstm_fw_cell = rnn.BasicLSTMCell(num_hidden, forget_bias=1.0)
    lstm_bw_cell = rnn.BasicLSTMCell(num_hidden, forget_bias=1.0)

    outputs, _, _ = rnn.static_bidirectional_rnn(lstm_fw_cell, lstm_bw_cell, x, dtype=tf.float32)


    return tf.matmul(outputs[-1], weights['out']) + biases['out']

logits = BiRNN(X, weights, biases)
prediction = tf.nn.softmax(logits)

loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=Y))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
train_op = optimizer.minimize(loss_op)

correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

init = tf.global_variables_initializer()

sess = tf.Session()

sess.run(init)

errorArr = []
accuracyArr = []

'''======================== TRAIN ========================'''


for step in range(1, training_steps+1):
    batch_x, batch_y = detech.next_batch_one_hot(batch_size)

    batch_x = batch_x.reshape((batch_size, timesteps, num_input))

    sess.run(train_op, feed_dict={X: batch_x, Y: batch_y})
    if step % display_step == 0 or step == 1:

        loss, acc = sess.run([loss_op, accuracy], feed_dict={X: batch_x, Y: batch_y})
        errorArr.append(loss)
        accuracyArr.append(acc)
        print("Step " + str(step) + ", Minibatch Loss= " + "{:.4f}".format(loss) + ", Training Accuracy= " + "{:.3f}".format(acc))

plt.plot(np.arange(len(errorArr)), errorArr, 'r', np.arange(len(accuracyArr)), accuracyArr, 'b')
plt.show()

print("Optimization Finished!")



'''======================== TEST ========================'''

test_x, test_y = detech.get_test_data()

print(sess.run(prediction, feed_dict={X: test_x, Y: test_y}))
