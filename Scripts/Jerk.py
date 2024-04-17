import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.fftpack import fft
from scipy.signal import butter, filtfilt
from scipy.integrate import simpson
import json

def extractData(landmark_name, landmark_dict, data):
    if landmark_name not in landmark_dict:
        raise ValueError(f"{landmark_name} is not a valid landmark name.")
    # Extract indices
    x_idx = landmark_dict[landmark_name]['x']
    y_idx = landmark_dict[landmark_name]['y']
    # Extract data
    time = data.iloc[3:, 1].astype(float)  # Time column is consistent
    x_coords = data.iloc[3:, x_idx].astype(float)
    y_coords = data.iloc[3:, y_idx].astype(float)
    return time, x_coords, y_coords

def butter_lowpass_filter(data, cutoff_freq, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

def calculate_jerk(speed, fs):
    dt = 1/fs
    jerk = np.diff(speed, n=2) / dt**2
    jerk_metric = simpson(jerk**2, dx=dt)
    return jerk_metric

def getJerk(filename):
    data = pd.read_csv('Results/'+filename+'_BLAZEPOSE_points.csv')
    landmark_names = data.iloc[1, 2::3].values 
    landmark_indices = range(2, len(landmark_names)*3 + 2, 3)
    landmark_dict = {name: {'x': i, 'y': i+1} for name, i in zip(landmark_names, landmark_indices)}


    fileMapFile = open('Constants/FileMap.json')
    jointMapFile = open('Constants/JointMap.json')
    fileMap = json.load(fileMapFile)
    jointMap = json.load(jointMapFile)
    fileMapFile.close()
    jointMapFile.close()
    jointList = fileMap[filename]
    landmarks = []
    for i in jointList:
        landmarks += jointMap[i]

    jerkList = {}
    for point in landmarks: 
        time, x_coords, y_coords = extractData(point, landmark_dict, data)

        # Interpolate to create a uniform sampling rate
        fs = 1 / np.mean(np.diff(time))  # Estimate the sampling frequency
        time_uniform = np.arange(time.iloc[0], time.iloc[-1], 1/fs)
        interp_x = interp1d(time, x_coords, kind='linear')(time_uniform)
        interp_y = interp1d(time, y_coords, kind='linear')(time_uniform)

        # Apply the Butterworth Low-Pass Filter to the interpolated coordinates
        cutoff_frequency = 4
        filtered_x = butter_lowpass_filter(interp_x, cutoff_frequency, fs)
        filtered_y = butter_lowpass_filter(interp_y, cutoff_frequency, fs)

        # Calculate the speed profile from the filtered coordinates
        speed = np.sqrt(np.diff(filtered_x)**2 + np.diff(filtered_y)**2) * fs
        jerk_metric = calculate_jerk(speed, fs)
        jerkList[point] = jerk_metric

    jerkList = sorted(jerkList.items(), key=lambda x: x[1])
    totalJerk = 0
    for i in jerkList:
        totalJerk += i[1]
    totalJerk /= len(jerkList)


    video_duration = time.iloc[-1] - time.iloc[0]
    normalized_totalJerk = totalJerk / video_duration
    normalized_smooth = (1 / (1 + normalized_totalJerk)) * 10 ** 10

    for key, value in jerkList:
        print(f"{key}: {value}")

    return normalized_totalJerk, normalized_smooth * 0.75


