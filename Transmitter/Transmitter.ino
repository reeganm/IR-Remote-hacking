#define mod_t 9 //1/2 modulation period
// 1 / 38000 Hz * 1000000us =  26
// 26 / 2 = 13
// rounding down to 9 works so I went with it

#define bit_t 470
#define msg_len 15

#define msg_start '%'
#define temp_request '$'

uint8_t buff[msg_len]; //global msg buffer

#define IR_p 12
#define LED_p 13

#define temp_v A0
#define temp_r A1
#define temp_g A2

uint32_t blink_t;

#define ON 1
#define OFF 0

//send message stored in global buffer
void ir_send_msg(void)
{
  //loop through all msg bytes
  for(uint8_t a = 0;a<msg_len;a++)
  {
    //loop through all msg bits
    for(uint8_t b = 0;b<8;b++)
    {
      bool st;
      if(buff[a] & (1 << b))
      {
        st = 1;
      }
      else
      {
        st = 0;
      }
      int16_t bt = bit_t;
      while(bt > 0)
      {
        digitalWrite(IR_p,st);
        _delay_us(mod_t);
        digitalWrite(IR_p,LOW);
        _delay_us(mod_t);
        bt -= 2*mod_t;
      }
    }
  }
}

bool check_for_start(void)
{
  char val = Serial.read();
  if(val == msg_start)
  {
    return(msg_start);
  }
  else if(val == temp_request)
  {
    return(temp_request);
  }
  else
  {
    return(0);
  }
}

void get_code(void)
{
  for(uint8_t a = 0;a < msg_len;a++)
  {
    while(Serial.available() == 0);
    buff[a] = (uint8_t)Serial.read(); //convert ascii to binary
  }
}

void echo_code(void)
{
  for(uint8_t a = 0;a < msg_len;a++)
  {
    Serial.write(buff[a]);
  }
  Serial.print('\n');
}

void Temp_Sensor_ctr(bool val)
{
  if(val)
  {
    //turn temp sensor on
    //set pin mode
    pinMode(temp_v,OUTPUT); //supply pin
    pinMode(temp_r,INPUT); //signal pin
    pinMode(temp_g,OUTPUT); //Ground

    //turn power on
    digitalWrite(temp_v,HIGH);
    digitalWrite(temp_g,LOW);
  }
  else
  {
    //turn power off
    digitalWrite(temp_v,LOW);
  }
}

void Send_Temp(void)
{
  //take an average of multiple readings
  uint32_t sum = 0;
  uint16_t num = 0;
  while(num <= 500)
  {
    sum += analogRead(temp_r);
    num++;
  }
  float temp = (float)sum / float(num);
  Serial.println(temp);
}

void setup ()
{
  Serial.begin(9600);
  
  pinMode(IR_p,OUTPUT);
  pinMode(LED_p,OUTPUT);
}

void loop () 
{
  switch(check_for_start())
  {
    case msg_start:
      digitalWrite(LED_p,HIGH);
      get_code();
      echo_code();
      ir_send_msg();
      break;
    case temp_request:
      digitalWrite(LED_p,HIGH);
      Temp_Sensor_ctr(ON);
      delay(1000); //let sensor warm up
      Send_Temp(); //send temperature over serial
      Temp_Sensor_ctr(OFF);
      break;
  }

  if(millis()-blink_t > 1000)
  {
    if(digitalRead(LED_p))
    {
      digitalWrite(LED_p,LOW);
    }
    else
    {
      digitalWrite(LED_p,HIGH);
    }
    blink_t = millis();
  }
  delay(1);
}
