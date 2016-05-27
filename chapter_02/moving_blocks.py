"""
The problem in the book is stated as 'missionaries and cannibals', and the alternate
name for the problem is 'jealous husbands'. Both of these framings are problematic,
so we're just going to reword it as a blocks game. The rules are as follows:

- You're a small child that has a pile of 3 red and 3 blue blocks.
- You want to move all of your blocks from one pile to another pile.
- Each block is the size of your hand, so you can at most move two blocks at a time
    (one for each hand).
- When moving between piles, you must always move at least one block.
- To make the game more fun, you're not allowed to have a pile where the red blocks
    outnumber the blue blocks at any time.
- You can always carry a block and choose not to put it in the pile.
"""

from search import AbstractNode


DEFAULT_BLUE_BLOCKS = 3
DEFAULT_RED_BLOCKS = 3


class BlockConfigurationNode(AbstractNode):
    """
    TODO: write docs
    """

    # TODO: want to generate a valid starting and ending state

    def __init__(self, blue_blocks=DEFAULT_BLUE_BLOCKS, red_blocks=DEFAULT_RED_BLOCKS):
        self.starting_state = {

        }

    def generate_child_nodes(self):
        pass

    def fulfills_goal(self, ending_state):
        return self.starting_state == ending_state


if __name__ == '__main__':
    pass
    '''
    3 B in P0
    3 R in P0
    0 B in H
    0 R in H
    0 B in P1
    0 R in P1

    {
        'P0': {'R': 3, 'B': 3 },
        'H': {'R': 1, 'B':
    '''
