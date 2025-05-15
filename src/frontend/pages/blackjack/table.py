from src.frontend.pages.blackjack.player import Player
from src.frontend.pages.blackjack.dealer import Dealer
from src.frontend.pages.blackjack.card_deck_handler import CardDeckHandler
from src.frontend.pages.blackjack.components.score_tracker import ScoreTracker
from src import data
import gFrame as gf
from src.frontend.pages.blackjack.components.center_text_handler import CenterTextHandler
from src.enums import gameStatus


class Table:
    def __init__(self):
        self.deck = CardDeckHandler()
        self.player = Player(self.deck)
        self.dealer = Dealer(self.deck)
        self.player_second_hand = Player(self.deck, positioned_left=False)
        self.score_tracker = ScoreTracker(
            self.player, self.player_second_hand, self.dealer)
        self.stage = 0
        self.dealer_card_down = True
        self.center_text_handler = CenterTextHandler()
        self.active_hand = self.player

    def table_handler(self):
        # print(self.player.result, self.player_second_hand.result)
        if not data.splitted:
            if self.player.result is not None:
                data.game_state = self.player.result
        else:
            if self.player.result is not None and self.player_second_hand.result is not None:
                if self.player.hand[0].active == False:
                    self.player.activate_animation()
                elif self.player_second_hand.hand[0].active == False:
                    self.player_second_hand.activate_animation()
                data.game_state = Table.compare_results(
                    self.player, self.player_second_hand)
            # elif self.player.result is

    def compare_results(hand1: Player, hand2: Player) -> gameStatus:
        # If both hands doubled down
        if hand1.double_down and hand2.double_down:
            if hand1.result == gameStatus.blackjack and hand2.result == gameStatus.blackjack:
                return gameStatus.bigWin
            elif hand1.result == gameStatus.blackjack or hand2.result == gameStatus.blackjack:
                return gameStatus.win  # One blackjack is enough to be a win
            elif hand1.result == gameStatus.bust and hand2.result == gameStatus.bust:
                return gameStatus.lose  # Both bust = total loss
            elif hand1.result == gameStatus.bust or hand2.result == gameStatus.bust:
                return gameStatus.splitResult  # One bust, one win/loss
            elif hand1.result == gameStatus.push or hand2.result == gameStatus.push:
                return gameStatus.push  # At least one push = tie result
            else:
                return gameStatus.splitResult  # One win, one loss

        # If one hand doubled down
        if hand1.double_down or hand2.double_down:
            winning_hand = hand1 if hand1.result in [gameStatus.blackjack, gameStatus.win] else hand2
            losing_hand = hand1 if hand1.result in [gameStatus.bust, gameStatus.lose] else hand2

            if winning_hand.result == gameStatus.blackjack:
                return gameStatus.bigWin  # Prioritize blackjack wins
            elif losing_hand.result == gameStatus.bust:
                return gameStatus.lose  # Prioritize a bust-based loss
            elif winning_hand.result == gameStatus.win:
                return gameStatus.win  # Normal win if one succeeds
            elif winning_hand.result == gameStatus.push or losing_hand.result == gameStatus.push:
                return gameStatus.push  # Any push should be considered
            else:
                return gameStatus.splitResult  # Mixed result

        # If neither hand doubled down
        if hand1.result == gameStatus.blackjack and hand2.result == gameStatus.blackjack:
            return gameStatus.bigWin
        elif hand1.result == gameStatus.blackjack or hand2.result == gameStatus.blackjack:
            return gameStatus.win
        elif hand1.result == gameStatus.bust and hand2.result == gameStatus.bust:
            return gameStatus.lose
        elif hand1.result == gameStatus.bust or hand2.result == gameStatus.bust:
            return gameStatus.splitResult
        elif hand1.result == gameStatus.push or hand2.result == gameStatus.push:
            return gameStatus.push
        else:
            return gameStatus.splitResult


    def check_player_score(self):
        if self.active_hand.score > 21:
            self.active_hand.result = gameStatus.bust
            self.active_hand.show_animated_text("BUST", gf.Color.LAVA_RED)
            self.switch_hand()
        elif self.active_hand.score == 21:
            self.active_hand.result = gameStatus.blackjack
            self.active_hand.show_animated_text("BLACKJACK", gf.Color.GREEN)

        if data.splitted:
            if (self.player.result is not None and self.player_second_hand.standing) or (self.player_second_hand.result is not None and self.player.standing):
                data.game_state = data.gameStatus.stand

    def stand(self):
        self.active_hand.standing = True

        if not data.splitted:
            if self.player.standing:
                data.game_state = data.gameStatus.stand
        else:
            if (self.player.standing or self.player.result is not None) and (self.player_second_hand.standing or self.player_second_hand.result is not None):
                if self.player.hand[0].active == False:
                    self.player.activate_animation()
                elif self.player_second_hand.hand[0].active == False:
                    self.player_second_hand.activate_animation()
                data.game_state = data.gameStatus.stand
            else:
                self.active_hand.standing = True
                self.switch_hand()

    def init_card_handler(self):
        match self.stage:
            case 0:
                self.player.get_card(face_up=False)
            case 1:
                self.player.hand[-1].flip()
            case 2:
                self.player.get_score()
                self.score_tracker.update()
                self.dealer.get_card(face_up=False)
            case 3:
                self.dealer.hand[-1].flip()
            case 4:
                self.dealer.get_score()
                self.score_tracker.update()
                self.player.get_card(face_up=False)
            case 5:
                self.player.hand[-1].flip()
            case 6:
                self.player.get_score()
                self.check_player_score()
                self.score_tracker.update()
                self.dealer.get_card(face_up=False)
            case 7:
                if self.player.hand[0].value == self.player.hand[1].value:
                    data.split_possible = True
                data.game_state = data.gameStatus.hit
        self.stage += 1

    def switch_hand(self):
        if data.splitted:
            if self.active_hand == self.player and not self.player_second_hand.standing and self.player_second_hand.result is None:
                self.active_hand.deactivate_animation()
                self.active_hand = self.player_second_hand
                self.active_hand.activate_animation()
            elif self.active_hand == self.player_second_hand and not self.player.standing and self.player.result is None:
                self.active_hand.deactivate_animation()
                self.active_hand = self.player
                self.active_hand.activate_animation()

    def hit_handler(self):
        match self.stage:
            case 0:
                self.active_hand.get_card(face_up=False)
            case 1:
                self.active_hand.hand[-1].flip()
            case 2:
                self.active_hand.get_score()
                self.check_player_score()
                self.score_tracker.update()
            case 3:
                self.switch_hand()  # if splitted
        self.stage += 1

    def split_hand(self):
        data.splitted = True
        self.stage = 0
        data.game_state = data.gameStatus.splitting

    def split_handler(self):
        match self.stage:
            case 0:
                self.player_second_hand.hand.append(self.player.hand.pop())
                self.player_second_hand.hand[0].move_animation(
                    (self.player_second_hand.card_x, self.player_second_hand.card_y), 0.5)
            case 1:
                self.player.get_score()
                self.player_second_hand.get_score()
                self.score_tracker.update()
                self.player.get_card(face_up=False)
            case 2:
                self.player.hand[-1].flip()
            case 3:
                self.player.get_score()
                self.check_player_score()
                self.score_tracker.update()
                self.player_second_hand.get_card(face_up=False)
            case 4:
                self.player_second_hand.hand[-1].flip()
            case 5:
                self.player_second_hand.get_score()
                self.check_player_score()
                self.score_tracker.update()
                if self.player.result is None:
                    self.player_second_hand.deactivate_animation()
                data.game_state = data.gameStatus.hit
        self.stage += 1

    def stand_handler(self):
        if self.dealer_card_down:
            match self.stage:
                case 0:
                    self.dealer.hand[-1].flip()
                    self.stage += 1
                case 1:
                    self.dealer.get_score()
                    self.score_tracker.update()
                    if self.dealer.score < 17:
                        self.stage = 0
                        self.dealer_card_down = False
                    else:
                        self.stage += 1
                        self.compare_score()
        else:
            match self.stage:
                case 0:
                    self.dealer.get_card(face_up=False)
                    self.stage += 1
                case 1:
                    self.dealer.hand[-1].flip()
                    self.stage += 1
                case 2:
                    self.dealer.get_score()
                    self.score_tracker.update()
                    if self.dealer.score < 17:
                        self.stage = 0
                    else:
                        self.stage += 1
                        self.compare_score()

    def repack_handler(self):
        match self.stage:
            case 0:
                for card in self.player.hand:
                    card.flip()
                for card in self.dealer.hand:
                    if card.face_up:
                        card.flip()
                if data.splitted:
                    for card in self.player_second_hand.hand:
                        card.flip()
                self.stage += 1
            case 1:
                x_pos = self.deck.card_deck[-1].rect.x
                y_pos = self.deck.card_deck[-1].rect.y
                for card in self.player.hand:
                    card.move_animation((x_pos, y_pos), 0.5, -90)
                for card in self.dealer.hand:
                    card.move_animation((x_pos, y_pos), 0.5, -90)
                if data.splitted:
                    for card in self.player_second_hand.hand:
                        card.move_animation((x_pos, y_pos), 0.5, -90)

                self.stage += 1
            case 2:
                self.deck.card_deck.extend(
                    self.player.hand + self.dealer.hand + self.player_second_hand.hand)
                self.stage += 1
            case 3:
                self.reset()
                self.deck.shuffle()
                self.deck.reorder_deck()
                data.game_state = gameStatus.start
                self.stage = 0

    def compare_score(self):
        def compare_hand_to_dealer(self: 'Table', hand: Player):
            if hand.score == 21:
                hand.show_animated_text("BLACKJACK", gf.Color.WHITE)
                hand.result = data.gameStatus.win
            elif self.dealer.score == 21:
                self.dealer.show_animated_text("BLACKJACK", gf.Color.WHITE)
                hand.result = data.gameStatus.lose
            elif hand.score > 21:
                hand.show_animated_text("BUST", gf.Color.REDWOOD)
                hand.result = data.gameStatus.bust
            elif self.dealer.score > 21:
                self.dealer.show_animated_text("BUST", gf.Color.REDWOOD)
                hand.result = data.gameStatus.win
            elif hand.score == self.dealer.score:
                hand.result = data.gameStatus.push
            elif hand.score > self.dealer.score:
                hand.result = data.gameStatus.win
            else:
                hand.result = data.gameStatus.lose
        if self.player.result is None:
            compare_hand_to_dealer(self, self.player)
        if data.splitted and self.player_second_hand.result is None:
            compare_hand_to_dealer(self, self.player_second_hand)

    def draw(self):
        self.center_text_handler.draw()
        self.deck.draw()
        self.score_tracker.draw()
        self.player.draw()
        if data.splitted:
            self.player_second_hand.draw()
        self.dealer.draw()

    def reset(self):
        self.player.score = 0
        self.player.hand = []
        self.player.standing = False
        self.player.result = None
        self.player_second_hand.score = 0
        self.player_second_hand.hand = []
        self.player_second_hand.standing = False
        self.player_second_hand.result = None
        self.dealer.score = 0
        self.dealer.hand = []
        self.stage = 0
        self.dealer_card_down = True
        data.split_possible = False
        data.splitted = False
        self.active_hand = self.player
        self.score_tracker.reset()
