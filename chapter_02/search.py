"""
Implements the depth-first and breadth-first algorithms described on pg. 33
"""
from abc import ABCMeta, abstractmethod


class AbstractNode(object):
    """
    Base class for all nodes used with an AbstractSearch-based class.

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


class AbstractSearch(object):
    """
    Base class for all types of searches implemented in Chapter 02 study questions.

    Should implement the following methods:

        _return_result
    """

    def depth_first(self, starting_node, goal):
        """
        Does a depth-first search of nodes

        :param starting_node: node object for the beginning state of the search
        :param goal: object representing the desired end state
        :return: dependent on the implementation of _return_result

        Word of caution: this algorithm can potentially run infinitely if the problem
            space is has branches that are infinitely deep without returning a solution
        """
        return self._search(starting_node, goal, self._generate_depth_first_queue)

    def breadth_first(self, starting_node, goal):
        """
        Does a breadth-first search of nodes

        :param starting_node: node object for the beginning state of the search
        :param goal: object representing the desired end state
        :return: dependent on the implementation of _return_result
        """
        return self._search(starting_node, goal, self._generate_breadth_first_queue)

    def _generate_depth_first_queue(self, current_node, pending_nodes):
        return current_node.generate_child_nodes() + pending_nodes

    def _generate_breadth_first_queue(self, current_node, pending_nodes):
        return pending_nodes + current_node.generate_child_nodes()

    def _search(self, starting_node, goal, queue_expansion_function):
        """
        :param starting_node: node object for the beginning state of the search
        :param goal: object representing the desired end state
        :param queue_expansion_function: function to determine how to add more nodes to
                the queue
        :return: the result of calling _return_result, which is dependent on the class
                that implements it.
        """

        # While the algorithm specifications are written recursively, Python does
        # not handle tail recursion very well. To prevent running out the stack, the
        # algorithm is written iteratively.
        pending_nodes = []
        current_node = starting_node
        while not current_node.fulfills_goal(goal):
            new_current, new_pending = queue_expansion_function(current_node, pending_nodes)
            if not new_pending:
                return self._return_result(current_node, False)
        return self._return_result(current_node, True)

    @abstractmethod
    def _return_result(self, final_node, is_success):
        pass


class DoesItHaveASolution(AbstractSearch):
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

    Per the algorithm described, this search only returns True or False to the question
    "Is there a solution to the problem in the given problem space?"
    """

    def _return_result(self, final_node, is_success):
        return is_success
