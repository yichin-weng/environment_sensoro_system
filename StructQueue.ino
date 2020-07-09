/*
 * Example of a basic FreeRTOS queue
 * https://www.freertos.org/Embedded-RTOS-Queues.html
 */

// Include Arduino FreeRTOS library
#include <Arduino_FreeRTOS.h>

// Include queue support
#include <queue.h>

// Include the part we need in CO2 sensor
#include <SoftwareSerial.h>
#include <MHZ.h>

// Define a struct
struct ppm {
  int ppm_uart;
  int ppm_pwm;
};

// macro for instantiation
#define CO2_IN 10 // pin for pwm reading
#define MHZ14A_RX 11 // pin for UART RX
#define MHZ14A_TX 12 // pin for UART TX

// static instantiation of Sensor we will use
MHZ co2(MH_Z14_RX, MH_Z14_TX, CO2_IN, MHZ14A);

//
// Declaring a global variable of type QueueHandle_t
//

QueueHandle_t structQueue;

void setup() {

  /**
   * Create a queue.
   * https://www.freertos.org/a00116.html
   */
  structQueue = xQueueCreate(10, // Queue length
                              sizeof(struct ppm) // Queue item size unit(bytes)
                              );
  
  if (structQueue != NULL) {
    
    // Create task that consumes the queue if it was created.
    xTaskCreate(TaskSerial, // Task function
                "Serial", // A name just for humans
                128,  // This stack size can be checked & adjusted by reading the Stack Highwater
                NULL, 
                2, // Priority, with 3 (configMAX_PRIORITIES - 1) being the highest, and 0 being the lowest.
                NULL);

    xTaskCreate(TaskSensor, // Task function for sensor control
                "Sensor1", // A name just for humans
                128, //
                NULL,
                2, // it means it is important to execute this task
                NULL
    );
}

void loop() {}


/**
 * periodic task to read data from CO2 sensor
 * Reads an analog input on pin 0 and send the readed value through the queue.
 * See Blink_AnalogRead example.
 */
void TaskSensor(void *pvParameters)
{
  (void) pvParameters;
  co2.calibrate();
  for (;;)
  {
    int ppm_uart = co2.readCO2UART();

    /**
     * Post an item on a queue.
     * https://www.freertos.org/a00117.html
     */
    xQueueSend(structQueue, &currentPinRead, portMAX_DELAY);

    // One tick delay (15ms) in between reads for stability
    vTaskDelay(1);
  }
}

/**
 * Serial task.
 * Prints the received items from the queue to the serial monitor.
 */
void TaskSerial(void * pvParameters) {
  (void) pvParameters;

  // Init Arduino serial
  Serial.begin(9600);

  // Wait for serial port to connect. Needed for native USB, on LEONARDO, MICRO, YUN, and other 32u4 based boards.
  while (!Serial) {
    vTaskDelay(1);
  }
  
  for (;;) 
  {

    struct pinRead currentPinRead;

    /**
     * Read an item from a queue.
     * https://www.freertos.org/a00118.html
     */
    if (xQueueReceive(structQueue, &currentPinRead, portMAX_DELAY) == pdPASS) {
      Serial.print("Pin: ");
      Serial.print(currentPinRead.pin);
      Serial.print(" Value: ");
      Serial.println(currentPinRead.value);
    }
  }
}

