#include "DHT.h"

#define DHTPIN A6        // Pin connected to DHT11
#define DHTTYPE DHT11    // DHT 11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Print data in CSV format: temperature,humidity
  Serial.print(temperature);
  Serial.print(",");
  Serial.println(humidity);

  delay(500); 
}