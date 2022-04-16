"""
Created on Sun May 24 22:21:12 2020
NL Holdem
@author: Stamatis
"""

""" import libraries """
from collections import Counter
from deckofcards import Card, Deck
from itertools import combinations
from modules import ImageEditor as imgedt
from tkinter import *
from PIL import ImageTk,Image  
import random
import time
import tkinter.font as font

class Player:
    def __init__(self, root, positions, font_family, name, stack, seat=0):
        self.name = name
        self.stack = stack
        self.seat = seat
        self.bet = 0
        self.total_bet = 0
        self.all_in = False
        self.eliminated = False
        self.showing_cards = [0, 0]
        self.card_back = ImageTk.PhotoImage(Image.open('Images/Small/Gray_back.jpg'))
        self.hand = []
        self.hand_image = []
        self.hand_image_gui = []
        self.widgets = dict()
        self.widgets['player_bet'] = Label(root, text=self.bet)
        self.widgets['player_bet']['font'] = font.Font(family=font_family, size=8)
        self.widgets['player_info'] = LabelFrame(root, bg='#F0FFFF', text='', padx=0, pady=0)
        self.widgets['player_info'].place(x=positions['player_info'][self.seat][0], y=positions['player_info'][self.seat][1])
        self.widgets['player_name'] = Label(self.widgets['player_info'], bg='#F0FFFF', text=self.name)
        self.widgets['player_name'].grid(row=0,column=0)
        self.widgets['player_name']['font'] = font.Font(family=font_family, size=10)
        self.widgets['player_stack'] = Label(self.widgets['player_info'], bg='#F0FFFF', text=self.stack)
        self.widgets['player_stack'].grid(row=1, column=0)
        self.widgets['player_stack']['font'] = font.Font(family=font_family, size=10)
        self.widgets['player_hand'] = []
        for i in range(2):
            self.widgets['player_hand'].append(Button(root, image=self.card_back, command=lambda: self.show_or_hide(i)))
    
    def draw(self, deck):
        c = deck.drawCard()
        card_front = ImageTk.PhotoImage(Image.open('Images/Small/{}{}.jpg'.format(c.figure, c.suit[0])))
        self.hand.append(c)
        self.hand_image.append('Images/Original/{}{}.jpg'.format(c.figure, c.suit[0]))
        self.hand_image_gui.append([self.card_back, card_front])
        
    def reveal(self):
        for c in self.hand:
            c.reveal()
    
    def showHand(self):
        print("{} - Hand".format(self.name))
        hand_img = imgedt().merge_n_images(self.hand_image)
        imgedt().print_image(hand_img)
        
    def show_or_hide(self, card_no):
        self.showing_cards[card_no] ^= 1
        self.widgets['player_hand'][card_no].configure(image=self.hand_image_gui[card_no][self.showing_cards[card_no]])
        
    def create_widgets(self, root, positions, card_no):
        self.widgets['player_hand'][card_no].configure(image=self.hand_image_gui[card_no][self.showing_cards[card_no]], command=lambda: self.show_or_hide(card_no))
        self.widgets['player_hand'][card_no].place(x=positions['player_hands'][self.seat][card_no][0], y=positions['player_hands'][self.seat][card_no][1])
        if self.bet > 0:
            self.widgets['player_bet'].configure(text=self.bet)
            self.widgets['player_bet'].place(x=positions['player_bets'][self.seat][0], y=positions['player_bets'][self.seat][1])
        
    def destroy_widgets(self):
        try:
            self.widgets['player_bet'].place_forget()
            self.widgets['player_hand'][0].place_forget()
            self.widgets['player_hand'][1].place_forget()
        except:
            pass
        
    def should_act(self, game):
        return self.hand and not self.eliminated and not self.all_in and (self.bet != game.current_bet or game.current_bet == 0 or (game.current_bet == game.settings['big blind'] and not game.board))
    
    def valid_action(self, game, action):
        if not (action in {'Fold', 'Check', 'Call'} or (action.startswith('Bet') and action[4:].isnumeric())):
            return False
        if action == 'Fold':
            return True
        if action == 'Check':
            return self.bet == game.current_bet
        if action == 'Call':
            return game.current_bet != 0 and self.bet != game.current_bet
        if action.startswith('Bet'):
            if int(action[4:]) > self.stack + self.bet:
                return False
            return (int(action[4:]) - game.current_bet >= game.current_raise) or (int(action[4:]) == self.stack + self.bet)
            
    def fold(self):
        self.bet = 0
        self.hand = []
        
    def foldGUI(self, game):
        if not game.block_player_actions:
            self.bet = 0
            self.hand = []
            for i in range(2):
                self.widgets['player_hand'][i].place_forget()
            game.update_player_speaking()
    
    def check(self):
        pass
    
    def checkGUI(self, game):
        if not game.block_player_actions:
            if self.bet == game.current_bet:
                game.update_player_speaking()
            else:
                print("Error! Wrong action chosen. Please repeat.")
    
    def call(self, amount_bet):
        self.stack += self.bet
        self.bet = min(amount_bet, self.stack)
        self.stack -= self.bet
        self.all_in = (self.stack == 0)
        return self.bet
    
    def callGUI(self, game):
        if not game.block_player_actions:
            if game.current_bet != 0 and self.bet != game.current_bet:
                game.pot -= self.bet
                self.stack += self.bet
                self.total_bet -= self.bet
                self.bet = min(game.current_bet, self.stack)
                self.total_bet += self.bet
                self.stack -= self.bet
                self.all_in = (self.stack == 0)
                game.pot += self.bet
                if self.bet > 0:
                    self.widgets['player_bet'].configure(text=self.bet)
                    self.widgets['player_bet'].place(x=game.positions['player_bets'][self.seat][0], y=game.positions['player_bets'][self.seat][1])
                self.widgets['player_stack'].configure(text=self.stack)
                game.widgets['pot'].configure(text='Pot: {}'.format(game.pot))
                game.update_player_speaking()
            else:
                print("Error! Wrong action chosen. Please repeat.")
    
    def betraise(self, amount_raise):
        self.stack += self.bet
        self.bet = min(amount_raise, self.stack)
        self.stack -= self.bet
        self.all_in = (self.stack == 0)
        return self.bet
    
    def betraiseGUI(self, game, amount_raise):
        if not game.block_player_actions:
            if amount_raise > self.stack + self.bet:
                print("Error! Wrong action chosen. Please repeat.")
                return
            if (amount_raise - game.current_bet >= game.current_raise) or (amount_raise == self.stack + self.bet):
                game.pot -= self.bet
                self.stack += self.bet
                self.total_bet -= self.bet
                self.bet = min(amount_raise, self.stack)
                self.total_bet += self.bet
                self.stack -= self.bet
                self.all_in = (self.stack == 0)
                game.current_raise = max(self.bet - game.current_bet, game.current_raise)
                game.current_bet = self.bet
                game.pot += game.current_bet
                if self.bet > 0:
                    self.widgets['player_bet'].configure(text=self.bet)
                    self.widgets['player_bet'].place(x=game.positions['player_bets'][self.seat][0], y=game.positions['player_bets'][self.seat][1])
                self.widgets['player_stack'].configure(text=self.stack)
                game.widgets['raise_amount_entry'].delete(0, END)
                game.widgets['raise_amount_scale'].set(min(game.current_bet+game.current_raise, game.player_speaking.stack+game.player_speaking.bet))
                game.widgets['pot'].configure(text='Pot: {}'.format(game.pot))
                game.update_player_speaking()
            else:
                print("Error! Wrong action chosen. Please repeat.")
            
    def score(self, board):
        if not self.hand: return 0
        candidates, max_score = self.hand + board, ''
        for item in list(combinations(candidates,5)):
            item_score = PokerScorer(item).evaluate()
            if item_score > max_score:
                max_score = item_score
        return max_score



