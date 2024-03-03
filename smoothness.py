import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.fftpack import fft
from scipy.signal import butter, filtfilt
from scipy.integrate import simpson

# Load the data
file_path = './results/walk_BLAZEPOSE_points.csv'  # Adjust this to your actual file path
data = pd.read_csv(file_path)

# Creating the mapping dictionary
landmark_names = data.iloc[1, 2::3].values  # Extract landmark names starting from column index 2, every 3 columns
landmark_indices = range(2, len(landmark_names)*3 + 2, 3)  # Calculate indices for x coordinates of each landmark

# Map landmark names to their x and y column indices
landmark_dict = {name: {'x': i, 'y': i+1} for name, i in zip(landmark_names, landmark_indices)}

# Now, define the function to extract time, x, and y coordinates for a given landmark name
def extractData(landmark_name):
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


# Define the Butterworth Low-Pass Filter Function
def butter_lowpass_filter(data, cutoff_freq, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

def calculate_sparc(speed, fs):
    n = len(speed)
    freq = np.fft.rfftfreq(n, d=1/fs)
    fft_magnitude = np.abs(fft(speed, n=n))
    
    # Normalize the FFT magnitude
    fft_magnitude = fft_magnitude / np.max(fft_magnitude)
    
    # Calculate the derivative of the magnitude spectrum
    d_fft_magnitude = np.diff(fft_magnitude)
    
    # Calculate the delta frequency
    df = np.mean(np.diff(freq))
    
    # Calculate the spectral arc length
    sparc = -np.sum(np.sqrt(d_fft_magnitude**2 + df**2))
    return sparc

def calculate_jerk(speed, fs):
    dt = 1/fs
    jerk = np.diff(speed, n=2) / dt**2
    jerk_metric = simpson(jerk**2, dx=dt)
    return jerk_metric


# landmarks = ['LHip', 'LEyeOuter', 'LKnee', 'REye', 'RMouth', 'LEyeInner', 'LPinky', 'LEar', 'RIndex', 'LEye', 'RShoulder', 'RHip', 'Nose', 'RAnkle', 'RWrist', 'LAnkle', 'LHeel', 'REyeInner', 'LEyeInner', 'REyeOuter', 'RThumb', 'LShoulder', 'LThumb', 'RElbow', 'RHeel', 'RMouth', 'RKnee', 'LEye', 'LWrist', 'REar', 'LBigToe', 'LIndex', 'LElbow', 'LPinky']

landmarks = ['Nose', 'RShoulder', 'LShoulder', 'RHip', 'LHip', 'RKnee', 'LKnee', 'RAnkle', 'LAnkle', 'RBigToe', 'LBigToe', 'RWrist', 'LWrist', 'RIndex', 'LIndex']

sparcList = {}
jerkList = {}
for point in landmarks: 
    time, x_coords, y_coords = extractData(point)


    # Interpolate to create a uniform sampling rate
    fs = 1 / np.mean(np.diff(time))  # Estimate the sampling frequency
    time_uniform = np.arange(time.iloc[0], time.iloc[-1], 1/fs)
    interp_x = interp1d(time, x_coords, kind='linear')(time_uniform)
    interp_y = interp1d(time, y_coords, kind='linear')(time_uniform)


    # Apply the Butterworth Low-Pass Filter to the interpolated coordinates
    cutoff_frequency = 4  # Define your cutoff frequency based on your data analysis
    filtered_x = butter_lowpass_filter(interp_x, cutoff_frequency, fs)
    filtered_y = butter_lowpass_filter(interp_y, cutoff_frequency, fs)

    # Calculate the speed profile from the filtered coordinates
    speed = np.sqrt(np.diff(filtered_x)**2 + np.diff(filtered_y)**2) * fs
    # Perform calculations
    sparc = calculate_sparc(speed, fs)
    jerk_metric = calculate_jerk(speed, fs)

    # print(f"SPARC: {sparc}")
    # print(f"Jerk Metric: {jerk_metric}")

    sparcList[point] = sparc
    jerkList[point] = jerk_metric

sparcList = sorted(sparcList.items(), key=lambda x: x[1])
for key, value in sparcList:
    print(f"{key}: {value}")


print("\n ------------------------------ \n")

jerkList = sorted(jerkList.items(), key=lambda x: x[1])
for key, value in jerkList:
    print(f"{key}: {value}")