# -*- coding: utf-8 -*-
"""
Contains the imports and functions used by a variety of scripts
Created on Mon July 29 09:05:37 2019
@author: Mutegeki Ronald - murogive@gmail.com - iSPL / KNU
"""

# Importing tensorflow
import tensorflow as tf

# Import Keras
from keras import backend as K
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import LSTM, TimeDistributed, Conv1D, MaxPooling1D, Flatten
from keras.layers.core import Dense, Dropout
from keras.models import Sequential
from keras.models import load_model

# Import support libraries
from sklearn import metrics
from sklearn.model_selection import train_test_split
import datetime
import os
import matplotlib.pyplot as plt
# To create nicer plots
import seaborn as sns
import numpy as np
# To measure time
import time
import pandas as pd
from pywt import dwt  # For signal processing
from scipy import signal  # For signal processing
from skimage.transform import downscale_local_mean  # For Augmentation
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels

# Common Variables used
# ...


# Utility function to print the confusion matrix
def confusion_m(Y_true, Y_pred, activities):
    Y_true = pd.Series([activities[y] for y in np.argmax(Y_true, axis=1)])
    Y_pred = pd.Series([activities[y] for y in np.argmax(Y_pred, axis=1)])

    return pd.crosstab(Y_true, Y_pred, rownames=['True'], colnames=['Pred'])


# Utility function to read the data from csv file
def _read_csv(filename):
    return pd.read_csv(filename, delim_whitespace=True, header=None)


def load_dataset(data_path, delimiter=",", n_signals=6, n_timesteps=128):
    """
    Loads any data row by row and the data file contains an array 
    of the shape (n_examples, (signals, time_steps))
    with flattened features that are organized by signal type
    :param data_path: Path to dataset
    :param delimiter: Defaults to "," that separates the strings of the data.
    :param n_signals: The number of signals acc x, y, z and gyro x, y, z
    :param n_timesteps: Based on the sampling rate, how many samples for each window
    :return data_array: a dataset (n_examples, time_steps, signals)
    """
    with open(data_path) as file:
        # Read dataset from disk
        data_array = np.loadtxt(data_path, delimiter=delimiter)

    return np.transpose(data_array.reshape((len(data_array), n_signals, -1)), (0, 2, 1))


def load_signals(folder, subset, signals):
    signals_data = []

    for signal in signals:
        filename = f'{folder}/{subset}/Inertial Signals/{signal}_{subset}.txt'
        signals_data.append(
            _read_csv(filename).values
        )

    # Transpose is used to change the dimensionality of the output,
    # aggregating the signals by combination of sample/timestep.
    # Resultant shape is (7352 train/2947 test samples, 128 timesteps, 9 signals)
    return np.transpose(signals_data, (1, 2, 0))


# Label loader for normal dataset
def load_labels(label_path, delimiter=","):
    with open(label_path, 'rb') as file:
        # Read labels from disk, dealing with text file's syntax
        y_ = np.loadtxt(label_path, delimiter=delimiter)
    return y_


# Alternative label loader for UCI dataset
def load_y(label_path, subset):
    """
    We are trying to predict  an integer, from 1 to 6,
    that represents a human activity. We return a binary representation of
    every sample objective as a 6 bits vector using One Hot Encoding
    (https://pandas.pydata.org/pandas-docs/stable/generated/pandas.get_dummies.html)
    """
    filename = f'{label_path}/{subset}/y_{subset}.txt'
    y = _read_csv(filename)[0]

    return pd.get_dummies(y).as_matrix()


# Utility function to count the number of classes
def _count_classes(y):
    return len(set([tuple(category) for category in y]))


# Process Raw data and return corresponding fourier transformed data input(values) is the same as XFfg/a or YFfg
# Retrieved update from https://stackoverflow.com/questions/31101987/different-spectrogram-between-matlab-and-python
def stft(dataset):
    # Fast Fourier Transform, STFT, for this window.
    # Number of sample points
    fs = 50  # sampling frequency, Fs = 50Hz = 1/2ns (N)
    # Number of elements the window must have
    n_window = dataset.shape[1]
    # The hanning window
    window = np.hanning(n_window)
    nfft = max(128, n_window)
    # We use a 50% overlap
    noverlap = 0.5 * n_window

    # Create a holder for our feature data
    feature_data = []
    # let's loop through the dataset
    for example in range(dataset.shape[0]):
        features = []
        for axis in range(dataset.shape[2]):
            sxx = dataset[example][:, axis]

            # Our feature extractor
            f, t, sx = signal.spectrogram(sxx, fs=fs, nfft=nfft, window=window, noverlap=noverlap)

            features.append(sx)
        feature_data.append(np.ravel(features))

    return np.array(feature_data)  # Returns a feature extracted dataset


