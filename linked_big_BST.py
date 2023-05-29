"""
File: linkedbst.py
Author: Ken Lambert
"""
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log
from time import time
import random
from tqdm import tqdm
class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""
    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)
    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""
        stack = LinkedStack()
        current = self._root
        level = 0
        string = ''
        while True:
            if current is not None:
                stack.push((current, level))
                current = current.right
                level += 1
            elif stack:
                current, level = stack.pop()
                string += '| ' * level
                string += str(current.data) + '\n'
                current = current.left
                level += 1
            else:
                break
        return string
    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)
    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None
    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()
        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)
        recurse(self._root)
        return iter(lyst)
    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None
    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None
    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None
    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        current = self._root
        while current is not None:
            if item == current.data:
                return current.data
            elif item < current.data:
                current = current.left
            else:
                current = current.right
        return self._root
    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0
    def add(self, item):
        """Adds item to the tree."""
        if self.isEmpty():
            self._root = BSTNode(item)
            self._size += 1
            return
        current = self._root
        while True:
            if item < current.data:
                if current.left is None:
                    current.left = BSTNode(item)
                    self._size += 1
                    return
                else:
                    current = current.left
            else:
                if current.right is None:
                    current.right = BSTNode(item)
                    self._size += 1
                    return
                else:
                    current = current.right
    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")
        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left
        # Begin main part of the method
        if self.isEmpty(): return None
        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right
        # Return None if the item is absent
        if itemRemoved == None: return None
        # The item is present, so remove its node
        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:
            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right
                # Case 3: The node has no right child
            else:
                newChild = currentNode.left
                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild
        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved
    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None
    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            else:
                return 1 + max(height1(top.left), height1(top.right))
        return height1(self._root)
    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() <= 2 * log(self._size + 1) - 1
    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        return [verticle for verticle in self.inorder() if low <= verticle <= high]
    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        trvrsed_verticles = [verticle for verticle in self.inorder()]
        self.clear()
        def recurse(input_verticles):
            if input_verticles:
                mid = len(input_verticles) // 2
                return BSTNode(input_verticles[mid], recurse(input_verticles[:mid]),\
                               recurse(input_verticles[mid + 1:]))
        self._root = recurse(trvrsed_verticles)
        self._size = len(trvrsed_verticles)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        top = self._root
        result = None
        while top:
            if top.data > item:
                result = top.data
                top = top.left
            elif top.data <= item:
                top = top.right
        return result

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        bot = self._root
        result = None
        while bot:
            if bot.data < item:
                result = bot.data
                bot = bot.right
            elif bot.data >= item:
                bot = bot.left
        return result
    
    @staticmethod
    def demo_bst(path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        test_btree = LinkedBST()
        with open(path) as file:
            words = [word for word in file.read().split()]

        # 1. The search time for 10000 random words in an alphabetically ordered dictionary
        # (searching a list of words using methods of the built-in list type).

        words = words[:30000]
        search_list = random.sample(words, 10000)
        cur_time = time()
        for i in tqdm(search_list, desc='Searching in list', colour='yellow'):
            words.index(i)
        print(f'1. Searching of 10000 random words in the list (size=30k) using methods of the built-in list type took {time() - cur_time} second\n')


        # 2. Is the search time for 10000 random words in a dictionary represented as a binary search tree.
        # The binary search tree is built on the basis of sequentially adding words from the dictionary to the tree, which is ordered alphabetically.
        
        for i in words:
            test_btree.add(i)
        cur_time = time()
        for i in tqdm(search_list, desc='Searching in unbalanced alphabetical order tree', colour='red'):
            test_btree.find(i)
        print(f'2. Searching of 10000 random words in unbalanced alphabetical tree (size=30k) took {time() - cur_time} second\n')


        # 3. Іs the search time for 10000 random words in a dictionary represented as a binary search tree.
        # The binary search tree is built on the basis of sequentially adding words from the dictionary to the tree,
        # which is not ordered alphabetically (words are added to the tree randomly).

        test_btree.clear()
        random.shuffle(words)
        for i in words:
            test_btree.add(i)
        cur_time = time()
        for i in tqdm(search_list, desc='Searching in unbalanced unalphabetical order tree', colour='cyan'):
            test_btree.find(i)
        print(f'3. Searching of 10000 random words in unbalanced unalphabetical tree (size=30k) took {time() - cur_time} second\n')


        # 4. Is the search time for 10,000 random words in the dictionary, which is represented as a binary search tree after its balancing.\

        test_btree.rebalance()
        cur_time = time()
        for i in tqdm(search_list, desc='Searching in balanced unalphabetical order tree', colour='green'):
            test_btree.find(i)
        print(f'4. Searching of 10000 random words in balanced unalphabetical tree (size=30k) took {time() - cur_time} second\n')
        
        return print('''Note! Asymptotic complexity in 3 and 4 is the same.
But sometimes 3 is faster than 4 because in 4 will be pure log n, and 3 will be randomised log n
It should be in the following order from the fastest to the slowest method: 4 -> 3 -> 1 -> 2''')

if __name__ == '__main__':
    LinkedBST.demo_bst('words.txt')