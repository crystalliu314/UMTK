#include "UMTK.h"  
#include <HX711.h> //You must have this library in your arduino library folder

#define DOUT_Dis 31
#define DOUT_Load 23 
#define CLK_Dis 30
#define CLK_Load 22

#define BUTTON 2

UMTK Slide(DOUT_Dis, CLK_Dis);
HX711 LoadCell(DOUT_Load, CLK_Load);
 
//Change this calibration factor as per your load cell once it is found you many need to vary it in thousands
float calibration_factor_load = -22025; //-106600 worked for my 40Kg max scale setup 
float calibration_factor_displacement = -98.9;

int lastButtonState = 0;
 
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
  LoadCell.set_scale();
  LoadCell.tare(); //Reset the scale to 0
  Slide.set_scale();
  Slide.tare(); //Reset the scale to 0
 
  long zero_factor_load = LoadCell.read_average(); //Get a baseline reading
  long zero_factor_displacement = Slide.read_average(); //Get a baseline reading
  /*Serial.print("Zero factor: "); //This can be used to remove the need to tare the scale. Useful in permanent scale projects.
  Serial.println(zero_factor);
  */

  pinMode(BUTTON, INPUT);
}
 
//=============================================================================================
//                         LOOP
//=============================================================================================
void loop() {
 
  LoadCell.set_scale(calibration_factor_load); //Adjust to this calibration factor
  Slide.set_scale(calibration_factor_displacement); //Adjust to this calibration factor

  if(digitalRead(BUTTON) == HIGH){
    if(lastButtonState == 1){
      lastButtonState = 0;
      Serial.print("END\n");
    }
    else{
      lastButtonState = 1;
      Serial.print("BEGIN\n");
    }
    delay(300);
  }
 
//  Serial.print("Reading: ");
  Serial.print(Slide.get_units(), 3);
  Serial.print(", ");
  Serial.println(LoadCell.get_units(), 3);
//  Serial.print(Slide.read());
//  Serial.print(" calibration_factor: ");
//  Serial.print(calibration_factor);
 
  if(Serial.available())
  {
    char temp = Serial.read();
    if(temp == '+' || temp == 'a')
      calibration_factor_load += 10;
    else if(temp == '-' || temp == 'z')
      calibration_factor_load -= 10;
    else if(temp == 's')
      calibration_factor_load += 100;  
    else if(temp == 'x')
      calibration_factor_load -= 100;  
    else if(temp == 'd')
      calibration_factor_load += 1000;  
    else if(temp == 'c')
      calibration_factor_load -= 1000;
    else if(temp == 'f')
      calibration_factor_load += 10000;  
    else if(temp == 'v')
      calibration_factor_load -= 10000;  
    else if(temp == 't')
      LoadCell.tare();
      Slide.tare(); //Reset to zero
  }
}
//================================================================
