import cv2
import mediapipe as mp
import time
import streamlit as st
import os








def pose_detection(file_path):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose


    font = cv2.FONT_HERSHEY_SIMPLEX 
      
    # org 
    org = (50,50) 
      
    # fontScale 
    fontScale = 1
      
    # Blue color in BGR 
    color = (255, 0, 0) 
      
    # Line thickness of 2 px 
    thickness = 2

    

    cap = cv2.VideoCapture(file_path)
    _, frame = cap.read()
    filename = file_path.split('/')[-1].split('.')[0].replace(' ','') + '_output.mp4'
    fps = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(filename,cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(frame.shape[1]), int(frame.shape[0])), isColor=True)
    with mp_pose.Pose(
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8) as pose:
      while True:
        start_time = time.time()
        success, image = cap.read()
        if not success:
          print("Ignoring empty camera frame.")
          # If loading a video, use 'break' instead of 'continue'.
          break

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        fps = 1/(time.time() - start_time)
        # cv2.putText(image, "FPS : " + str(int(fps)), org, font,  
        #               fontScale, color, thickness, cv2.LINE_AA)
        out.write(image)
        # cv2.imshow('MediaPipe Pose', image)
        # if cv2.waitKey(5) & 0xFF == 27:
        #   break
    cap.release()
    return filename

st.markdown("<h1>Well Yoga AI Test</h1><br>", unsafe_allow_html=True)

uploaded_video = st.file_uploader("Choose video", type=["mp4", "mov"])

if uploaded_video is not None: # run only when user uploads video
    vid = uploaded_video.name
    with open(vid, mode='wb') as f:
        f.write(uploaded_video.read()) # save video to disk

    st.markdown(f"""
    ### Files
    - {vid}
    """,
    unsafe_allow_html=True) 
    result_filename = pose_detection(vid)
    result_streamlit_filename = result_filename.split('.')[0] + '_streamlit.mp4'
    #result_filename = os.path.abspath('YogFront-SampleVideo_output.mp4')
    os.system(f'ffmpeg -i {result_filename} -vcodec libx264 {result_streamlit_filename} -y')
    #print(result_filename)
    video_file = open(result_streamlit_filename, 'rb')
    video_bytes = video_file.read()

    st.video(video_bytes)