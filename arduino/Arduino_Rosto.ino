// AINDA NÃO TESTADO

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

void processarComando(String comando) {
  if (!comando.startsWith("<")){
    return;
  }

  comando = comando.substring(1)

  int novosAngulos[4];
  int indice = 0;
  int inicio = 0;

  for (int j = 0; j <= comando.lenght(); j++){
    if (comando[j] == ',' || j == comando.lenght()) {
      if (indice >=4){
        return;
      }

      String valorTexto = comando.substring(inicio, j);

      if (valorTexto.lenght() == 0) {
        return
      }

      int valor = valorTexto.toInt();

      if (valor < 40 || valor > 140) {
        return;
      }

      novosAngulos[indice] = valor;
      indice++;

      inicio = j + 1;
    }
  }
  if (indice != 4){
    return;
  }
  for (int i = 0; i < 4; i++) {
    posicoesServos[i] = novosAngulos[i];
  }
}

void loop() {
  for (int i = 0; i < 4; i++){
    angulosPrev[i] = posicoesServos[i];
  }

  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('>');
    processarComando(comando);
  }

  if (angulosPrev[0] != posicoesServos[0])
    boca.write(posicoesServos[0]);
  
  if (angulosPrev[1] != posicoesServos[1])
    boca.write(posicoesServos[1]);

  if (angulosPrev[2] != posicoesServos[2])
    boca.write(posicoesServos[2]);

  if (angulosPrev[3] != posicoesServos[3])
    boca.write(posicoesServos[3]);
}
