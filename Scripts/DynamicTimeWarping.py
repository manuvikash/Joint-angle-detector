import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fastdtw import fastdtw
import json
import Normalize


def prepare(filename):
    path = 'Results/' + filename + '_BLAZEPOSE_angles.csv'
    data = pd.read_csv(path)
    data.columns = data.iloc[1]
    data = data.drop(index=[0, 1, 2])
    data = data.reset_index(drop=True)
    data = data.astype(float)
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


def plotMapping(std, test, joint, path, title):
    data1 = prepare(std)
    data2 = prepare(test)
    angle1 = data1[joint].values
    angle2 = data2[joint].values
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot both time series
    ax.plot(angle1, label='Standard Time Series', marker='o')
    ax.plot(angle2, label='Test Time Series', marker='x')

    # Draw lines between aligned points
    for a, b in path:
        ax.plot([a, b], [angle1[a], angle2[b]], 'k-', linewidth=0.4, alpha=0.5)

    ax.set_xlabel('Frame')
    ax.set_ylabel('Joint Angle')
    ax.set_title(title)
    ax.legend()

    return fig


def dtw(std, test):
    fileMapFile = open('Constants/FileMap.json')
    fileMap = json.load(fileMapFile)
    fileMapFile.close()
    jointAngles = fileMap[std]

    avgDist = 0
    avgSim = 0
    perJointSim = {}
    graphs = []
    for i in jointAngles:
        distance, path, sim = applyDtw(std, test, i)
        sim = Normalize.calcAvgSim(sim, test)
        avgDist += distance
        avgSim += sim
        perJointSim[i] = sim

        graphs.append(plotMapping(std, test, i, path, i))

    avgDist /= len(jointAngles)
    avgSim = avgSim/len(jointAngles)

    return avgDist, avgSim, perJointSim, graphs

# std = 'v3'
# test = 'test3'
# dist, sim, perJointSim = dtw(std, test)

# print(dist, sim, perJointSim)

# print(dist)
# print(sim.round(3))
# plotMapping(std, test, 'Right hip', path)
