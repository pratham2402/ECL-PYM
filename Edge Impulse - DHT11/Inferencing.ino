#include <DHT.h>
#include <DHT11_Environment_Classification_inferencing.h>  // Edge Impulse model

#define DHTPIN A6
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

float features[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE];

// Required function to provide signal data to the classifier
int get_feature_callback(size_t offset, size_t length, float *out_ptr) {
  memcpy(out_ptr, features + offset, length * sizeof(float));
  return 0;
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  delay(1000);
  Serial.println("Edge Impulse Inferencing Started!");
}

void loop() {
  // Read sensor values
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Sensor read failed");
    delay(1000);
    return;
  }

  // Fill the features buffer (duplicate values for simplicity)
  for (size_t i = 0; i < EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE; i += 2) {
    features[i] = temperature;
    features[i + 1] = humidity;
  }

  // Create signal object
  signal_t signal;
  signal.total_length = EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE;
  signal.get_data = &get_feature_callback;

  // Run the classifier
  ei_impulse_result_t result = { 0 };
  EI_IMPULSE_ERROR res = run_classifier(&signal, &result, false);

  if (res != EI_IMPULSE_OK) {
    Serial.print("Inference failed: ");
    Serial.println(res);
    return;
  }

  // Print predictions
  Serial.println("Predictions:");
  for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
    Serial.print("  ");
    Serial.print(result.classification[ix].label);
    Serial.print(": ");
    Serial.println(result.classification[ix].value, 4);
  }

  delay(2000);  // Wait 2 seconds before next inference
}
