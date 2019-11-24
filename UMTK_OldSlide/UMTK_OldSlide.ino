#include "slide
.h"  
#include "PCB_PinMap.h"
#include "HX711.h"
#include "setup.h"
#include "dispmeow.h"

slide Slide(SLIDE_DATA, SLIDE_CLOCK);
HX711 LoadCell(LOADCELL_DATA, LOADCELL_CLOCK);
 
//Change this calibration factor as per your load cell once it is found you many need to vary it in thousands
float calibration_factor_load = -22025; //-106600 worked for my 40Kg max scale setup 
float calibration_factor_displacement = -98.9;

int lastSWITCH_STARTState = 0;
int i = 0;
int loopcount = 0;
float set_speed = 1.5;
int max_control = 1023;
int min_control = 80;
long control_signal = set_speed/3 * 1023;
double dis_now = 0;
double dis_last = 0;
long t_now = 0;
long t_last = 0;
long t_last_PID;
long T_sample = 50;
long dt = 0;
float Load = 0;
float Distance = 0;
float cur_speed = 0;
float total_error = 0;
float last_error;
float error;

long pid_p = 0;
long pid_i = 0;
long pid_d = 0;
float Kp = 50;
float Ki = 0;  
float Kd = 0; 

enum state {
  JOG_UP,
  JOG_DOWN,
  RECORDING,
  STANDBY
} state;

enum sevseg {
  DIG1,
  DIG2,
  DIG3,
  DIG4,
  DIG_OFF
  } sevseg;

//=============================================================================================
//                         SETUP
//=============================================================================================
void setup() {
  Serial.begin(9600);
  LoadCell.set_scale();
  LoadCell.tare(); //Reset the scale to 0
  Slide.set_scale();
  Slide.tare(); //Reset the scale to 0
  long zero_factor_load = LoadCell.read_average(); //Get a baseline reading
  long zero_factor_displacement = Slide.read_average(); //Get a baseline reading

  setPins();
  
  digitalWrite(MOTOR_DISABLE, LOW);
  digitalWrite(DISP1_OE, LOW);
  digitalWrite(DISP2_OE, LOW);
  state = STANDBY;
  sevseg = DIG_OFF;

}
 
//=============================================================================================
//                         LOOP
//=============================================================================================
void loop() {
  
  LoadCell.set_scale(calibration_factor_load); //Adjust to this calibration factor
  Slide.set_scale(calibration_factor_displacement); //Adjust to this calibration factor

  if(digitalRead(SWITCH_AUX) == LOW){
    i = i+1;
    if(i == 10){
      i = 0;
      dis_last = dis_now;
      t_last = t_now;
      dis_now = (Slide.get_units());
      t_now = millis();
      cur_speed = fabs((1000*(dis_now - dis_last))/((double)(t_now - t_last)));
      
    
      PID_Control();
    
      analogWrite(M_IN1, control_signal);
      analogWrite(M_IN2, 0);
    }
  }




  // Process State Machine Actions
  switch (state){
    case JOG_UP:
      if(digitalRead(SWITCH_MVUP) == HIGH){
        state = STANDBY;
        analogWrite(M_IN1, 1023);
        analogWrite(M_IN2, 1023);
        break;
      }
    break;

    case JOG_DOWN:
      if(digitalRead(SWITCH_MVDOWN) == HIGH){
        state = STANDBY;
        analogWrite(M_IN1, 1023);
        analogWrite(M_IN2, 1023);
        break;
      }
    break;

    case STANDBY:
      if(digitalRead(SWITCH_MVUP) == LOW){
        state = JOG_UP;
        analogWrite(M_IN1, 0);
        analogWrite(M_IN2, 1023);
        break;
      }
      
      if(digitalRead(SWITCH_MVDOWN) == LOW){
        state = JOG_DOWN;
        analogWrite(M_IN1, 1023);
        analogWrite(M_IN2, 0);
        break;
      }

      if(digitalRead(SWITCH_ZERO) == LOW){
        sevenSeg::refresh(5);
        LoadCell.tare();
        Slide.tare();
      }
      
      if(digitalRead(SWITCH_START) == LOW){
        state = RECORDING;
        Serial.println("BEGIN\n");
      }
    break;

    case RECORDING:
      if(digitalRead(SWITCH_STOP) == LOW){
        state = STANDBY;
        Serial.println("END\n");
      }
    break;
  }

  switch (sevseg){
    case DIG1:
        sevenSeg::refresh(0);
        sevseg = DIG2;
        delay(2);
        break;
        
    case DIG2:
        sevenSeg::refresh(1);
        sevseg = DIG3;
        delay(2);
        break;
        
    case DIG3:
        sevenSeg::refresh(2);
        sevseg = DIG4;
        delay(2);
        break;
        
    case DIG4:
        sevenSeg::refresh(3);
        sevseg = DIG_OFF;
        delay(2);
        break;

    case DIG_OFF:
        sevenSeg::refresh(5);
        if (loopcount > 10){
        Load = LoadCell.get_units(1);
        Distance = Slide.get_units();
        loopcount = 0;
        };
        sevenSeg::setInt( 1, abs ((int) round (Distance*10)), 1);
        sevenSeg::setInt( 2, abs ((int) round (Load*9.8)), 1);
        sevseg = DIG1;
        Serial.print(round(Distance*10));
        Serial.print(", ");
        Serial.println(round(Load*9.8));
        //Serial.println();
        loopcount ++;
        break;
  }

  
//
  //Print disp, force data to serial (so python can save to .csv file)

  

  /*
  Serial.print(t_now);
  Serial.print(", ");
  Serial.print(control_signal);
  Serial.print(", ");
  Serial.print(cur_speed);
  Serial.print(", ");
  Serial.print(-Slide.get_units(), 3);
  Serial.print(", ");
  Serial.println(-LoadCell.get_units(), 3);
  */

  /*
  if(Serial.available()){
    char temp = Serial.read();
    if(temp == 't'){
      LoadCell.tare();
      Slide.tare(); //Reset to zero
    }
  }
  */
  

}

void Move_Up(long Control_Signal){
    analogWrite(M_IN1, Control_Signal);
    analogWrite(M_IN2, 0);
    delay(300);
}

void Move_Down(long Control_Signal){
    analogWrite(M_IN1, 0);
    analogWrite(M_IN2, Control_Signal);
    delay(300);  
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

 /*   Serial.print("Control Parameters: ");
    Serial.print(pid_p);
    Serial.print(", ");
    Serial.print(pid_d);
    Serial.print(", ");
    Serial.println(pid_i);
*/
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
