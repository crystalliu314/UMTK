#pragma once

#include <Arduino.h>
#include "PCB_PinMap.h"

namespace sevenSeg{
  static const byte digitPins[] = {DISP_D1, DISP_D2, DISP_D3, DISP_D4};
  static const byte segmentPins1[] = {DISP1_A, DISP1_B, DISP1_C, DISP1_D, DISP1_E, DISP1_F, DISP1_G, DISP1_DP};
  static const byte segmentPins2[] = {DISP2_A, DISP2_B, DISP2_C, DISP2_D, DISP2_E, DISP2_F, DISP2_G, DISP2_DP};
  
  static const byte digitCodeMap[] = {
    //     GFEDCBA  Segments      7-segment map:
    B00111111, // 0   "0"          AAA
    B00000110, // 1   "1"         F   B
    B01011011, // 2   "2"         F   B
    B01001111, // 3   "3"          GGG
    B01100110, // 4   "4"         E   C
    B01101101, // 5   "5"         E   C
    B01111101, // 6   "6"          DDD
    B00000111, // 7   "7"
    B01111111, // 8   "8"
    B01101111, // 9   "9"
    B01110111, // 65  'A'
    B01111100, // 66  'b'
    B00111001, // 67  'C'
    B01011110, // 68  'd'
    B01111001, // 69  'E'
    B01110001, // 70  'F'
    B00111101, // 71  'G'
    B01110110, // 72  'H'
    B00000110, // 73  'I'
    B00001110, // 74  'J'
    B01110110, // 75  'K'  Same as 'H'
    B00111000, // 76  'L'
    B00000000, // 77  'M'  NO DISPLAY
    B01010100, // 78  'n'
    B00111111, // 79  'O'
    B01110011, // 80  'P'
    B01100111, // 81  'q'
    B01010000, // 82  'r'
    B01101101, // 83  'S'
    B01111000, // 84  't'
    B00111110, // 85  'U'
    B00111110, // 86  'V'  Same as 'U'
    B00000000, // 87  'W'  NO DISPLAY
    B01110110, // 88  'X'  Same as 'H'
    B01101110, // 89  'y'
    B01011011, // 90  'Z'  Same as '2'
    B00000000, // 32  ' '  BLANK
    B01000000, // 45  '-'  DASH
  };
  
  // Constant pointers to constant data
  const byte * const numeralCodes = digitCodeMap;
  const byte * const alphaCodes = digitCodeMap + 10;
  

  void setStr(byte dispNum, char str[]);
  void setDigit(byte dispNum, byte digits[], int decPlaces);
  void refresh(byte digitNum);
  void setInt(byte dispNum, int number, int decPlaces);
}
