import random as rd
from typing import List, Tuple

SUIT = ('Club', 'Diamond', 'Heart', 'Spade')
VALUE = ('3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2')
COMB_RANKING = ('high', 'pair', 'straight', 'full house', 'four of a kind', 'flush straight')
SUIT_st = ('Clb', 'Dmd', 'Hrt', 'Spd')


class Card(object):

    def __init__(self,
                 number: int = None,
                 suit: int = None,
                 value: int = None,
                 sv=''):

        self.num = number if type(number) is int else None

        if self.num is not None:

            self.suit = self.num % 4
            self.value = self.num // 4

        else:

            self.suit = suit if type(suit) is int else None
            self.value = value if type(value) is int else None

            if len(sv) > 0 and (self.suit is None or self.value is None):

                for i, suit_i in enumerate(x[0].lower() for x in SUIT):
                    if sv[0] == suit_i:
                        self.suit = i
                for j, value_j in enumerate(x[0].lower() for x in VALUE):
                    if sv[1] == value_j:
                        self.value = j
                del i, suit_i, j, value_j

                if self.suit is None or self.value is None:
                    print('entered wrong!')
                    self.suit, self.value = None, None

            if type(self.suit) is int and type(self.value) is int:
                self.num = self.value * 4 + self.suit

        if self.num is not None:
            if not (52 > self.num >= 0 and
                    4 > self.suit >= 0 and
                    13 > self.value >= 0):
                print('something wrong!')
                self.suit, self.value, self.num = None, None, None

    def print_card(self, short=True):

        if self.suit is None or self.value is None:
            print('undefined card!')

        else:

            if short:
                print(SUIT_st[self.suit], '%-2s' % VALUE[self.value], sep='.', end=' ')

            else:
                print('%-7s' % SUIT[self.suit], '_', VALUE[self.value])

    def input_card(self):

        s_correct = False
        v_correct = False

        again = ''
        while s_correct is False or v_correct is False:
            sv = input(f'enter card {again}: ')
            for i, suit_i in enumerate(x[0].lower() for x in SUIT):
                if sv[0] == suit_i:
                    self.suit = i
                    s_correct = True
            for j, value_j in enumerate(x[0].lower() for x in VALUE):
                if sv[1] == value_j:
                    self.value = j
                    v_correct = True
            again = 'again'
        del i, suit_i, j, value_j, s_correct, v_correct, again


class CardList(List[Card]):

    def __init__(self, cards: List[Card] = None):
        super().__init__()
        if cards is not None:
            super().extend(cards)

    def append(self, card_obj: Card = None, card_num: int = None):

        if type(card_obj) is Card:
            card = card_obj
        elif type(card_num) is int:
            card = Card(card_num)
        else:
            print('something wrong!')
            return

        if card.num is not None:

            if card.num in [x.num for x in self]:
                print('cannot append repeated card!')

            else:
                for i, ori_card in enumerate(self):
                    if ori_card.num > card.num:
                        super().insert(i, card)
                        break

    def print_cards(self, form=0):

        if form == 0:

            for card in self:
                card.print_card()
            print('')

        else:

            for i, card in enumerate(self):
                print('%3s' % SUIT_st[card.suit], end=' | ' if i != len(self) - 1 else '')
            print('')

            for i, card in enumerate(self):
                print('%3s' % VALUE[card.value], end=' | ' if i != len(self) - 1 else '')
            print('')

            if form == 2:
                for i in range(len(self)):
                    print('%3s' % str(i+1), end='   ' if i != len(self) - 1 else '')
                print('')

    def remove_multi_cards(self, cards):

        for card in cards:
            if card in self:
                self.remove(card)
            else:
                print('card not found!')
                return

    def rank_list(self):
        return [x.num for x in self]

    def to_list(self):
        return [x for x in self]


class CardCombinations(CardList):

    def __init__(self, rank: int, key_card: Card):
        super().__init__()
        self.rank = rank
        self.key_card = key_card
        self.name = COMB_RANKING[rank].upper()

    def print_comb(self, show_all_cards=False, show_comb_name=False):

        if show_comb_name:
            print(self.name, end=' ')

        if show_all_cards:
            self.print_cards()

        else:
            self.key_card.print_card()


class High(CardCombinations):

    def __init__(self, card: Card):
        super().__init__(0, card)
        self.extend([card])


class Pair(CardCombinations):

    def __init__(self, cards: List[Card]):

        if len(cards) == 2 and cards[0].value == cards[1].value:
            super().__init__(1, cards[-1])
            self.extend(cards)

        else:
            print('Not a PAIR!')
            return


class Straight(CardCombinations):

    def __init__(self, cards: List[Card]):

        if len(cards) == 5:
            for i in range(1, 5):

                if cards[i].value - 1 != cards[i - 1].value:
                    print('Not a STRAIGHT!')
                    return

                if i == 4:
                    super().__init__(2, cards[-1])
                    self.extend(cards)

        else:
            print('WRONG CARDS NUMBER for a Straight!')
            return