# For now, let's just return the original dataset
def wavelet(dataset):
    """
    Single level Discrete Wavelet Transform.
    :param dataset: Raw data with corresponding sensors and signals
    :return feature_data: Feature extracted dataset that combines features for all inputs
    """
    # Create a holder for our feature data
    feature_data = []
    # let's loop through the dataset
    for example in range(dataset.shape[0]):
        features = []
        for axis in range(dataset.shape[2]):
            sxx = dataset[example][:, axis]

            # Our feature extractor.
            # Returns a tuple with
            sx, _ = dwt(sxx, "db2")
            np.savetxt("wavelet.txt", sx)

            features.append(sx)

        feature_data.append(np.ravel(features))
    return np.array(feature_data)


def get_features(dataset, method="stft"):
    """
    Extracts features from a given dataset
    :param method: Can be stft, dwt, etc
    :param dataset: With Accelerometer, Gyroscope and/or Linear Acc x, y, z data
    :return feature_data: feature extracted data
    """
    feature_data = None
    # Check the feature extraction method
    if method == "stft":
        feature_data = stft(dataset)
    elif method == "dwt":
        feature_data = wavelet(dataset)

    # Check the number of examples returned equal those from the original dataset
    assert feature_data.shape[0] == dataset.shape[0]

    return feature_data


def normalize_dataset(dataset):
    """
    Normalizes the given dataset for every example
    :param dataset:
    :return: a normalized dataset
    """
    mu = np.mean(dataset, axis=0)
    sigma = np.std(dataset, axis=0)
    return (dataset - mu) / sigma


def augment_per_class(x, y, method="local_averaging"):
    """
    :param x: Numpy array that contains the input data to be augmented
    :param y: Numpy array with labels that correspond to the input X data
    :param method: str representing the augmentation method
    :return: dataset and labels
    """
    dataset = np.array([])
    labels = np.array([])
    x = x.reshape(x.shape[0], x.shape[1])

    if method == "local_averaging":
        # Augment the X input data using the local averaging method from scipy
        augmented_data = downscale_local_mean(x, (4, 1))
        augmented_labels = np.ones((augmented_data.shape[0], y.shape[1]))  # Create a new array of ones that

        dataset = np.concatenate((x, augmented_data))
        labels = np.concatenate((y, augmented_labels * y[0]))

    return dataset.reshape((dataset.shape[0], dataset.shape[1], 1)), np.asarray(labels, dtype=np.int32)


def augment(x, y):
    """
    Augments the dataset given. the dataset is of the shape (m, n)
    :param x: The features of the dataset
    :param y: Labels for the dataset
    :return: 
    """
    augmented_x = np.array([])
    augmented_y = np.array([])
    # Perform data augmentation class by class
    for label in np.unique(y):
        x_original = []
        y_original = []
        for i in range(y.shape[0]):
            if y[i] == label:
                x_original.append(x[i])
                y_original.append(y[i])

        augment_x, augment_y = augment_per_class(np.array(x_original), np.array(y_original))
        if augmented_x.size > 0 and augmented_y.size > 0:
            augmented_x = np.concatenate((augmented_x, np.array(augment_x)))
            augmented_y = np.concatenate((augmented_y, np.array(augment_y)))
        else:
            augmented_x = np.array(augment_x)
            augmented_y = np.array(augment_y)

    return np.array(augmented_x), np.array(augmented_y)


# Plotting training graphs
def plot_graphs(history, string):
    plt.plot(history.history[string])
    plt.plot(history.history['val_' + string])
    plt.xlabel("Epochs")
    plt.ylabel(string)
    plt.legend([string, 'val_' + string])
    plt.show()


def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues,
                          activities=None):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_m(y_true, y_pred, activities)
    # Only use the labels that appear in the data
    classes = np.asarray(classes)
    classes = classes[np.asarray(unique_labels(y_true, y_pred), dtype=int) - 1]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return cm, ax


# Used in windowing the data given data that is not windowed. Refer to Thu's Approach on that
def window(arr, window, step):
    return None


# Creates a generator that continuously reads data from a file
def follow(thefile):
    thefile.seek(0, 0)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


if __name__ == "__main__":
    print("This is a utility function :)")
