import warnings
warnings.filterwarnings("ignore")

import copy
import random
import pygame

pygame.init()

#game variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9','10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4

WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')

fps = 60
timer = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)

active = False

# win, loss, draw/push
records = [0, 0, 0]
player_score = 0
dealer_score = 0


# game conditions and buttons
def draw_game(act, record):
    buttons_list = []
    if not act:
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5,)
        pygame.draw.rect(screen, 'green', [150, 20, 300, 100], 3, 5,)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (165, 50))
        buttons_list.append(deal)
    else:
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5,)
        pygame.draw.rect(screen, 'green', [0, 700, 300, 100], 3, 5,)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (55, 735))
        buttons_list.append(hit)

        stand = pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 0, 5,)
        pygame.draw.rect(screen, 'green', [300, 700, 300, 100], 3, 5,)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (355, 735))
        buttons_list.append(hit)

        score_text = smaller_font.render(f'Wins: {records[0]}   Losses: {records[1]}   Draws: {records[2]}   ', True, 'white')
        screen.blit(score_text, (15, 800))


    return buttons_list


# GAME LOOP

run = True
while run:
    #run game at our framerate and fill screen with rbg color
    timer.tick(fps)
    screen.fill('black')

    if initial_deal:
        for i in range(2):
            my_hand, game_deck = dealer_cards(my_hand, game_deck)
            dealer_hand, game_deck = dealer_cards(dealer_hand, game_deck)
        initial_deal = False

    buttons = draw_game(active, records)

    # event handling: if quite, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0 

    pygame.display.flip()
pygame.quit()

