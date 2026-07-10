//bibliotecas
#include <Servo.h>

int servoPalpebraPin=6;
int servoOlhoEsquerdoPin=10;
int servoOlhoDireitoPin=5;
int servoBocaPin=9;

Servo boca;
Servo olhoEsquerdo;
Servo olhoDireito;
Servo palpebra;

//vetor de posiçoes dos servos, nessa ordem: boca, olho esquerdo, olho direito, palpebra
int posicoesServos[4] = {40, 90, 90, 40};
int angulosPrev[4];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.setTimeout(10);
  
  boca.attach(servoBocaPin);
  olhoEsquerdo.attach(servoOlhoEsquerdoPin);
  olhoDireito.attach(servoOlhoDireitoPin);
  palpebra.attach(servoPalpebraPin);

  boca.write(posicoesServos[0]);
  olhoEsquerdo.write(posicoesServos[1]);
  olhoDireito.write(posicoesServos[2]);
  palpebra.write(posicoesServos[3]);
}

void loop() {
  for (int i = 0; i < 4; i++){
    angulosPrev[i] = posicoesServos[i];
  }

  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('>');
    if (comando.startsWith("<")) {
      comando = comando.substring(1); // remove o '<'
      
      int i = 0;
      int inicio = 0;
      for (int j = 0; j <= comando.length(); j++) {
        if (comando[j] == ',' || j == comando.length()) {
          posicoesServos[i++] = comando.substring(inicio, j).toInt();
          inicio = j + 1;
        }
      }
    }
  }
  for (int i = 0; i < 4; i++){
    if (angulosPrev[i] != posicoesServos[i]){
      boca.write(posicoesServos[0]);
      olhoEsquerdo.write(posicoesServos[1]);
      olhoDireito.write(posicoesServos[2]);
      palpebra.write(posicoesServos[3]);
    }
  }
}