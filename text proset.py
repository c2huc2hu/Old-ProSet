#WORKING IMPLEMENTATION OF PROSET

import random
import pygame

deck = list(range(1, 64))
random.shuffle (deck)
working_deck = deck [:7]

def formatCard(i):
    return ("{:0>6}".format (bin(i) [2:])).replace('0', ' ')

while deck:
    for i, card in enumerate(working_deck):
        print(i, ": ", formatCard(card))

    selection = input("What cards do you want to select? >>> ")
    nim_sum = 0

    for digit in selection:
        nim_sum ^= int (digit)
    if nim_sum == 0:
        print("Valid")

        for digit in selection:
            working_deck [int(digit)] = deck.pop()
    else:
        print ("invalid combination")

