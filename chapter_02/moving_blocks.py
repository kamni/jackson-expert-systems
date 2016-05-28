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
                 parent=None):
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
        self._moves = self._generate_valid_moves()
        self._valid = self._set_validity()

    def _generate_valid_moves(self):
        VALID_MOVES = {
            PILE1_REPR: [
                ((-1, 1), (0, 0)),  # R moves to pile2
                ((-2, 2), (0, 0)),  # RR moves to pile2
                ((-1, 1), (-1, 1)),  # RB moves to pile 2
                ((0, 0), (-2, 2)),  # BB moves to pile 2
                ((0, 0), (-1, 1)),  # B moves to pile 2
            ],
            PILE2_REPR: [
                ((1, -1), (0, 0)),  # R moves to pile1
                ((2, -2), (0, 0)),  # RR moves to pile1
                ((1, -1), (1, -1)),  # RB moves to pile 1
                ((0, 0), (2, -2)),  # BB moves to pile 1
                ((0, 0), (1, -1)),  # B moves to pile 1
            ]
        }

    def _set_validity(self):
        # block count shouldn't exceed expected total number between pile1 and pile2
        red_count_is_valid = self._check_block_count(self.RED_INDEX, self._red)
        blue_count_is_valid = self._check_block_count(self.BLUE_INDEX, self._blue)

        change_from_parent = self._calculate_state_change()

    # total number of blue across sides
    # total number of red across sides
    # difference between parent and node on any side must be at least one
    # difference between parent and node can't be more than number of hands
    # red on any side can't be greater than blue on same side

    def _check_block_count(self, game_state_index, total_expected_count):
        raise NotImplementedError

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
        pass

    def fulfills_goal(self, ending_state):
        pass


class BlockGameSolver(object):
    pass


if __name__ == '__main__':
    pass
