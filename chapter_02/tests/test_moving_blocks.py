import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from moving_blocks import BlockConfigurationNode


class BlockConfigurationNodeTests(unittest.TestCase):
    """Tests for chapter_02.moving_blocks.BlockConfigurationNode"""

    def test_init__default(self):
        state1 = ((3,0), (3,0), 0)
        node1 = BlockConfigurationNode(state1)

        self.assertEqual(node1._current_state, state1)
        self.assertEqual(None, node1._parent)
        self.assertEqual(node1._game_state, [state1])
        self.assertEqual(node1._num_hands, 2)
        self.assertTrue(node1._is_valid)

    def test_init__num_hands_specified(self):
        state1 = ((3, 0), (3, 0), 0)
        node1 = BlockConfigurationNode(state1, num_hands=3)

        self.assertEqual(state1, node1._current_state)
        self.assertEqual(None, node1._parent)
        self.assertEqual([state1], node1._game_state)
        self.assertEqual(3, node1._num_hands)
        self.assertTrue(node1._is_valid)

    def test_init__child_node(self):
        state1 = ((3, 0), (3, 0), 0)
        node1 = BlockConfigurationNode(state1)
        next_state = ((2, 1), (2, 1), 0)
        node2 = BlockConfigurationNode(next_state, parent=node1, num_hands=3)

        self.assertEqual(next_state, node2._current_state)
        self.assertEqual(node1, node2._parent)
        self.assertEqual(node1._game_state + [next_state], node2._game_state)
        # should ignore extra num_hands parameter when parent specified
        self.assertEqual(node2._num_hands, node1._num_hands)
        self.assertTrue(node2._is_valid)

    def test_init__node_isnt_valid(self):
        too_many_reds_state = ((3, 0), (2, 1), 0)
        node1 = BlockConfigurationNode(too_many_reds_state)
        self.assertFalse(node1._is_valid)

    def test_init__child_node_isnt_valid(self):
        state1 = ((3, 0), (3, 0), 0)
        node1 = BlockConfigurationNode(state1)

        state2 = ((1, 2), (3, 0), 1)
        node2 = BlockConfigurationNode(state2, parent=node1)
        self.assertFalse(node2._is_valid)

    def test_calculate_possible_moves__one_red_and_blue_plus_one_hand(self):
        state1 = ((1, 0), (1, 0), 0)
        node1 = BlockConfigurationNode(state1, num_hands=1)
        expected_pile1 = [
            ((-1, 1), (0, 0)),
            ((0, 0), (-1, 1))
        ]
        expected_pile2 = [
            ((1, -1), (0, 0)),
            ((0, 0), (1, -1))
        ]

        returned_pile1, returned_pile2 = node1._calculate_possible_moves()
        self.assertEqual(len(expected_pile1), len(returned_pile1))
        self.assertEqual(len(expected_pile2), len(returned_pile2))
        for move in expected_pile1:
            self.assertTrue(move in returned_pile1)
        for move in expected_pile2:
            self.assertTrue(move in returned_pile2)

    def test_calculate_possible_moves__three_red_and_blue_plus_two_hands(self):
        state1 = ((2, 1), (3, 0), 0)
        node1 = BlockConfigurationNode(state1, num_hands=2)
        expected_pile1 = [
            ((-1, 1), (0, 0)),
            ((0, 0), (-1, 1)),
            ((-1, 1), (-1, 1)),
            ((-2, 2), (0, 0)),
            ((0, 0), (-2, 2))
        ]
        expected_pile2 = [
            ((1, -1), (0, 0)),
            ((0, 0), (1, -1)),
            ((1, -1), (1, -1)),
            ((2, -2), (0, 0)),
            ((0, 0), (2, -2))
        ]

        returned_pile1, returned_pile2 = node1._calculate_possible_moves()
        self.assertEqual(len(expected_pile1), len(returned_pile1))
        self.assertEqual(len(expected_pile2), len(returned_pile2))
        for move in expected_pile1:
            self.assertTrue(move in returned_pile1)
        for move in expected_pile2:
            self.assertTrue(move in returned_pile2)

    def test_generate_possible_moves__more_hands_than_blocks(self):
        # We don't want to generate more moves than blocks
        state1 = ((1, 0), (1, 0), 0)
        node1 = BlockConfigurationNode(state1, num_hands=5)
        expected_pile1 = [
            ((-1, 1), (0, 0)),
            ((0, 0), (-1, 1)),
            ((-1, 1), (-1, 1))
        ]
        expected_pile2 = [
            ((1, -1), (0, 0)),
            ((0, 0), (1, -1)),
            ((1, -1), (1, -1))
        ]

        returned_pile1, returned_pile2 = node1._calculate_possible_moves()
        self.assertEqual(len(expected_pile1), len(returned_pile1))
        self.assertEqual(len(expected_pile2), len(returned_pile2))
        for move in expected_pile1:
            self.assertTrue(move in returned_pile1)
        for move in expected_pile2:
            self.assertTrue(move in returned_pile2)

    '''
    def test_get_validity__default(self):
        starting_state = ((3, 0), (3, 0), 0)
        node1 = BlockConfigurationNode(starting_state)
        self.assertTrue(node1.get_validity())

        next_state = ((2,1), (2, 1), 1)
        node2 = BlockConfigurationNode(next_state, parent=node1)
        self.assertTrue(node2.get_validity())

    def test_get_validity__more_red_than_blue(self):
        starting_state = ((3, 0), (2, 1), 0)
        node1 = BlockConfigurationNode(starting_state)
        self.assertFalse(node1.get_validity())

    def test_get_validity__non_negative_pile_numbers(self):
        starting_state = ((-1, -2), (2, -1), 0)
        node1 = BlockConfigurationNode(starting_state)
        self.assertFalse(node1.get_validity())

    def test_get_validity__expected_pile_numbers_match_total_count(self):
        starting_state = ((3, 0), (3, 0), 0)
        node1 = BlockConfigurationNode(starting_state)
        node1._color_count = (2, 2)
        self.assertFalse(node1.get_validity())

    def test_get_validity__no_state_repeats(self):
        starting_state = ((3, 0), (3, 0), 0)
        node1 = BlockConfigurationNode(starting_state)
        node2 = BlockConfigurationNode(starting_state, parent=node1)
        self.assertFalse(node2.get_validity())





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
    '''

    # tests for total_red_and_blue_count_for_state

    # tests for red_and_blue_counts_for_each_pile

if __name__ == '__main__':
    unittest.main()