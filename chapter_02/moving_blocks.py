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

from search import AbstractNode


class BlockConfigurationNode(AbstractNode):
    """
    TODO: write docs
    """

    _allowed_moves = {}

    PILE1_REPR = 0
    PILE2_REPR = 1

    PILE1_INDEX = 0
    HAND_INDEX = 1
    PILE2_INDEX = 2
    HAND_POS_INDEX = 3

    RED_INDEX = 0
    BLUE_INDEX = 1

    def __init__(self, state_for_red, state_for_blue,
                 total_red, total_blue, total_hands,
                 allowed_moves, parent=None):
        """
        Creates a node for use in the 'Block Game' problem.

        :param state_for_red: tuple in the form (pile1, pile2, hand_location)
        :param state_for_blue: tuple in the form (pile1, pile2, hand_location)
        :param total_red: integer, expected total number of red blocks
        :param total_blue: integer, expected total number of blue blocks
        :param total_hands: integer, how many hands can move blocks
        :param parent: parent node
        """
        self._red = total_red
        self._blue = total_blue
        self._hands = total_hands
        self._parent = parent

        # game state setup
        self._state = self.game_state(state_for_red, state_for_blue)
        self._valid = self._set_validity()

    def _set_validity(self):
        pile1_red, pile2_red = self._get_block_count(self.RED_INDEX)
        pile1_blue, pile2_blue = self._get_block_count(self.BLUE_INDEX)

        # block count shouldn't exceed expected total number between pile1 and pile2
        valid_red_pile1_count = 0 <= pile1_red <= self._red
        valid_red_pile2_count = 0 <= pile2_red <= self._red
        valid_blue_pile1_count = 0 <= pile1_blue <= self._blue
        valid_blue_pile2_count = 0 <= pile2_blue <= self._blue

        # can't have more reds than blues in any pile
        valid_red_vs_blue_count = pile1_red <= pile1_blue and pile2_red <= pile2_blue

        return (valid_red_pile1_count and valid_red_pile2_count and
                valid_blue_pile1_count and valid_blue_pile2_count and
                valid_red_vs_blue_count)

    def _get_block_count(self, game_state_index):
        pile1_count = self._state[game_state_index][self.PILE1_INDEX]
        pile2_count = self._state[game_state_index][self.PILE2_INDEX]
        return pile1_count, pile2_count

    def allowed_moves(self):
        """
        Generates or gets from memoization valid moves for each pile of blocks.

        :return: dict representing allowed moves for each pile
        """
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

    @staticmethod
    def state_for_block_type(pile1, hand, pile2, hand_location):
        # While it looks like the method is just returning *args, this is a means of
        # decoupling so we can change the representation later without a complete rewrite
        return (pile1, hand, pile2, hand_location)

    @staticmethod
    def game_state(state_for_red, state_for_blue):
        # While it looks like the method is just returning *args, this is a means of
        # decoupling so we can change the representation later without a complete rewrite
        return (state_for_red, state_for_blue)

    def is_valid(self):
        return self._valid

    def generate_child_nodes(self):
        child_nodes = []

        # we don't want to waste time generating children for invalid nodes
        if self.is_valid():

            return []

        return child_nodes

    def fulfills_goal(self, ending_state):
        return self._state == ending_state


class BlockGameSolver(object):
    pass


if __name__ == '__main__':
    pass
