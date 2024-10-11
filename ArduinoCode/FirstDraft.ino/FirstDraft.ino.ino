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

// Servo Motor
Servo myservo;  // create servo object to control a servo

int servo_pin = 0;  // analog pin used to connect the potentiometer
int servo_value;

// CO2 Sensor
#define RX_PIN 2       // Rx pin which the MHZ19 Tx pin is attached to
#define TX_PIN 3       // Tx pin which the MHZ19 Rx pin is attached to
#define BAUDRATE 9600  // Device to MH-Z19 Serial baudrate (should not be changed)

MHZ19 myMHZ19;                            // Constructor for library
SoftwareSerial mySerial(RX_PIN, TX_PIN);  // (Uno example) create device to MH-Z19 serial

unsigned long getDataTimer = 0;

void setup() {

  Serial.begin(9600);  // Device to serial monitor feedback

  // start DHT
  dht.begin();

  // start LCD
  lcd.begin(16, 2);

  // start and reset servo
  myservo.attach(8);

  if (myservo.read() != 0) {
    myservo.write(0);
  }

  // Start CO2 sensor
  mySerial.begin(BAUDRATE);  // (Uno example) device to MH-Z19 serial start
  myMHZ19.begin(mySerial);   // *Serial(Stream) refence must be passed to library begin().
  myMHZ19.autoCalibration();
}

void loop() {

  if (millis() - getDataTimer >= 10000) {
    lcd.clear();

    float humidity = dht.readHumidity();
    float temp = dht.readTemperature();
    float co2 = GetCo2();

    PrintDataToLCD(temp, humidity, co2);

    SendSerialMessage(temp, humidity, co2);

    

    getDataTimer = millis();
  }
}

void OpenWindow() {
  int currentAngle = myservo.read();

  if (currentAngle < 90) {
    for (int pos = 0; pos <= 90; pos += 1) {
      myservo.write(pos);
      delay(15);
    }
  } else {
    for (int pos = currentAngle; pos >= 90; pos -= 1) {
      myservo.write(pos);
      delay(15);
    }
  }
}

void CloseWindow() {
  int currentAngle = myservo.read();

  if (currentAngle > 0) {
    for (int pos = currentAngle; pos <= 0; pos -= 1) {
      myservo.write(pos);
      delay(15);
    }
  }
}

float GetCo2() {
  int CO2;

  CO2 = myMHZ19.getCO2();  // Request CO2 (as ppm)

  Serial.print("CO2 (ppm): ");
  Serial.println(CO2);

  return CO2;
}

void PrintDataToLCD(float temperature, float humidity, float co2) {
  lcd.noAutoscroll();

  // log temperature
  lcd.clear();
  lcd.setCursor(0, 0);

  String tempMessage = "Temp.: " + String(temperature) + " C";
  int messageLength = tempMessage.length();

  char chars[messageLength];

  tempMessage.toCharArray(chars, messageLength + 1);

  for (int i = 0; i < tempMessage.length(); i++) {
    lcd.write(chars[i]);
    delay(50);
  }

  delay(3000);

  // log humudity
  lcd.clear();
  lcd.setCursor(0, 0);

  String humMessage = "Humid.: " + String(humidity) + " %";
  int humMessageLength = humMessage.length();

  char humChars[humMessageLength];

  humMessage.toCharArray(humChars, humMessageLength + 1);

  for (int i = 0; i < humMessageLength; i++) {
    lcd.write(humChars[i]);
    delay(50);
  }
  delay(3000);

  // log co2
  lcd.clear();
  lcd.setCursor(0, 0);

  String co2Message = "CO2: " + String(co2) + " PPM";
  int co2MessageLength = co2Message.length();

  char cChars[co2MessageLength];

  co2Message.toCharArray(cChars, co2MessageLength + 1);

  for (int i = 0; i < co2MessageLength; i++) {
    lcd.write(cChars[i]);
    delay(50);
  }

  delay(3000);
}

void WriteMessageToLCD(String message) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(message);
}

void SendSerialMessage(float temperature, float humidity, float co2) {
  String temperatureStr = "\"temperature\": " + String(temperature);
  String humidityStr = "\"humidity\": " + String(temperature);
  String co2Str = "\"co2\": " + String(temperature);

  String jsonMessage = "{ " + temperatureStr + ", " + humidityStr + ", " + co2Str + " }";

  Serial.println(jsonMessage);
}