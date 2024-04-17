from Sports2D import Sports2D
import numpy
import cv2
import toml
import os
import pandas as pd
import plotly.express as px

def detectAngles(filename):
    filename = filename + ".mp4" 
    with open('Constants/Config.toml', 'r') as f:
        config = toml.load(f)

    avl = os.listdir('./videos')
    vid = filename
    if(vid not in avl):
        print('Chosen video not in list\n')
    print(f'Running joint detection on - {vid}')
    config['project']['video_file'] = vid
    with open('Constants/Config.toml', 'w') as f:
        toml.dump(config, f)

    try:    
        Sports2D.detect_pose('Constants/Config.toml')
        Sports2D.compute_angles('Constants/Config.toml')
    except Exception as e:
        print('Joint detection had the following error')
        print(e)

def displayJA(filename):
    vid = filename + ".mp4"
    print("Displaying video with joint-angle overlay")
    cap = cv2.VideoCapture('Results/' + vid[:-4] + '_BLAZEPOSE.mp4')
    if (cap.isOpened()== False): 
        print("Error opening video file") 
    
    while(cap.isOpened()):  
        ret, frame = cap.read() 
        if ret == True: 
            cv2.imshow('Frame', frame) 
            if cv2.waitKey(25) & 0xFF == ord('q'): 
                break
        else: 
            break
    
    cap.release() 
    cv2.destroyAllWindows()

def plotgraph(filename, jointList):
    plot_variable_names = str(jointList)
    csv_to_show = 'Results/'+ filename + '_BLAZEPOSE_angles.csv'
    # Retrieve csv results
    table = pd.read_csv(csv_to_show, index_col=0, header=[0,1,2,3])
    table = table.droplevel([0,1], axis=1)
    print('Plotting requested graph')
    try:
        plot_variable_names = eval(plot_variable_names)
        plot_variable_names = ['Time']+plot_variable_names
        table_select = table[plot_variable_names]
        table_select.columns = [' '.join(col).strip() for col in table_select.columns.values]
        table_select = table_select.set_index(list(table_select)[0])
          # Applying moving average smoothing
        table_smoothed = table_select.rolling(10).mean()  # Adjust window size as needed
        fig = px.line(data_frame=table_smoothed, width=1310, height=699)
        fig.show()
    except:
        print('Variables could not be found in csv file')

# detectAngles('test3')
# displayJA('test3.mp4')

# plotgraph("test3", [ "Right hip"])
# plotgraph("v3", [ "Right hip"])

