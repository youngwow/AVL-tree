from main_logic import AVLTree


if __name__ == '__main__':
    Tree = AVLTree()
    root = None
    while True:
        try:
            print("Type 'Exit' to exit the program.")
            print("Type 'Search' to search a value.")
            print("Type 'Show' to show the tree.")
            print("What to insert in AVL-tre? Data: ", end='')
            data = input()
            if data == 'Exit':
                break
            if data == 'Search':
                root_found = int(input())
                root_found = Tree.search(root, root_found)
                Tree.breadth_first_search(root, 'search.png')
                break
            if data == 'Show':
                Tree.breadth_first_search(root, 'show.png')
                break
            root = Tree.insert(root, int(data))
        except (TypeError, ValueError, AttributeError):
            print("Smth went wrong, plz try again!")
            print("Probably, you typed not a number.")
            print()
