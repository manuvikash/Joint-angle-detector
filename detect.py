from Sports2D import Sports2D
import numpy
import cv2
import toml
import os
import pandas as pd
import plotly.express as px

def detectAngles(filename): 
    with open('Config.toml', 'r') as f:
        config = toml.load(f)

    avl = os.listdir('./videos')
    vid = filename
    if(vid not in avl):
        print('Chosen video not in list\n')
    print(f'Running joint detection on - {vid}')
    config['project']['video_file'] = vid
    with open('Config.toml', 'w') as f:
        toml.dump(config, f)

    try:    
        Sports2D.detect_pose('Config.toml')
        Sports2D.compute_angles('Config.toml')
    except Exception as e:
        print('Joint detection had the following error')
        print(e)

def displayJA(filename):
    vid = filename
    print("Displaying video with joint-angle overlay")
    cap = cv2.VideoCapture('./results/' + vid[:-4] + '_BLAZEPOSE.mp4')
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
    csv_to_show = './results/'+ filename[:-4] + '_BLAZEPOSE_angles.csv'
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
        fig = px.line(data_frame=table_select, width=1310, height=699)
        fig.show()
    except:
        print('Variables could not be found in csv file')

# detectAngles('demo.mp4')
# displayJA('demo.mp4')
plotgraph('demo.mp4', ['Right knee','Left knee'])