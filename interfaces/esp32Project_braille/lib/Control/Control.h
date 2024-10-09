#ifndef CONTROL_H
#define CONTROL_H
bool output[6];

void reset_output(void) {
  for (int i = 0; i < 6; i++) {
    output[i] = 0;
  }
}

void define_caractere(char caractere) {
  switch (caractere) {
  case 97: // a
    output[0] = 1;
    break;
  case 98: // b
    output[0] = 1;
    output[1] = 1;

    break;
  case 99: // c
    output[0] = 1;
    output[3] = 1;

    break;
  case 100: // d
    output[0] = 1;
    output[3] = 1;
    output[4] = 1;

    break;
  case 101: // e
    output[0] = 1;
    output[4] = 1;

    break;
  case 102: // f
    output[0] = 1;
    output[1] = 1;
    output[3] = 1;

    break;
  case 103: // g
    output[0] = 1;
    output[1] = 1;
    output[3] = 1;
    output[4] = 1;

    break; // h
  case 104:
    output[0] = 1;
    output[1] = 1;
    output[4] = 1;

    break;
  case 105: // i
    output[1] = 1;
    output[3] = 1;

    break;
  case 106: // j
    output[1] = 1;
    output[3] = 1;
    output[4] = 1;

    break;
  case 107: // k
    output[0] = 1;
    output[2] = 1;

    break;
  case 108: // l
    output[0] = 1;
    output[1] = 1;
    output[2] = 1;

    break;
  case 109: // m
    output[0] = 1;
    output[2] = 1;
    output[3] = 1;

    break;
  case 110: // n
    output[0] = 1;
    output[2] = 1;
    output[3] = 1;
    output[4] = 1;

    break;
  case 111: // o
    output[0] = 1;
    output[2] = 1;
    output[4] = 1;

    break;
  case 112: // p
    output[0] = 1;
    output[1] = 1;
    output[2] = 1;
    output[3] = 1;

    break;
  case 113: // q
    output[0] = 1;
    output[1] = 1;
    output[2] = 1;
    output[3] = 1;
    output[4] = 1;

    break;
  case 114: // r
    output[0] = 1;
    output[1] = 1;
    output[2] = 1;
    output[4] = 1;

    break;
  case 115: // s
    output[1] = 1;
    output[2] = 1;
    output[3] = 1;

    break;
  case 116: // t
    output[1] = 1;
    output[2] = 1;
    output[3] = 1;
    output[4] = 1;

    break;
  case 117: // u
    output[0] = 1;
    output[2] = 1;
    output[5] = 1;

    break;
  case 118: // v
    output[0] = 1;
    output[1] = 1;
    output[2] = 1;
    output[5] = 1;

    break;
  case 119: // w
    output[1] = 1;
    output[3] = 1;
    output[4] = 1;
    output[5] = 1;

    break;
  case 120: // x
    output[0] = 1;
    output[2] = 1;
    output[3] = 1;
    output[5] = 1;

    break;
  case 121: // y
    output[0] = 1;
    output[2] = 1;
    output[3] = 1;
    output[4] = 1;
    output[5] = 1;

    break;
  case 122: // z
    output[0] = 1;
    output[2] = 1;
    output[4] = 1;
    output[5] = 1;

    break;

  default:
    for (int i = 0; i < 6; i++) { // inicia o array com 0
      output[i] = 0;

    }
    break;
  }
}


#endif // CONTROL_H
