"""
setup jupyter for data analysis. 
"""
from .defaultlog import log
import logging
if log.getEffectiveLevel() > logging.DEBUG:
    import warnings
    warnings.filterwarnings("ignore")

def flog(text):
    """ for finding logging problems """
    with open("c:/log1.txt", "a") as f:
        f.write(str(text))

################## extensions ################################
get_ipython().magic('load_ext autoreload')
get_ipython().magic('autoreload 2')      # autoreload all modules
try:
    get_ipython().magic('matplotlib inline')  # show charts inline
except:
    pass
try:
    get_ipython().magic('load_ext cellevents')  # show time and alert
except:
    pass

################## common ################################
import os
import sys
from os.path import join, expanduser
HOME = os.path.expanduser("~")
try:
    from tqdm import tqdm_notebook as tqdm
except:
    pass

################## analysis ################################
try:
    import scipy as sp
except:
    pass
try:
    import pandas as pd
except:
    pass
try:
    import numpy as np
except:
    pass

################# visualisation #############################
from pprint import pprint
try:
    import matplotlib as mpl
    import matplotlib.cm as cm
    import matplotlib.pyplot as plt
except:
    pass
try:
    from skimage.io import imread, imshow, imsave
except:
    pass
from IPython.display import display as d
from IPython.core.display import HTML

def wide():
    """ makes notebook fill screen width """
    d(HTML("<style>.container { width:100% !important; }</style>"))