#include <Wire.h>
#include "RunningAverage.h"

#define CALIBRATING_LED_PIN A3

#define NUMBER_OF_LAMPS 1
#define LAMP_0_ANALOG_PIN 0

// none can be on PORT B !!!
int lampsReadings[NUMBER_OF_LAMPS];
int lampsAnalogPins[NUMBER_OF_LAMPS] = {LAMP_0_ANALOG_PIN};
int lampFeedbackLedsPins[NUMBER_OF_LAMPS] = {2}; // 2, 3, 4
int lampThresholds[NUMBER_OF_LAMPS];

#define resolution 8
#define mains 50 
#define refresh 2 * 1000000 / mains

// all must be on PORT B !!!
#define NUMBER_OF_PRESENCE_SENSORS 2
#define PRESENCE_SENSOR_0_PIN 8
#define PRESENCE_SENSOR_1_PIN 9

int presenceSensorsPins[NUMBER_OF_PRESENCE_SENSORS] = {PRESENCE_SENSOR_0_PIN, PRESENCE_SENSOR_1_PIN};
int presenceSensorFeebackLedsPins[NUMBER_OF_PRESENCE_SENSORS] = {5,6}; // 5, 6, 7
byte presenceSensorsPinBitmasks[NUMBER_OF_PRESENCE_SENSORS] = {B00000001, B00000010};
int presenceSensorsThresholds[NUMBER_OF_PRESENCE_SENSORS];

RunningAverage presenceSensorsReadings[NUMBER_OF_PRESENCE_SENSORS] = {
  RunningAverage(10),
  RunningAverage(10)
};

#define I2C_SLAVE_ADDRESS 0x03
#define COMMS_BUFFER_SIZE 4
#define COMMAND_GET_LAMP 0
#define COMMAND_GET_PRESENCE 1
 
void setup(void) {
  Serial.begin(115200); // for debugging
  Serial.print("Started the i2c-sensors-worker, at i2c address x");
  Serial.println(I2C_SLAVE_ADDRESS, HEX);

  Wire.begin(I2C_SLAVE_ADDRESS);
  Wire.onReceive(i2c_receiveData);
  Wire.onRequest(i2c_sendData);

  // explicitely start each running average clean
  for (int i = 0; i < NUMBER_OF_PRESENCE_SENSORS; i++) {
    pinMode(presenceSensorsPins[i], INPUT);
    presenceSensorsReadings[i].clear();
  }

  // for presence sensor
  startTimer();

  pinMode(CALIBRATING_LED_PIN, OUTPUT);
  digitalWrite(CALIBRATING_LED_PIN, HIGH);

  Serial.print("Establishing thresholds for ");
  Serial.print(NUMBER_OF_PRESENCE_SENSORS);
  Serial.println(" presence sensors.");
  for (int i = 0; i < NUMBER_OF_PRESENCE_SENSORS; i++) {
    pinMode(presenceSensorFeebackLedsPins[i], OUTPUT);
    
    long sum = 0;
    for(int j = 0; j < 200; j++) {
      sum += time(presenceSensorsPins[i], presenceSensorsPinBitmasks[i]);
    }
    int baseline = sum / 200;
    presenceSensorsThresholds[i] = baseline * 1.003;
  }

  Serial.print("Establishing thresholds for ");
  Serial.print(NUMBER_OF_LAMPS);
  Serial.println(" lamp sensors.");
  for (int i = 0; i < NUMBER_OF_LAMPS; i++) {
    pinMode(lampFeedbackLedsPins[i], OUTPUT);
    long sum = 0;
    for(int j = 0; j < 200; j++) {
      sum += analogRead(lampsAnalogPins[i]);
    }
    int baseline = sum / 200;
    lampThresholds[i] = baseline * 1.6;
  }
  
  Serial.println("Finished setting up everything. ");
  digitalWrite(CALIBRATING_LED_PIN, LOW);
}
 
