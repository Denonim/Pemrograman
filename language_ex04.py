#!/usr/bin/env python3
""" A Solution For language_ex04

    Write a program that prompts twice for an integer.
    • The program should output the sum of the integers within
      the range of those two numbers inclusively.
    • For example, if the user inputs the numbers 10 and 15
      then the sum would be 75.
          10 + 11 + 12 + 13 + 14 + 15 = 75
"""
prompt = "Masukkan {} integer: "
first = int(input(prompt.format("pertama")))
second = int(input(prompt.format("kedua")))
counter = first
total = 0
while(counter <= second):
    total += counter
    counter += 1

print("Total = ", total)

# Alternative way to calculate the sum
total = 0
for value in range(first, second + 1):
    total += value

print("Total = ", total)
