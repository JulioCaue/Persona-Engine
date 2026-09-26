from animation.olhos import FaceTracker
import animation.boca as boca
import cv2 as cv
import threading


#dar um dicionario?
#controla todo o sistema de movimentação?

#ESSE CODIGO AINDA É CONCEITUAL! NÃO DAR COMMIT (no main branch :P)!
#tudo aqui pode ser removido no futuro. Apenas ideias ainda. Ficará oque funcionar.
dict_anim = {
    "eye_value": 0.92,
    "mouth_value": 0.50,
    "eyebrow_value": 0.27
}

mouth_options = {
    "audio": boca.sincronizar_com_audio,
    "microfone": boca.sincronizar_com_microfone
}

class AnimControl():
    def __init__(self) -> None:
        self.will_speak = False
        self.is_speaking = False
        self.is_looking  = False
        self.eye_weight = None
        self.mouth_weight = None
        self.eyebrow_weight = None

        self.prev_eye_value = None
        self.prev_mouth_value = None
        self.prev_eyebrow_value = None

        self.olhos = FaceTracker()
        self.detector = self.olhos.detector

    def get_mouth_pos(self):
        #aqui fazer a atual posição da boca no loop (loop maior que pega tudo)
        pass

    def get_eye_pos(self):
        #aqui achar rosto e mover o olho
        pass

    def eyebrow(self):
        #???
        #como fazer isso?
        pass

    def send_final_commands(self):
        current_eye_value = dict_anim["eye_value"]
        current_mouth_value = dict_anim["mouth_value"]
        current_eyebrow_value = dict_anim["eyebrow_value"]

        if current_eye_value != self.prev_eye_value:
            pass #send?
            self.prev_eye_value = current_eye_value

        if current_mouth_value != self.prev_mouth_value:
            pass #send?
            self.prev_mouth_value = current_mouth_value

        if current_eyebrow_value != self.prev_eyebrow_value:
            pass #send?
            self.prev_eyebrow_value = current_eyebrow_value


    def test_final(self,speech_type,will_speak, is_looking):
        #funcao separada para teste de completa

        #atribuições idiotas e placeholder por enquanto. Talvez sejam deletadas
        self.will_speak = will_speak

        self.is_looking = is_looking

        # usar while not parar_modo.is_set() no loop real?
        with self.detector:
            while True: #seria o loop principal pra TODAS AS ANIM

                #captura cada frame, fora daqui faz só o primeiro. Quem diria!
                resultado_centro_rosto = self.olhos.pegar_rosto_centro_atual()

                if self.will_speak:
                    #speech type will be string
                    if not self.is_speaking:
                        speaker_thread = threading.Thread(target=mouth_options[speech_type],daemon=True)
                        speaker_thread.start()
                        self.is_speaking = True

                #movimento da boca
                if self.is_looking:
                    self.olhos.seguir_rosto(resultado_centro_rosto)

                #TODO movimento da sobrancelha / func da sobrancelha

        if self.olhos.cap or not self.is_looking:
            self.olhos.cap.release()
            cv.destroyAllWindows()


controler = AnimControl()

#usar isso para um possivel loop com flag da func de olhos?
speech_type = "audio"
will_speak = True
is_looking = True

controler.test_final(speech_type,will_speak,is_looking)