import asyncio
import datetime
from moviepy.editor import *
import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
import vlc

import cv2
from VideoPlayer import VideoPlayer

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
video_name = 'vid4.mp4'
cap = cv2.VideoCapture(0)
video = cv2.VideoCapture(video_name)

if video.isOpened():
    print('video opened')
else:
    print('error')

scale = 0

video_playing = False
can_play = True
last_played = datetime.datetime.now()
audio_up = True

window = 'Video'
cv2.namedWindow(window)

def MP4toMP3(mp4, mp3):
    videoclip = VideoFileClip(mp4)
    audioclip = videoclip.audio
    audioclip.write_audiofile(mp3)
    videoclip.close()
    audioclip.close()
def detect_face(img, draw=False):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_img, 1.1, 5, minSize=(40, 40))
    if draw:
        for(x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return faces

MP4toMP3(video_name, 'audio.mp3')
audio = vlc.MediaPlayer('audio.mp3')
res2, vid_frame = video.read()
while True:
    res1, frame = cap.read()
    if video_playing:
        res2, vid_frame = video.read()
        cv2.putText(vid_frame, 'Playing...', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    elif can_play:
        cv2.putText(vid_frame, 'Not playing', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    else:
        cv2.putText(vid_frame, 'Cooldown', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    if audio_up and can_play:
        audio.play()
        audio_up = False


    if res1 is False:
        break

    faces = detect_face(frame, draw=True)

    if len(faces) > 0 and can_play:
        video_playing = True

    if datetime.datetime.now().second == last_played.second+3:
        can_play = True

    cv2.imshow('Video', vid_frame)
    cv2.imshow('Video1', frame)

    if video.get(1) == video.get(7):
        audio = vlc.MediaPlayer('audio.mp3')
        video = cv2.VideoCapture(video_name)
        video_playing = False
        can_play = False
        last_played = datetime.datetime.now()

    if(cv2.waitKey(1) and 0xFF == ord("q")):
        break

cap.release()
cv2.destroyAllWindows()