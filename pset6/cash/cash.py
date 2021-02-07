from cs50 import get_float

owe = 0.0
while True:
    owe = get_float("Change owed: ")
    if owe > 0:
        break

total = round(owe * 100)
coins = [25, 10, 5, 1]
totalCoins = 0

for i in range(len(coins)):
    if total < coins[i]:
        continue

    mod = total % coins[i]
    numberOfCoins = (total - mod) / coins[i]
    totalCoins += numberOfCoins
    total = mod

print(f"{totalCoins:.0f}")