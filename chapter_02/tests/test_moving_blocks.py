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
        self.assertEqual(None, node1._parent)
        self.assertEqual(node1._game_state, [starting_state])
        self.assertEqual(node1._color_count, (3, 3))
        self.assertEqual(node1._num_hands, 2)

    def test_init__num_hands_specified(self):
        starting_state = ((3, 0), (3, 0), 0)
        node1 = BlockConfigurationNode(starting_state, num_hands=3)

        self.assertEqual(starting_state, node1._current_state)
        self.assertEqual(None, node1._parent)
        self.assertEqual([starting_state], node1._game_state)
        self.assertEqual((3, 3), node1._color_count)
        self.assertEqual(3, node1._num_hands)

    def test_init__child_node(self):
        starting_state = ((3, 0), (3, 0), 0)
        node1 = BlockConfigurationNode(starting_state)
        next_state = ((1,2), (3, 0), 0)
        node2 = BlockConfigurationNode(next_state, parent=node1, num_hands=3)

        self.assertEqual(next_state, node2._current_state)
        self.assertEqual(node1, node2._parent)
        self.assertEqual(node1._game_state + [next_state], node2._game_state)
        self.assertEqual(node1._color_count, node2._color_count)
        # should ignore extra num_hands parameter when parent specified
        self.assertEqual(node2._num_hands, node1._num_hands)

    def test_init__node_isnt_valid(self):
        too_many_reds_state = ((3, 0), (2, 1), 0)
        node1 = BlockConfigurationNode(too_many_reds_state)
        self.assertFalse(node1._valid)

    def test_init__child_node_isnt_valid(self):
        starting_state = ((3, 0), (3, 0), 0)
        node1 = BlockConfigurationNode(starting_state)

        lost_some_blocks = ((2, 0), (2, 0), 1)
        node2 = BlockConfigurationNode(lost_some_blocks, parent=node1)
        self.assertFalse(node2._valid)

    def test_get_validity__default(self):
        starting_state = ((3, 0), (3, 0), 0)
        node1 = BlockConfigurationNode(starting_state)
        self.assertTrue(node1._get_validity())

        next_state = ((2,1), (2, 1), 1)
        node2 = BlockConfigurationNode(next_state, parent=node1)
        self.assertTrue(node2._get_validity())

    def test_get_validity__more_red_than_blue(self):
        starting_state = ((3, 0), (2, 1), 0)
        node1 = BlockConfigurationNode(starting_state)
        self.assertFalse(node1._get_validity())

    def test_get_validity__non_negative_pile_numbers(self):
        starting_state = ((-1, -2), (2, -1), 0)
        node1 = BlockConfigurationNode(starting_state)
        self.assertFalse(node1._get_validity())

    def test_get_validity__expected_pile_numbers_match_total_count(self):
        starting_state = ((3, 0), (3, 0), 0)
        node1 = BlockConfigurationNode(starting_state)
        node1._color_count = (2, 2)
        self.assertFalse(node1._get_validity())

    def test_get_validity__no_state_repeats(self):
        starting_state = ((3, 0), (3, 0), 0)
        node1 = BlockConfigurationNode(starting_state)
        node2 = BlockConfigurationNode(starting_state, parent=node1)
        self.assertFalse(node2._get_validity())

    def test_get_count_for_piles(self):
        starting_state = ((2, 1), (3, 2), 0)
        node1 = BlockConfigurationNode(starting_state)
        self.assertEqual((2, 1), node1._get_count_for_piles(BlockConfigurationNode.RED_INDEX))
        self.assertEqual((3, 2), node1._get_count_for_piles(BlockConfigurationNode.BLUE_INDEX))

    def test_repr(self):
        state1 = ((3, 0), (3, 0), 0)
        node1 = BlockConfigurationNode(state1, num_hands=3)
        expected1 = '[RRR | BBB] OOO    [    |    ]'
        self.assertEqual(expected1, repr(node1))

        state2 = ((2, 1), (2, 1), 1)
        node2 = BlockConfigurationNode(state2, parent=node1)
        expected2 = os.linesep.join([expected1, '[RR  | BB ]    OOO [R   | B  ]'])
        self.assertEqual(expected2, repr(node2))

    def test_repr_for_state__hand_on_left(self):
        starting_state = ((2, 1), (3, 2), 0)
        node1 = BlockConfigurationNode(starting_state)
        expected_repr = '[RR  | BBB  ] OO   [R   | BB   ]'
        self.assertEqual(expected_repr, node1._repr_for_state(starting_state))

    def test_repr_for_state__hand_on_right(self):
        starting_state = ((2, 1), (3, 2), 1)
        node1 = BlockConfigurationNode(starting_state)
        expected_repr = '[RR  | BBB  ]   OO [R   | BB   ]'
        self.assertEqual(expected_repr, node1._repr_for_state(starting_state))


if __name__ == '__main__':
    unittest.main()