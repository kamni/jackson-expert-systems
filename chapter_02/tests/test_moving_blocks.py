import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from moving_blocks import BlockConfigurationNode


class BlockConfigurationNodeTests(unittest.TestCase):
    """Tests for chapter_02.moving_blocks.BlockConfigurationNode"""

    def test_init__default(self):
        starting_state = ((3,0), (3,0), 0)
        node1 = BlockConfigurationNode(starting_state)

        self.assertEqual(node1._current_state, starting_state)
        self.assertEqual(node1._game_state, [starting_state])
        self.assertEqual(node1._color_count, (3, 3))
        self.assertEqual(node1._num_hands, 2)

    def test_init__num_hands_specified(self):
        starting_state = ((3, 0), (3, 0), 0)
        node1 = BlockConfigurationNode(starting_state, num_hands=3)

        self.assertEqual(starting_state, node1._current_state)
        self.assertEqual([starting_state], node1._game_state)
        self.assertEqual((3, 3), node1._color_count)
        self.assertEqual(3, node1._num_hands)

    def test_init__child_node(self):
        starting_state = ((3, 0), (3, 0), 0)
        node1 = BlockConfigurationNode(starting_state)
        next_state = ((1,2), (3, 0), 0)
        node2 = BlockConfigurationNode(next_state, parent=node1, num_hands=3)

        self.assertEqual(next_state, node2._current_state)
        self.assertEqual(node1._game_state + [next_state], node2._game_state)
        self.assertEqual(node1._color_count, node2._color_count)
        # should ignore extra num_hands parameter when parent specified
        self.assertEqual(node2._num_hands, node1._num_hands)

    def test_init__node_isnt_valid(self):
        raise NotImplementedError

    def test_init__child_node_isnt_valid(self):
        # test from parent state
        raise NotImplementedError


if __name__ == '__main__':
    unittest.main()