#ifndef BUTTONS_H
#define BUTTONS_H
#include<Arduino.h>

class Btn
{
  public:
    int pino;
    bool btn_liberado, btn_clicado;
    bool ativo_alto; // Variável para configurar o botão como ativo alto ou baixo

    // Construtor modificado para incluir a configuração do tipo de botão (ativo alto ou baixo)
    Btn(int p, bool ativoAlto = true) // 'ativoAlto = true' significa padrão como ativo alto
    {
      pino = p;
      btn_liberado = btn_clicado = 0;
      ativo_alto = ativoAlto;
    }

    // Getter para retornar o pino
    int getPino() const
    {
      return pino;
    }

    // Função press modificada para considerar o tipo de ativação do botão
    bool press()
    {
      // Verifica se o botão está pressionado com base no tipo de ativação
      bool estado_btn = digitalRead(pino); 
      if (ativo_alto) // Caso o botão seja ativo alto
      {
        if (estado_btn == HIGH)
        {
          btn_liberado = 0;
          btn_clicado = 1;
        }
        else
        {
          btn_liberado = 1;
        }
      }
      else // Caso o botão seja ativo baixo
      {
        if (estado_btn == LOW)
        {
          btn_liberado = 0;
          btn_clicado = 1;
        }
        else
        {
          btn_liberado = 1;
        }
      }

      // Lógica para detectar o clique do botão
      if (btn_clicado && btn_liberado)
      {
        btn_liberado = btn_clicado = 0;
        return true;  // Botão pressionado e liberado
      }
      else
      {
        return false; // Botão ainda não foi liberado ou pressionado
      }
    }
};


#endif // !BUTTONS_H
