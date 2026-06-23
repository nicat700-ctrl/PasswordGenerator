import random
import string

length = int(input("Parol uzunluğu: "))

numbers = input("Rəqəm olsun? (y/n): ")
symbols = input("Simvol olsun? (y/n): ")

characters = string.ascii_letters

if numbers == "y":
    characters += string.digits

if symbols == "y":
    characters += string.punctuation

password = ""

for i in range(length):
    password += random.choice(characters)

print("Parol:", password)