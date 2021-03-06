'''
COMP9418 Assignment 2
This file is the example code to show how the assignment will be tested.

Name: Minrui Lu    zID: z5277884

Name:  Yangqi Zhang   zID: z5235062
'''

import numpy as np 
import pandas as pd
import datetime 


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



def u2_update(state_vector):
    state_vector[16] = max(state_vector[16],0.25)
    state_vector[17] = max(state_vector[17],0.25)
    state_vector[19] = max(state_vector[19],0.25)
    state_vector[20] = max(state_vector[20],0.25)
    return (state_vector)

def r2_update(state_vector):
    # state_vector[8] = min(state_vector[8],0.24)
    # state_vector[12] = min(state_vector[12],0.25)
    # state_vector[5] = max(state_vector[5],0.26)
    return (state_vector)


def robot_overwrite(robot_info, vector):
    "arguments: a string of robot information pair;"
    robot_info = robot_info.replace("(","")
    robot_info = robot_info.replace(")","")
    robot_info = robot_info.replace(" ","")
    robot_info = robot_info.replace("'","")
    robot_list = robot_info.split(",")
    place_list = ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15', 'r16', 'r17', 'r18', 'r19', 'r20', 'r21', 'r22', 'r23', 'r24', 'r25', 'r26', 'r27', 'r28', 'r29', 'r30', 'r31', 'r32', 'r33', 'r34', 'r35', 'c1', 'c2', 'c3', 'c4', 'o1', 'outside']
    vector[place_list.index(robot_list[0])] = int(robot_list[1]) 
    return(vector)


def censor_update(sensor_data, censor_room_match, state_vector):
    for censor_name, censor_status in sensor_data.items():
        if censor_status == None:
            continue 
        if censor_status == "no motion": 
            # print("censor_name:",censor_name)
            # continue
            censor_abb = censor_name[0] + censor_name[-1]
            room = censor_room_match[censor_abb]
            state_vector[room] = 0
            continue 

        if censor_status == 0: 
            continue
        if censor_status == "motion":
            censor_abb = censor_name[0] + censor_name[-1]
            room = censor_room_match[censor_abb]
            if(censor_abb=="u2"):
                state_vector = u2_update(state_vector) 
            elif(censor_abb=="r2"):
                state_vector = r2_update(state_vector)

            
            state_vector[room] = max(state_vector[room], 1)
        elif censor_name[:3] == 'rob':
            state_vector = robot_overwrite(censor_status, state_vector)
        
        elif censor_status > 0:
            censor_abb = censor_name[0] + censor_name[-1]
            rooms = censor_room_match[censor_abb]
            state_vector[rooms] = [max(state_vector[rooms[0]], 1), max(state_vector[rooms[1]],1)]

    return(state_vector)


def turn_on(my_bool):
    if my_bool == True:
        action = 'on'
    else:
        action = 'off'
    return(action)

def make_decision(state_vector, theta = 0.25):
    room_state = state_vector[:35]
    return(room_state > theta)

def keep_sensor_info(sensor_dict):
    sensor_info = {k:v for k,v in sensor_dict.items() if k!='time' if k!= 'electricity_price'}
    return(sensor_info)
    
  
def resample(curr_state, people_num):
    prob_state = [i/sum(curr_state) for i in curr_state]
    sampling = list(np.random.choice(41,people_num, p = prob_state))
    new_people = [sampling.count(i) for i in range(41)]
    return(new_people)
    
    