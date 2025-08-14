import cv2
import numpy as np
import librosa

def solution(audio_path):
    ############################
    ############################

    wave_form, samp_rate = librosa.load(audio_path)
    mel_spectogram = librosa.feature.melspectrogram(y=wave_form, sr=samp_rate) #getting the mel spectogram of the audio
    mel_spec_to_db = librosa.power_to_db(np.abs(mel_spectogram), ref=np.max) #converting power to decibel scale

    cv2.imwrite('mel_spectrogram.png', np.uint8(mel_spectogram))
    mel_spec = cv2.imread('mel_spectrogram.png')
    mel_spec = cv2.cvtColor(mel_spec, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(mel_spec, 100, 200) #using canny edge detection to decibel scalled mel spectogram

    #determining the class based on the sum of edges. it was observered that the metal class has significantly higher sum of the edges
    if np.sum(edges) > 78975:
        class_name = 'metal'
    else:
        class_name = 'cardboard'

    ############################
    ############################
    ## comment the line below before submitting else your code wont be executed##
    # pass
    # class_name = 'cardboard'
    return class_name
