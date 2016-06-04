//#include <MemoryFree.h>
#define F_CPU 16000000UL //16MHz
#include <util/delay.h>

#define OUT 6
#define Vs 5
#define GND 4

#define correction_factor 3

uint32_t starttime_u;
uint32_t starttime_m;
uint32_t timer;

#define num_readings 1600
#define SAMPLE_RATE 50 //microseconds
uint8_t readings[num_readings];

uint8_t bitlength_estimate;
uint32_t baud_estimate;

void outputData(void)
{
  Serial.print("START ");
  for( uint16_t i = 0; i<num_readings; i++)
  {
    Serial.print(readings[i]);
  }
  Serial.print("END\n ");
}

uint8_t MinTimeHigh(void)
{
  bool hold = readings[0];
  uint8_t min_ = 255;
  uint8_t time_ = 0;
  for(uint16_t i = 0; i<num_readings;i++)
  {
    if(readings[i] == 1)
    {
      time_++;
      hold = 1;
    }
    else
    {
      if(hold == 1)
      {
        hold = 0;
        if(time_ < min_)
        {
          min_ = time_;
        }
      }
      time_ = 0;
    }
  }
  return(min_);
}

uint8_t MinTimeLow(void)
{
  bool hold = readings[0];
  uint8_t min_ = 255;
  uint8_t time_ = 0;
  for(uint16_t i = 0; i<num_readings;i++)
  {
    if(readings[i] == 0)
    {
      time_++;
      hold = 0;
    }
    else
    {
      if(hold == 0)
      {
        hold = 1;
        if(time_ < min_)
        {
          min_ = time_;
        }
      }
      time_ = 0;
    }
  }
  return(min_);
}

void undersample_estimate_code(uint8_t bitlength_estimate)
{
  Serial.print("Code: ");
  for(uint8_t i=0; i<(num_readings/bitlength_estimate);i++)
  {
    Serial.print(readings[i*bitlength_estimate+bitlength_estimate/correction_factor]); //bitlength estimate with correction factor
  }
  Serial.print('\n');
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(OUT,INPUT);
  pinMode(Vs,OUTPUT);
  pinMode(GND,OUTPUT);
  digitalWrite(GND,LOW);
  digitalWrite(Vs,HIGH);
  delay(100);
  starttime_u = micros();
  starttime_m = millis();
}

void loop() {
  if(digitalRead(OUT) == 0)
  {
    for(uint16_t i = 0; i < num_readings; i++)
    {
      readings[i] = digitalRead(OUT)^1;
      _delay_us(SAMPLE_RATE);
    }
    outputData();
    uint8_t tlow = MinTimeLow();
    uint8_t thigh = MinTimeHigh();
    bitlength_estimate = (tlow + thigh);
    Serial.print("Bit length: ");
    Serial.println(bitlength_estimate)/2;
    baud_estimate = 1000000 / SAMPLE_RATE / bitlength_estimate ;
    Serial.print("Baud :");
    Serial.println(baud_estimate);
    undersample_estimate_code(bitlength_estimate);
  }
//  if(millis() -timer > 2000)
//  {
//    Serial.print("freeMemory: ");
//    Serial.println(freeMemory());
//    timer = millis();
//  }
}
