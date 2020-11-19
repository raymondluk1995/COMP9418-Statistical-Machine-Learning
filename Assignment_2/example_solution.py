'''
COMP9418 Assignment 2
This file is the example code to show how the assignment will be tested.

Name:     zID:

Name:     zID:
'''

# Make division default to floating-point, saving confusion
from __future__ import division
from __future__ import print_function

# Allowed libraries 
import numpy as np
import pandas as pd
import scipy as sp
import scipy.special
import heapq as pq
import matplotlib as mp
import matplotlib.pyplot as plt
import math
from itertools import product, combinations
from collections import OrderedDict as odict
import collections
from graphviz import Digraph, Graph
from tabulate import tabulate
import copy
import sys
import os
import datetime
import sklearn
import ast
import re

import my_function

###################################
# Code stub
# 
# The only requirement of this file is that is must contain a function called get_action,
# and that function must take sensor_data as an argument, and return an actions_dict
# 

tran_matrix_0 = pd.read_csv("tran_matrix0.csv")
tran_matrix_1 = pd.read_csv("tran_matrix1.csv")
tran_matrix_2 = pd.read_csv("tran_matrix2.csv")
tran_matrix_3 = pd.read_csv("tran_matrix3.csv")
tran_matrix_4 = pd.read_csv("tran_matrix4.csv")

tran_matrix0 = np.array([tran_matrix_0.iloc[i].values.tolist()[2:] for i in range(tran_matrix_0.shape[0])])
tran_matrix1 = np.array([tran_matrix_1.iloc[i].values.tolist()[2:] for i in range(tran_matrix_1.shape[0])])
tran_matrix2 = np.array([tran_matrix_2.iloc[i].values.tolist()[2:] for i in range(tran_matrix_2.shape[0])])
tran_matrix3 = np.array([tran_matrix_3.iloc[i].values.tolist()[2:] for i in range(tran_matrix_3.shape[0])])
tran_matrix4 = np.array([tran_matrix_4.iloc[i].values.tolist()[2:] for i in range(tran_matrix_4.shape[0])]) 


censor_to_room_indx = {'r1' : 15, 'r2': 4, 'r3':24, 'r4': 30, 
                       'u1': 39, 'u2': 37, 'u3': 0, 'u4': 23,
                      'd1': [7,8], 'd2': [35,36], 'd3': [25,26], 'd4': [34,38]}


def choose_tran_matrix(time):
    if(time<datetime.time(hour=8,minute=1)):
        return tran_matrix0 
    elif (time<datetime.time(hour=8,minute=5)):
        return tran_matrix1 
    elif (time<datetime.time(hour=17,minute=30)):
        return tran_matrix2
    elif (time<datetime.time(hour=17,minute=41)):
        return tran_matrix3 
    else:
        return tran_matrix4  
        return tran_matrix4 


people = round(np.random.normal(20,1)) 
people = 20
init_state = np.array([0]*40+[people])

curr_state = init_state 


# this global state variable demonstrates how to keep track of information over multiple 
# calls to get_action 
state = {} 

# params = pd.read_csv(...)

def get_action(sensor_data):
    # declare state as a global variable so it can be read and modified within this function
    global curr_state
    global params
    #print(curr_state)
    # TODO: Add code to generate your chosen actions, using the current state and sensor_data
    light_list = ['lights1', 'lights2', 'lights3', 'lights4', 'lights5', 'lights6', 'lights7', 'lights8', 'lights9', 'lights10', 'lights11', 'lights12', 'lights13', 'lights14', 'lights15', 'lights16', 'lights17', 'lights18', 'lights19', 'lights20', 'lights21', 'lights22', 'lights23', 'lights24', 'lights25', 'lights26', 'lights27', 'lights28', 'lights29', 'lights30', 'lights31', 'lights32', 'lights33', 'lights34', 'lights35']
    sensor_only = my_function.keep_sensor_info(sensor_data)
    
    tran_matrix = choose_tran_matrix(sensor_data['time'])
    
    #print(tran_matrix)
    
    
    curr_state = curr_state @ tran_matrix #transition 
    curr_state = my_function.censor_update(sensor_only, censor_to_room_indx, curr_state) #update by censors 
    
    decision_by_state = my_function.make_decision(curr_state)
    actions_dict = {k: my_function.turn_on(v) for k,v in zip(light_list, decision_by_state)}
    
    if sensor_data['time'] >= datetime.time(hour=17,minute=41):
        actions_dict  ={k: 'off' for k in light_list}
    """
    1. get the correct matrix 
    2. keep the 
    """
    
    #actions_dict = {'lights1': 'off', 'lights2': 'on', 'lights3': 'off', 'lights4': 'off', 'lights5': 'off', 'lights6': 'off', 'lights7': 'off', 'lights8': 'off', 'lights9': 'off', 'lights10': 'off', 'lights11': 'off', 'lights12': 'off', 'lights13': 'off', 'lights14': 'off', 'lights15': 'off', 'lights16': 'off', 'lights17': 'off', 'lights18': 'off', 'lights19': 'off', 'lights20': 'off', 'lights21': 'off', 'lights22': 'off', 'lights23': 'off', 'lights24': 'off', 'lights25': 'off', 'lights26': 'off', 'lights27': 'off', 'lights28': 'off', 'lights29': 'off', 'lights30': 'off', 'lights31': 'off', 'lights32': 'off', 'lights33': 'off', 'lights34': 'off', 'lights35':'on'}
    return actions_dict



