from keyboard import crossover

# Test tho crossover algorithm
qwerty_layout = list("qwertyuiopasdfghjkl;zxcvbnm,.'")
dvorak_layout = list("',.pyfgcrlaoeuidhtns;qjkxbmwvz")
aaa_layout = list("abcdefghijklmnopqrstuvwxyz',.;")
new_layout = crossover(aaa_layout, qwerty_layout)

# Print qwerty and dvorak layouts
for i in range(3):
    for k in range(10):
        print(qwerty_layout[i*10+k], end=" ")
    print(5*" ", end="")
    for k in range(10):
        print(aaa_layout[i*10+k], end=" ")
    print()
print()
        
# Print new layout
print(12*" ", end="")
for i, key in enumerate(new_layout, 1):
    print(key, end=" ")
    if i % 10 == 0:
        print()
        print(12*" ", end="")
print()