class PokerGame:
    def __init__(self):
        self.settings = self.define_settings()
        self.players = self.define_players()
        self.remaining_players = self.players
        self.waiting_time = [1, 1, 1, 1] # waiting time for showing hand, flop, turn and river
        self.num_remaining_players = len(self.remaining_players)
        self.button = random.randint(0,self.num_remaining_players-1)
        self.player_speaking = self.players[(self.button+3)%self.num_remaining_players]
    
    def define_settings(self):
        settings = dict()
        settings['small blind'] = int(input("Enter small blind value: "))
        settings['big blind'] = int(input("Enter big blind value: "))
        settings['buy-in'] = int(input("Enter buy-in: "))
        settings['starting stack'] = int(input("Enter starting stack: "))
        settings['blind change'] = int(input("Blind change every: "))
        return settings
    
    def define_players(self):
        num_players = int(input("Enter number of players: "))
        player_list = []
        for i in range(num_players):
            player_name = input("Enter name of player {}: ".format(i+1))
            globals()[player_name] = Player(player_name, self.settings['starting stack'])
            player_list.append(globals()[player_name])
        return player_list
    
    def start_hand(self):
        for i, player in enumerate(self.remaining_players):
            if i == (self.button+1)%self.num_remaining_players:
                player.bet = self.settings['small blind']
                player.stack -= player.bet
            elif i == (self.button+2)%self.num_remaining_players:
                player.bet = self.settings['big blind']
                player.stack -= player.bet
            else:
                player.bet = 0
            player.hand = []
            player.hand_image = []
            player.all_in = False
        self.deck = Deck()
        self.board = []
        self.board_image = []
        self.pot = self.settings['small blind'] + self.settings['big blind']
        self.current_bet = self.settings['big blind']
        self.current_raise = self.settings['big blind']
        self.deal()
        for player in self.remaining_players:
            player.showHand(self.waiting_time[0])
        
    def play_hand(self):
        # pre-flop betting round
        self.bet()
        fold_all, more_betting, winner = self.check_end_hand()
        if not fold_all:
            # flop
            self.flop()
            # flop betting round
            if more_betting:
                self.bet()
                fold_all, more_betting, winner = self.check_end_hand()
            if not fold_all:
                # turn
                self.turn()
                # turn betting round
                if more_betting:
                    self.bet()
                    fold_all, more_betting, winner = self.check_end_hand()
                if not fold_all:
                    # river
                    self.river()
                    # river betting round
                    if more_betting:
                        self.bet()
                        fold_all, more_betting, winner = self.check_end_hand()
                    if not fold_all:
                        # showdown
                        winner = self.showdown()
        return winner
        
    def end_hand(self, winning_players):
        for player in winning_players:
            player.stack += (self.pot / len(winning_players))
        for player in self.remaining_players:
            player.eliminated = (player.stack == 0)
        self.remaining_players = [player for player in self.remaining_players if not player.eliminated]
        self.num_remaining_players = len(self.remaining_players)
        self.button = (self.button+1)%self.num_remaining_players
    
    def deal(self):
        self.deck.shuffle()
        for i in range(2):
            for player in self.remaining_players:
                player.draw(self.deck)
                
    def bet(self):
        end_round = False
        while not end_round:
            speaks_first = (self.button+1)%self.num_remaining_players
            if not self.board:
                speaks_first = (speaks_first+2)%self.num_remaining_players
            for player in self.remaining_players[speaks_first:] + self.remaining_players[:speaks_first]:
                if player.should_act(self):
                    self.player_speaking = player
                    player_action = input("{} - Fold, Check, Call, Bet? ".format(player.name))
                    while not player.valid_action(self, player_action):
                        print("Error: Wrong action chosen! Please repeat.\n")
                        player_action = input("{} - Fold, Check, Call, Bet? ".format(player.name))
                    if player_action == "Fold":
                        player.fold()
                    elif player_action == "Check":
                        player.check()
                    elif player_action == "Call":
                        self.pot -= player.bet
                        self.pot += player.call(self.current_bet)
                    else:
                        self.pot -= player.bet
                        self.current_raise = max(player.betraise(int(player_action[4:])) - self.current_bet, self.current_raise)
                        self.current_bet = player.bet
                        self.pot += self.current_bet
            end_round = self.check_end_round()
    
    def check_end_round(self):
        for player in self.remaining_players:
            if player.bet != self.current_bet and player.should_act(self):
                return False
        else:
            self.current_bet = 0
            self.current_raise = self.settings['big blind']
            for player in self.players:
                player.bet = 0
            return True
        
    def check_end_hand(self):
        fold_all, more_betting, winner = False, True, ''
        nonfolded_players = self.players_with_hand()
        if len(nonfolded_players) == 1:
            fold_all, more_betting, winner = True, False, [nonfolded_players[0]]
        else:
            num_stacked_players = self.count_players_with_hand_and_stack()
            fold_all, more_betting, winner = False, (num_stacked_players > 1), ''
        return fold_all, more_betting, winner        
                       
    def flop(self):
        self.deck.drawCard()
        for i in range(3):
            c = self.deck.drawCard()
            self.board.append(c)
            self.board_image.append('Images/Original/{}{}.jpg'.format(c.figure, c.suit[0]))
        board_img = imgedt().merge_n_images(self.board_image)
        imgedt().print_image(board_img)
        
    def turn(self):
        self.deck.drawCard()
        c = self.deck.drawCard()
        self.board.append(c)
        self.board_image.append('Images/Original/{}{}.jpg'.format(c.figure, c.suit[0]))
        board_img = imgedt().merge_n_images(self.board_image)
        imgedt().print_image(board_img)
        
    def river(self):
        self.deck.drawCard()
        c = self.deck.drawCard()
        self.board.append(c)
        self.board_image.append('Images/Original/{}{}.jpg'.format(c.figure, c.suit[0]))
        board_img = imgedt().merge_n_images(self.board_image)
        imgedt().print_image(board_img)
        
    def showdown(self):
        winner, cur_max = [], ''
        for player in self.remaining_players:
            if player.hand:
                player_score = player.score(self.board)
                if player_score > cur_max:
                    winner, cur_max = [player], player_score
                elif player_score == cur_max:
                    winner += [player]
        return winner
    
    def players_with_hand(self):
        return [player if player.hand else 0 for player in self.remaining_players]
    
    def count_players_with_hand_and_stack(self):
        return sum([1 if player.hand and (player.stack > 0) else 0 for player in self.remaining_players])
        
    def statistics(self):
        for player in self.players:
            print("{}: {}".format(player.name, player.stack))
        
        
                
