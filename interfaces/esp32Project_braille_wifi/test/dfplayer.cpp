#include <Arduino.h>
#include "DFRobotDFPlayerMini.h"

// Use pins 26 and 27 to communicate with DFPlayer Mini
#define PIN_MP3_TX 26 // Connects to module's RX 
#define PIN_MP3_RX 27 // Connects to module's TX 
#define LED_BOARD 2

// Create the Player object
DFRobotDFPlayerMini player;

void setup() {
  // Init USB serial port for debugging
  Serial.begin(9600);
  pinMode(LED_BOARD, OUTPUT);

  // Init Serial1 for DFPlayer Mini
  Serial1.begin(9600, SERIAL_8N1, PIN_MP3_RX, PIN_MP3_TX);
  digitalWrite(LED_BOARD, 1);

  // Start communication with DFPlayer Mini
  if (!player.begin(Serial1)) {
    Serial.println("Connecting to DFPlayer Mini failed!");
    while (true);
  } 
  else {
    digitalWrite(LED_BOARD, 0);
    Serial.println("Connection OK");

    // Set volume to maximum (0 to 30).
    player.volume(30);
    // Play the first MP3 file on the SD card
    player.play(1);
  } 
}

void loop() {
  if (Serial.available() > 0) {
    String buffer = Serial.readStringUntil('\n');
    int buffer_length = buffer.length();
    String data = buffer.substring(0,buffer_length);
    int index = data.toInt();
    player.play(index);
    delay(200);
  }
}

