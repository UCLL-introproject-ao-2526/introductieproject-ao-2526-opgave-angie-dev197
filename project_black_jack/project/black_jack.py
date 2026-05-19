import warnings
warnings.filterwarnings("ignore")
import copy
import random
import pygame

pygame.init()

# Display on screen
WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')

fps = 60
timer = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)

active = False

# GAME VARIABLES

cards = ['2', '3', '4', '5', '6', '7', '8', '9','10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4

# win, loss, draw/push
records = [0, 0, 0]
player_score = 0
dealer_score = 0

# FUNCTIONS

# deal cards by selecting randomly from deck; make funct for each card at a time
def dealer_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    print(current_hand, current_deck)
    return current_hand,current_deck

# draw cards viz on screen
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
        screen.blit(font.render(player[i], True, 'black'), (75 + 70*i, 465 + 5*i))
        screen.blit(font.render(player[i], True, 'black'), (75 + 70*i, 635 + 5*i))
        pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)

    # if player did not finish turn, then dealer hide one card
    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70*i, 165 + 5*i))
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70*i, 335 + 5*i))
        else:
            screen.blit(font.render('???', True, 'black'), (75 + 70*i, 165 + 5*i))
            screen.blit(font.render('???', True, 'black'), (75 + 70*i, 335 + 5*i))
        pygame.draw.rect(screen, 'dark red', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)

# pass for player or dealer and get best score
def calculate_score(hand):
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
    if hand[i] in ['10', 'J', 'Q', 'K']:
        hand_score += 10
    elif hand[i] == 'A':
        hand_score += 11
    if hand_score > 21 and aces_count > 0:
        for i in range(1, aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score

def draw_scores(player, dealer):
    screen.blit(font.render(f'score[{player}]', True, 'white'), (350, 400))
    if reveal_dealer:
        screen.blit(font.render(f'score[{dealer}]', True, 'white'), (350, 100))

# game conditions and buttons
def draw_game(act, record):
    buttons_list = []
    if not act:
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5,)
        pygame.draw.rect(screen, 'pink', [150, 20, 300, 100], 3, 5,)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (165, 50))
        buttons_list.append(deal)
    else:
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5,)
        pygame.draw.rect(screen, 'dark blue', [0, 700, 300, 100], 3, 5,)
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


# GAME-LOOP

# state of the game when game starts
run = True
initial_deal = False
game_deck = []
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False

while run:
    #run game at our framerate and fill screen with rbg color
    timer.tick(fps)
    screen.fill('black')

    if initial_deal:
        for i in range(2):
            my_hand, game_deck = dealer_cards(my_hand, game_deck)
            dealer_hand, game_deck = dealer_cards(dealer_hand, game_deck)
        print(my_hand, dealer_hand)
        initial_deal = False

    # once game is activated & dealt, calculate scores and display cards
    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        draw_scores(player_score, dealer_score)

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
