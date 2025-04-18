# -*- coding: utf-8 -*-
"""Practical Project 2 - Classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12Lu1acPBzu96s3FG6rKUZ7n8orsyue43

# **Practical Project 2 - Classification**

> Nome: Tiago Miguel Fernandes Marques | Nº: 51653 | Curso: IACD | Aprendizagem Computacional | UBI
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from tensorflow.keras.layers import Dense
from sklearn.metrics import roc_curve, auc
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from sklearn.preprocessing import label_binarize
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split

# Leitura dos ficheiros

ficheiro_train = "mnist_train.csv"
ficheiro_test = "mnist_test.csv"

df_train = pd.read_csv(ficheiro_train)
df_test = pd.read_csv(ficheiro_test)

print("Ficheiro train.csv: ")
print(df_train.head())
print("\n")
print("Ficheiro test.csv: ")
print(df_test.head())

# Verificar valores Nulls

print("Valores Nulls treino.csv:\n")
print(df_train.isna().sum())
print("\n")
print("Valores Nulls teste.csv:\n")
print(df_test.isna().sum())

# Defenição de variáveis

x_train = df_train.drop(["label"], axis=1)
y_train = df_train["label"].array.reshape(-1,1)

x_test = df_test.drop(["label"], axis=1)
y_test = df_test["label"].array.reshape(-1,1)

# Mostrar uma imagem do csv

img = x_train.iloc[1,:].array.reshape(28,28)
plt.imshow(img)
plt.axis("off")
plt.show()

# Verificar númerod e variáveis

className = df_train["label"].unique()
numberOfClass = len(className)
print("NumberOfClass: ",numberOfClass)

# Normalizar variáveis

x_train_normalizado = x_train / 255
x_test_normalizado = x_test / 255

# Transformar variável dependente (one-hot encoding)

lb = LabelBinarizer()
y_train = lb.fit_transform(y_train)
y_test = lb.transform(y_test)

# Rede Neuronal

def rede_neuronal(x_train_normalizado, y_train, x_test_normalizado, y_test):

    model = Sequential()

    model.add(Dense(64, input_shape=(784,), activation='sigmoid'))

    model.add(Dense(32, activation='sigmoid'))

    model.add(Dense(10, activation='softmax'))

    optimizer = Adam(learning_rate = 0.001)

    model.compile(optimizer = optimizer, loss='categorical_crossentropy', metrics=['accuracy'])


    hist = model.fit(x_train_normalizado, y_train, epochs=20, batch_size=32, validation_data=(x_test_normalizado, y_test))
    print(hist)

    test_loss, test_acc = model.evaluate(x_test, y_test)

    print(hist.history.keys())

    plt.plot(hist.history["loss"],label = "Train Loss")
    plt.plot(hist.history["val_loss"],label="Validation Loss")
    plt.legend()
    plt.show()

    plt.plot(hist.history["accuracy"],label = "Train Accuracy")
    plt.plot(hist.history["val_accuracy"],label="Validation Accuracy")
    plt.legend()
    plt.show()


    y_pred = model.predict(x_test_normalizado)


    y_test_bin = label_binarize(y_test, classes=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    n_classes = y_test_bin.shape[1]


    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_pred[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])


    plt.figure()
    colors = ['aqua', 'darkorange', 'cornflowerblue', 'red', 'green', 'purple', 'brown', 'pink', 'gray', 'blue']
    for i in range(n_classes):
        plt.plot(fpr[i], tpr[i], color=colors[i], lw=2, label='Classe {0} (área = {1:0.2f})'.format(i, roc_auc[i]))

    plt.plot([0, 1], [0, 1], 'k--', lw=2)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('True Postive Rate')
    plt.ylabel('False Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.show()


rede_neuronal(x_train_normalizado, y_train, x_test_normalizado, y_test)

# Processamento do PCA para verificar a imagem

def aplicar_pca(x_train, variancia_desejada=0.95):
    pca = PCA(n_components=variancia_desejada)
    x_train_pca = pca.fit_transform(x_train)
    return pca, x_train_pca

def reconstruir_e_visualizar_imagem(pca, x_train_pca, indice_imagem=1):

    x_train_reconstruido = pca.inverse_transform(x_train_pca)
    img_reconstruida = x_train_reconstruido[indice_imagem].reshape(28, 28)

    plt.imshow(img_reconstruida)
    plt.axis("off")
    plt.show()


pca, x_train_reduzido = aplicar_pca(x_train_normalizado, variancia_desejada=0.95)
x_test_reduzido = aplicar_pca(x_test_normalizado, variancia_desejada=0.95)

reconstruir_e_visualizar_imagem(pca, x_train_reduzido, indice_imagem=1)

# Rede Neuronal após o processamento do PCA

def rede_neuronal(x_train_normalizado, y_train, x_test_normalizado, y_test):

    pca = PCA(0.95)
    x_train_pca = pca.fit_transform(x_train_normalizado)
    x_test_pca = pca.transform(x_test_normalizado)

    model = Sequential()

    model.add(Dense(64, input_shape=(x_train_pca.shape[1],), activation='sigmoid'))
    model.add(Dense(32, activation='sigmoid'))
    model.add(Dense(10, activation='softmax'))

    optimizer = Adam(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    hist = model.fit(x_train_pca, y_train, epochs=20, batch_size=32, validation_data=(x_test_pca, y_test))
    print(hist)

    test_loss, test_acc = model.evaluate(x_test_pca, y_test)
    print(f'Test Loss: {test_loss}, Test Accuracy: {test_acc}')

    print(hist.history.keys())

    plt.plot(hist.history["loss"], label="Train Loss")
    plt.plot(hist.history["val_loss"], label="Validation Loss")
    plt.legend()
    plt.show()

    plt.plot(hist.history["accuracy"], label="Train Accuracy")
    plt.plot(hist.history["val_accuracy"], label="Validation Accuracy")
    plt.legend()
    plt.show()

    y_pred = model.predict(x_test_pca)

    y_test_bin = label_binarize(y_test, classes=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    n_classes = y_test_bin.shape[1]

    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_pred[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    plt.figure()
    colors = ['aqua', 'darkorange', 'cornflowerblue', 'red', 'green', 'purple', 'brown', 'pink', 'gray', 'blue']
    for i in range(n_classes):
        plt.plot(fpr[i], tpr[i], color=colors[i], lw=2, label='Classe {0} (área = {1:0.2f})'.format(i, roc_auc[i]))

    plt.plot([0, 1], [0, 1], 'k--', lw=2)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('True Postive Rate')
    plt.ylabel('False Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.show()


rede_neuronal(x_train_normalizado, y_train, x_test_normalizado, y_test)