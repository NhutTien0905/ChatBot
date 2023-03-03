import openai
from os import walk
import os
import playsound
import speech_recognition as sr
from gtts import gTTS
from langdetect import detect
# import cv2
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import datetime
import serial 
import serial.tools.list_ports

start_signal = 's'
end_signal = 'x'

"""
lấy API key từ web, key này xài chung nên sẽ bị lỗi quá nhiều request nó sẽ ko trả lời đc
"""
def getKey():
    pd.set_option('display.max_colwidth', 500)
    page = requests.get("https://chatgptvietnam.org/account/api-keys")
    soup = bs(page.content)
    keys = soup.find_all(class_='badge badge-primary')
    key = keys[0].text
    return key

def speak(text,lang):
    if text == "":
        text = "Xin lỗi tôi không nghe rõ"
    tts = gTTS(text = text,lang=lang,slow=False)
    savepath = f"t1.mp3"
    tts.save(savepath)
    ser.write(bytes(start_signal, 'utf-8')) # xem có delay ko
    playsound.playsound(savepath)
    ser.write(bytes(end_signal, 'utf-8'))
    os.remove(savepath)

# lấy API
def APIcall(prompt):
    Api_key = getKey()
    openai.api_key = Api_key
    model = "text-davinci-003"

    response = openai.Completion.create(
        prompt = prompt,
        model = model,
        max_tokens = 1500,
        top_p = 1,
        frequency_penalty = 0.6
    )
    text = response['choices'][0]['text']
    text = text.replace("\n","")
    text = text.replace("?","")
    return text.lower()

def speech_to_text():
    # initialize the recognizer
    r = sr.Recognizer()
    # use the default microphone as the audio source
    with sr.Microphone() as source:
        print("AI: Speak now...")
        audio = r.listen(source)

    try:
        # Use Google Speech Recognition to transcribe audio
        text = r.recognize_google(audio, language='vi-VN')
        print(f"Human: {text}")

        # Use language detection to check if text is in Vietnamese
        lang = detect(text)
        if lang != "vi":
            lang = "en"
    except sr.UnknownValueError:
        # text = "Xin lỗi tôi không hiểu"
        text =""
        lang = "vi"
        # print("Xin lỗi tôi không hiểu")
    except sr.RequestError as e:
        text = "Xin lỗi hiện đang gặp lỗi nào đó"
        lang = "vi"
        print(f"Xin lỗi hiện đang gặp lỗi nào đó")
    return text, lang

# def face_detect(cap):
#     _, img = cap.read()
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=2, minSize=(30, 30))
#     print(type(faces))
#     face_detected = True
#     if faces == ():
#         face_detected = False
#         return face_detected
#     for (x, y, w, h) in faces:
#         cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
#     cv2.imshow('img', img)
#     return face_detected

# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
# cap = cv2.VideoCapture(0)

ports = serial.tools.list_ports.comports(include_links=False)
port = ""
for p in ports:
    print("port:",p.device)
    port = p.device
ser = serial.Serial(port, 115200,timeout=.1)

while True:
    ques,lang = speech_to_text()
    list_ans = []
    if ques == "":
        pass
    elif "xin chào" in ques.lower():
        list_ans.append("Xin chào mình là Hana, minh đến từ UEH")
    elif "hello" in ques.lower():
        list_ans.append("Hi, I'm Hana, I'm from UEH")
    elif "ngày mấy" in ques.lower():
        list_ans.append(str(datetime.now().strftime('%Y-%m-%d')))
    elif "today" in ques.lower():
        list_ans.append(str(datetime.now().strftime('%Y-%m-%d')))
    elif "mấy giờ" in ques.lower():
        list_ans.append(str(datetime.now().strftime('%H:%M:%S')))
    elif "time" in ques.lower():
        list_ans.append(str(datetime.now().strftime('%H:%M:%S')))
    elif ques == "stop now" or ques == "dừng lại":
        speak("Goodbye, see ya",lang)
        print("AI: Goodbye, see ya")
        break
    else:
        answer = APIcall(ques)
        list_ans.append(answer)
    for ans in list_ans:
        speak(ans,lang)
        print(f"AI: {ans}")
    # speak(answer,lang)
    # print(answer)
    print("---------")
    list_ans = []
# cap.release()