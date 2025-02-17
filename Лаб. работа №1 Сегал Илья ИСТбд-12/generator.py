import random

def generate(count=1000, digits=6):
    return [random.randint(0, 10**digits - 1) for _ in range(count)]

def save(filename, numbers):
    with open(filename, 'w') as file:
        for number in numbers:
            file.write(f"{number}\n")

numbers = generate()

save('1lab.txt', numbers)


