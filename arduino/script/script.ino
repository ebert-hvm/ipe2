#include <Servo.h>

#define A1 2
#define B1 3
#define C1 4
#define D1 5
#define A2 6
#define B2 7
#define D2 8
#define C2 9
#define N 4
#define servoPin 10

int key, timedelay, start, stop_count, total_probes;
int pins1[N] = {A1, B1, C1, D1};
int pins2[N] = {A2, B2, C2, D2};
unsigned char ch1, ch2;
Servo myservo;

void setup()
{
    Serial.begin(9600);
    pinMode(A1, OUTPUT);
    pinMode(B1, OUTPUT);
    pinMode(C1, OUTPUT);
    pinMode(D1, OUTPUT);
    pinMode(A2, OUTPUT);
    pinMode(B2, OUTPUT);
    pinMode(C2, OUTPUT);
    pinMode(D2, OUTPUT);
    pinMode(A0, INPUT);
    myservo.attach(servoPin,600,2300);
    key = 8;
    start = 0;
    stop_count = 0;
    timedelay = 1000;
    total_probes = 4;
}

void loop()
{
    if(Serial.available() > 0)
    {
        ch1 = Serial.read();
        if(ch1)
        {
            start = 1;
            total_probes = ch1 >> 4;
            ch1<<=4;
            timedelay = 1000*(1 + (ch1>>3));
        }
        else
        {
            stop_count = 0;
            start = 0;
            key = 8;
        }
    }
    if(start)
    {
        for(int i = 0; i < N; i++)
        {
            if (key & (1 << i))
            {
                digitalWrite(pins1[i], HIGH);
                digitalWrite(pins2[i], HIGH);
            }
            else
            {
                digitalWrite(pins1[i], LOW);
                digitalWrite(pins2[i], LOW);
            }
        }
        // Serial.println(analogRead(A0));
        key = 8 + (key + 1 - 8) % N;
        myservo.write(0);
        delay(timedelay);
        myservo.write(90);
        if(++stop_count == total_probes)
        {
            stop_count = 0;
            start = 0;
            key = 8;
        }
    }
}
