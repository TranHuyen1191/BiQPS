import tensorflow as tf
from tensorflow.contrib import rnn
import pdb
from tensorflow.python.ops.rnn import bidirectional_dynamic_rnn as bi_rnn
import os
import warnings
warnings.filterwarnings("ignore") 

class calLocalComp(object):
    def __init__(self):
        learning_rate = 0.01
        num_hidden  = 5
        num_classes = 1
        num_input   = 6
        keep_rate_DROPOUT = 1
        self.X = tf.placeholder("float", [1, None, num_input])
        self.Y = tf.placeholder("float", [None, num_classes])
        # Define weights
        self.weights = {
            'out': tf.Variable(tf.random_normal([num_hidden, num_classes]))
        }
        self.biases = {
            'out': tf.Variable(tf.random_normal([num_classes]))
        }
        self.lstm_fw_cell = rnn.BasicLSTMCell(num_hidden, forget_bias=1.0,reuse=False)
        self.lstm_fw_cell = rnn.DropoutWrapper(self.lstm_fw_cell,input_keep_prob=keep_rate_DROPOUT, output_keep_prob=keep_rate_DROPOUT, state_keep_prob=keep_rate_DROPOUT)
        # Backward direction cell
        self.lstm_bw_cell = rnn.BasicLSTMCell(num_hidden, forget_bias=1.0,reuse=False)
        self.lstm_bw_cell = rnn.DropoutWrapper(self.lstm_bw_cell,input_keep_prob=keep_rate_DROPOUT, output_keep_prob=keep_rate_DROPOUT, state_keep_prob=keep_rate_DROPOUT)
        # Get lstm cell output
        self.LSTM_outputs, _ = bi_rnn(self.lstm_fw_cell, self.lstm_bw_cell, self.X,
                            dtype=tf.float32,scope="bidirectional_rnn") 
        #Attention
        fw_outputs, bw_outputs = self.LSTM_outputs #fw_o and bw_o :(batch_size,windowSize,num_hidden)(76x412x5)
        Hidden_fw_bw = fw_outputs+bw_outputs # (batch_size,windowSize,num_hidden)
        Hidden_fw_bw_t = tf.transpose(Hidden_fw_bw,[0,2,1]) # Doi vi tri cot 2 cho 1: (batch_size,num_hidden,windowSize)
        Hidden_fw_bw_2D = tf.reshape(Hidden_fw_bw,[-1,num_hidden]) # (batch_size*windowSize,num_hidden)
        M=tf.tanh(Hidden_fw_bw_2D) #(batch_size*windowSize,num_hidden)
        W= tf.Variable(tf.random_normal([num_hidden])) #(1,num_hidden)
        W_t=tf.reshape(W,[-1,1]) #(num_hidden,1)
        MxW = tf.matmul(M,W_t) #(batch_size*windowSize,num_hidden)*(num_hidden,1) =  (batch_size*windowSize,1)
        MxW_3D = tf.reshape(MxW,[1,-1,1]) #(batch_size,windowSize,1)
        self.alpha_3D = tf.nn.softmax(MxW_3D,axis=1) # (batch_size,windowSize,1)
        r=tf.matmul(Hidden_fw_bw_t,self.alpha_3D) #(batch_size,num_hidden,windowSize)* (batch_size,windowSize,1) = (batch_size,num_hidden,1)
        r= tf.reshape(r,[-1,num_hidden]) # (batch_size,num_hidden)
        self.h_star = tf.tanh(r) # (batch_size,num_hidden)
        prediction = tf.matmul(self.h_star, self.weights['out']) + self.biases['out']

        self.Prediction_MOS = tf.add(tf.multiply(prediction, 4), 1) 
        self.Label_MOS = tf.add(tf.multiply(self.Y, 4), 1)
        LOSS = tf.sqrt(tf.reduce_mean(tf.square(tf.subtract(self.Prediction_MOS, self.Label_MOS))))
        PCC = tf.contrib.metrics.streaming_pearson_correlation(labels=self.Prediction_MOS, predictions=self.Label_MOS, name='pearson_r')
        optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
        train_op = optimizer.minimize(LOSS)
        init = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
        self.saverModel = tf.train.Saver()

    def _loadModel(self,step,idx_Test):    
        with tf.Session() as self.sess:
            self.sess = tf.Session()
            LSTMfile = "Model"+str(step)+"_"+str(idx_Test)+".ckpt"
            dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"LSTM"))
            print(dir_path)
            print(os.path.join(dir_path,LSTMfile))
            self.saverModel.restore(self.sess,os.path.join(dir_path,LSTMfile))
    
    def _predict(self,input,label):
        tempInst,tempsub,alpha_3D = self.sess.run([self.Prediction_MOS,self.Label_MOS,self.alpha_3D], feed_dict = {self.X: input, self.Y: label}) ## Min and Max to 5
        instWQ    = max(min(tempInst[0],5),1)
        subWQ    = max(min(tempsub[0],5),1)
        return instWQ
    def _delete(self):
        pdb.set_trace()
        #del "bidirectional_rnn/fw/basic_lstm_cell/kernel"

