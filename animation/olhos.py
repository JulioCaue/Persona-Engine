"""
Arquivo usado para enviar comandos ao arduino.
Usa volume no arquivo wav para criar comandos para os servos.
"""

import mediapipe as mp
import requests
import cv2 as cv
import time
from logs import log_writer

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

class EyeTracker:
    def __init__(self) -> None:
        self.cap = cv.VideoCapture("/dev/video0") #caminho da camera
        self.FaceDetector = mp.tasks.vision.FaceDetector
        self.face_recognizer_model_path = 'testes/blaze_face_short_range.tflite'
        self.BaseOptions = mp.tasks.BaseOptions
        self.FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
        self.VisionRunningMode = mp.tasks.vision.RunningMode
        self.options = self.FaceDetectorOptions(
            base_options = self.BaseOptions(model_asset_path = self.face_recognizer_model_path),
            running_mode = self.VisionRunningMode.VIDEO
        )
        self.detector = self.FaceDetector.create_from_options(self.options)

        # --- variaveis de movimento ---
        self.min_x = 30
        self.max_x = 170
        self.olho_centro = 90
        self.ALPHA = 0.75
        self.angulo_anterior = None

        #angulos estão na perspectiva da cabeça
        self.angulo_max_direita = 30
        self.angulo_max_esquerda = 170

    def pegar_face_centro_atual(self):
        """Olha o frame atual da webcam e retorna o centro de um rosto detectado."""


        # Capturar frame por frame
        ret, frame = self.cap.read()

        if not ret:
            return
        
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        timestamp_ms = time.monotonic_ns() // 1_000_000

        detection_result = self.detector.detect_for_video(mp_image, timestamp_ms)

        if detection_result.detections:
            detections = detection_result.detections[0]
            box = detections.bounding_box

            image_x = box.origin_x
            image_y = box.origin_y
            width = box.width
            height = box.height

            #pega o maximo do eixo horizontal x (largura) e maximo vertical y (altura)
            #altura atualmente não usado por conta dos olhos apenas seguindo eixo x
            altura, largura = frame.shape[:2]

            ponto_inicial = (image_x,image_y)
            ponto_final = (image_x + width, image_y + height)

            color = (0, 255, 0)

            cv.rectangle(frame, ponto_inicial, ponto_final, color)

            cv.imshow('Visão do modelo', frame)
            
            if cv.waitKey(1) == ord('q'):
                return

            centro_x = image_x + (width / 2)

            #deixando aqui pois virá a ser util caso olhos ganhem movimento no eixo y
            #centro_y = image_y + (height / 2)

            return centro_x, largura


    def seguir_rosto(self):
        """
        segue o rosto do usuario com os olhos (horizontal apenas).
        """

        with self.detector:
            
            if not self.cap.isOpened():
                print("Camera não foi encontrada aberta")
                exit()
                return
            # --- inicio da conexão ---
            try:
                while True:
                    resultado_centro_rosto = self.pegar_face_centro_atual()

                    

                    if resultado_centro_rosto:
                        centro_x, largura = resultado_centro_rosto

                        angulo_atual = self.angulo_max_direita + (centro_x / largura) * (self.angulo_max_esquerda - self.angulo_max_direita)

                        if not self.angulo_anterior:
                            self.angulo_anterior = angulo_atual
                            angulo_suavizado = angulo_atual

                        else:
                            #suaviza o angulo atual para movimentos menos brutos
                            angulo_suavizado = (angulo_atual * self.ALPHA) + (self.angulo_anterior * (1 - self.ALPHA))

                        #transforma angulo final em valor que bottango entende (entre 0.0 e 1.0)
                        #conta: valor_bottango = (angulo - angulo_min) / (angulo_max - angulo_min)
                        
                        valor_angulo_final = round(
                            (
                                angulo_suavizado - self.angulo_max_direita
                            ) / (
                                self.angulo_max_esquerda - self.angulo_max_direita
                            ), 3
                        )


                        valor_angulo_final = max(0.0, min(1.0, valor_angulo_final))

                        #Envia angulos direto para o bottango pois o codigo do arduino que observa a porta serial é substituido quando uma animação do arduino é tocada.

                        if abs(valor_angulo_final - self.angulo_anterior) > 0.010:
                            print(valor_angulo_final)
                            response = requests.put(
                                "http://localhost:59224/ControlInput/",
                                json={
                                    "identifier": "mexerOlhos",
                                    "value": valor_angulo_final
                                }
                            )

                            response.raise_for_status()
                        self.angulo_anterior = valor_angulo_final

            except KeyboardInterrupt:
                try:
                    response = requests.put(
                        "http://localhost:59224/ControlInput/",
                        json={
                            "identifier": "mexerOlhos",
                            "value": valor_angulo_final
                        }
                    )

                    response.raise_for_status()

                except Exception as e:
                    log_writer.write(__name__, f"Ocorreu um problema durante o fechamento do track de olhos: {e}")

            except Exception as e:
                print(e)
                log_writer.write(__name__, e)


        self.cap.release()
        cv.destroyAllWindows()