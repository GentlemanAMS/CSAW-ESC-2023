#include <Wire.h>

#define SLAVE_ADDRESS 0x20

void setup() {
  Wire.begin(SLAVE_ADDRESS); 
  Wire.onReceive(receiveEvent); 
  Wire.onRequest(requestEvent); 
  Serial.begin(115200); 
}

uint32_t button[10] = {1, 1, 3, 7, 5, 6, 7, 4, 9, 6};
#define COUNTER_THRESHOLD_1 2
#define COUNTER_THRESHOLD_2 4
#define COUNTER_THRESHOLD_3 1
int counter1 = COUNTER_THRESHOLD_1;
int counter2 = COUNTER_THRESHOLD_2;
int counter3 = COUNTER_THRESHOLD_3;
int which_digit = 0;
bool column_check = true;
bool received_new_information = false;


void loop() {

  while(Serial.available() == 0) {}

  String temp1 = Serial.readStringUntil('\n');
  String temp2 = Serial.readStringUntil('\n');

  uint32_t temp_int1 = (temp1.toInt());
  uint32_t temp_int2 = (temp2.toInt());
  Serial.println(temp_int1);
  Serial.println(temp_int2);

  noInterrupts();

  button[0] = temp_int1 % 100000     ;   button[0] = button[0] / 10000     ;
  button[1] = temp_int1 % 10000      ;   button[1] = button[1] / 1000      ;
  button[2] = temp_int1 % 1000       ;   button[2] = button[2] / 100       ;
  button[3] = temp_int1 % 100        ;   button[3] = button[3] / 10        ;
  button[4] = temp_int1 % 10         ;   button[4] = button[4] / 1         ;
  button[5] = temp_int2 % 100000     ;   button[5] = button[5] / 10000     ;
  button[6] = temp_int2 % 10000      ;   button[6] = button[6] / 1000      ;
  button[7] = temp_int2 % 1000       ;   button[7] = button[7] / 100       ;
  button[8] = temp_int2 % 100        ;   button[8] = button[8] / 10        ;
  button[9] = temp_int2 % 10         ;   button[9] = button[9] / 1         ;

  counter1 = COUNTER_THRESHOLD_1;
  counter2 = COUNTER_THRESHOLD_2;
  counter3 = COUNTER_THRESHOLD_3;
  which_digit = 0;

  interrupts();
}




void receiveEvent(int byteCount) {
  byte receivedData;
  while (Wire.available()) {
    receivedData = Wire.read();
    // Serial.print("R:");    
    // Serial.println((uint8_t)receivedData);
    if (receivedData > 15) column_check = true;
    else column_check = false;
  }
}

void requestEvent() {

  char dataToSend;
  if (which_digit > 9) which_digit = 0;
  dataToSend = mapping(button[which_digit], column_check);
  Wire.write(dataToSend);
  // Serial.print("S:");  
  // Serial.print((uint8_t) dataToSend);
  // Serial.print("I:");
  // Serial.println((uint8_t)which_digit);
}


char mapping(uint32_t button, bool column_check) {

  char dataToSend;

  // if (received_new_information == false)
  // {
  //   dataToSend = column_check ? 240 : 15;
  //   return dataToSend;
  // }

  if (counter1 > 0) {
    counter1 = counter1 - 1;
    dataToSend = 240;
    return dataToSend;
  }

  if (counter2 > 0) {

    if (column_check){
      if      (button == 1  || button == 4  || button == 7  || button == 14) dataToSend = 224;
      else if (button == 2  || button == 5  || button == 8  || button == 0 ) dataToSend = 208;
      else if (button == 3  || button == 6  || button == 9  || button == 15) dataToSend = 176;
      else if (button == 10 || button == 11 || button == 12 || button == 13) dataToSend = 112;
      counter2 = counter2 - 1;
    }

    else{
      if      (button == 1  || button == 2 || button == 3   || button == 10)  dataToSend = 14;
      else if (button == 4  || button == 5 || button == 6   || button == 11)  dataToSend = 13;
      else if (button == 7  || button == 8 || button == 9   || button == 12)  dataToSend = 11;
      else if (button == 14 || button == 0 || button == 15  || button == 13)  dataToSend = 7 ;
      counter2 = 0;
    }

    return dataToSend;
  }

  if (counter3 > 0) {
    counter3 = counter3 - 1;
    dataToSend = 240;
  }

  if (counter3 == 0)
  {
    received_new_information = false;
    which_digit = (which_digit + 1);
    counter1 = COUNTER_THRESHOLD_1;
    counter2 = COUNTER_THRESHOLD_2;
    counter3 = COUNTER_THRESHOLD_3;
  }

  return dataToSend;

}
