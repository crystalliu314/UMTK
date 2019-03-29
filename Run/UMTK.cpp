#include <Arduino.h>
#include "UMTK.h"

UMTK::UMTK(byte dout, byte pd_sck, byte gain) {
	begin(dout, pd_sck, gain);
}

UMTK::UMTK() {
}

UMTK::~UMTK() {
}

void UMTK::begin(byte dout, byte pd_sck, byte gain) {
	PD_SCK = pd_sck;
	DOUT = dout;

	pinMode(PD_SCK, OUTPUT);
	pinMode(DOUT, INPUT);

	set_gain(gain);
}

bool UMTK::is_ready() {
	return 1;
}

void UMTK::set_gain(byte gain) {
	switch (gain) {
		case 128:		// channel A, gain factor 128
			GAIN = 1;
			break;
		case 64:		// channel A, gain factor 64
			GAIN = 3;
			break;
		case 32:		// channel B, gain factor 32
			GAIN = 2;
			break;
	}

	digitalWrite(PD_SCK, LOW);
	read();
}

unsigned long shiftMeow(uint8_t dataPin, uint8_t clockPin, uint8_t bitOrder)
{
  unsigned long value = 0;
  uint8_t i;

  for (i = 0; i < 32; ++i)
        {
    digitalWrite(clockPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(clockPin, LOW);
    if (bitOrder == LSBFIRST)
      value |= digitalRead(dataPin) << i;
    else
      value |= digitalRead(dataPin) << (31 - i);
    
    delayMicroseconds(50);
  }
  return value;
}

long UMTK::read() {
	// wait for the chip to become ready
	unsigned long value;
  digitalWrite(PD_SCK, LOW);
	// pulse the clock pin 32 times to read the data
  value = shiftMeow(DOUT, PD_SCK, LSBFIRST);
	return static_cast<long>(value);
}

long UMTK::read_average(byte times) {
	long sum = 0;
	for (byte i = 0; i < times; i++) {
		sum += read();
		yield();
	}
	return sum / times;
}

double UMTK::get_units(byte times) {
	return (read_average(times) - OFFSET)/SCALE;
}
/*
double UMTK::get_units(byte times) {
	return get_value(times) / SCALE;
}
*/
void UMTK::tare(byte times) {
	double sum = read_average(times);
	set_offset(sum);
}

void UMTK::set_scale(float scale) {
	SCALE = scale;
}

float UMTK::get_scale() {
	return SCALE;
}

void UMTK::set_offset(long offset) {
	OFFSET = offset;
}

long UMTK::get_offset() {
	return OFFSET;
}

void UMTK::power_down() {
	digitalWrite(PD_SCK, LOW);
	digitalWrite(PD_SCK, HIGH);
}

void UMTK::power_up() {
	digitalWrite(PD_SCK, LOW);
}
