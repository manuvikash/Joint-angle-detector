import streamlit as st
import os
import Score
import pandas as pd

def display_data(data):
    st.title("Performance Analysis Report")
    st.header("Overall Performance")
    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Score", f"{data['Overall score']:.2f}")
    col2.metric("Overall Similarity", f"{data['Overall Similarity']:.2f}")
    col3.metric("Overall Smoothness", f"{data['Overall Smoothness']:.2f}")

    # Prepare data for the table
    joint_data = {
        "Joint": [],
        "Score": [],
        "Similarity": [],
        "Smoothness": []
    }

    # Populate the dictionary with data
    for joint, metrics in data['Per Joint values'].items():
        joint_data["Joint"].append(joint)
        joint_data["Score"].append(f"{metrics['Score']:.2f}")
        joint_data["Similarity"].append(f"{metrics['Similarity']:.2f}")
        joint_data["Smoothness"].append(f"{metrics['Smoothness']:.2f}")

    # Convert dictionary to DataFrame
    df = pd.DataFrame(joint_data)

    # Style the DataFrame before displaying
    def make_pretty(styler):
        styler.set_table_styles([{
            'selector': 'th',
            'props': [ ('font-size', '16px')]
        }, {
            'selector': 'td',
            'props': [('font-size', '14px')]
        }])
        styler.set_properties(**{
            'width': '300px',  # Sets the width of the columns
            'text-align': 'center'  # Centers the text in the cells
        })
        return styler

    st.header("Detailed Joint Analysis")
    st.table(make_pretty(df.style))
def main():
    video_files = os.listdir('./Videos')
    st.title("Video File Selector")

    video1 = st.selectbox('Video to be tested:', video_files)
    video2 = st.selectbox('Standard Video:', video_files)
    
    if st.button('Submit'):
        results, graphs = Score.runDemo(video1[:-4], video2[:-4])
        display_data(results)

        with st.expander("Watch selected videos"):
            st.write('Test video')
            st.video('./Videos/' + video1)
            st.write('Standard video')
            st.video('./Videos/' + video2)

        with st.expander("See Dynamic Time Warping graphs"):
            for i in graphs:
                st.pyplot(i)
        
if __name__ == "__main__":
    main()