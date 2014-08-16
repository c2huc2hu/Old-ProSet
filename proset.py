import random
import time
import pygame

deck = list(range(1, 64))
random.shuffle (deck)
working_deck = [deck.pop() for i in range (7)]

#def formatCard(i):
#    return ("{:0>6}".format (bin(i) [2:])).replace('0', ' ')

def draw_all_cards ():
    for c in range(len (working_deck)):
        cx = c%4
        cy = c//4
        pygame.draw.rect(main_surface, 0x000000, (cx*150+30, cy*200+30, 110, 150), 0)
        pygame.draw.rect(main_surface, 0x888888, (cx*150+30, cy*200+30, 110, 150), 5)
        for i,blip in enumerate('%0.6d' % int(bin(working_deck[c])[2:])):
            if blip == '1':
                bx = i%2
                by = i//2
                colors = [0xff0000, 0xff8800, 0xffff00, 0x00aa00, 0x0055ff, 0x8800ff]
                pygame.draw.circle(main_surface, colors[i], (cx*150+bx*40+60, cy*200+by*40+60), 10, 0)

pygame.init()
window = pygame.display.set_mode((600, 400))
main_surface = pygame.Surface ((600, 400))
clock = pygame.time.Clock()

while working_deck:
    clock.tick(60)
    for event in pygame.event.get():
        pass
    
    #output deck
##    for i, card in enumerate(working_deck): #for text outputting the deck. WE HAVE VISUAL OUTPUT!!!! YAY! -SL
##        print(i, ": ", formatCard(card))
    pygame.draw.rect(main_surface, 0x444444, (0,0,600,400), 0)
    draw_all_cards()
    window.blit(main_surface, (0,0))
    pygame.display.flip()

    inp = input("What cards do you want to select? >>> ")
    selection_cards = [i-1 for i in map(int, inp)]
    selection = set(selection_cards)
    
    nim_sum = 0
    #validate selections
    for digit in selection:
        nim_sum ^= working_deck[digit]
    if nim_sum == 0:
        print("Valid")

        #flash outline for correct cards. 
        for c in range (len (working_deck)):
            if c in selection:
                cx = c%4
                cy = c//4
                pygame.draw.rect(main_surface, 0xff8800, (cx*150+25, cy*200+25, 120, 160))
        draw_all_cards()
        window.blit(main_surface, (0,0))
        pygame.display.flip()

        pygame.time.wait(500 * len(selection) - 500)
            
        for digit in selection:
            try:
                working_deck [int(digit)] = deck.pop()
            except IndexError:
                pass
    else:        
        print ("invalid combination, nim sum is %s" % bin(nim_sum))
        pygame.draw.rect (main_surface, 0xff0000, (0, 0, 600, 400), 0) #flash background red
        draw_all_cards()
        window.blit(main_surface, (0, 0))
        pygame.display.flip()
        pygame.time.wait(700)
