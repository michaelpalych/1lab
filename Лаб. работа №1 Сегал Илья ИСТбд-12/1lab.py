DIGITS = {
    '0': 'ноль', '1': 'один', '2': 'два', '3': 'три', '4': 'четыре',
    '5': 'пять', '6': 'шесть', '7': 'семь', '8': 'восемь', '9': 'девять'
}

def number_to_words(number: str) -> str:
    return ' '.join(DIGITS[digit] for digit in number)

def process_stream(filename: str):
    with open(filename, 'r') as file:
        data = file.read().split()
    
    numbers = [num for num in data if num.isdigit() and len(num) <= 5 and int(num) % 2 == 0]
    
    for i, num in enumerate(numbers):
        print(number_to_words(num) if i % 2 == 0 else num)

process_stream("1lab.txt")

