# username - complete info
# id1      - complete info
# name1    - complete info
# id2      - complete info
# name2    - complete info


"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int or None
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        self.size = 0

    def is_real_node(self) -> bool:
        """returns whether self is not a virtual node
        @rtype: bool
        @returns: False if self is a virtual node, True otherwise.
        Time complexity O(1) because obv
        """
        if self.height == -1:
            return False
        return True


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.root = None
        self.vn = AVLNode(None, None)

    def _create_ghost_children(self, node: AVLNode) -> None:
        """
        Connects any node to virtual node, for eazy acsess later. Connects everyone to the same node to save memory
        TC: O(1)
        """
        node.left = self.vn
        node.right = self.vn

    def _create_child(self, node: AVLNode, key: int, value: str) -> None:
        """
        Student created function for cleaner code. Given a node, it creates for him a child
        with all the necessery paramaters.
        note: should have used match-case, but was not sure what version of python the grader
        would run on. In addition, in my opinion, "right" and "left" should have been saved as
        values in a config file to avoid errors.
        @pre: Given node is a leaf
        :param node: The node you wish that would bear a child
        :param key: The created child's key
        :param value: The created child's value
        :return: None
        TC: O(1)
        """
        if node.key < key:
            node.right = AVLNode(key, value)
            node.right.height = 0
            self._create_ghost_children(node.right)
            node.right.parent = node
        elif node.key > key:
            node.left = AVLNode(key, value)
            node.left.height = 0
            self._create_ghost_children(node.left)
            node.left.parent = node
        else:
            raise Exception

    def _update_height(self, current_node: AVLNode) -> None:
        """
        Updates the height of all the nodes in the path of a height change
        @pre: a leaf was added so the height of the tree changed
        @param current_node: the parent of the newely created leaf
        TC: O(logn). each itteration, checks childrens heights 2* O(1), and does so along the tree until root, so
            O(logn).
        """
        while current_node != self.root:
            current_node.height = 1 + max(current_node.right.height, current_node.left.height)
            current_node = current_node.parent
        self.root.height = 1 + max(self.root.right.height, self.root.left.height)

    def search(self, key):
        """
        searches for a node in the dictionary corresponding to the key
        @type key: int
        @param key: a key to be searched
        @rtype: AVLNode
        @returns: node corresponding to key
        Time complexity O(logn). The code starts from the root and compares the node key to passed key.
        In AVL Max depth is logn thus the TC is O(logn)
        """
        if self.root is None:
            print("Tree is empty")
            return None
        current_node = self.root
        for i in range(self.size()):  # To avoid bug causing an infinate loop
            if not current_node.is_real_node():
                print(f'Key {key} not in tree')
                return None
            if current_node.key == key:
                return current_node
            elif key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
        print(f'Key {key} not in tree')
        return None

    def insert(self, key: int, val: str) -> int:
        """inserts a new node into the dictionary with corresponding key and value
        Keys in tree must be unique!

        @type key: int
        @pre: key currently does not appear in the dictionary
        @param key: key of item that is to be inserted to self
        @type val: string
        @param val: the value of the item
        @rtype: int
        @returns: the number of rebalancing operation due to AVL rebalancing
        """
        if self.size() == 0:  # first insertion
            self.root = AVLNode(key, val)
            self.root.height = 0
            self._create_ghost_children(self.root)
            return 0
        height_changed = False
        current_node = self.root
        for i in range(self.size()):
            current_node.size = current_node.size+1
            if key < current_node.key:
                if current_node.left.is_real_node():
                    current_node = current_node.left
                else:
                    self._create_child(current_node, key, val)
                    if not current_node.right.is_real_node():
                        self._update_height(current_node)
                        height_changed= True
                    break
            elif key > current_node.key:
                if current_node.right.is_real_node():
                    current_node = current_node.right
                else:
                    self._create_child(current_node, key, val)
                    if not current_node.left.is_real_node():
                        self._update_height(current_node)
                        height_changed = True
                    break
        balances = self.balance_tree(current_node, height_changed)
        return balances

    def left_rotaion(self, node: AVLNode) -> None:
        o_right = node.right
        o_right_o_left = o_right.left
        o_right.left = node
        node.right = o_right_o_left
        o_right.parent = node.parent
        node.parent = o_right
        o_right_o_left.parent = node

        node.height = 1 + max(node.left.height, node.right.height)
        o_right.height = 1 + max(o_right.left.height, o_right.left.height)
        if node == self.root:
            self.root = node.parent
        elif o_right.parent.left == node:
            o_right.parent.left = o_right
        else:
            o_right.parent.right = o_right

    def right_rotate(self, node: AVLNode) -> None:
        o_left = node.left
        o_left_o_right = o_left.right
        o_left.right = node
        node.left = o_left_o_right

        o_left.parent = node.parent
        o_left_o_right.parent = node
        node.parent = o_left

        node.height = 1 + max(node.left.height, node.right.height)
        o_left.height = 1 + max(o_left.left.height, o_left.right.height)
        if node == self.root:
            self.root = node.parent
        elif o_left.parent.left == node:
            o_left.parent.left = o_left
        else:
            o_left.parent.right = o_left

    def balance_tree(self, current_node : AVLNode, height_changed: bool) -> int:
        balances = 0
        while current_node is not None:
            bf = current_node.left.height - current_node.right.height
            if abs(bf) < 2 and not height_changed:
                return balances
            elif abs(bf) < 2 and height_changed:
                current_node = current_node.parent
            else:
                if bf == -2:
                    if current_node.right.left.height - current_node.right.right.height <= 0:
                        self.left_rotaion(current_node)
                        balances = balances + 1
                        current_node = current_node.parent.parent
                    else:
                        self.right_rotate(current_node)
                        #current_node = current_node.parent
                        self.left_rotaion(current_node)
                        current_node = current_node.parent.parent
                        balances = balances + 2
                else:
                    if current_node.left.left.height - current_node.left.right.height < 0:
                        self.left_rotaion(current_node)
                        #current_node = current_node.parent
                        self.right_rotate(current_node)
                        balances = balances + 2
                        current_node = current_node.parent.parent
                    else:
                        self.right_rotate(current_node)
                        balances = balances + 1
                        current_node = current_node.parent.parent
        return balances

    def delete(self, node):
        """deletes node from the dictionary

        @type node: AVLNode
        @pre: node is a real pointer to a node in self
        @rtype: int
        @returns: the number of rebalancing operation due to AVL rebalancing
        """
        current_node = node.parent
        prev_height = current_node.height
        if not node.left.is_real_node():
            tmp = node.right
            if node.key < current_node.key:
                current_node.left = tmp
                tmp.parent = current_node
            else:
                current_node.right = tmp
                tmp.parent = current_node
            self._update_height(current_node)
        elif not node.right.is_real_node():
            tmp = node.left
            if node.key < current_node.key:
                current_node.left = tmp
                tmp.parent = current_node
            else:
                current_node.right = tmp
                tmp.parent = current_node
            self._update_height(current_node)

        else: #node is in middle
            min_node = self._find_min(node.right)
            node.key = min_node.key
            node.value = min_node.value
            return self.delete(min_node)

        height_changed = False
        if prev_height != current_node.height:
            height_changed = True

        balances = self.balance_tree(current_node, height_changed)
        return balances

    def _find_min(self, node: AVLNode) -> AVLNode:
        while node is not None:
            if node.left.is_real_node():
                node = node.left
            else:
                return node

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """

    def avl_to_array(self):
        res = []
        tmp_stack = []
        current_node = self.root
        while True: # very sad to use, but better then recursive
            if current_node.is_real_node():
                tmp_stack.append(current_node)
                current_node = current_node.left
            elif tmp_stack:
                current_node = tmp_stack.pop()
                res.append((current_node.key, current_node.value, current_node.height))
                current_node = current_node.right
            else:
                break
        return res

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self) -> int:
        if self.root is None:
            return 0
        return self.root.size + 1

    """compute the rank of node in the dictionary

    @type node: AVLNode
    @pre: node is in self
    @param node: a node in the dictionary to compute the rank for
    @rtype: int
    @returns: the rank of node in self
    """

    def rank(self, node):
        return -1

    """finds the i'th smallest item (according to keys) in the dictionary

    @type i: int
    @pre: 1 <= i <= self.size()
    @param i: the rank to be selected in self
    @rtype: AVLNode
    @returns: the node of rank i in self
    """

    def select(self, i):
        return None

    """finds the node with the largest value in a specified range of keys

    @type a: int
    @param a: the lower end of the range
    @type b: int
    @param b: the upper end of the range
    @pre: a<b
    @rtype: AVLNode
    @returns: the node with maximal (lexicographically) value having a<=key<=b, or None if no such keys exist
    """

    def max_range(self, a, b):
        return None

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    TC: O(1)
    """

    def get_root(self) -> AVLNode:
        return self.root
