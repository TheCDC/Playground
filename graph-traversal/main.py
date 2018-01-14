class Node:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.type = None

    def __repr__(self):
        return 'Node({})'.format(self.value)


def traverse1(node):
    if node is None:
        return
    else:
        print(node)
        traverse1(node.left)
        traverse1(node.right)


def traverse2(node):
    if node is None:
        return
    else:
        traverse2(node.left)
        print(node)
        traverse2(node.right)


def traverse3(node):
    """post order"""
    if node is None:
        return
    else:
        traverse3(node.left)
        traverse3(node.right)
        print(node)


def post_iterative(root):
    stack = [root]
    outstack = list()
    while len(stack) > 0:
        node = stack.pop()
        if node.left is not None:
            stack.append(node.left)
        if node.right is not None:
            stack.append(node.right)
        outstack.append(node)
        print(node)
    # while len(outstack) > 0:
    #     print(outstack.pop())


delimiter = '=' * 30


def google_main():
    google_tree = [Node(i + 1) for i in range(2**3 - 1)]
    print(google_tree)
    google_root = google_tree[6]
    google_root.left = google_tree[2]
    google_root.right = google_tree[5]
    google_tree[5].left = google_tree[3]
    google_tree[5].right = google_tree[4]
    google_tree[2].left = google_tree[0]
    google_tree[2].right = google_tree[1]
    traverse1(google_root)
    print(delimiter)
    traverse2(google_root)
    print(delimiter)
    traverse3(google_root)
    print(delimiter)
    post_iterative(google_root)


def csc311_main():
    nodes = {k: Node(k) for k in "Sab+c-="}
    nodes['='].left = nodes['S']
    nodes['='].right = nodes['-']
    nodes['-'].left = nodes['+']
    nodes['-'].right = nodes['c']
    nodes['+'].left = nodes['a']
    nodes['+'].right = nodes['b']
    post_iterative(nodes['='])

    pass


def main():
    csc311_main()


if __name__ == '__main__':
    main()
