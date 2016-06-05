"""
The problem in the book is stated as 'missionaries and cannibals', and the alternate
name for the problem is 'jealous husbands'. Both of these framings are problematic,
so we're just going to reword it as a blocks game. The rules are as follows:

- You're a small child that has a pile of 3 red and 3 blue blocks.
- You want to move all of your blocks from one pile to another pile.
- Each block is the size of your hand, so you can at most move two blocks at a time
    (one for each hand). You may enlist your friends to play this game (more hands),
    but the default is just you.
- When moving between piles, you must always move at least one block.
- To make the game more fun, you're not allowed to have a pile where the red blocks
    outnumber the blue blocks at any time.
- You can ignore the blue/red count for blocks in the hand
"""

import os

from search import AbstractNode, AbstractSearch


class BlockConfigurationNode(AbstractNode):
    """
    TODO: write docs
    """

    _allowed_moves = {}

    PILE1_INDEX = 0
    PILE2_INDEX = 1
    HAND_POS_INDEX = 2

    RED_INDEX = 0
    BLUE_INDEX = 1

    def __init__(self, new_state, parent=None, num_hands=2):
        """
        Creates a node for use in the 'Block Game' problem.

        :param new_state: tuple representing the current node state. Should be
                generated using BlockConfigurationNode.create_state
        :param parent: node that is the parent of the current node in the search tree
        :param num_hands: integer, number of hands available to move blocks. Ignore
                this param if passing parent -- the value will be taken from the
                parent if the parent exists.
        """
        self._current_state = new_state
        self._parent = parent

        if parent:
            self._game_state = parent._game_state + [new_state]
            self._num_hands = parent._num_hands
            self._possible_moves = parent._possible_moves
        else:
            self._game_state = [new_state]
            self._num_hands = num_hands
            self._possible_moves = self._calculate_possible_moves()

        self._is_valid = self._calculate_validity(self._current_state)

    def _calculate_possible_moves(self):
        """
        Figures out the possible moves for each pile of blocks.
        Note: this only generates possible moves, not necessarily valid moves for the
            current node. The node itself should evaluate whether or not it is valid
            when it is created.

        :return: tuple of two lists, where each item in the list represents a move that
            can be made from a given pile
        """
        red_count, blue_count = self.total_red_and_blue_count_for_state(self._current_state)
        pile1 = []
        pile2 = []

        for red in range(self._num_hands+1):
            for blue in range(self._num_hands, -1, -1):
                move_is_possible = (red <= red_count and
                                    blue <= blue_count and
                                    red + blue <= self._num_hands and
                                    not (red == 0 and blue == 0))

                if move_is_possible:
                    pile1.append(((-red, red), (-blue, blue)))
                    pile2.append(((red, -red), (blue, -blue)))

        return pile1, pile2

    def _calculate_validity(self, state_tuple):
        """
        Checks that a new node has a valid state.
        NOTE: does not check for states that would be unlikely to be generated using
        the public methods provided -- for example, mismatched parent and child nodes

        :return: boolean, whether node meets the criteria for a valid node
        """
        pile1, pile2 = self.red_and_blue_counts_for_each_pile(state_tuple)
        pile1_red, pile1_blue = pile1
        pile2_red, pile2_blue = pile2

        # block count should always be a positive number
        non_negative_pile_counts = (pile1_red >= 0 and pile2_red >= 0 and
                                    pile1_blue >= 0 and pile2_blue >=0)

        # can't have more reds than blues in any pile
        valid_red_vs_blue_count = pile1_red <= pile1_blue and pile2_red <= pile2_blue

        # don't repeat an existing game state
        non_repeating_game_state = True
        for state in self._game_state[:-1]:
            non_repeating_game_state = state != self._current_state

        return (non_negative_pile_counts and valid_red_vs_blue_count and
                non_repeating_game_state)





    def __repr__(self):
        return os.linesep.join([self._repr_for_state(state) for state in self._game_state])

    def _repr_for_state(self, state_tuple):
        pile_counts = (state_tuple[self.RED_INDEX], state_tuple[self.BLUE_INDEX])
        total_colors = (sum(pile_counts[0]), sum(pile_counts[1]))

        state_repr = ''
        for pile_index in (self.PILE1_INDEX, self.PILE2_INDEX):
            pile_repr = '['

            for color_index in (self.RED_INDEX, self.BLUE_INDEX):
                color_repr = ''

                for i in range(total_colors[color_index]):
                    if i < pile_counts[color_index][pile_index]:
                        color_repr += ['R', 'B'][color_index]
                    else:
                        color_repr += ' '

                if color_index == self.RED_INDEX:
                    separator = ' | '
                    color_repr += separator

                pile_repr += color_repr

            pile_repr += ']'

            hand_location_repr = ''
            if pile_index == self.PILE1_INDEX:
                hands_repr = 'O' * self._num_hands
                space_repr = ' ' * self._num_hands

                hand_location_repr = ' '
                if state_tuple[self.HAND_POS_INDEX] == self.PILE1_INDEX:
                    hand_location_repr += hands_repr + space_repr
                else:
                    hand_location_repr += space_repr + hands_repr
                hand_location_repr += ' '

            state_repr += pile_repr + hand_location_repr

        return state_repr

    def __unicode__(self):
        return unicode(repr(self))


    @staticmethod
    def red_and_blue_counts_for_each_pile(state_tuple):
        """
        Returns the red and blue counts for each pile of a given state tuple

        :param state_tuple: tuple representing a valid node state
        :return: ((reds in pile1, blues in pile1), (reds in pile2, blues in pile2))
        """
        pile1_red, pile2_red = state_tuple[BlockConfigurationNode.RED_INDEX]
        pile1_blue, pile2_blue = state_tuple[BlockConfigurationNode.BLUE_INDEX]
        return (pile1_red, pile1_blue), (pile2_red, pile2_blue)

    @staticmethod
    def total_red_and_blue_count_for_state(state_tuple):
        """
        Returns the total count of reds, blues for a given state tuple

        :param state_tuple: tuple representing a valid node state
        :return: (total reds, total blues)
        """
        red_state, blue_state, _ = state_tuple
        return sum(red_state), sum(blue_state)



    '''
    def _new_move(self, old_move_tuple, new_move_tuple):
        raise Exception("Not Updated")
        move = []
        move[self.PILE1_INDEX] = old_move_tuple[self.PILE1_INDEX] + new_move_tuple[self.PILE1_INDEX]
        move[self.PILE2_INDEX] = old_move_tuple[self.PILE2_INDEX] + new_move_tuple[self.PILE2_INDEX]
        return move

    def _new_child_node(self, new_red_state, new_blue_state, new_hand_location):
        raise Exception("Not Updated")
        return BlockConfigurationNode(new_red_state, new_blue_state, new_hand_location,
                                       self._red, self._blue, self._hands, self)
    '''

    '''
    @classmethod
    def create_state(cls, red_pile1, red_pile2, blue_pile1, blue_pile2, hand_location):
        raise NotImplementedError

    @staticmethod
    def state_for_block_type(pile1, pile2):
        raise Exception("Not Updated")
        # While it looks like the method is just returning *args, this is a means of
        # decoupling so we can change the representation later without a complete rewrite
        return pile1, pile2

    @staticmethod
    def game_state(state_for_red, state_for_blue, current_hand):
        raise Exception("Not Updated")
        # While it looks like the method is just returning *args, this is a means of
        # decoupling so we can change the representation later without a complete rewrite
        return state_for_red, state_for_blue, current_hand
    '''
    def is_valid(self):
        return self._valid

    def generate_child_nodes(self):
        raise Exception('Not Implemented')
        child_nodes = []

        # we don't want to waste time generating children for invalid nodes
        if self.is_valid():
            next_hand_loc = self._hand_loc + 1 % self._hands
            for move in self._allowed_moves:
                new_move_red = self._new_move(self._state[self.RED_INDEX], move)
                new_move_blue = self._new_move(self._state[self.BLUE_INDEX], move)
                new_node = self._new_child_node(new_move_red, new_move_blue, next_hand_loc)
                child_nodes.append(new_node)

        return child_nodes

    def fulfills_goal(self, ending_state):
        raise Exception("Not Updated")
        return self._state == ending_state

'''
class BlockGameSolver(AbstractSearch):
    """
    TODO: write docs
    """

    def __init__(self, num_red_blocks, num_blue_blocks, num_hands):
        self._red = num_red_blocks
        self._blue = num_blue_blocks
        self._hands = num_hands

        self.paths
'''

if __name__ == '__main__':
    pass

