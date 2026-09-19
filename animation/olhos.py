"""
Arquivo usado para enviar comandos ao arduino.
Usa volume no arquivo wav para criar comandos para os servos.
"""

import mediapipe as mp
import requests
import cv2 as cv
import time

#suprimir mensagens de erros do ALSA
from ctypes import cdll, CFUNCTYPE, c_char_p, c_int
_alsa_handler_ref = None

try:
    _HANDLER_TYPE = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
    _alsa_handler_ref = _HANDLER_TYPE(lambda *_: None)  # guardado na global
    cdll.LoadLibrary('libasound.so.2').snd_lib_error_set_handler(_alsa_handler_ref)
except Exception:
    pass

#continua normalmente

def pegar_face_centro_atual(cap,detector):
    """Olha o frame atual da webcam e retorna o centro de um rosto detectado."""


    # Capturar frame por frame
    ret, frame = cap.read()
    
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    timestamp_ms = time.monotonic_ns() // 1_000_000

    detection_result = detector.detect_for_video(mp_image, timestamp_ms)

    if detection_result.detections:
        detections = detection_result.detections[0]
        box = detections.bounding_box

        image_x = box.origin_x
        image_y = box.origin_y
        width = box.width
        height = box.height

        #pega o maximo do eixo horizontal x (largura) e maximo vertical y (altura)
        altura, largura = frame.shape[:2]

        min_x = 0
        max_x = largura - 1

        min_y = 0
        max_y = altura - 1

        ponto_inicial = (image_x,image_y)
        ponto_final = (image_x + width, image_y + height)

        color = (0, 255, 0)

        cv.rectangle(frame, ponto_inicial, ponto_final, color)

        cv.imshow('Visão do modelo', frame)
        
        if cv.waitKey(1) == ord('q'):
            return

        return image_x, image_y, max_x, min_x



def seguir_rosto():
    """
    segue o rosto do usuario com os olhos (horizontal apenas).
    """

    face_recognizer_model_path = 'testes/blaze_face_short_range.tflite'

    BaseOptions = mp.tasks.BaseOptions
    FaceDetector = mp.tasks.vision.FaceDetector
    FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    # Create a face detector instance with the image mode:
    options = FaceDetectorOptions(
        base_options=BaseOptions(model_asset_path = face_recognizer_model_path),
        running_mode=VisionRunningMode.VIDEO
    )

    # --- variaveis de movimento ---
    min_x = 30
    max_x = 170
    olho_centro = 90
    ALPHA = 0.8
    angulo_anterior = olho_centro


    with FaceDetector.create_from_options(options) as detector:
        cap = cv.VideoCapture("/dev/video0") #caminho da camera
        if not cap.isOpened():
            print("Camera não foi aberta")
            exit()
        # --- inicio da conexão ---
        try:
            while True:
                resultado_frame = pegar_face_centro_atual(cap,detector)

                if resultado_frame:
                    image_x, width, max_x, min_x = resultado_frame

                    centro_x = image_x + width / 2

                #suaviza o angulo atual para movimentos menos brutos
                angulo_suavizado = ALPHA * centro_x + (1 - ALPHA) * angulo_anterior

                #transforma angulo final em valor que bottango entende (entre 0.0 e 1.0)
                valor_angulo_final = round((centro_x - min_x) / (max_x - min_x),3)
                valor_angulo_final = max(0.0, min(1.0, valor_angulo_final))

                #Envia angulos direto para o bottango pois o codigo do arduino que observa a porta serial é substituido quando uma animação do arduino é tocada.

                if not angulo_anterior or abs(valor_angulo_final - angulo_anterior) > 0.010:
                    print(valor_angulo_final)
                    respose = requests.put(
                        "http://localhost:59224/ControlInput/",
                        json={
                            "identifier": "mexerOlhos",
                            "value": valor_angulo_final
                        }
                    )

                    respose.raise_for_status()
                angulo_anterior = valor_angulo_final

        except Exception as e:
            print(e)

    cap.release()
    cv.destroyAllWindows()


seguir_rosto()