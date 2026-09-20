from olhos import FaceTracker
import cv2 as cv


#dar um dicionario?
#controla todo o sistema de movimentação?

#ESSE CODIGO AINDA É CONCEITUAL! NÃO DAR COMMIT!
dict_anim = {
    "eye_value": 0.92,
    "mouth_value": 0.50,
    "eyebrow_value": 0.27
}

class AnimControl():
    def __init__(self) -> None:
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


    def test_final(self):
        #funcao separada para teste de completa

        resultado_centro_rosto = self.olhos.pegar_rosto_centro_atual()

        # usar while not parar_modo.is_set() no loop real?
        with self.detector:
            while True: #seria o loop principal pra TODAS AS ANIM
                #movimento da boca
                self.olhos.seguir_rosto(resultado_centro_rosto)
                #movimento da sobrancelha

        self.olhos.cap.release()
        cv.destroyAllWindows()