class FullHouse(CardCombinations):

    def __init__(self, cards: List[Card]):

        if len(cards) == 5:
            values = [x.value for x in cards]
            if values[1] == values[0] and values[4] == values[3] == values[2]:
                super().__init__(3, cards[-1])
                self.extend(cards)
            else:
                print('NOT a FULL HOUSE!')
                return

        else:
            print('WRONG CARD NUMBER for a FULL HOUSE!')
            return


class FourOfAKind(CardCombinations):

    def __init__(self, cards: List[Card]):

        if len(cards) == 4:

            for i in range(3):
                if cards[i].value != cards[i + 1].value:
                    print('NOT a FULL HOUSE!')
                    return
                if i == 2:
                    super().__init__(4, cards[-1])
                    self.extend(cards)

        else:
            print('WRONG CARD NUMBER for a FULL HOUSE!')
            return


class FlushStraight(CardCombinations):

    def __init__(self, cards: List[Card]):

        if len(cards) == 5:
            for i in range(1, 5):

                if cards[i].value - 1 != cards[i - 1].value or \
                        cards[i].suit != cards[i - 1].suit:
                    print('Not a FLUSH STRAIGHT!')
                    return

                if i == 4:

                    super().__init__(5, cards[-1])
                    self.extend(cards)

        else:
            print('WRONG CARDS NUMBER for a FLUSH STRAIGHT!')
            return


class Table(List[CardCombinations]):

    def __init__(self):
        super().__init__()
        self.pass_count = 0

    def print_current_comb(self):
        print('CURRENT CARDS IS:', end='   ')
        self[-1].print_comb(False, True)
        print('\n')

    def append(self, comb: CardCombinations):
        super(Table, self).append(comb)
        self.pass_count = 0

    def clear(self):
        super(Table, self).clear()
        self.pass_count = 0


