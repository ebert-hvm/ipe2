#define A1 0
#define B1 1
#define C1 2
#define D1 3
#define A2 4
#define B2 5
#define D2 6
#define C2 7
#define N 4

int start;
int stop_count;
int key;
int pins1[N] = {A1, B1, C1, D1};
int pins2[N] = {A2, B2, C2, D2};

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
    key = 8, start = 0, stop_count = 0;
}

void loop()
{
    if(Serial.read() != -1)
    {
        start = Serial.read()
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
        delay(5000);
        if(++stop_count == N)
        {
            stop_count = 0;
            start = 0;
        }
    }
}