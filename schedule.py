class Day:
    # Default schedule. Goes to bed at 11, wakes up at 7
    # class at nine, ten and 2
    # Meals at 8, noon, and 6
    # work from 7-9
    # 6 free blocks

    def __init__(self, day):
        print("Creating day " + str(day))
        self.day = day
        self.blocks = [None] * 24
        self.blocks[8] = "Meal"
        self.blocks[9] = "Class"
        self.blocks[10] = "Class"
        self.blocks[12] = "Meal"
        self.blocks[14] = "Class"
        self.blocks[18] = "Meal"
        self.blocks[19] = "Work"
        self.blocks[20] = "Work"
        self.blocks[21] = "Work"
        self.blocks[23] = "Sleep"
        self.blocks[0] = "Sleep"
        self.blocks[1] = "Sleep"
        self.blocks[2] = "Sleep"
        self.blocks[3] = "Sleep"
        self.blocks[4] = "Sleep"
        self.blocks[5] = "Sleep"
        self.blocks[6] = "Sleep"

    def __str__(self):
        return "Day " + str(self.day)

class Week: 
    def __init__(self):
        print("Initializing")
        self.week = [Day(day) for day in range(1, 8)]

    def printWeek(self):
        for day in self.week:
            print("Blocks for", day)
            for i, block in enumerate(day.blocks):
                if block is not None:
                    print(f"Block {i}: {block}")
                else:
                    print(f"Block {i}: None")
            print()

test = Week()
test.printWeek()
print("Done")