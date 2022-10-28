import cv2
import os
import speech_recognition as sr

def takeName():
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
    except Exception as e:
        return "None"
    return query

def cap():
    video = cv2.VideoCapture(0) 
    while True:
        check, frame = video.read()
        cv2.imshow("Press Spacebar to Capture !!",frame)
        key = cv2.waitKey(1)
        if key == ord(" "):
            break
    os.chdir("C:\Everything\FRIDAY\Captures")
    cv2.waitKey(300)
    filename = takeName().title()
    showPic = cv2.imwrite(filename+".jpg",frame)
    # print(showPic)
    video.release()
    cv2.destroyAllWindows()