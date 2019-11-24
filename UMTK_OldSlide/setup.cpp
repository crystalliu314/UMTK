#include "setup.h"


void setPins(){
  pinMode(M_IN1, OUTPUT);
  pinMode(M_IN2, OUTPUT);
  pinMode(MOTOR_DISABLE, OUTPUT);
  
  pinMode(DISP1_OE, OUTPUT);
  pinMode(DISP2_OE, OUTPUT);  
  pinMode(DISP_D1, OUTPUT);
  pinMode(DISP_D2, OUTPUT);  
  pinMode(DISP_D3, OUTPUT);
  pinMode(DISP_D4, OUTPUT);  
  pinMode(DISP1_D1, OUTPUT);
  pinMode(DISP1_D2, OUTPUT);  
  pinMode(DISP1_D3, OUTPUT);
  pinMode(DISP1_D4, OUTPUT);
  pinMode(DISP2_D1, OUTPUT);
  pinMode(DISP2_D2, OUTPUT);  
  pinMode(DISP2_D3, OUTPUT);
  pinMode(DISP2_D4, OUTPUT);
  pinMode(DISP1_A, OUTPUT);
  pinMode(DISP1_B, OUTPUT);  
  pinMode(DISP1_C, OUTPUT);
  pinMode(DISP1_D, OUTPUT);
  pinMode(DISP1_E, OUTPUT);
  pinMode(DISP1_F, OUTPUT);  
  pinMode(DISP1_G, OUTPUT);
  pinMode(DISP1_OE, OUTPUT);
  pinMode(DISP1_DP, OUTPUT);
  
  pinMode(DISP2_A, OUTPUT);
  pinMode(DISP2_B, OUTPUT);  
  pinMode(DISP2_C, OUTPUT);
  pinMode(DISP2_D, OUTPUT);
  pinMode(DISP2_E, OUTPUT);
  pinMode(DISP2_F, OUTPUT);  
  pinMode(DISP2_G, OUTPUT);
  pinMode(DISP2_OE, OUTPUT); 
  pinMode(DISP2_DP, OUTPUT);

  

    
  pinMode(SWITCH_START, INPUT);
  pinMode(SWITCH_STOP, INPUT);
  pinMode(SWITCH_ZERO, INPUT);
  pinMode(SWITCH_MVUP, INPUT);
  pinMode(SWITCH_MVDOWN, INPUT);
}

