#include <MemoryFree.h>
#define F_CPU 16000000UL //16MHz
#include <util/delay.h>

#define OUT 6
#define Vs 5
#define GND 4


uint32_t timer;

#define num_readings 1700
#define SAMPLE_RATE 33 //microseconds
uint8_t readings[num_readings];

void outputData(void)
{
  for( uint16_t i = 0; i<num_readings; i++)
  {
    Serial.print(readings[i]);
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
  }
  if(millis() -timer > 2000)
  {
    //Serial.print("freeMem: ");
    //Serial.println(freeMemory());
    timer = millis();
  }
}
