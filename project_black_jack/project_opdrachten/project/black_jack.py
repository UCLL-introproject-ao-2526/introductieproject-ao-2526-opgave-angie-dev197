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
hand_active = False
add_score = False
results = ['', 'Player BUSTED o_O', 'Player WINS :D', 'Dealer WINS :(', 'Tie Game...']

# win, loss, draw/push
records = [0, 0, 0]
player_score = 0
dealer_score = 0




# FUNCTIONS

# deal cards by selecting randomly from deck; make funct for each card at a time
def dealer_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card -1])
    current_deck.pop(card -1)
    return current_hand, current_deck


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
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score


# pass player/dealer hand & get best score
def draw_scores(player, dealer):
    screen.blit(font.render(f'score[{player}]', True, 'white'), (350, 400))
    if reveal_dealer:
        screen.blit(font.render(f'score[{dealer}]', True, 'white'), (350, 100))


# game conditions and buttons
def draw_game(act, record, result):
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
        buttons_list.append(stand)

        score_text = smaller_font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}   ', True, 'white')
        screen.blit(score_text, (15, 840))
    # if there is an outcome for the hand was played, then diplay restart button & tell user what happened
    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (15, 25))
        deal = pygame.draw.rect(screen, 'white', [150, 220, 300, 100], 0, 5,)
        pygame.draw.rect(screen, 'pink', [150, 220, 300, 100], 3, 5,)
        pygame.draw.rect(screen, 'black', [153, 223, 294, 94], 3, 5,)
        deal_text = font.render('NEW HAND', True, 'black')
        screen.blit(deal_text, (165, 250))
        buttons_list.append(deal)

    return buttons_list


# check endgame conditions function
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    # end game scenarios, player stood, busted or blackjack
    # result 1- bust, 2- win, 3- win, 3-los, 4- push
    if not hand_active and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
    return result, totals, add

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
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = dealer_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)

    buttons = draw_game(active, records, outcome)

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
                    hand_active = True
                    reveal_dealer = False
                    outcome = 0
                    add_score = True
            else:
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = dealer_cards(my_hand, game_deck)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0


    # en turn if player busts (treat like stand)
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

    pygame.display.flip()
pygame.quit()
