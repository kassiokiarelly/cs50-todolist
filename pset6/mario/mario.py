from cs50 import get_int


height = 0
while True:
    height = get_int("Height: ")
    if height > 0 and height <= 8:
        break

for i in range(1, height+1):
    for j in range(height, 0, -1):
        if j <= i:
            print("#", end="")
        else:
            print(" ", end="")
    print()
