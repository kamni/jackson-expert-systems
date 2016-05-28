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
- You can always carry a block and choose not to put it in the pile.
"""

from search import AbstractNode


class BlockConfigurationNode(AbstractNode):
    """
    TODO: write docs
    """
    DEFAULT_NUM_BLUE_BLOCKS = 3
    DEFAULT_NUM_RED_BLOCKS = 3
    DEFAULT_NUM_HANDS = 2

    PILE1 = 0
    HAND = 1
    PILE2 = 2
    HAND_POSITION = 3

    def __init__(self, num_blue_blocks=DEFAULT_NUM_BLUE_BLOCKS,
                 num_red_blocks=DEFAULT_NUM_RED_BLOCKS, num_hands=DEFAULT_NUM_HANDS):
        self.hand_count = num_hands
        self.blue_count = num_blue_blocks
        self.red_count = num_red_blocks

        # basic setup
        self.beginning_state = self._create_game_state(
            self._create_state_for_block_type(self.red_count, 0, 0, 0),
            self._create_state_for_block_type(self.blue_count, 0, 0, 0)
        )
        self.game_paths = [self.beginning_state]
        self.end_goal = self._create_game_state(
            self._create_state_for_block_type(0, 0, self.red_count, 1),
            self._create_state_for_block_type(0, 0, self.blue_count, 1)
        )

    def generate_child_nodes(self):
        pass

    def fulfills_goal(self, ending_state):
        pass

    def _create_state_for_block_type(self, pile1, hand, pile2, hand_location):
        # While it looks like the method is just returning *args, this is a means of
        # decoupling so we can change the representation later without a complete rewrite
        return (pile1, hand, pile2, hand_location)

    def _create_game_state(self, state_for_red, state_for_blue):
        # While it looks like the method is just returning *args, this is a means of
        # decoupling so we can change the representation later without a complete rewrite
        return (state_for_red, state_for_blue)


if __name__ == '__main__':
    pass
