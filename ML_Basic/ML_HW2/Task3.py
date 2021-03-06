import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

class NN:
    def __init__(self, images, labels):
        self.images = images
        self.labels = labels
        
    def accuracy(self, predictions, labels):
        return (100.0 * np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1)) / predictions.shape[0])

    def train_data(self, images_val, labels_val, images_test, labels_test, i):
        # Place the input image and corresponding label into the placeholders
        X = tf.placeholder(tf.float32, [None, 784], name='image')
        Y = tf.placeholder(tf.float32, [None, 10], name='label')
        
        # Set up the 4 weight matrices: bias/input->hidden unit, bias/hidden unit->output
        b1 = tf.Variable(tf.zeros([i]), name='weight_b2h')
        w1 = tf.Variable(tf.truncated_normal([784, i], stddev=0.1), name='weight_i2h')
        b2 = tf.Variable(tf.zeros([10]), name='weight_b2o')
        w2 = tf.Variable(tf.truncated_normal([i, 10], stddev=0.1), name='weight_h2o')
        
        # Set up the hyperparameters
        learning_rate = 0.05
        momentum = 0.4
        training_epochs = 1000

        # Set up 2 math operations: input -> hidden unit, hidden unit -> output
        layer1_result = tf.nn.relu(tf.add(tf.matmul(X, w1), b1))
        logits = tf.add(tf.matmul(layer1_result, w2), b2)
        # start to train the model, maximize the log-likelihood
        cost_batch = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=Y)
        cost = tf.reduce_mean(cost_batch)

        optimizer = tf.train.MomentumOptimizer(learning_rate, momentum)
        train_step = optimizer.minimize(cost)
        
        # Compute the log-likelihood of training data and validation data
        log_likelihood_train = -tf.reduce_mean(cost_batch)
        layer1_result_valid = tf.nn.relu(tf.add(tf.matmul(images_val, w1), b1))
        logits_valid = tf.add(tf.matmul(layer1_result_valid, w2), b2)
        log_likelihood_valid = -tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits_valid, labels=labels_val))

        # Calculate the predition with softmax
        train_predition = tf.nn.softmax(logits)
        valid_prediction = tf.nn.softmax(logits_valid)
        layer1_result_valid = tf.nn.relu(tf.add(tf.matmul(images_test, w1), b1))
        logits_test = tf.add(tf.matmul(layer1_result_valid, w2), b2)
        test_prediction = tf.nn.softmax(logits_test)

        sess = tf.InteractiveSession()
        init = tf.initialize_all_variables()
        sess.run(init)

        result = np.zeros(shape=(5, training_epochs))
        log_likelihood_max = -float("inf")
        lilelihood_overfitting = False
        lilelihood_oscillation = 0

        filename1 = 'err_early_' + repr(i)
        filename2 = 'log_early_' + repr(i)
        filename3 = 'err_' + repr(i)
        filename4 = 'log_' + repr(i)

       
        print "Number of hidden units:%04d" % i
        for epoch in range(training_epochs):
            for i in xrange(300):
                batch_xs = self.images[i * 50: (i + 1) * 50]
                batch_ys = self.labels[i * 50: (i + 1) * 50]
                cost_np, _ = sess.run([cost,train_step], feed_dict={X: batch_xs, Y: batch_ys})

            likelihood_train, predictions_train = sess.run([log_likelihood_train, train_predition], 
                feed_dict={X: self.images, Y:self.labels})
            accuracy_train = self.accuracy(predictions_train, self.labels)
            likelihood_val = log_likelihood_valid.eval()
            accuracy_val = self.accuracy(valid_prediction.eval(), labels_val)

            result[0, epoch] = epoch + 1
            result[1, epoch] = (100 - accuracy_val) * 1000 / 100
            result[2, epoch] = (100 - accuracy_train) * 15000 / 100
            result[3, epoch] = likelihood_train
            result[4, epoch] = likelihood_val  

            if(epoch % 50 == 0):
                print ("Epoch:%04d, Train Accuracy=%0.4f, Eval Accuracy=%0.4f, log_likelyhood_train:%0.6f, log_likelyhood_val:%0.6f" % 
                    (epoch+1, accuracy_train, accuracy_val, likelihood_train, likelihood_val))

            # When the log-likelihood reaches at maximum, use the early stopping to stop the training
            if(log_likelihood_max < likelihood_val):
                log_likelihood_max = likelihood_val
                lilelihood_oscillation = 0
            elif(log_likelihood_max - likelihood_val > 0):
	        	lilelihood_oscillation += 1

            if(lilelihood_overfitting == False):
	        	if(lilelihood_oscillation >= 15):
	        	    lilelihood_overfitting = True
	        	    print "Likelihood overfitting"
	        	    print ("Epoch:%04d, Train Accuracy=%0.4f, Eval Accuracy=%0.4f, log_likelyhood_train:%0.6f, log_likelyhood_val:%0.6f" % 
		               (epoch+1, accuracy_train, accuracy_val, likelihood_train, likelihood_val))
	        	    accuracy_test = self.accuracy(test_prediction.eval(), labels_test)
	        	    print ("Test Accuracy=%0.4f" % (accuracy_test))
	        	    print 'Test_Error: ' + repr((100 - accuracy_test) * 2720 / 100)


	        	    plt.plot(result[0,:epoch], result[1,:epoch],'b-', label='Validation Error')
	        	    plt.plot(result[0,:epoch], result[2,:epoch],'r-', label = 'Training Error')
	        	    plt.legend(loc = 'upper right', numpoints = 1)
	        	    plt.xlabel('Number of Epochs')
	        	    plt.ylabel('Number of Errors')
	        	    plt.savefig(filename1)
	        	    plt.close()
                    	        	    
	        	    plt.plot(result[0,:epoch], result[3,:epoch],'b-', label = 'Log-likelihood_Training')
	        	    plt.plot(result[0,:epoch], result[4,:epoch],'r-', label = 'Log-likelihood_Validation')
	        	    plt.legend(loc = 'right', numpoints = 1)
	        	    plt.xlabel('Number of Epochs')
	        	    plt.ylabel('Log-likelihood')
	        	    plt.savefig(filename2)
	        	    plt.close()   

        # Compute the test errors after the complete training process
        print "Complete:"
        accuracy_test = self.accuracy(test_prediction.eval(), labels_test)
        print ("Test Accuracy=%0.4f" % (accuracy_test))
        print 'Test_Error: ' + repr((100 - accuracy_test) * 2720 / 100)

    	plt.plot(result[0,:], result[1,:],'b-', label='Validation Error')
    	plt.plot(result[0,:], result[2,:],'r-', label = 'Training Error')
    	plt.legend(loc = 'upper right', numpoints = 1)
    	plt.xlabel('Number of Epochs')
    	plt.ylabel('Number of Errors')
        plt.savefig(filename3)
        plt.close()

    	plt.plot(result[0,:], result[3,:],'b-', label = 'Log-likelihood_Training')
    	plt.plot(result[0,:], result[4,:],'r-', label = 'Log-likelihood_Validation')
    	plt.legend(loc = 'right', numpoints = 1)
    	plt.xlabel('Number of Epochs')
    	plt.ylabel('Log-likelihood')
        plt.savefig(filename4)
        plt.close()
        
    def constru_NN(self, images_val, labels_val, images_test, labels_test):
        # Try different number of hidden units
        num_hidden_units = [100, 500, 1000]
        for i in num_hidden_units:
            self.train_data(images_val, labels_val, images_test, labels_test, i)

        
with np.load("notMNIST.npz") as data:
    images , labels = data["images"], data["labels"]

# Reshape the imput data 
images_in = images.reshape(784,18720).T.astype("float32")
labels_in = np.zeros([18720,10]).astype("float32")
index = 0
for i in labels:
    labels_in[index, i] = 1
    index +=1

cnn = NN(images_in[:15000,:]/255, labels_in[:15000,:])
cnn.constru_NN(images_in[15000:16000,:]/255, labels_in[15000:16000,:], images_in[16000:18720,:]/255, labels_in[16000:18720,:])
