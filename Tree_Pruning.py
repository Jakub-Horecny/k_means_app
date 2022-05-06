from typing import Any


class Node:

    def __init__(self, parent: Any, data: Any, key: Any) -> None:
        """
        create new tree node
        :param parent: node parent
        :param data: node data
        :param key: node key
        :rtype: None
        """
        self.parent: Any = parent
        self.data: Any = data
        self.key: Any = key  # name
        self.sons: list = []

    def add_son(self, new_son: Any) -> None:
        """
        add new son a sort list of sons
        :param new_son: new son node
        :rtype: None
        """
        self.sons.append(new_son)
        self.sons.sort(key=lambda x: x.key, reverse=False)

    def delete_sons(self) -> None:
        """
        delete all sons
        :rtype: None
        """
        del self.sons[0:len(self.sons) - 1]

    def __delete__(self) -> None:
        del self.sons
        del self.parent
        del self.data
        del self.key


class Tree:

    def __init__(self) -> None:
        self.root = None

    def is_root(self, node: Node) -> bool:
        """
        check if node is tree root
        :param node: tree node
        :return: result if node is tree root
        :rtype: bool
        """
        if node.parent is None:
            return True
        else:
            return False

    def is_leaf(self, node: Node) -> bool:
        """
        check if node is leaf - has no sons
        :param node: tree node
        :return: result if node is a leaf
        :rtype: bool
        """
        return len(node.sons) == 0

    def inorder(self, node: Node):
        if node is None:
            return

        for s in node.sons:
            self.inorder(s)

        print(node.data)

    def delete_node_sons(self, node: Node) -> None:
        """
        delete all node sons
        :rtype: None
        :param node: tree node
        """
        for s in node.sons:
            if self.is_leaf(s):
                del s
            else:
                self.delete_node_sons(s)

    def insert(self, key: Any, data: Any, parent_key: Any) -> None:
        """
        insert new node to the tree
        :param key: new node key
        :param data: new node data
        :param parent_key: key of parent
        :rtype: None
        """
        parent_node: Node = self.__find_node(parent_key)
        new_node: Node = Node(parent_node, data, key)

        new_node.parent = parent_node
        parent_node.add_son(new_node)

    def find(self, key: Any) -> Any:
        """

        :return: value in Node
        :rtype: Any
        :param key: node key
        """
        if self.root is None:
            return None

        node: Node = self.root
        while True:
            if self.is_leaf(node):
                return None

            for s in node.sons:
                if s.key == key:
                    return s.data
                elif s.key > key:
                    node = s.data
                    break
            node = node.sons[len(node.sons) - 1]

    def __find_node(self, key: Any) -> Any:
        """

        :param key:
        :return:
        :rtype: Any
        """
        if self.root is None:
            return None

        node: Node = self.root
        while True:
            if self.is_leaf(node):
                return None

            for s in node.sons:
                if s.key == key:
                    return s
                elif s.key > key:
                    node = s
                    break
            node = node.sons[len(node.sons) - 1]