void loop(void) {
//  Serial.println("Current light readings/thresholds: ");
  for (int i = 0; i < NUMBER_OF_LAMPS; i++) {
    lampsReadings[i] = analogRead(lampsAnalogPins[i]);
    
    if(lampsReadings[i] > lampThresholds[i]) {
      digitalWrite(lampFeedbackLedsPins[i], HIGH);
    } else {
      digitalWrite(lampFeedbackLedsPins[i], LOW);
    }
//    Serial.print("    Lamp "); Serial.print(i); Serial.print(": "); 
//    Serial.print(lampsReadings[i]); Serial.print("/"); Serial.println(lampThresholds[i]);
  }
//  Serial.println();

  
//  Serial.println("Current presence sensor readings/thresholds: ");
  for (int i = 0; i < NUMBER_OF_PRESENCE_SENSORS; i++) {
    presenceSensorsReadings[i].addValue(time(presenceSensorsPins[i], presenceSensorsPinBitmasks[i]));
    
    if(presenceSensorsReadings[i].getAverage() > presenceSensorsThresholds[i]) {
      digitalWrite(presenceSensorFeebackLedsPins[i], HIGH);
    } else {
      digitalWrite(presenceSensorFeebackLedsPins[i], LOW);
    }
//    Serial.print("    Presence sensor "); Serial.print(i); Serial.print(": "); 
//    Serial.print(presenceSensorsReadings[i].getAverage()); Serial.print("/"); Serial.println(presenceSensorsThresholds[i]);
  }
//  Serial.println();
}

// presence
long time(int pin, byte mask) {
  unsigned long count = 0, total = 0;
  while(checkTimer() < refresh) {
    // pinMode is about 6 times slower than assigning
    // DDRB directly, but that pause is important
    pinMode(pin, OUTPUT);
    PORTB = 0;
    pinMode(pin, INPUT);
    while((PINB & mask) == 0)
      count++;
    total++;
  }
  startTimer();
  return (count << resolution) / total;
}

// presence
extern volatile unsigned long timer0_overflow_count;

// presence
void startTimer() {
  timer0_overflow_count = 0;
  TCNT0 = 0;
}

// presence
unsigned long checkTimer() {
  return ((timer0_overflow_count << 8) + TCNT0) << 2;
}

/*
 * [command, sensor_index, value_high, value_low]
 * command 0 - get lamp sensor
 * command 1 - get presence sensor
*/
byte receiveBuffer[COMMS_BUFFER_SIZE];
byte sendBuffer[COMMS_BUFFER_SIZE];

//  callback for received data
void i2c_receiveData(int byteCount) {

  byte index = 0;
  while(Wire.available() > 0 && index < COMMS_BUFFER_SIZE)
  {
    receiveBuffer[index] = Wire.read();
    index++;
  }

  int command = receiveBuffer[0];
  int sensor_index = receiveBuffer[1];
  
  int value = receiveBuffer[2] << 8;
  value |= receiveBuffer[3];
//
//  Serial.print("[command: ");
//  Serial.print(command);
//  Serial.print(", sensor_index: ");
//  Serial.print(sensor_index);
//  Serial.print(", value: ");
//  Serial.print(value);
//  Serial.println("]");

  // mirror back the command and sensor_index about which we're replying
  sendBuffer[0] = command;
  sendBuffer[1] = sensor_index;
    
  if (command == COMMAND_GET_LAMP) {
    int is_on = lampsReadings[sensor_index] > lampThresholds[sensor_index];

    // put the requested value into the send buffer
    sendBuffer[2] = highByte(is_on);
    sendBuffer[3] = lowByte(is_on);
  }
  
  if (command == COMMAND_GET_PRESENCE) {
    int is_present = presenceSensorsReadings[sensor_index].getAverage() > presenceSensorsThresholds[sensor_index] ? 1 : 0;

    // put the requested value into the send buffer
    sendBuffer[2] = highByte(is_present);
    sendBuffer[3] = lowByte(is_present);
  }
}

// callback for sending data
void i2c_sendData() {
//  Serial.print("Sending back data [command: ");
//  Serial.print(sendBuffer[0]);
//  Serial.print(", sensor_index: ");
//  Serial.print(sendBuffer[1]);
//  Serial.print(", value: ");
  int value = sendBuffer[2] << 8;
  value |= sendBuffer[3];
//  Serial.print(value);
//  Serial.println("]");
  
  Wire.write(sendBuffer, COMMS_BUFFER_SIZE);
}