class Players(CardList):

    def __init__(self, name=None, assign_card=None, get_card=0, used_card=None):

        super().__init__()
        self.name = name

        if assign_card is not None:

            if type(assign_card[0]) is int:
                super().extend([Card(x) for x in assign_card])
            elif type(assign_card[0]) is Card:
                super().extend(assign_card)
            else:
                print('wrong assignment')

        if get_card:

            unused = [x for x in range(52) if x not in used_card] \
                if type(used_card) is list else list(range(52))

            for rd_num in rd.sample(unused, get_card):
                super().append(Card(rd_num))
            del unused

        super().sort(key=lambda s: s.num)

    def hand(self, print_hand=False):

        high = [High(x) for x in self]
        pair = []
        straight = []
        full_house = []
        four = []
        flush_straight = []

        if len(self) > 4:

            str_temp = []
            values = [x.value for x in self]
            unrepeated = []

            for v in values:
                if v not in unrepeated:
                    unrepeated.append(v)

            for i in range(3, len(unrepeated)):
                if unrepeated[i - 4] == unrepeated[i] - 4:
                    str_temp.append(unrepeated[i])

            if len(str_temp) > 0:

                for str_top in str_temp:

                    str_lowers = [x for x in self if str_top > x.value >= str_top - 4]
                    str_tops = [x for x in self if x.value == str_top]

                    for cd in str_tops:
                        flu = [x for x in str_lowers if x.suit == cd.suit]
                        if len(flu) == 4:
                            flush_straight.append(FlushStraight(flu[:] + [cd]))

                    n = 0
                    while len(str_lowers) > 4:
                        if str_lowers[n].value == str_lowers[n + 1].value:
                            str_lowers.pop(n + 1)
                        else:
                            n += 1

                    for cd in str_tops:
                        straight.append(Straight(str_lowers[:] + [cd]))

        if len(self) > 1:

            three = []
            for count_2 in range(1, len(self)):

                if self[count_2].value == self[count_2 - 1].value:
                    pair_low = [x for x in self if x.value == self[count_2].value][0]
                    pair.append(Pair([pair_low, self[count_2]]))

                if count_2 >= 2 and len(self) > 4:

                    if self[count_2].value == self[count_2 - 2].value:
                        temp_three = [x for x in self if x.value == self[count_2].value][0:2]
                        three.append(temp_three + [self[count_2]])

                    if count_2 >= 3 and self[count_2].value == self[count_2 - 3].value:
                        four.append(FourOfAKind([x for x in self if
                                                 x.value == self[count_2].value]))

            if len(three) > 0 and len(pair) > 2:
                for fh in three:
                    fh_low = pair[0] if pair[0][0].value != fh[0].value else pair[2]
                    full_house.append(FullHouse(fh_low.to_list() + fh))

        hand_list: Tuple[List[High],
                         List[Pair],
                         List[Straight],
                         List[FullHouse],
                         List[FourOfAKind],
                         List[FlushStraight]] \
            = (high, pair, straight, full_house, four, flush_straight)

        if print_hand:

            print(f'{self.name} hand:\n')
            for i in range(1, 6):
                if len(hand_list[i]) > 0:
                    print(hand_list[i][0].name, ':', end=' ')
                    for j in hand_list[i]:
                        j.print_comb(False, False)
                    print('')
            print('')

        return hand_list

    def put_card(self, table: Table, fst_round=False) -> bool:

        if table.pass_count == 3:
            table.clear()
            print('New Round!\n')

        print(self.name.upper(), '\'s turn:')
        self.print_cards(1)
        print('')
        hands = self.hand()
        to_pass = False
        super_card = False

        if len(table) > 0:
            table.print_current_comb()
            if table[-1].rank < 4 and (len(hands[4]) > 0 or len(hands[5]) > 0) and \
                    input('\n***use super cards (FOUR or FLUSH_Str)?*** (y) :') == 'y':
                super_card = True

        if len(table) == 0:

            hand_choices = [x for x in hands if len(x) > 0]

            if fst_round:

                hand_choices_2 = []

                for i in range(len(hand_choices)):
                    comb_2 = []
                    for cb in hand_choices[i]:
                        fst = False
                        for cd in cb:
                            if cd.num == 0:
                                fst = True
                        if fst:
                            comb_2.append(cb)
                    if len(comb_2) > 0:
                        hand_choices_2.append(comb_2)

                hand_choices.clear()
                hand_choices = hand_choices_2[:]

            if len(hand_choices) > 1:

                for i in range(len(hand_choices)):

                    if hand_choices[i][0].rank == 0:
                        continue
                    print('%2s' % str(i), '_', hand_choices[i][0].name, end=' :  ')
                    for cb in hand_choices[i]:
                        cb.print_comb()
                    print('')
                print('')
                choose = enter_num('choose combination (0 for high):', len(hand_choices)-1, 0)
                print('')

            else:
                choose = 0

            comb_choices = hand_choices[choose][:]

        elif super_card:

            hand_choices = [x for x in hands[4:] if len(x) > 0]

            for i in range(len(hand_choices)):

                print('%2s' % str(i+1), '_', hand_choices[i][0].name, end=' :   ')
                for cb in hand_choices[i]:
                    cb.print_comb()

                print('\n')

            choose = enter_num('choose super combination:', len(hand_choices), 1) - 1
            print('')

            comb_choices = hand_choices[choose][:]

        else:

            comb_choices = [x for x in hands[table[-1].rank] if
                            x.key_card.num > table[-1].key_card.num]

        if len(comb_choices) == 0:

            input('no choice but PASS! (press to continue)')
            to_pass = True
            chosen_cards = None

        else:

            for i, cb in enumerate(comb_choices):

                print('%2s' % str(i+1), end=' _ ')
                if comb_choices[0].rank == 0:
                    cb.print_comb()
                    print('   ', end='\n' if i % 3 == 2 or i == len(comb_choices) - 1 else '')
                else:
                    cb.print_comb(True)

            pass_tx = '' if len(table) == 0 or super_card else '(0 for pass)'

            if pass_tx == '' and len(comb_choices) == 1:
                choose = 1
                input('\nthe only choice to put (press to continue)')
                print('')

            else:
                print('')
                choose = enter_num(f'choose which {comb_choices[0].name} to put {pass_tx}:',
                                   len(comb_choices), 0 if pass_tx != '' else 1)
                print('')

            if choose == 0:

                to_pass = True
                chosen_cards = None

            else:
                chosen_cards = comb_choices[choose - 1]

        if to_pass:

            print('')
            print('=' * 5, self.name, 'PASS', '=' * 5, end='\n\n')
            table.pass_count += 1

        else:

            if chosen_cards.rank == 4:
                extras = [x for x in self if x.value != chosen_cards.key_card.value]
                for cd in extras:
                    cd.print_card()
                print('')
                for i in range(len(extras)):
                    print('  %2s   ' % str(i+1), end='')
                print('\n')
                choose_low = enter_num('choose which to put with FOak:', len(extras), 1)
                self.remove(extras[choose_low-1])

            table.append(chosen_cards)
            print_process(chosen_cards, self.name)
            self.remove_multi_cards(chosen_cards)

        if len(self) == 0:
            print(f'{self.name.upper()} is the winner')
            return True

        else:
            return False


def print_process(x: CardCombinations, name):

    print('')
    print('=' * 5, name, 'PUT', '=' * 5)
    x.print_comb(False, True)
    print('')
    print('=' * 24)
    print('')


def enter_num(txt: str, top, low):

    success = False
    again = ''
    num = low - 1

    while not success:

        try:
            num = int(input(f'{again}{txt} '))
        except ValueError:
            num = top + 1

        if top >= num >= low:
            success = True
        else:
            again = 'AGAIN '

    return num


if __name__ == '__main__':

    starting = 'Play game'

    while input(f'{starting}?(y) :') == 'y':

        print('\n======GAME STARTED!======\n')

        c = [x for x in range(52)]
        rd.shuffle(c)
        table_0 = Table()

        players = (Players('Player 1', c[:13]),
                   Players('Player 2', c[13:26]),
                   Players('Player 3', c[26:39]),
                   Players('Player 4', c[39:]))

        fst_round_0 = True
        end = False

        while not end:

            for plr in players:

                if fst_round_0 and plr[0].num != 0:
                    continue
                elif end:
                    break
                else:
                    end = plr.put_card(table_0, fst_round_0)
                    fst_round_0 = False

        starting = 'Another Round'
