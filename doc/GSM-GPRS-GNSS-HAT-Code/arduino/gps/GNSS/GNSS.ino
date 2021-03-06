/*
  Software serial multple serial test

 Receives from the hardware serial, sends to software serial.
 Receives from software serial, sends to hardware serial.

 The circuit:
 * RX is digital pin 10 (connect to TX of other device)
 * TX is digital pin 11 (connect to RX of other device)

 Note:
 Not all pins on the Mega and Mega 2560 support change interrupts,
 so only the following can be used for RX:
 10, 11, 12, 13, 50, 51, 52, 53, 62, 63, 64, 65, 66, 67, 68, 69

 Not all pins on the Leonardo support change interrupts,
 so only the following can be used for RX:
 8, 9, 10, 11, 14 (MISO), 15 (SCK), 16 (MOSI).

 created back in the mists of time
 modified 25 May 2012
 by Tom Igoe
 based on Mikal Hart's example

 This example code is in the public domain.

 */
#include <SoftwareSerial.h>

//#define SERIAL_TX_BUFFER_SIZE 256
//#define SERIAL_RX_BUFFER_SIZE 256
SoftwareSerial mySerial(2, 3); // RX, TX
String comdata = "";
void setup()
{
  // Open serial communications and wait for port to open:
  Serial.begin(9600);

 while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // set the data rate for the SoftwareSerial port
  mySerial.begin(9600);
  delay(200);
}

void loop() // run over and over
{
  delay(2000);
   mySerial.println("AT");   
  delay(200);
  //Send message
  mySerial.println("AT+CGNSPWR=1");
  delay(200);
  mySerial.println("AT+CGNSSEQ=\"RMC\"");
  delay(200);
  mySerial.println("AT+CGNSINF");
  delay(200);
  mySerial.println("AT+CGNSURC=2");
  delay(200);
  //reset GPS in autonomy mode
  mySerial.println("AT+CGNSTST=1");
  delay(200);
   mySerial.listen();
   while(1)
  {  
    while(mySerial.available()>0)  
        Serial.write(mySerial.read());
   while(Serial.available())
    mySerial.write(Serial.read());  //Arduino send the sim868 feedback to computer     
  } 
}