class PokerGameGUI:
    def __init__(self, root, widgets, positions, font_family):
        self.root = root
        self.widgets = widgets
        self.positions = positions
        self.font_family = font_family
        self.settings = self.define_settings()
        self.players = self.define_players()
        self.remaining_players = self.players
        self.start_time = time.time()
        self.waiting_time = [0, 0, 0, 0, 0] # waiting time for dealing, showing hand, flop, turn and river
        self.num_remaining_players = len(self.remaining_players)
        self.pot = 0
        self.button = random.choice([player.seat for player in self.remaining_players])
        self.button_idx = [player.seat for player in self.remaining_players].index(self.button)
        self.button_img = ImageTk.PhotoImage(Image.open('Images/Small/Dealer_button.jpg'))
        self.current_bet = self.settings['big blind']
        self.current_raise = self.settings['big blind']
        self.players_to_act_ordered = iter(self.remaining_players[(self.button_idx+3)%self.num_remaining_players:] + self.remaining_players[:(self.button_idx+3)%self.num_remaining_players])
        self.player_speaking = next(self.players_to_act_ordered)
        
    def define_settings(self):
        settings = dict()
        settings['small blind'] = int(self.widgets['small_blind_entry'].get())
        settings['big blind'] = int(self.widgets['big_blind_entry'].get())
        settings['buy-in'] = int(self.widgets['buy_in_entry'].get())
        settings['starting stack'] = int(self.widgets['starting_stack_entry'].get())
        settings['blind change'] = int(self.widgets['blind_change_entry'].get())
        return settings
    
    def define_players(self):
        player_list = []
        for i in range(9):
            player_name = self.widgets['player_names_entries'][i].get()
            if player_name:
                globals()[player_name] = Player(self.root, self.positions, self.font_family, player_name, self.settings['starting stack'], i+1)
                player_list.append(globals()[player_name])
        return player_list
    
    def initialize_widgets(self):
        self.widgets['prize_pool'] = LabelFrame(self.root, bg='#F0FFFF', text='Prize Pool')
        self.widgets['prize_pool'].place(x=self.positions['prize_pool'][0], y=self.positions['prize_pool'][1])
        self.widgets['prize_pool']['font'] = font.Font(family=self.font_family, size=15)
        self.widgets['prizes'], self.prize_pool, self.colors = [], self.num_remaining_players*self.settings['buy-in'], ['#FFD700', '#C0C0C0', '#CD7F32']
        if self.num_remaining_players // 3 == 3:
            self.breakdown = [2/3, 2/9, 1/9]
            for i in range(3):
                self.widgets['prizes'].append(Label(self.widgets['prize_pool'], bg=self.colors[i], text='Place {}: {}$'.format(i+1, round(self.prize_pool*self.breakdown[i]))))
                self.widgets['prizes'][-1].grid(row=i, column=0)
                self.widgets['prizes'][-1]['font'] = font.Font(family=self.font_family, size=11)
        elif self.num_remaining_players // 3 == 2:
            self.breakdown = [2/3, 1/3]
            for i in range(2):
                self.widgets['prizes'].append(Label(self.widgets['prize_pool'], bg=self.colors[i], text='Place {}: {}$'.format(i+1, round(self.prize_pool*self.breakdown[i]))))
                self.widgets['prizes'][-1].grid(row=i, column=0)
                self.widgets['prizes'][-1]['font'] = font.Font(family=self.font_family, size=11)
        elif self.num_remaining_players // 3 <= 1:
            self.widgets['prizes'].append(Label(self.widgets['prize_pool'], bg=self.colors[0], text='Place {}: {}$'.format(1, round(self.prize_pool))))
            self.widgets['prizes'][-1].grid(row=0, column=0)
            self.widgets['prizes'][-1]['font'] = font.Font(family=self.font_family, size=11)
        self.widgets['dealer'] = LabelFrame(self.root, bg='#F0FFFF')
        self.widgets['dealer'].place(x=self.positions['dealer'][0], y=self.positions['dealer'][1])
        self.widgets['deal'] = Button(self.widgets['dealer'], bg='#C1CDCD', text='Deal', command=self.play_hand)
        self.widgets['deal'].grid(row=0, column=0)
        self.widgets['deal']['font'] = font.Font(family=self.font_family, size=10)
        self.widgets['pot'] = Label(self.widgets['dealer'], bg='#F0FFFF', text='Pot: {}'.format(self.pot), width=20)
        self.widgets['pot'].grid(row=1, column=0)
        self.widgets['pot']['font'] = font.Font(family=self.font_family, size=10)
        self.widgets['button'] = Label(self.root, image=self.button_img)
        self.widgets['button'].place(x=self.positions['button'][self.button-1][0], y=self.positions['button'][self.button-1][1])
        self.widgets['player_actions'] = LabelFrame(self.root, padx=0, pady=0)
        self.widgets['player_actions'].place(x=self.positions['player_actions'][0], y=self.positions['player_actions'][1])
        self.widgets['fold'] = Button(self.widgets['player_actions'], bd=10, bg='#FFF68F', text='Fold', command=lambda: self.player_speaking.foldGUI(self))
        self.widgets['fold'].grid(row=0, column=0)
        self.widgets['fold']['font'] = font.Font(family=self.font_family, size=17, weight='bold')
        self.widgets['check'] = Button(self.widgets['player_actions'], bd=10, bg='#FFF68F', text='Check', command=lambda: self.player_speaking.checkGUI(self))
        self.widgets['check'].grid(row=0, column=1)
        self.widgets['check']['font'] = font.Font(family=self.font_family, size=17, weight='bold')
        self.widgets['call'] = Button(self.widgets['player_actions'], bd=10, bg='#FFF68F', text='Call', command=lambda: self.player_speaking.callGUI(self))
        self.widgets['call'].grid(row=0, column=2)
        self.widgets['call']['font'] = font.Font(family=self.font_family, size=17, weight='bold')
        self.widgets['betraise'] = Button(self.widgets['player_actions'], bd=10, bg='#FFF68F', text='Bet', command=lambda: self.player_speaking.betraiseGUI(self, int(self.widgets['raise_amount_entry'].get())))
        self.widgets['betraise'].grid(row=0, column=3)
        self.widgets['betraise']['font'] = font.Font(family=self.font_family, size=17, weight='bold')
        self.widgets['raise_amount'] = LabelFrame(self.root, bg='#FFF68F', padx=0, pady=0)
        self.widgets['raise_amount'].place(x=self.positions['raise_amount'][0], y=self.positions['raise_amount'][1])
        def scale_callback(event):
            self.widgets['raise_amount_entry'].delete(0, END)
            self.widgets['raise_amount_entry'].insert(0, self.widgets['raise_amount_scale'].get())
        def entry_callback(sv):
            if sv.get():
                self.widgets['raise_amount_scale'].set(int(sv.get()))
            self.widgets['betraise'].configure(text='Bet {}'.format(sv.get()))
        sv = StringVar()
        sv.trace('w', lambda name, index, mode, sv=sv: entry_callback(sv))
        self.widgets['raise_amount_entry'] = Entry(self.widgets['raise_amount'], width=8, justify='center', textvariable=sv)
        self.widgets['raise_amount_entry'].grid(row=0, column=0)
        self.widgets['raise_amount_entry']['font'] = font.Font(family=self.font_family, size=10)
        self.widgets['raise_amount_scale'] = Scale(self.widgets['raise_amount'], length=170, bg='#FFF68F', from_=min(self.current_bet+self.current_raise, self.player_speaking.stack+self.player_speaking.bet), to=self.player_speaking.stack+self.player_speaking.bet, orient=HORIZONTAL, command=scale_callback, showvalue=0)
        self.widgets['raise_amount_scale'].grid(row=0, column=1)
        self.widgets['raise_amount_scale']['font'] = font.Font(family=self.font_family, size=10)
        
    def create_widgets(self):
        pass
    
    def destroy_widgets(self):
        for i in range(5):
            try:
                self.widgets['board'][i].destroy()
            except:
                pass
        for player in self.players:
            player.destroy_widgets()
        self.widgets['deal'].configure(text='Deal', command=self.play_hand)
        self.widgets['button'].place(x=self.positions['button'][self.button-1][0], y=self.positions['button'][self.button-1][1])
        self.widgets['pot'].configure(text='Pot: 0')
        self.widgets['raise_amount_entry'].delete(0, END)
        self.widgets['raise_amount_scale'].configure(from_=min(2*self.settings['big blind'], self.player_speaking.stack+self.player_speaking.bet), to=self.player_speaking.stack+self.player_speaking.bet)
        self.widgets['raise_amount_scale'].set(min(2*self.settings['big blind'], self.player_speaking.stack+self.player_speaking.bet))
    
    def start_hand(self):
        for i, player in enumerate(self.remaining_players):
            if ((i == (self.button_idx+1)%self.num_remaining_players) and (self.num_remaining_players > 2)) or ((i == self.button_idx) and (self.num_remaining_players == 2)):
                player.bet = self.settings['small blind']
                player.stack -= player.bet
                player.widgets['player_stack'].configure(text=player.stack)
            elif ((i == (self.button_idx+2)%self.num_remaining_players) and (self.num_remaining_players > 2)) or ((i == (self.button_idx+1)%self.num_remaining_players) and (self.num_remaining_players == 2)):
                player.bet = self.settings['big blind']
                player.stack -= player.bet
                player.widgets['player_stack'].configure(text=player.stack)
            else:
                player.bet = 0
            player.total_bet = player.bet
            player.hand = []
            player.showing_cards = [0, 0]
            player.hand_image = []
            player.hand_image_gui = []
            player.all_in = False
        self.deck = Deck()
        self.board = []
        self.board_image = []
        self.board_image_GUI = []
        self.widgets['board'] = []
        self.pot = sum([player.bet for player in self.remaining_players])
        self.widgets['pot'].configure(text='Pot: {}'.format(self.pot))
        self.current_bet = self.settings['big blind']
        self.current_raise = self.settings['big blind']
        self.players_to_act_ordered = iter(self.remaining_players[(self.button_idx+3)%self.num_remaining_players:] + self.remaining_players[:(self.button_idx+3)%self.num_remaining_players])
        if self.num_remaining_players == 2:
            self.players_to_act_ordered = iter(self.remaining_players[self.button_idx:] + self.remaining_players[:self.button_idx])
        self.player_speaking = next(self.players_to_act_ordered)
        self.widgets['deal'].configure(text='{} speaking'.format(self.player_speaking.name), state=DISABLED)
        self.widgets['raise_amount_scale'].configure(from_=min(self.current_bet+self.current_raise, self.player_speaking.stack+self.player_speaking.bet), to=self.player_speaking.stack+self.player_speaking.bet)
        self.block_player_actions = False
            
    def play_hand(self):
        self.start_hand()
        self.deal()
            
    def continue_hand(self):
        self.current_bet = 0
        self.current_raise = self.settings['big blind']
        for player in self.remaining_players:
            player.bet = 0
            player.widgets['player_bet'].place_forget()
        self.players_to_act_ordered = iter(self.find_players_to_act(self.remaining_players[(self.button_idx+1)%self.num_remaining_players:] + self.remaining_players[:(self.button_idx+1)%self.num_remaining_players]))
        self.player_speaking = next(self.players_to_act_ordered, None)
        if self.player_speaking:
            self.widgets['deal'].configure(text='{} speaking'.format(self.player_speaking.name), state=DISABLED)
            self.widgets['raise_amount_scale'].configure(from_=min(self.current_bet+self.current_raise, self.player_speaking.stack+self.player_speaking.bet), to=self.player_speaking.stack+self.player_speaking.bet)
        if self.check_end_hand():
            players_with_hand = self.find_players_with_hand()
            winners, pots = [players_with_hand], [self.pot]
            if len(players_with_hand) > 1:
                self.give_remaining_cards()
                pots, players_per_pot = self.main_side_pots()
                winners = self.showdown(pots, players_per_pot)
            self.end_hand(winners, pots)
        else:
            self.give_next_card()
            
    def end_hand(self, winning_players, pots):
        for i, pot in enumerate(pots):
            for player in winning_players[i]:
                player.stack += (pot / len(winning_players[i]))
                player.stack = round(player.stack)
                player.widgets['player_stack'].configure(text=player.stack)
        for player in self.remaining_players:
            player.eliminated = (player.stack == 0)
        self.button_idx = (self.button_idx+1)%self.num_remaining_players
        self.remaining_players = [player for player in self.remaining_players if not player.eliminated]
        self.num_remaining_players = len(self.remaining_players)
        self.button_idx = min(self.button_idx, self.num_remaining_players-1)
        self.button = self.remaining_players[self.button_idx].seat
        if self.check_end_game():
            print('Game over! Winner is {}.'.format(self.remaining_players[0].name))
            self.widgets['deal'].configure(text='Quit game', command=self.root.destroy, state=NORMAL)
        else:
            self.statistics()
            self.block_player_actions = True
            self.widgets['deal'].configure(text='New hand', command=self.destroy_widgets, state=NORMAL)
            
    def deal(self):
        self.deck.shuffle()
        for i in range(2):
            for player in self.remaining_players:
                player.draw(self.deck)
                player.create_widgets(self.root, self.positions, i)
        for player in self.remaining_players:
            player.showHand()
            
    def update_player_speaking(self):
        try:
            self.player_speaking = next(self.players_to_act_ordered)
            if len(self.find_players_with_hand()) > 1:
                self.widgets['deal'].configure(text='{} speaking'.format(self.player_speaking.name), state=DISABLED)
                self.widgets['raise_amount_scale'].configure(from_=min(self.current_bet+self.current_raise, self.player_speaking.stack+self.player_speaking.bet), to=self.player_speaking.stack+self.player_speaking.bet)
            else:
                self.continue_hand()
        except:
            if not self.check_end_round():
                self.continue_round()
            else:
                self.continue_hand()

    def check_end_round(self):
        for player in self.remaining_players:
            if (player.bet != self.current_bet) and player.hand and not player.all_in:
                return False
        else:
            return True
    
    def check_end_hand(self):
        return (len(self.board) == 5) or (self.players_to_act_ordered.__length_hint__() == 0)
    
    def check_end_game(self):
        return self.num_remaining_players <= 1
    
    def continue_round(self):
        if not self.board:
            self.players_to_act_ordered = iter(self.find_players_to_act(self.remaining_players[(self.button+3)%self.num_remaining_players:] + self.remaining_players[:(self.button+3)%self.num_remaining_players]))
            if self.num_remaining_players == 2:
                self.players_to_act_ordered = iter(self.find_players_to_act(self.remaining_players[self.button:] + self.remaining_players[:self.button]))
        else:
            self.players_to_act_ordered = iter(self.find_players_to_act(self.remaining_players[(self.button+1)%self.num_remaining_players:] + self.remaining_players[:(self.button+1)%self.num_remaining_players]))
        self.player_speaking = next(self.players_to_act_ordered)
        self.widgets['deal'].configure(text='{} speaking'.format(self.player_speaking.name), state=DISABLED)
        self.widgets['raise_amount_scale'].configure(from_=min(self.current_bet+self.current_raise, self.player_speaking.stack+self.player_speaking.bet), to=self.player_speaking.stack+self.player_speaking.bet)
            
    def flop(self):
        self.deck.drawCard()
        for i in range(3):
            c = self.deck.drawCard()
            card_img = ImageTk.PhotoImage(Image.open('Images/Small/{}{}.jpg'.format(c.figure, c.suit[0])))
            self.board.append(c)
            self.board_image.append('Images/Small/{}{}.jpg'.format(c.figure, c.suit[0]))
            self.board_image_GUI.append(card_img)
            self.widgets['board'].append(Label(self.root, image=self.board_image_GUI[-1]))
            self.widgets['board'][-1].place(x=self.positions['board'][i][0], y=self.positions['board'][i][1])
        board_img = imgedt().merge_n_images(self.board_image)
        imgedt().print_image(board_img)
        
    def turn(self):
        self.deck.drawCard()
        c = self.deck.drawCard()
        card_img = ImageTk.PhotoImage(Image.open('Images/Small/{}{}.jpg'.format(c.figure, c.suit[0])))
        self.board.append(c)
        self.board_image.append('Images/Small/{}{}.jpg'.format(c.figure, c.suit[0]))
        self.board_image_GUI.append(card_img)
        self.widgets['board'].append(Label(self.root, image=self.board_image_GUI[-1]))
        self.widgets['board'][-1].place(x=self.positions['board'][3][0], y=self.positions['board'][3][1])
        board_img = imgedt().merge_n_images(self.board_image)
        imgedt().print_image(board_img)
        
    def river(self):
        self.deck.drawCard()
        c = self.deck.drawCard()
        card_img = ImageTk.PhotoImage(Image.open('Images/Small/{}{}.jpg'.format(c.figure, c.suit[0])))
        self.board.append(c)
        self.board_image.append('Images/Small/{}{}.jpg'.format(c.figure, c.suit[0]))
        self.board_image_GUI.append(card_img)
        self.widgets['board'].append(Label(self.root, image=self.board_image_GUI[-1]))
        self.widgets['board'][-1].place(x=self.positions['board'][4][0], y=self.positions['board'][4][1])
        board_img = imgedt().merge_n_images(self.board_image)
        imgedt().print_image(board_img)
        
    def main_side_pots(self):
        pots, players_per_pot = [], []
        total_bets = [player.total_bet for player in self.remaining_players if player.hand]
        pot_levels = list(sorted(list(set(total_bets))))
        prev_level = 0
        for level in pot_levels:
            pots.append(0)
            players_per_pot.append([])
            for player in self.remaining_players:
                if player.hand:
                    if player.total_bet >= level:
                        pots[-1] += (level - prev_level)
                        players_per_pot[-1].append(player)
                elif player.total_bet >= prev_level:
                    pots[-1] += min(level, player.total_bet - prev_level)
            prev_level = level
        return pots, players_per_pot
    
    def showdown(self, pots, players_per_pots):
        winners = []
        for player in self.remaining_players:
            if player.hand:
                for j in range(2):
                    player.widgets['player_hand'][j].configure(image=player.hand_image_gui[j][1])
        for i, pot in enumerate(pots):
            winner_pot, cur_max = [], ''
            for player in players_per_pots[i]:                    
                player_score = player.score(self.board)
                if player_score > cur_max:
                    winner_pot, cur_max = [player], player_score
                elif player_score == cur_max:
                    winner_pot += [player]
            winners.append(winner_pot)
        return winners
    
    def statistics(self):
        for player in self.players:
            print("{}: {}".format(player.name, player.stack))
    
    def give_next_card(self):
        if not self.board:
            self.flop()
        elif len(self.board) == 3:
            self.turn()
        elif len(self.board) == 4:
            self.river()
    
    def give_remaining_cards(self):
        if not self.board:
            self.flop()
        if len(self.board) == 3:
            self.turn()
        if len(self.board) == 4:
            self.river()
    
    def find_players_to_act(self, players):
        players_with_hand_and_stack = [player for player in players if player.hand and not player.all_in]
        players_with_max_bet = [i for i, player in enumerate(players_with_hand_and_stack) if player.bet == self.current_bet]
        if len(players_with_max_bet) in {len(players_with_hand_and_stack), 0}:
            return players_with_hand_and_stack
        return players_with_hand_and_stack[(players_with_max_bet[-1]+1):] + players_with_hand_and_stack[:players_with_max_bet[0]] 
    
    def find_players_with_hand(self):
        return [player for player in self.remaining_players if player.hand]
    
    

