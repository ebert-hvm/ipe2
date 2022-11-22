#define A1 0
#define B1 1
#define C1 2
#define D1 3
#define A2 4
#define B2 5
#define D2 6
#define C2 7
#define N 4

int key, timedelay, start, stop_count, total_probes;
int pins1[N] = {A1, B1, C1, D1};
int pins2[N] = {A2, B2, C2, D2};
unsigned char ch1, ch2;

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
    key = 8, start = 0, stop_count = 0, timedelay = 2000, total_probes = 4;
}

void loop()
{
    if(!start && Serial.available() > 0)
    {
        ch1 = Serial.read();
        if(ch1)
        {
            start = 1;
            total_probes = ch1 >> 4;
            ch1<<=4;
            timedelay = 1 + (ch1>>3);
        }
        else
        {
            start = 0;
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
        delay(timedelay);
        if(++stop_count == total_probes)
        {
            stop_count = 0;
            start = 0;
        }
    }
}