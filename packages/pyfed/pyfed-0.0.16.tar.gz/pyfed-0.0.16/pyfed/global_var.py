import os
import time
import h5py
import copy
import socket
import datetime
import warnings
import numpy as np
from io import BytesIO
import tensorflow as tf
import concurrent.futures
from joblib import load, dump
from tensorflow.keras.models import save_model, load_model


IP = "127.0.0.1"
PORT = 124
SIZE = 1024
FORMAT = "utf-8"
PATH = "pyfed_logs/fit"