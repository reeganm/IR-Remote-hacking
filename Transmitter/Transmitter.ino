#define mod_t 13 //1/2 modulation period
#define bit_t 480
#define msg_len 15

#define msg_start '%'

uint8_t buff[msg_len]; //global msg buffer

#define IR_p 12
#define LED_p 13

uint32_t blink_t;

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
  if(Serial.available())
  {
    return(Serial.read() == msg_start);
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

void setup ()
{
  Serial.begin(9600);
  pinMode(IR_p,OUTPUT);
  pinMode(LED_p,OUTPUT);
}

void loop () 
{
  if(check_for_start())
  {
    digitalWrite(LED_p,HIGH);
    get_code();
    echo_code();
    ir_send_msg();
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
}
