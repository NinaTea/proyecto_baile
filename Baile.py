""" 
-*- coding: utf-8 -*-
@author: NinaTea
"""

import numpy as np
import mediapipe as mp
import cv2

"""
Notas:
    Sólo compara el lado izquierdo del cuerpo, esta es una version beta. Planeo en total 8 gradientes distintos. 
    16 matrices en total x, y
"""
#mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

videos = ["fancam_kpop.mp4", "prueba_baile1.mp4"] #los dos videos a comparar

# def audio comparacion <--- Posibles actualizaciones

# def editor de video

matriz_1_x = np.array([])
matriz_1_y = np.array([])

matriz_2_x = np.array([])
matriz_2_y = np.array([])

def gradiente_sup(frames, coord1):
    x1 = results.pose_landmarks.landmark[coord1].x
    y1 = results.pose_landmarks.landmark[coord1].y 
               
    x2 = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x
    y2 = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y
        
    delta1_x = x1 - x2
    delta1_y = y1 - y2    
        
    return delta1_x, delta1_y
    
def gradiente_inf(frames, coord1):
    x1 = results.pose_landmarks.landmark[coord1].x
    y1 = results.pose_landmarks.landmark[coord1].y
                
    x2 = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x
    y2 = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y
        
    delta1_x = x1 - x2
    delta1_y = y1 - y2    

    return delta1_x, delta1_y

for i in videos: 
    cap = cv2.VideoCapture(i)  
    gradiente_x = np.repeat(0.0, 1166*4).reshape(1166, 4)
    gradiente_y = np.repeat(0.0, 1166*4).reshape(1166, 4)
 
    with mp_pose.Pose(static_image_mode = False) as pose:
        c = 0
        while True:
            
            ret, frame = cap.read()
            if ret == False:
                break
        
            height, width, _ = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb) 
            
            coordenadas_izq_sup = np.array(["mp_pose.PoseLandmark.LEFT_WRIST", "mp_pose.PoseLandmark.LEFT_ELBOW"])                                    
            coordenadas_izq_inf = np.array(["mp_pose.PoseLandmark.LEFT_ANKLE", "mp_pose.PoseLandmark.LEFT_KNEE"])
                       
            n = 0
            for k in range(len(coordenadas_izq_sup)):               
                posiciones = gradiente_sup(results, k)
                gradiente_x[(c,n)] = posiciones[0]
                gradiente_y[(c,n)] = posiciones[1]
                n+= 1
                
            j = 2   
            for m in range(len(coordenadas_izq_inf)):
                posiciones = gradiente_inf(results, m)
                gradiente_x[(c,j)] = posiciones[0]
                gradiente_y[(c,j)] = posiciones[1]
                j+= 1
            
            if c == 1165:
                if i == videos[0]: 
                    matriz_1_x = gradiente_x
                    matriz_1_y = gradiente_y
                else:
                    matriz_2_x = gradiente_x
                    matriz_2_y = gradiente_y
                break
            
            c+=1    

def comparar(matriz1, matriz2):
    
    matriz_resultado = np.repeat("  ", 1166*4).reshape(1166, 4)
    
    for i in range(0, len(matriz1)): #filas
        for j in range(4): #columnas:
            
            valor = abs(abs(matriz2[i,j]) -  abs(matriz1[i,j])) 
            
            if 0 <= valor <= 0.005:
                matriz_resultado[i,j] = "MB"
            elif 0.005 < valor <= 0.01:
                matriz_resultado[i,j] = "B"
            else:
                matriz_resultado[i,j] = "M"
            
    return matriz_resultado
            
def evaluacion(matriz_a_evaluar):
    msj = ""
    m_cont = 0
    mb_cont = 0
    b_cont = 0
    mitad = int(0.5 * np.size(matriz_a_evaluar))
    tercio = int(0.3 * np.size(matriz_a_evaluar))
    
    for i in range(1165):
        for j in matriz_a_evaluar[i]:
            if j == "M":
                m_cont +=1
            if j == "MB":
                mb_cont+=1
            else:
                b_cont+=1
    
    if m_cont >= mitad:
        msj = "¡Vas por buen camino, pulamos más detalles y sigamos bailando! ;)"
    elif m_cont <= tercio and mb_cont >= tercio:
        msj = "¿No serás idol? #yen2aCorea"
    else:
        msj = "¡Vas re bien! Sacando unos detallitos, casi que sos idol :D"
    
    return msj

prueba1 = comparar(matriz_1_x, matriz_2_x)

