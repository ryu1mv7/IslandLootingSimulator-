from __future__ import annotations
from island import Island
from heap import MaxHeap


class Mode2Navigator:
    """
            I used Heap(Max heap) to keep getting the island which leads to the max/highest score(formula)to get the
            island to return. Normally,numbers is used for heap to compare, so scores is considered to be used.
            However, scores themselves don't have nothing, but islands could have attributes, so using islands
            considered to be more flexible.
            Make a list of islands and heapify it. Of course, islands themselves are not comparable
            so I added the score method for the calculation of the score(2*c+m).Then, I also added three magic methods,
            which enables islands comparable each other. Then, each pirate picking up the optimal island by get_max()
            among the current islands they can choose at that time(They cannot choose ones whose all money are taken).
            Hence, after once island is removed by get_max(), and add it back to the heap as long as money of the island
            still remaining (not zero).For the islands that have lost all money, leave it (don't add it back)
            This is conducted after calculation based on the situation, for example,
            subtracting(changing values of variables) money and marine particular island have lost...etc.
            As the example of how this all works,
            1) case: one pirate can send enough crews to the particular island retrieved by get_max() and stolen
                all money in the island
            --The first pirate makes 400 gold by going to Island A(money: 400, marines: 100) and sending 100 their crew.
            Final score: 400 from the formula and this island A will be no longer back in the heap bcs all money is
            stolen.
            2) case: the other pirate can send smaller number of crews to the particular island and the money
            is still remaining.
            --The second pirate going to Island G(money: 400, marines: 100) and stole 200 money. G have still 200 money,
            so the island is added back to heap and being in the heap until it lose all money.

            Complexity Analysis- refer to docstrings of each function.
            More details for each function can be refer to comments.
    """

    def __init__(self, n_pirates: int) -> None:
        """
        O(1) for Best/Worst Case where N is the current number of islands,
        C is the number of captains participating in the Davy back Fight.
        Just Initializing doesn't get affected by both N and C.
        """
        self.n_pirates = n_pirates
        self.island = []

    def add_islands(self, islands: list[Island]):
        """
        Best/Worst Case: Both O(N) where N is the current number of islands,
        C is the number of captains participating in the Davy back Fight.
        keep adding islands with non-zero money
        """
        for island in islands: #O(N)
            if island.marines != 0 and island.money != 0:
                self.island.append(island)

    def simulate_day(self, crew: int) -> list[tuple[Island|None, int]]:
        """
        Best/Worst Case: both O(N +ClogN) where N is the current number of islands,
        C is the number of captains participating in the Davy back Fight.
        When N is the the current number of islands with non-zero money, blocks of both "if condition" will be executed.
        Therefore, according to complexity in comments, O(N) + O(N) + O(C) * (O(log(N))+ O(log(N)) = O(N+C*logN)
        # get_max() and add() for heap costs O(logN) assumed that balanced tree.
        """

        # I added some additional attributes for solving problem
        # Before heapify islands, I need to add(complement/interpolate) =  update correct values of those attributes.
        for island in self.island: #O(N)
            island.crew_to_send = min(island.marines, crew)
            island.original_crew = crew

        heap = MaxHeap.heapify(self.island, len(self.island)) #O(N)
        return_list = []

        for i in range(self.n_pirates): # O(C)
            island_to_attack = heap.get_max() #O(logN)
            if island_to_attack.money != 0 or island_to_attack.marines != 0:
                crew_to_send = island_to_attack.crew_to_send
                return_list.append((island_to_attack, crew_to_send))
                # losing money for the island
                losing_money = (island_to_attack.crew_to_send / island_to_attack.marines) * island_to_attack.money
                island_to_attack.money -= losing_money
                island_to_attack.marines -= island_to_attack.crew_to_send
                island_to_attack.crew_to_send -= crew_to_send # after sending crew, this will be the max to send for next
                if island_to_attack.money > 0:
                    heap.add(island_to_attack) #O(logN)
                crew = crew - crew_to_send
                island_to_attack.crew = crew #update crew after the fight
        return return_list
