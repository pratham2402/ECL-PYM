#include <Arduino_OV767X.h>
#include <ei_run_classifier.h>

// Camera resolution — match this with your model's input dimensions
#define EI_CAMERA_WIDTH 96
#define EI_CAMERA_HEIGHT 96

// Image buffer
static uint8_t image_buffer[EI_CAMERA_WIDTH * EI_CAMERA_HEIGHT];

// Setup
void setup() {
  Serial.begin(115200);
  while (!Serial);

  // Initialize camera
  if (!Camera.begin(EI_CAMERA_WIDTH, EI_CAMERA_HEIGHT, CAMERA_RGB565, 1)) {
    Serial.println("Failed to initialize camera!");
    while (1);
  }

  Serial.println("Camera initialized. Starting inference...");
}

// Convert RGB565 to grayscale
void rgb565_to_grayscale(uint8_t *gray_buf, uint8_t *rgb565_buf, int width, int height) {
  for (int i = 0; i < width * height; i++) {
    uint16_t pixel = ((uint16_t *)rgb565_buf)[i];
    uint8_t r = (pixel >> 11) & 0x1F;
    uint8_t g = (pixel >> 5) & 0x3F;
    uint8_t b = pixel & 0x1F;

    // Convert to 8-bit grayscale (approximation)
    gray_buf[i] = (uint8_t)(((r << 3) * 30 + (g << 2) * 59 + (b << 3) * 11) / 100);
  }
}

// Main loop
void loop() {
  if (!Camera.capture()) {
    Serial.println("Image capture failed!");
    return;
  }

  // Convert captured RGB565 image to grayscale
  rgb565_to_grayscale(image_buffer, Camera.getRGB565(), EI_CAMERA_WIDTH, EI_CAMERA_HEIGHT);

  // Create a signal from the image buffer
  signal_t signal;
  int ret = numpy::signal_from_buffer(image_buffer, EI_CAMERA_WIDTH * EI_CAMERA_HEIGHT, &signal);
  if (ret != 0) {
    Serial.print("Failed to create signal: ");
    Serial.println(ret);
    return;
  }

  // Run the model
  ei_impulse_result_t result = { 0 };
  EI_IMPULSE_ERROR res = run_classifier(&signal, &result, false);
  if (res != EI_IMPULSE_OK) {
    Serial.print("Inference failed: ");
    Serial.println(res);
    return;
  }

  // Print classification results
  Serial.println("=== Prediction ===");
  for (size_t ix = 0; ix < result.classification.count; ix++) {
    ei_printf("  %s: %.2f\n", result.classification[ix].label, result.classification[ix].value);
  }

  // Optional: Delay before next capture
  delay(2000);
}