class PokerScorer:
    def __init__(self, cards):
        if not len(cards):
            return "Error: Wrong number of cards!"
        self.ranks = [card.rank for card in cards]
        self.suits = [card.suit for card in cards]
        self.count = Counter(self.ranks).most_common()
    
    def isStraight(self):
        if list(sorted(self.ranks)) == [2, 3, 4, 5, 14]:
            self.ranks = [rank if rank != 14 else 1 for rank in self.ranks]
            return True
        return list(sorted(self.ranks)) == list(range(min(self.ranks), max(self.ranks)+1))
    
    def isFlush(self):
        return len(set(self.suits)) == 1
    
    def evaluate(self):
        # flush royale
        if self.isStraight() and self.isFlush() and max(self.ranks) == 14:
            return 'K'
        # straight flush
        if self.isStraight() and self.isFlush():
            return 'I' + chr(max(self.ranks)+64)
        # four of a kind
        if self.count[0][1] == 4:
            return 'H' + chr(self.count[0][0]+64) + chr(self.count[1][0]+64)
        # full house
        if self.count[0][1] == 3 and self.count[1][1] == 2:
            return 'G' + chr(self.count[0][0]+64) + chr(self.count[1][0]+64)
        # flush
        if self.isFlush():
            return 'F' + ''.join([chr(x+64) for x in list(sorted(self.ranks,reverse=True))])
        # straight
        if self.isStraight():
            return 'E' + chr(max(self.ranks)+64)
        # three of a kind
        if self.count[0][1] == 3:
            return 'D' + chr(self.count[0][0]+64) + ''.join(sorted(chr(self.count[1][0]+64)+chr(self.count[2][0]+64),reverse=True))
        # two pair
        if self.count[0][1] == 2 and self.count[1][1] == 2:
            return 'C' + ''.join(sorted(chr(self.count[0][0]+64)+chr(self.count[1][0]+64),reverse=True)) + chr(self.count[2][0]+64)
        # one pair
        if self.count[0][1] == 2:
            return 'B' + chr(self.count[0][0]+64) + ''.join(sorted(chr(self.count[1][0]+64)+chr(self.count[2][0]+64)+chr(self.count[3][0]+64),reverse=True))
        # high card
        return 'A' + ''.join(sorted(chr(self.count[0][0]+64)+chr(self.count[1][0]+64)+chr(self.count[2][0]+64)+chr(self.count[3][0]+64)+chr(self.count[4][0]+64),reverse=True))
        
    