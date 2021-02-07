#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float owe = 0;
    do
    {
        owe = get_float("Change owed: ");
    }
    while (!(owe > 0));

    int total = round(owe * 100);
    int coins[4] = {25, 10, 5, 1};
    int totalCoins = 0;

    for (int i = 0; i < 4; i++)
    {
        if (total < coins[i])
        {
            continue;
        }

        int mod = total % coins[i];
        int numberOfCoins = (total - mod) / coins[i];
        totalCoins += numberOfCoins;
        total = mod;
    }
    printf("%i\n", totalCoins);
}