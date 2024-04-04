from tabulate import tabulate

class Day:
    # Default schedule. Goes to bed at 11, wakes up at 7
    # class at nine, ten and 2
    # Meals at 8, noon, and 6
    # work from 7-9
    # 6 free blocks

    def __init__(self, day):
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

class Week: 
    def __init__(self):
        self.week = [Day(day) for day in range(1, 8)]

    def printWeek(self):
        table = []
        for day in self.week:
            row = [str(day.day)]
            row.extend(day.blocks)
            table.append(row)

        headers = ["Day", "12:00am", "1:00am", "2:00am", "3:00am", "4:00am", "5:00am", "6:00am", "7:00am",
                   "8:00am", "9:00am", "10:00am", "11:00am", "12:00pm", "1:00pm", "2:00pm", "3:00pm", "4:00pm",
                   "5:00pm", "6:00pm", "7:00pm", "8:00pm", "9:00pm", "10:00pm", "11:00pm"]

        print(tabulate(table, headers=headers, tablefmt="grid"))

test = Week()
test.printWeek()
print("Done")




