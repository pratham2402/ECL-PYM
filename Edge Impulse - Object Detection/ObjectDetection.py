#include <Arduino.h>
#include <Wire.h>
#include <ei_run_classifier.h>
#include <Arduino_OV767X.h> // For camera module

// Set resolution (change if your project uses different input size)
#define EI_CAMERA_WIDTH 96
#define EI_CAMERA_HEIGHT 96

// Create image buffer
static uint8_t image_buffer[EI_CAMERA_WIDTH * EI_CAMERA_HEIGHT];

// Setup camera
void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!Camera.begin(EI_CAMERA_WIDTH, EI_CAMERA_HEIGHT, CAMERA_RGB565, 1)) {
    Serial.println("Failed to initialize camera!");
    while (1);
  }

  ei_printf("Camera initialized\n");
}

// Convert RGB565 to Grayscale (Edge Impulse expects grayscale or RGB888 usually)
void rgb565_to_grayscale(uint8_t *gray_buf, uint8_t *rgb565_buf, int width, int height) {
  for (int i = 0; i < width * height; i++) {
    uint16_t pixel = ((uint16_t *)rgb565_buf)[i];
    uint8_t r = (pixel >> 11) & 0x1F;
    uint8_t g = (pixel >> 5) & 0x3F;
    uint8_t b = pixel & 0x1F;

    // Convert to 8-bit grayscale
    uint8_t gray = (r << 3) * 0.3 + (g << 2) * 0.59 + (b << 3) * 0.11;
    gray_buf[i] = gray;
  }
}

void loop() {
  if (!Camera.capture()) {
    Serial.println("Failed to capture image");
    return;
  }

  // Convert RGB565 to grayscale
  rgb565_to_grayscale(image_buffer, Camera.getRGB565(), EI_CAMERA_WIDTH, EI_CAMERA_HEIGHT);

  // Setup signal from buffer
  signal_t signal;
  int ret = numpy::signal_from_buffer(image_buffer, EI_CAMERA_WIDTH * EI_CAMERA_HEIGHT, &signal);
  if (ret != 0) {
    ei_printf("Failed to create signal from buffer (%d)\n", ret);
    return;
  }

  // Run inference
  ei_impulse_result_t result = { 0 };
  EI_IMPULSE_ERROR res = run_classifier(&signal, &result, false);
  if (res != EI_IMPULSE_OK) {
    ei_printf("Classification failed (%d)\n", res);
    return;
  }

  // Print results
  ei_printf("Predictions:\n");
  for (size_t ix = 0; ix < result.classification.count; ix++) {
    ei_printf("  %s: %.2f\n", result.classification[ix].label, result.classification[ix].value);
  }

  // Optional delay
  delay(2000);
}
