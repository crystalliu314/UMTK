#include <Arduino.h>
#include "slide.h"

slide::slide(byte dout, byte pd_sck, byte gain) {
	begin(dout, pd_sck, gain);
}

slide::slide() {
}

slide::~slide() {
}

void slide::begin(byte dout, byte pd_sck, byte gain) {
	PD_SCK = pd_sck;
	DOUT = dout;

	pinMode(PD_SCK, OUTPUT);
	pinMode(DOUT, INPUT);

	set_gain(gain);
}

bool slide::is_ready() {
	return 1;
}

void slide::set_gain(byte gain) {
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

long slide::read() {
	// wait for the chip to become ready
	unsigned long value;
  digitalWrite(PD_SCK, LOW);
	// pulse the clock pin 32 times to read the data
  value = shiftMeow(DOUT, PD_SCK, LSBFIRST);
	return static_cast<long>(value);
}

long slide::read_average(byte times) {
	long sum = 0;
	for (byte i = 0; i < times; i++) {
		sum += read();
		yield();
	}
	return sum / times;
}

double slide::get_units(byte times) {
	return (read_average(times) - OFFSET)/SCALE;
}
/*
double slide::get_units(byte times) {
	return get_value(times) / SCALE;
}
*/
void slide::tare(byte times) {
	double sum = read_average(times);
	set_offset(sum);
}

void slide::set_scale(float scale) {
	SCALE = scale;
}

float slide::get_scale() {
	return SCALE;
}

void slide::set_offset(long offset) {
	OFFSET = offset;
}

long slide::get_offset() {
	return OFFSET;
}

void slide::power_down() {
	digitalWrite(PD_SCK, LOW);
	digitalWrite(PD_SCK, HIGH);
}

void slide::power_up() {
	digitalWrite(PD_SCK, LOW);
}
