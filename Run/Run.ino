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
float calibration_factor_displacement = -100.8;

int lastButtonState = 0;
const int motorPin1 = 7;
const int motorPin2 = 8;
float set_speed = 0.833;
int max_control = 1024;
int min_control = 0;
long control_signal = set_speed/3 * 1024;
long dis_now = 0;
long dis_last = 0;
long t_now = 0;
long t_last = 0;
long t_last_PID;
long T_sample = 50;
long dt = 0;
float cur_speed = 0;
float total_error = 0;
float last_error;
float error;

long pid_p = 0;
long pid_i = 0;
long pid_d = 0;
float Kp = 100;
float Ki = 0;  
float Kd = 0; 
//=============================================================================================
//                         SETUP
//=============================================================================================
void setup() {
  Serial.begin(9600);
  
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
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

/*  if(digitalRead(BUTTON) == HIGH){
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
 */
  dis_last = dis_now;
  t_last = t_now;
  dis_now = Slide.get_units();
  t_now = millis();
  cur_speed = abs((dis_now - dis_last)/(t_now - t_last));
  

  PID_Control();
  
  analogWrite(motorPin1, control_signal);
  analogWrite(motorPin2, 0);
  delay(5);
  
//  Serial.print(t_now);
//  Serial.print(", ");
  Serial.print(Slide.get_units(), 3);
  Serial.print(", ");
  Serial.print(cur_speed);
  Serial.print(", ");
  Serial.print(control_signal);
  Serial.print(", ");
  Serial.print(error);
  Serial.print(", ");
  Serial.print(set_speed);
  Serial.print(", ");
  Serial.println(LoadCell.get_units(), 3);

  if(Serial.available())
  {
    char temp = Serial.read();
    if(temp == 't'){
      LoadCell.tare();
      Slide.tare(); //Reset to zero
    }
  }
}

void PID_Control(){
  
  if (t_now - t_last_PID > T_sample){
    t_last_PID = t_now;
    t_now = millis();
    dt = t_now - t_last_PID;

    error = (set_speed - cur_speed);
    pid_p = Kp*error;
    pid_d = 0; //Kd*((error - last_error)/dt);
    pid_i = Ki*total_error;  

    Serial.print("Control Parameters: ");
    Serial.print(pid_p);
    Serial.print(", ");
    Serial.print(pid_d);
    Serial.print(", ");
    Serial.println(pid_i);

    last_error = error;
    total_error = error*dt + total_error;
  }
  control_signal = pid_p + pid_d + pid_i + 100;
  
  if (control_signal > max_control){
    control_signal = max_control;
  }
  else if(control_signal < min_control){
    control_signal = min_control;
  }
  
}
//================================================================
