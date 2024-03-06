from scipy.signal import savgol_filter, find_peaks
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def preprocess_csv(file_path):
    df = pd.read_csv(file_path, skiprows=3)
    df.set_index(df.columns[0], inplace=True)
    df = df.apply(pd.to_numeric, errors='coerce')
    
    return df

df_standard_corrected = preprocess_csv('results/v2_BLAZEPOSE_angles.csv')
df_test_corrected = preprocess_csv('results/test3_BLAZEPOSE_angles.csv')

angle_column = 'dorsiflexion'  # Example joint angle
window_length, polyorder = 51, 3  # Parameters for Savitzky-Golay filter, window length and polynomial order

# Ensure window length is odd and less than the size of the dataset
if window_length % 2 == 0: window_length += 1
window_length = min(window_length, len(df_standard_corrected) - 1)

# Apply smoothing
smoothed_angles_standard = savgol_filter(df_standard_corrected[angle_column].values, window_length, polyorder)

# Find peaks (crests) and troughs in the smoothed data
peaks, _ = find_peaks(smoothed_angles_standard)
troughs, _ = find_peaks(-smoothed_angles_standard)

# Visualization to verify the process
plt.figure(figsize=(14, 7))
plt.plot(df_standard_corrected[angle_column].values, label='Original', alpha=0.5)
plt.plot(smoothed_angles_standard, label='Smoothed', color='red')
plt.scatter(peaks, smoothed_angles_standard[peaks], marker='x', color='green', label='Peaks')
plt.scatter(troughs, smoothed_angles_standard[troughs], marker='o', color='blue', label='Troughs')
plt.title(f'Smoothing and Peak Detection for {angle_column.capitalize()} Angle')
plt.legend()
plt.show()

# Return counts of peaks and troughs for initial comparison
print(len(peaks), len(troughs))
