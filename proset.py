import random
import time
import pygame

#CONSTANTS
card_num_by_key = {a:b for b,a in enumerate('qwerasd')}

deck = list(range(1, 64))
random.shuffle (deck)
working_deck = [deck.pop() for i in range(7)]
selected = {i:False for i in range(7)}

def draw_all_cards ():
    """Draws the cards on playing field"""
    for c in range(len (working_deck)):
        cx = c%4
        cy = c//4
        pygame.draw.rect(main_surface, 0x000000, (cx*150+30, cy*200+30, 110, 150), 0)

        if selected[c]:
            # selected card
            pygame.draw.rect(main_surface, 0xffffff, (cx*150+30, cy*200+30, 110, 150), 5)
        else:
            # non-selected card
            pygame.draw.rect(main_surface, 0x666666, (cx*150+30, cy*200+30, 110, 150), 5)
        for i,blip in enumerate('%0.6d' % int(bin(working_deck[c])[2:])):
            if blip == '1':
                bx = i%2
                by = i//2
                colors = [0xff0000, 0xff8800, 0xffff00, 0x00aa00, 0x0055ff, 0x8800ff]
                pygame.draw.circle(main_surface, colors[i], (cx*150+bx*40+60, cy*200+by*40+60), 10, 0)

def nim_sum(cards):
    """Return the nim sum of cards by xoring them all"""
    res = 0
    for i in cards:
        res ^= i
    return res

def find_set(working_deck):
    """
    Finds and returns a set. Currently works by brute forcing in O(2^n) time, but in theory,
    could be reduced to O(n^2) by reducing to a set of linear equations and solving by Gaussian elimination.
    I barely know what that means, but one of the QCSYS 2014 people does. 
    """
    import itertools
    for number_of_cards in range (3, 8):
        for subset in itertools.permutations(working_deck, number_of_cards):
            if nim_sum(subset) == 0:
                return subset

def get_card_from_coords(x,y):
    """
    Given coordinates, returns card index. Currently a non-robust function dependent on the
    coordinates used to draw rectangles. So if that is changed, then this function must be
    modified as well.
    """
    card = -1
    if x < 630 and y < 430 and (x-30)%150 <= 110 and (y-30)%200 <= 150:
        cx = (x-30)/150
        cy = (y-30)/200
        card = 4*cy + cx
        if card >= 7:
            card = -1
    return card

pygame.init()
window = pygame.display.set_mode((600, 400))
main_surface = pygame.Surface ((600, 400))
clock = pygame.time.Clock()

while working_deck:
    clock.tick(60)
    
    pygame.draw.rect(main_surface, 0x444444, (0,0,600,400), 0)
    draw_all_cards()
    window.blit(main_surface, (0,0))
    pygame.display.flip()

    # Get input
    done_input = False
    while not done_input:
        clock.tick(60)
        for event in pygame.event.get():
            #Keyboard input
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key in card_num_by_key:
                    card = card_num_by_key[key]
                    if card >= len(working_deck):
                        break
                    selected[card] = not selected[card]
                elif key == 'return': #submit that set
                    if sum(selected.values()) > 0:
                        done_input = True
                elif key == 'space': #automatically find a set.
                    found_set = find_set(working_deck) #a set known to work.
                    for i, c in enumerate(working_deck):
                        selected[i] = c in found_set
                else:
                    print(key)
                draw_all_cards()
                window.blit(main_surface, (0,0))
                pygame.display.flip()
                
            #Mouse input
            elif event.type == pygame.MOUSEBUTTONUP:
                card = get_card_from_coords(event.pos[0], event.pos[1])
                if card != -1:
                    if card >= len(working_deck):
                        continue
                    selected[card] = not selected[card]
                draw_all_cards()
                window.blit(main_surface, (0,0))
                pygame.display.flip()

            elif event.type == pygame.QUIT:
                exit()

    selection = [i for i in selected if selected[i]]
    
    # Validate selection    
    if nim_sum([working_deck [i] for i in selection]) == 0:
        print("Valid. There are %d cards left in the deck." % max (len(deck) - len (selection), 0))

        # Flash outline for correct cards
        for c in range (len (working_deck)):
            if c in selection:
                cx = c%4
                cy = c//4
                pygame.draw.rect(main_surface, 0xff8800, (cx*150+25, cy*200+25, 120, 160))
        draw_all_cards()
        window.blit(main_surface, (0,0))
        pygame.display.flip()

        pygame.time.wait(200 * len(selection) - 500)

        # Draw new cards to replace the old cards. If no cards remain, replace them with empty cards. 
        for digit in selection:
            try:
                working_deck [digit] = deck.pop()
            except IndexError:
                working_deck [digit] = None
        while None in working_deck:
            working_deck.remove(None)
            selected.pop(len(selected) - 1)
            
    else:        
        print ("invalid combination, nim sum is %s" % bin(nim_sum([working_deck [i] for i in selection])))
        pygame.draw.rect (main_surface, 0xaa0000, (0, 0, 600, 400), 0) # Flash background red
        draw_all_cards()
        window.blit(main_surface, (0, 0))
        pygame.display.flip()
        pygame.time.wait(700)

    for i in selected:
        selected[i] = False

pygame.draw.rect (main_surface, 0x444444, (0, 0, 600, 400), 0)  #clear screen when done. 
window.blit(main_surface, (0, 0))
pygame.display.flip()
print ("Decks depleted")
