import pandas as pd
import numpy as np
import pickle

perf = pickle.load(open('skew_record.p', 'rb'))
perf.to_csv("skew_record.csv", index=False)