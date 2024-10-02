#include <LiquidCrystal.h>
#include <DHT.h>

#define DHTPIN 13

#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

const int rs = 10, en = 9, d4 = 7, d5 = 6, d6 = 5, d7 = 4;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);


void setup() {

// Serial.begin(9600);

dht.begin();

lcd.begin(16, 2);
}

void loop() {

  lcd.clear();

  float humidity = dht.readHumidity();
  float temp = dht.readTemperature();

  lcd.setCursor(0,0);
  lcd.print("hi");
  lcd.print("Temp: ");
  lcd.print(temp);
  lcd.print(" C");
  // Serial.print("Temp: ");
  // Serial.print(temp);
  // Serial.println();
  
  lcd.setCursor(0,1);
  lcd.print("Hum.: ");
  lcd.print(humidity);
  lcd.print(" %");
  delay(2000);
}