#ifndef BTN_H
#define BTN_H
#include <Arduino.h>

class Btn {
public:
  int pino;
  bool btn_liberado, btn_clicado;
  bool detectar_subida;          // Indica se a borda de subida será detectada
  Btn(int p, bool subida = true) // `subida` é true por padrão (borda de subida)
  {
    pino = p;
    detectar_subida = subida;
    btn_liberado = btn_clicado = 0;
    pinMode(pino, INPUT); // Configura o pino como entrada
  }

  bool press() {
    bool estado_atual = digitalRead(pino);

    if (detectar_subida) // Detectar borda de subida
    {
      if (estado_atual) {
        btn_liberado = 0;
        btn_clicado = 1;
      } else {
        btn_liberado = 1;
      }
    } else // Detectar borda de descida
    {
      if (!estado_atual) {
        btn_liberado = 0;
        btn_clicado = 1;
      } else {
        btn_liberado = 1;
      }
    }

    if (btn_clicado && btn_liberado) {
      btn_liberado = btn_clicado = 0;
      return true;
    } else {
      return false;
    }
  }
};

#endif // BTN_H
