#include <Servo.h>
#include <LiquidCrystal.h>
#include <DHT.h>
#include <Arduino.h>
#include "MHZ19.h"
#include <SoftwareSerial.h>


// DHT Sensor
#define DHTPIN 13

#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

// LCD
const int rs = 10, en = 9, d4 = 7, d5 = 6, d6 = 5, d7 = 4;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// CO2 Sensor
#define RX_PIN 2       // Rx pin which the MHZ19 Tx pin is attached to
#define TX_PIN 3       // Tx pin which the MHZ19 Rx pin is attached to
#define BAUDRATE 9600  // Device to MH-Z19 Serial baudrate (should not be changed)

MHZ19 myMHZ19;                            // Constructor for library
SoftwareSerial mySerial(RX_PIN, TX_PIN);  // (Uno example) create device to MH-Z19 serial

unsigned long getDataTimer = 0;

float humidity = 0;
float temp = -100;
float co2 = 0;

void setup() {

  Serial.begin(9600);  // Device to serial monitor feedback

  // start DHT
  dht.begin();

  // start LCD
  lcd.begin(16, 2);


  // Start CO2 sensor
  mySerial.begin(BAUDRATE);  // (Uno example) device to MH-Z19 serial start
  myMHZ19.begin(mySerial);   // *Serial(Stream) refence must be passed to library begin().
  myMHZ19.autoCalibration();

}

void loop() {

  if (millis() - getDataTimer >= 12000) {

    humidity = dht.readHumidity();
    temp = dht.readTemperature();
    co2 = GetCo2();

    PrintDataToLCD(temp, humidity, co2);

    SendSerialMessage(temp, humidity, co2);
    
    getDataTimer = millis();
  }
}


float GetCo2() {
  int CO2;

  CO2 = myMHZ19.getCO2();  // Request CO2 (as ppm)

  return CO2;
}

void PrintDataToLCD(float temperature, float humidity, float co2) {
  // log temperature
  lcd.clear();
  lcd.setCursor(0, 0);

  String tempMessage = "Temp.: " + String(temperature) + " C";
  lcd.print(tempMessage);

  delay(2500);

  // log humudity
  lcd.clear();
  lcd.home();

  String humMessage = "Humid.: " + String(humidity) + " %";
  lcd.print(humMessage);
  delay(2500);

  // log co2
  lcd.clear();
  lcd.home();

  String co2Message = "CO2: " + String(co2) + " PPM";
  lcd.print(co2Message);

  delay(2500);

}

void WriteMessageToLCD(String message) {
  int messageLength = message.length();

  lcd.clear();

  if (messageLength <= 16) {
    lcd.setCursor(0, 0);
    lcd.print(message);
  } else {
    lcd.setCursor(3, 0);
    lcd.print(message);

    for (int i = (messageLength - 13); i >= 0; i--) {
      lcd.scrollDisplayLeft();
      delay(750);
    }
  }
}

void SendSerialMessage(float temperature, float humidity, float co2) {

  String temperatureStr = "\"temperature\": " + String(temperature);
  String humidityStr = "\"humidity\": " + String(humidity);
  String co2Str = "\"co2\": " + String(co2);

  String jsonMessage = "{ " + temperatureStr + ", " + humidityStr + ", " + co2Str +  " }";

  Serial.println(jsonMessage);
  delay(1000);
}


// void ReadAndProcessSerialMessage(String message) {

//   if (message == "OPEN") {
//     OpenWindow();
//   } else if (message == "CLOSE") {
//     CloseWindow();
//     alert = false;
//   } else if (message == "ALERT") {
//     alert = true;
//   } else if (message == "DATA") {
//     Serial.read();
    
//     SendSerialMessage(temp, humidity, co2, windowIsOpen);
//   } else {
//     WriteMessageToLCD(message);
//   }

//   lcd.clear();
// }