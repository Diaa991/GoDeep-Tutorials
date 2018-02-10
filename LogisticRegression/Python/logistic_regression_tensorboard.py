import tensorflow as tf
import tensorflow.examples.tutorials.mnist.input_data as input_data
from datetime import datetime

mnist = input_data.read_data_sets('MNIST_data/', one_hot=True)

m,n = 28,28

n_input = m*n # 28x28 images
n_output = 10 # Classes

# Training a Logistic classifier: Xw + b = y
X = tf.placeholder(tf.float32,shape=[None,n_input],name="X") # input type and shape
W = tf.get_variable(name="Weights",shape=[784, 10],
                    initializer=tf.random_normal_initializer(stddev=0.3))
b = tf.Variable(tf.zeros([10]), name='bias')

#placeholder for gt values
y_ = tf.placeholder(tf.float32,[None,10])

with tf.name_scope("XW"):
    XW = tf.matmul(X,W)

# compute scores
y = XW + b

# XEntropy and loss functions definition
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y,labels=y_))


correct_prediction = tf.equal(tf.argmax(y,1),tf.arg_max(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

# Use GD to minimise loss
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.003)
train_step = optimizer.minimize(cross_entropy)

num_epochs = 100
batch_size = 100


init = tf.global_variables_initializer()

#Adding summaries
xentropy_summary = tf.summary.scalar(name='Xentropy',tensor=cross_entropy)
accuracy_summary = tf.summary.scalar(name="accuracy",tensor=accuracy)

with tf.Session(config=tf.ConfigProto(allow_soft_placement=True)) as session:
    session.run(init)

    # Training the model
    log_path_train = 'logdir' + '/train_{}'.format(datetime.utcnow().strftime("%Y%m%d%H%M%S"))
    train_writer = tf.summary.FileWriter(log_path_train, session.graph)
    summaries_train = tf.summary.merge_all()

    n_batches = int(mnist.train.num_examples / batch_size)

    for epoch_i in range(num_epochs):

        for batch_index in range(n_batches):

            batch_x, batch_y = mnist.train.next_batch(batch_size=batch_size)
            train_data = {X: batch_x, y_: batch_y}

            session.run(train_step, feed_dict=train_data)

            _, summary_str, acc, cross = session.run(
                [train_step, summaries_train, accuracy, cross_entropy],
                feed_dict=train_data,
            )


            if batch_index % 10 == 0: #Write every 10 batches
                step = epoch_i * n_batches + batch_index
                train_writer.add_summary(summary_str,global_step=step)
                print("Epoch: {0} Loss: {1}".format(epoch_i, cross))


