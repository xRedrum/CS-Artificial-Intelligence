import pandas as pd
import numpy as np

def preprocess():
    iris_data = pd.read_csv("C:/Users/xbaaa/Documents/My Documents/CS131/HW6/ANN - Iris data.txt", header=None)
    iris_data_values=iris_data.values
    Y_type = iris_data_values[:, 4]
    X = iris_data_values[:, 0:4]
    length_data=len(Y_type)
    Y = np.zeros([length_data, 3])
    a=np.array([1, 0, 0])
    b=np.array([0, 1, 0])
    c=np.array([0, 0, 1])
    for i in range(length_data):
        if Y_type[i] == 'Iris-setosa':
            Y[i] = a
        elif Y_type[i] == 'Iris-versicolor':
            Y[i] = b
        elif Y_type[i] == 'Iris-virginica':
            Y[i] = c

    a=len(X[0])
    b=len(Y[0])
    c=len(X)
    d=len(Y)

    x_test = np.zeros([a, int(c * 0.2)])
    x_train = np.zeros([a, int(c * 0.6)])
    y_test = np.zeros([b, int(d * 0.2)])
    y_train = np.zeros([b, int(d * 0.6)])
    x_validate=np.zeros([a, int(c * 0.2)])
    y_validate=np.zeros([b, int(d * 0.2)])
    test_temp = 0
    train_temp = 0
    x_y = 0
    for i in range(0, len(X)):
        if i % 5 == 0:
            x_test[:, test_temp] = X[i]
            y_test[:, test_temp] = Y[i]
            test_temp += 1
        elif i % 5 == 1:
            x_validate[:, x_y] = X[i]
            y_validate[:, x_y] = Y[i]
            x_y += 1
        else:
            x_train[:, train_temp] = X[i]
            y_train[:, train_temp] = Y[i]
            train_temp += 1
    return x_train, x_test, y_train, y_test, x_validate, y_validate


def forward(W1, B1, W2, B2, X):

    W_X=np.dot(W1, X)
    Z1 = B1 + W_X
    A1 = np.maximum(Z1, 0)
    Z2 = B2 + W2.dot(A1)
    sum_Z2=sum(np.exp(Z2))
    A2 = np.exp(Z2) / sum_Z2
    return Z1, A1, Z2, A2


def back(Z1, A1, A2, W2, X, Y):

    leng=X.shape[1]
    A2_Y=A2 - Y
    dW2 = A2_Y.dot(A1.T) / leng
    dB2 = np.sum(A2_Y) / leng
    Z1 = Z1 > 0
    dZ1 = W2.T.dot(A2_Y) * Z1
    dW1 = dZ1.dot(X.T) / leng
    dB1 = np.sum(dZ1) / leng
    return dW1, dB1, dW2, dB2


class ANN():


    def __init__(self, step, epoch, x_train, y_train, x_test, y_test,x_validate, y_validate):

        self.w1 = np.random.rand(4, 4)
        self.b1 = np.random.rand(4, 1)
        self.w2 = np.random.rand(3, 4)
        self.b2 = np.random.rand(3, 1)
        self.step=step
        self.epoch=epoch
        self.x_train=x_train
        self.y_train=y_train
        self.x_test=x_test
        self.y_test=y_test
        self.x_validate=x_validate
        self.y_validate=y_validate

    def train(self):
        for i in range(self.epoch):
            Z1, A1, Z2, A2 = forward(self.w1, self.b1, self.w2, self.b2, self.x_train)
            self.dw1, self.db1, self.dw2, self.db2 = back(Z1, A1, A2, self.w2, self.x_train, self.y_train)
            self.w1 -= self.dw1 * self.step
            self.b1 -= self.db1 * self.step
            self.w2 -= self.dw2 * self.step
            self.b2 -= self.db2 * self.step
            self.validation(self.x_validate, self.y_validate)

            count1 = 0
            for i in range(len(self.x_test[0])):
                x_curr = np.zeros([4, 1])
                x_curr[:, 0] = self.x_test[:, i]
                pre = self.predict(x_curr)
                r = -1
                c = -1
                for j in range(len(self.y_test[:, i])):
                    if self.y_test[:, i][j] > c:
                        r = j
                        c = self.y_test[:, i][j]
                if r == pre:
                    count1 += 1
            print("Current Accuracy : ", round(count1 / len(self.x_test[0])))

    def validation(self,x, y):
        c = 0
        for i in range(len(x[0])):
            pre = max(y[:, i])
            cor = np.zeros([4, 1])
            cor[:, 0] = x[:, i]
            if pre == self.predict(cor):
                c += 1
        print("Validation : ", round(c / len(x[0]), 1))


    def predict(self, X):
        Z1, A1, Z2, A2 = forward(self.w1, self.b1, self.w2, self.b2, X)
        r = -1
        c= -1
        for i in range(len(A2)):
            if A2[i] > c:
                r = i
                c = A2[i]
        return r

if __name__ == '__main__':
    x_train, x_test, y_train, y_test,x_validate, y_validate= preprocess()
    ann = ANN(0.1, 1000, x_train, y_train, x_test, y_test,x_validate, y_validate)
    print("---------------Start Training---------------")
    ann.train()
    print("----------------------------------Training Completed----------------------------------")

    print("---------------Manual Input and Response with a Predicted Class of Iris---------------")
    while True:
        print("Now classify the plants based on user input")
        print("Please follow the instruction")
        print("If you want to end program, input stop")
        sepal_length = input("Input sepal length in cm: ")
        if sepal_length == 'stop':
            break
        sepal_width = input("Input sepal width in cm: ")
        if sepal_width == 'stop':
            break
        petal_length = input("Input petal length in cm: ")
        if petal_length == 'stop':
            break
        petal_width = input("Input petal width in cm: ")
        if petal_width == 'stop':
            break
        predicted_data = np.reshape([float(sepal_length), float(sepal_width), float(petal_length), float(petal_width)],
                                    (-1, 1))
        Iris = ann.predict(predicted_data)
        if Iris == 0:
            print("Predicted result : Iris-setosa")
        elif Iris == 1:
            print("Predicted result : Iris-versicolo")
        elif Iris == 2:
            print("Predicted result : Iris-virginica")