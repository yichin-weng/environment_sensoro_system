#include <SoftwareSerial.h>
#include <MHZ.h>
#include <semphr.h>

//
// Declaring a global variable of
//

// Include FreeRTOS library
#include <Arduino_FreeRTOS.h>

// Include queue support
#include <queue.h>

// pin for pwm reading
#define CO2_IN 10

// pin for uart reading
#define MH_Z14_RX 11  // Uart3_Rx
#define MH_Z14_TX 12  // Uart3_Tx

MHZ co2(MH_Z14_RX, MH_Z14_TX, CO2_IN, MHZ14A);

SemaphoreHandle_t interruptSemaphore;

void setup() {
  Serial.begin(9600);
  pinMode(CO2_IN, INPUT);
  delay(100);
  Serial.println("MHZ 14A");

  xTaskCreate(TaskSerial, // Task function
  "Serial", // Task serial
  128, // Stack Size
  NULL,
  0, // Priority
  NULL
  );

  interruptSemaphore = xSemamphoreCreateBinary();
  if ( interruptSemaphore != NULL ) {
    // Attach interrupt for Arduino digital pin
    attachInterrupt(digital)
  }

  // enable debug to get addition information
  // co2.setDebug(true);

  if (co2.isPreHeating()) {
    Serial.print("Preheating");
//    while (co2.isPreHeating()) {
//      Serial.print(".");
//      delay(5000);
//    }
    Serial.println();
  }
  
  int calib = co2.calibrate();
  Serial.print(calib);
}

// loop can not be used.

void loop() {
  Serial.print("\n----- Time from start: ");
  Serial.print(millis() / 1000);
  Serial.println(" s");

  int ppm_uart = co2.readCO2UART();
  Serial.print("PPMuart: ");

  if (ppm_uart > 0) {
    Serial.print(ppm_uart);
  } else {
    Serial.print(ppm_uart);
    Serial.print("n/a");
  }

  int ppm_pwm = co2.readCO2PWM();
  Serial.print(", PPMpwm: ");
  Serial.print(ppm_pwm);

  int temperature = co2.getLastTemperature();
  Serial.print(", Temperature: ");

  if (temperature > 0) {
    Serial.println(temperature);
  } else {
    Serial.println("n/a");
  }

  Serial.println("\n------------------------------");
  delay(2000);
}
