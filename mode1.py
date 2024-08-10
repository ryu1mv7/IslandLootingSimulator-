from island import Island
from bst import BinarySearchTree, BSTInOrderIterator


class Mode1Navigator:
    """
    In this constructer, setting the instance variables from two arguments.Also, BST, which is the ADT I use for T1
        is instantiated.
    I used the BST, whose key is the ratio(money of island/ marines of island),which represents the efficiency
    of islands to be attacked.When deciding the most optimal island to visit, the larger the ratio,
    the more efficient to attack. By keep choosing optimal islands, maximizing total money is important.
    For example,
        self.a = Island("A", 400, 100) # ratio = 4
        self.b = Island("B", 300, 150) # ratio = 2
        self.c = Island("C", 100, 5)   # ratio = 20
        self.d = Island("D", 350, 90)  # ratio = 3.8
        self.e = Island("E", 300, 100) # ratio = 3
    The most efficient order of island to attack is C-> A-> D-> E-> B (high ratio -> low ratio) <descending order>

    Also, items of BST are the island objects.
    However, self.in_nodes get a list of sorted islands based on the key(ratio) in <ascending order>,
    so I retrieve elements(islands) from the last element,second last element...
    to get island <descending order> in select_islands(self) method.

    Complexity Analysis- refer to docstrings of each function.
    """

    def __init__(self, islands: list[Island], crew: int) -> None:
        """

        O(N) for both Best/Worst Case where N be the length of islands
        for loop iterate the number of islands times. Also, another for loop iterate the number of the elements I added
        to BST(=The number of nodes) = length of islands = N, O(N+N) = O(N)
        """
        self.islands = islands
        self.crew = crew
        self.bst = BinarySearchTree()

        for island in self.islands: # adding all island to the BST : O(N)
            ratio = island.money / island.marines # money/ marines = efficiency
            self.bst[ratio] = island  #key: ratio, item: island

        self.islands = [node.item for node in BSTInOrderIterator(self.bst.root)]  # O(N)

    def select_islands(self) -> list[tuple[Island, int]]:
        """
        Best: O(log N)/Worst Case: O(N) where N be the length of islands
        Best: If number of the crew is less than the first island to visit, append that to the return list
        and then break the loop.
        Worst: function iterating len(self.islands) = N times
        """
        return_list = []
        total_num_crew = self.crew
        for i in range(-1, -len(self.islands)-1, -1): #O(n)
            island = self.islands[i] #retrieving element from the last position(start attacking from most effcient one)
            # keep sending the max number of the crew(but equal or less than # of marines), (crew can't exceed marines)
            num_to_send = min(total_num_crew, island.marines)
            return_list.append((island, num_to_send))
            total_num_crew -= num_to_send
            if total_num_crew <= 0:
                break  # stop sending the crew when number of crew become 0.
        return return_list


    def select_islands_from_crew_numbers(self, crew_numbers: list[int]) -> list[float]:
        """
        Best/Worst Case- both O(C*N) where C is the length of the crew numbers and N is the length of islands
        For each of all C crews,  traversing the N(all) islands when calculating the most optimal island.
        No, code to break these iterations like break so both best and worst case is the same.
        """
        each_money_returned = []

        for crew_number in crew_numbers: #O(C)
            total_money = 0
            self.crew = crew_number # pass this to select_islands(this method use "self.crew" in it),n call it below
            for tuple_info in self.select_islands(): #O(N)
                island = tuple_info[0]
                crew = tuple_info[1] # optimised num of crew that should be sent to the island
                each_money = (min(crew, crew_number) / island.marines) * island.money
                total_money += each_money
                crew_number -= min(crew, crew_number)
                total_money = int(total_money)
            each_money_returned.append(total_money)
        return each_money_returned

    def update_island(self, island: Island, new_money: float, new_marines: int) -> None:
        """
        O(1) for Best/Worst Case where N is the length of islands.
        Since island has attributes, new_money and new_marines, update them by initializing them.
        The number of island, N, doesn't change this complexity, so constant time.
        """
        island.money = new_money
        island.marines = new_marines


