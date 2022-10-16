#include <SoftwareSerial.h>
char incoming_char=0;
char a,b;
String num = "9819830616";
//Create software serial object to communicate with SIM900
SoftwareSerial mySerial(7, 8); //SIM900 Tx & Rx is connected to Arduino #7 & #8

void setup()
{
  //Begin serial communication with Arduino and Arduino IDE (Serial Monitor)
  Serial.begin(9600);
  
  //Begin serial communication with Arduino and SIM900
  mySerial.begin(9600);

  Serial.println("Initializing..."); 
  

  mySerial.println("AT"); //Handshaking with SIM900
  updateSerial();

  mySerial.println("AT+CMGF=1"); // Configuring TEXT mode
  updateSerial();
  mySerial.println("AT+CMGS=\"+91"+ num +"\"");//change ZZ with country code and xxxxxxxxxxx with phone number to sms
  updateSerial();
  mySerial.print("location to delivery: 1-- orion 2-- lassi shop");  
  updateSerial();
  mySerial.write(26);
  delay(5000);
  mySerial.println("AT+CNMI=1,2,0,0,0"); // Decides how newly arrived SMS messages should be handled
  updateSerial();
  if(b != NULL | b<1 | b>2){
  mySerial.println("AT+CMGS=\"+91"+ num +"\"");//change ZZ with country code and xxxxxxxxxxx with phone number to sms
  updateSerial();
  mySerial.print("your package will be delivered to the location in few minutes");  
  updateSerial();
  mySerial.write(26);
  }
  delay(8000);
  mySerial.println("AT+CMGS=\"+91"+ num +"\"");//change ZZ with country code and xxxxxxxxxxx with phone number to sms
  updateSerial();
  mySerial.print("location confirmed. Timely delivery.");  
  updateSerial();
  mySerial.write(26);
  
  
}

void loop()
{
  updateSerial();

    if(mySerial.available() >0) {
    //Get the character from the cellular serial port
    incoming_char=mySerial.read(); 
    //Print the incoming character to the terminal
    Serial.print(incoming_char); 
    
  }  
  delay(4000);
}

void updateSerial()
{
  delay(500);
  while (Serial.available()) 
  {
    a = Serial.read();
    mySerial.write(a);
    //Forward what Serial received to Software Serial Port
  }
  while(mySerial.available()) 
  {
    b = mySerial.read();
    Serial.write(b);//Forward what Software Serial received to Serial Port
  }
}