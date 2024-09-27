#include <LiquidCrystal.h>
#include <DHT.h>

#define DHTPIN 13

#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

const int rs = 2, en = 3, d4 = 6, d5 = 7, d6 = 8, d7 = 9;
LiquidCrystal lcd (rs, en, d4, d5, d6, d7);



void setup() {

Serial.begin(9600);

dht.begin();

lcd.begin(16, 2);

}

void loop() {
  delay(2000);
  lcd.clear();
  lcd.setCursor(0,0);
  float humidity = dht.readHumidity();
  float temp = dht.readTemperature();

  lcd.print("Temp: ");
  lcd.print(temp);
  lcd.print(" C");

  lcd.setCursor(0,1);
  lcd.print("Hum.: ");
  lcd.print(humidity);
  lcd.print(" %");

}