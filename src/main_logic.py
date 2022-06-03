import pydot


class Node(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.h = 1  # высота считается в вершинах (в ребрах - 0)

    def __str__(self):
        left = self.left.value if self.left else None
        right = self.right.value if self.right else None
        return 'key: {}, left: {}, right: {}'.format(self.value, left, right)


class AVLTree(object):
    def __init__(self):
        self.style_left = 'line'
        self.style_right = 'dotted'
        self.visited = []

    def insert(self, root, key, show_left=True, show_right=True):
        if not root:
            return Node(key)
        elif key < root.value:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
        root.h = 1 + max(self.getHeight(root.left),
                         self.getHeight(root.right))

        b = self.getBal(root)

        if show_right:
            # Малое правое вращение
            if b > 1 and key < root.left.value:
                return self.rRotate(root)

        if show_left:
            # Малое левое вращение
            if b < -1 and key > root.right.value:
                return self.lRotate(root)

        if show_left and show_right:
            # Большое правое вращение
            if b > 1 and key > root.left.value:
                root.left = self.lRotate(root.left)
                return self.rRotate(root)
            # Большое левое вращение
            if b < -1 and key < root.right.value:
                root.right = self.rRotate(root.right)
                return self.lRotate(root)

        return root

    def lRotate(self, node_a):  # z
        node_b = node_a.right
        T2 = node_b.left

        node_b.left = node_a
        node_a.right = T2

        node_a.h = 1 + max(self.getHeight(node_a.left),
                      self.getHeight(node_a.right))
        node_b.h = 1 + max(self.getHeight(node_b.left),
                      self.getHeight(node_b.right))

        return node_b

    def rRotate(self, node_a):

        node_b = node_a.left
        T3 = node_b.right

        node_b.right = node_a
        node_a.left = T3

        node_a.h = 1 + max(self.getHeight(node_a.left),
                      self.getHeight(node_a.right))
        node_b.h = 1 + max(self.getHeight(node_b.left),
                      self.getHeight(node_b.right))

        return node_b

    def getHeight(self, root):
        if not root:
            return 0

        return root.h

    def getBal(self, root):
        if not root:
            return 0
        # if root.left is not None and root.right is not None:
        #     return self.getHeight(root.left) - self.getHeight(root.right)
        # elif root.left is not None and root.right is None:
        #     return self.getHeight(root.left)
        # elif root.left is None and root.right is not None:
        #     return -self.getHeight(root.right)
        return self.getHeight(root.left) - self.getHeight(root.right)

    def preOrder(self, root):

        if not root:
            return

        print("{0} ".format(root.value), end="")
        self.preOrder(root.left)
        self.preOrder(root.right)

    def search(self, root, value):
        if root is None:
            self.visited = []
            return
            # return False
        if root.value == value:
            return root
            # return True
        elif value < root.value:
            root = root.left if root.left is not None else None
            self.visited.append(root)
            root = self.search(root, value)
        else:
            root = root.right if root.right is not None else None
            self.visited.append(root)
            root = self.search(root, value)
        return root

    def inpre(self, root):
        while root.right is not None:
            root = root.right
        return root

    def insuc(self, root):
        while root.left is not None:
            root = root.left
        return root

    def remove(self, root, value):
        if root.left is None and root.right is None:
            root = None
            return None
        if root.value < value:
            root.right = self.remove(root.right, value)
        elif root.value > value:
            root.left = self.remove(root.left, value)
        else:
            if root.left is not None:
                q = self.inpre(root.left)
                root.value = q.value
                root.left = self.remove(root.left, q.value)
            else:
                q = self.insuc(root.right)
                root.value = q.value
                root.right = self.remove(root.right, q.value)
        if root is None:
            return root
            # update the height of the tree
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balance = self.getBal(root)
        # Left Left
        if balance > 1 and self.getBal(root.left) >= 0:
            return self.rRotate(root)
        # Right Right
        if balance < -1 and self.getBal(root.right) <= 0:
            return self.lRotate(root)
        # Left Right
        if balance > 1 and self.getBal(root.left) < 0:
            root.left = self.lRotate(root.left)
            return self.rRotate(root)
        # Right Left
        if balance < -1 and self.getBal(root.right) < 0:
            root.right = self.rRotate(root.right)
            return self.lRotate(root)

        return root

    def checking(self):
        if len(self.visited) > 0:
            self.style_left = 'line'
            self.style_right = 'line'
        else:
            self.style_left = 'line'
            self.style_right = 'dotted'

    def breadth_first_search(self, root, name):
        graph = pydot.Dot(graph_type="graph")
        graph.obj_dict['attributes']["size"] = '"10,10!"'
        graph.obj_dict['attributes']["dpi"] = "144"
        graph.add_node(pydot.Node(root.value))
        self.checking()
        vertices_count = 0
        queue = [root]
        while queue:
            tmp_queue = []
            for element in queue:
                if element.left:
                    if len(self.visited) > vertices_count:
                        if self.visited[vertices_count] == element.left:
                            self.style_left = 'dotted'
                            vertices_count += 1
                    graph.add_node(pydot.Node(element.left.value))
                    graph.add_edge(pydot.Edge(element.value, element.left.value, style=self.style_left))
                    tmp_queue.append(element.left)
                if element.right:
                    if len(self.visited) > vertices_count:
                        if self.visited[vertices_count] == element.right:
                            self.style_right = 'dotted'
                            vertices_count += 1
                    graph.add_node(pydot.Node(element.right.value))
                    graph.add_edge(pydot.Edge(element.value, element.right.value, style=self.style_right))
                    tmp_queue.append(element.right)
                # style_right = 'line'
                # style_left = 'line'
                self.checking()
                queue = tmp_queue
        graph.write(name, format='png')
        self.visited = []
