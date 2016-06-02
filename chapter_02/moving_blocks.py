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
            self._color_count = parent._color_count
            self._num_hands = parent._num_hands
        else:
            self._game_state = [new_state]
            self._color_count = (sum(self._get_count_for_piles(self.RED_INDEX)),
                                 sum(self._get_count_for_piles(self.BLUE_INDEX)))
            self._num_hands = num_hands

        self._valid = self._get_validity()

    def __repr__(self):
        for state in self._game_state:
            repr_string = '['
            for color_index in (self.RED_INDEX, self.BLUE_INDEX):

                for i in range(self._hands):
                    #if i <
                    pass

        raise NotImplementedError

    def __unicode__(self):
        return unicode(repr(self))

    def _get_validity(self):
        """
        Checks that a new node has a valid state.
        NOTE: does not check for states that would be unlikely to be generated using
        the public methods provided.

        :return: boolean, whether node meets the criteria for a valid node
        """
        pile1_red, pile2_red = self._get_count_for_piles(self.RED_INDEX)
        pile1_blue, pile2_blue = self._get_count_for_piles(self.BLUE_INDEX)

        # block count should always be a positive number
        non_negative_pile_counts = (pile1_red >= 0 and pile2_red >= 0 and
                                    pile1_blue >= 0 and pile2_blue >=0)

        # block count shouldn't exceed expected total number between pile1 and pile2
        total_reds = self._color_count[self.RED_INDEX]
        total_blues = self._color_count[self.BLUE_INDEX]
        valid_red_pile_count = sum([pile1_red, pile2_red]) == total_reds
        valid_blue_pile_count = sum([pile1_blue, pile2_blue]) == total_blues

        # can't have more reds than blues in any pile
        valid_red_vs_blue_count = pile1_red <= pile1_blue and pile2_red <= pile2_blue

        # don't repeat an existing game state
        non_repeating_game_state = True
        for state in self._game_state[:-1]:
            non_repeating_game_state = state != self._current_state

        return (non_negative_pile_counts and valid_red_vs_blue_count and
                valid_red_pile_count and valid_blue_pile_count and
                non_repeating_game_state)

    def _get_count_for_piles(self, color_index):
        """
        Count how many blocks of a given color are in each pile total
        :param color_index: integer representing which color should be returned for a
                block count; either RED_INDEX or BLUE_INDEX
        :return: tuple, (count for pile1, count for pile2)
        """
        return self._current_state[color_index]

    def _repr_for_state(self, state_tuple):
        state_repr = ''
        pile_counts = (self._get_count_for_piles(self.RED_INDEX),
                       self._get_count_for_piles(self.BLUE_INDEX))
        total_colors = (sum(pile_counts[0]), sum([1]))

        for pile_index in (self.PILE1_INDEX, self.PILE2_INDEX):
            state_repr += '['
            for color_index in (self.RED_INDEX, self.BLUE_INDEX):
                color_repr = ''
                for i in range(total_colors[color_index]):
                    if i < pile_counts[color_index][pile_index]:
                        color_repr += ['R', 'B'][color_index]
                    else:
                        color_repr += ' '
            state_repr += color_repr + ']'

            if pile_index == self.PILE1_INDEX:
                # repr for hand location
                if state_tuple[self.HAND_POS_INDEX] == self.PILE1_INDEX:
                    state_repr += 'O  '
                else:
                    state_repr += '  O'

        return state_repr

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

    def allowed_moves(self):
        """
        Generates or gets from memoization valid moves for each pile of blocks.

        :return: dict representing allowed moves for each pile
        """
        raise Exception("Not Updated")
        if not self._allowed_moves:
            pile1 = []
            pile2 = []

            for i in range(self._hands):  # counter for Red
                for j in range(self.hands - 1, -1, -1):  # counter for Blue
                    if not (i == 0 and j == 0):  # we have to move at least one block
                        pile1.append((-i, i), (-j, j))
                        pile2.append((i, -i), (j, -j))

            self._allowed_moves[self.PILE1_INDEX] = pile1
            self._allowed_moves[self.PILE2_INDEX] = pile2

        return self._allowed_moves

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
        raise Exception("Not Updated")
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

