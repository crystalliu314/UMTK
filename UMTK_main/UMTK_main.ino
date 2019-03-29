/*
 * circuits4you.com
 * 2016 November 25
 * Load Cell UMTK Module Interface with Arduino to measure weight in Kgs
 Arduino 
 pin 
 2 -> UMTK CLK
 3 -> DOUT
 5V -> VCC
 GND -> GND
 
 Most any pin on the Arduino Uno will be compatible with DOUT/CLK.
 The UMTK board can be powered from 2.7V to 5V so the Arduino 5V power should be fine.
*/
 
#include "UMTK.h"  //You must have this library in your arduino library folder
 
#define DOUT  31
#define CLK  2
 
UMTK scale(DOUT, CLK);
 
//Change this calibration factor as per your load cell once it is found you many need to vary it in thousands
float calibration_factor_loadcell = -22025; //-106600 worked for my 40Kg max scale setup 
float calibration_factor_scale = -100.8;
 
//=============================================================================================
//                         SETUP
//=============================================================================================
void setup() {
  Serial.begin(9600);
  /*Serial.println("UMTK Calibration");
  Serial.println("Remove all weight from scale");
  Serial.println("After readings begin, place known weight on scale");
  Serial.println("Press a,s,d,f to increase calibration factor by 10,100,1000,10000 respectively");
  Serial.println("Press z,x,c,v to decrease calibration factor by 10,100,1000,10000 respectively");
  Serial.println("Press t for tare");
  */
  scale.set_scale();
  scale.tare(); //Reset the scale to 0
 
  long zero_factor = scale.read_average(); //Get a baseline reading
  /*Serial.print("Zero factor: "); //This can be used to remove the need to tare the scale. Useful in permanent scale projects.
  Serial.println(zero_factor);
  */
}
 
//=============================================================================================
//                         LOOP
//=============================================================================================
void loop() {
 
  scale.set_scale(calibration_factor_scale); //Adjust to this calibration factor
 
  Serial.print("Reading: ");
  Serial.println(scale.get_units(), 3);
  Serial.print(scale.read());
  Serial.print(" mm"); //Change this to kg and re-adjust the calibration factor if you follow SI units like a sane person
  Serial.print(" calibration_factor: ");
  Serial.print(calibration_factor_scale);
  Serial.println();
 
  if(Serial.available())
  {
    char temp = Serial.read();
    if(temp == '+' || temp == 'a')
      calibration_factor_scale += 10;
    else if(temp == '-' || temp == 'z')
      calibration_factor_scale -= 10;
    else if(temp == 's')
      calibration_factor_scale += 100;  
    else if(temp == 'x')
      calibration_factor_scale -= 100;  
    else if(temp == 'd')
      calibration_factor_scale += 1000;  
    else if(temp == 'c')
      calibration_factor_scale -= 1000;
    else if(temp == 'f')
      calibration_factor_scale += 10000;  
    else if(temp == 'v')
      calibration_factor_scale -= 10000;  
    else if(temp == 't')
      scale.tare();  //Reset the scale to zero
  }
}
//================================================================