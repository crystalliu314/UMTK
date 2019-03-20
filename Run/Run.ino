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
long set_speed = 0.833;
int max_control = 1024;
int min_control = 0;
double control_signal = set_speed/4 * 1024;
long dis_now = 0;
long t_now = 0;
long t_last_PID;
long T_sample = 5;
long dt = 0;
double total_error = 0;
double last_error;
double error;

double pid_p = 0;
double pid_i = 0;
double pid_d = 0;
double Kp = 1;
double Ki = 0;  
double Kd = 0; 
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
  long dis_last = dis_now;
  long t_last = t_now;
  long dis_now = Slide.get_units();
  long t_now = millis();
  long cur_speed = abs((dis_now - dis_last)/(t_now - t_last));
  

  PID_Control();
  
  Serial.print(t_now);
  Serial.print(", ");
  Serial.print(Slide.get_units(), 3);
  Serial.print(", ");
  Serial.println(LoadCell.get_units(), 3);

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

void PID_Control(){
  
  if (t_now - t_last_PID > T_sample){
    t_last_PID = t_now;
    t_now = millis();
    dt = t_now - t_last_PID;

    error = (set_speed - cur_speed);
    pid_p = Kp*error;
    pid_d = Kd*((error - last_error)/dt);
    pid_i = Ki*total_error;  

    last_error = error;
    total_error = error*dt + total_error;
  }
  control_signal = pid_p + pid_d + pid_i;
  
  if (control_signal > max_control){
    control_signal = max_control;
  }
  else if(control_signal < min_control){
    control_signal = min_control;
  }
  
}
//================================================================
