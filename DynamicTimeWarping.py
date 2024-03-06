import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fastdtw import fastdtw
import json

def prepare(filename):
    path = './results/'+ filename + '_BLAZEPOSE_angles.csv'
    data = pd.read_csv(path)
    data.columns = data.iloc[1] 
    data =data.drop(index=[0, 1, 2])
    data =data.reset_index(drop=True)
    data =data.astype(float) 
    return data

def applyDtw(std, test, joint):
    data1 = prepare(std)
    data2 = prepare(test)
    angle1 = data1[joint].values
    angle2 = data2[joint].values

    distance, path = fastdtw(angle1, angle2, dist=2)
    path_length = len(path)  # Get the length of the alignment path
    normalized_distance = distance / path_length  # Normalize distance by path length
    similarity_score = (1 / (1 + normalized_distance)) * 10 ** 3
    return (normalized_distance, path, similarity_score)

def plotMapping(std, test, joint, path):
    data1 = prepare(std)
    data2 = prepare(test)
    angle1 = data1[joint].values
    angle2 = data2[joint].values
    plt.figure(figsize=(10, 5))

    # Plot both time series
    plt.plot(angle1, label='Time Series 1', marker='o')
    plt.plot(angle2, label='Time Series 2', marker='x')

    # Draw lines between aligned points
    for a, b in path:
        plt.plot([a, b], [angle1[a], angle2[b]], 'k-', linewidth=0.3, alpha=0.5)

    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.title('DTW Alignment between Two Time Series')
    plt.legend()
    plt.show()

def dtw(std, test):
    fileMapFile = open('FileMap.json')
    fileMap = json.load(fileMapFile)
    fileMapFile.close()
    jointAngles = fileMap[std]

    avgDist = 0
    avgSim = 0
    perJointSim = {}
    for i in jointAngles:
        distance, path, sim = applyDtw(std, test, i)
        avgDist += distance
        avgSim += sim
        perJointSim[i] = sim

        # plotMapping(std, test, i, path)

    avgDist /= len(jointAngles)
    avgSim /= len(jointAngles)

    return avgDist, avgSim, perJointSim


# std = 'v3'
# test = 'test3'
# dist, sim, perJointSim = dtw(std, test)

# print(dist, sim, perJointSim)

# print(difference)
# print(sim.round(3))
# plotMapping(data_1, data_2, 'Right hip', path)