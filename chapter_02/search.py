"""
Implements the depth-first and breadth-first algorithms described on pg. 33
"""
from abc import ABCMeta, abstractmethod


class AbstractNode(object):
    """
    Base class for all nodes used with Search.

    Should implement the following methods:
        generate_child_nodes
        fulfills_goal
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_child_nodes(self):
        """
        Generate a list of child nodes to be explored in the problem space.

        :return: list of nodes
        """
        pass

    @abstractmethod
    def fulfills_goal(self, goal):
        """
        Compares the self node with specified goal to see if search criteria is met

        :param goal: object that represents a goal that the node can be compared against
        :return: True, if current node fulfills goal; False otherwise
        """
        pass


class Search(object):
    """
    Searches through a problem space using the following algorithms:

    Depth-first search:

        dfs(goal, current, pending)
        {
            if current = goal, then success;
            else
            {
                pending := expand(current) + pending;
                if pending = () then fail;
                else dfs(goal, head(pending), tail(pending))
            }
        }

    Breadth-first search:

        dfs(goal, current, pending)
        {
            if current = goal, then success;
            else
            {
                pending := pending + expand(current);
                if pending = () then fail;
                else dfs(goal, head(pending), tail(pending))
            }
        }
    """

    def depth_first(self, starting_node, goal):
        """
        Does a depth-first search of nodes

        :param starting_node:
        :param goal:
        :return:
        """
        pass

    def breadth_first(self, starting_node, goal):
        """
        Does a breadth-first search of nodes

        :param starting_node:
        :param goal:
        :return:
        """
        pass

    '''
    def dfs(goal, current):
        pending = []
        while goal_is_unmet(goal, current):
            current, pending = dfs_helper(current, pending)
            if not pending:
                return False
        return True

    def dfs_helper(current, pending):
        new_pending = expand(current) + pending
        return new_pending[0], new_pending[1:]

    def goal_is_unmet(goal, node):
        # to be implemented depending on construction of goal/node
        # should perform some kind of comparison and return True if they are the 'same', and
        # False if they are different
        raise NotImplementedError

    def expand(node):
        # to be implemented depending on construction of node
        # returns a list of new nodes algorithmically generated from the old node
        raise NotImplementedError
    '''