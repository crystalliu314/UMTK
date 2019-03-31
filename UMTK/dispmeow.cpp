#include "dispmeow.h"

using namespace sevenSeg;

byte digitCodes[8];
void sevenSeg::setStr(byte dispNum, char str[])
{
  byte digitOffset = 0;
  if (dispNum == 2) digitOffset = 4;
  
  for (byte digit = 0; digit < 4; digit++) {
    digitCodes[digit+digitOffset] = 0;
  }

  for (byte digitNum = 0; digitNum < 4; digitNum++) {
    char ch = str[digitNum];
    if (ch == '\0') break; // NULL string terminator
    if (ch >= '0' && ch <= '9') { // Numerical
      digitCodes[digitNum+digitOffset] = numeralCodes[ch - '0'];
    }
    else if (ch >= 'A' && ch <= 'Z') {
      digitCodes[digitNum+digitOffset] = alphaCodes[ch - 'A'];
    }
    else if (ch >= 'a' && ch <= 'z') {
      digitCodes[digitNum+digitOffset] = alphaCodes[ch - 'a'];
    }
    else if (ch == ' ') {
      digitCodes[digitNum+digitOffset] = digitCodeMap[36];
    }
    else {
      // Every unknown character is shown as a dash
      digitCodes[digitNum+digitOffset] = digitCodeMap[37];
    }
  }
}

void sevenSeg::setDigit(byte dispNum, byte digits[], int decPlaces) {
  byte digitOffset = 0;
  if (dispNum == 2) digitOffset = 4;

  // Set the digitCode for each digit in the display
  for (byte i = 0 ; i < 4 ; i++) {
    digitCodes[i+digitOffset] = digitCodeMap[digits[i]];
    // Set the decimal place segment
  }
  
  if (decPlaces >= 0) digitCodes[digitOffset+4 - 1 - decPlaces] |= B10000000;
}

void sevenSeg::setInt(byte dispNum, int number, int decPlaces){
  byte digits[4];
  digits[3] = number%10;
  digits[2] = (number/10)%10;
  digits[1] = (number/100)%10;
  digits[0] = (number/1000)%10;
  setDigit(dispNum, digits, decPlaces);
}

void sevenSeg::refresh(byte digitNum){
  // Turn off all Digits
  for (byte i = 0 ; i < 4 ; i++) {
    digitalWrite(digitPins[i], LOW);
  }

  if (digitNum < 4){
    // Set segments for correct digit
    for (byte i = 0 ; i < 8 ; i++) {
        digitalWrite(segmentPins1[i], digitCodes[digitNum] & (1 << i));
        digitalWrite(segmentPins2[i], digitCodes[digitNum+4] & (1 << i));
    }
    
    // Turn on digit
    digitalWrite(digitPins[digitNum], HIGH);
  }
}
