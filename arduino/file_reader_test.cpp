#include <bits/stdc++.h>

using namespace std;

int main()
{
    freopen("input", "r", stdin);
    unsigned char b;
    int n, t;
    cin >> b;
    if (b){
        n = b>>4;
        b<<=4;
        t = (b>>3)+1;
        printf("n = %d, t = %d", n,t);
    }
    else
    {
        printf("stop");
    }
    return 0;
}