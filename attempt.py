from tabulate import tabulate

class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.solution = None

    def solve(self):
        assignment = {}
        self.solution = self.backtrack(assignment)
        return self.solution

    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]
        return None

    def select_unassigned_variable(self, assignment):
        unassigned_vars = [var for var in self.variables if var not in assignment]
        return min(unassigned_vars, key=lambda var: len(self.domains[var]))

    def order_domain_values(self, var, assignment):
        return self.domains[var]

    def is_consistent(self, var, value, assignment):
        for constraint_var in self.constraints[var]:
            if constraint_var in assignment and assignment[constraint_var] == value:
                return False
        return True

class Classes:
    def __init__(self):
        self.classes = []
        self.numClass = int(input("How many classes are you taking?\n"))
        for i in range(self.numClass):
            print(f"\nEnter details for Class {i+1}:")
            name = input("Name of the class: ")
            difficulty = input("Difficulty level (easy, medium, hard): ")
            study_hours = float(input("Ideal number of hours to study per week: "))
            self.classes.append({'name': name, 'difficulty': difficulty, 'study_hours': study_hours})

    def display_classes(self):
        print("\nYour classes and study goals:")
        for i, cls in enumerate(self.classes):
            print(f"Class {i+1}: {cls['name']}")
            print(f"   Difficulty: {cls['difficulty']}")
            print(f"   Ideal study hours per week: {cls['study_hours']}")

class Blockers:
    def __init__(self):
        print("Let's set up your daily schedule.")
        self.bedtime = input("When would you like to go to bed? (HH:MM AM/PM): ")
        self.wakeup_time = input("When would you like to wake up? (HH:MM AM/PM): ")
        self.classes = self.get_timings("class")
        self.work = self.get_timings("work")
        self.other_commitments = self.get_timings("other commitments")

    def get_timings(self, activity):
        num_timings = int(input(f"How many {activity} do you have? "))
        timings = []
        for i in range(num_timings):
            start_time = input(f"Enter start time for {activity} {i+1} (HH:MM AM/PM): ")
            end_time = input(f"Enter end time for {activity} {i+1} (HH:MM AM/PM): ")
            days = input(f"Enter days for {activity} {i+1} (comma-separated, e.g., Mon, Wed, Fri): ").split(',')
            timings.append({'start_time': start_time, 'end_time': end_time, 'days': days})
        return timings

    def display_schedule(self):
        print("\nYour daily schedule:")
        print(f"Bedtime: {self.bedtime}")
        print(f"Wake-up time: {self.wakeup_time}")
        self.display_activities("Classes", self.classes)
        self.display_activities("Work", self.work)
        self.display_activities("Other Commitments", self.other_commitments)

    def display_activities(self, activity_name, activities):
        print(f"\n{activity_name}:")
        for i, activity in enumerate(activities, start=1):
            print(f"{activity_name} {i}:")
            print(f"   Start time: {activity['start_time']}")
            print(f"   End time: {activity['end_time']}")
            print(f"   Days: {', '.join(activity['days'])}")

class Day:
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

    def edit(self):
        print("Working on this")

def prompt(test):
    print(" ")
    print("Choose an action:")
    action = input("Edit Timeslots      Provide Feedback       Print Schedule       Quit \n\n")
    if action == "Print Schedule":
        test.printWeek()
        prompt(test)
    elif action == "Edit Timeslots":
        test.edit()
        prompt(test)
    elif action == "Provide Feedback":
        print("Still working on this function")
        prompt(test)
    elif action == "Quit":
        print("Exiting program")
    else:
        print("Invalid command")
        prompt(test)

def satisfyConstraints(week, classes, blockers):
    variables = [(day, hour) for day in range(1, 8) for hour in range(24)]
    domains = {var: {'Sleep', 'Work', 'Meal', 'Class', 'Other'} for var in variables}
    constraints = {}
    
    # Define constraints to ensure activities don't overlap and respect user's input
    for day in range(1, 8):
        for hour in range(24):
            var = (day, hour)
            constraints[var] = []
            for i in range(-1, 2):
                for j in range(-1, 2):
                    neighbor = (day + i, hour + j)
                    if neighbor != var and neighbor in variables:
                        constraints[var].append(neighbor)
                        
    # Add constraints based on class timings, work hours, and other commitments
    for class_info in blockers.classes:
        for day, activity in enumerate(week.week):
            for hour, block in enumerate(activity.blocks):
                if (block == "Class" and str(day + 1) in class_info['days'] and
                        class_info['start_time'] <= blockers.classes[0]['start_time'] and
                        class_info['end_time'] >= blockers.classes[0]['end_time']):
                    constraints[(day + 1, hour)] = [block]

    # Implement the CSP algorithm to generate a feasible schedule
    csp = CSP(variables, domains, constraints)
    schedule = csp.solve()
    
    # Update the week object with the generated schedule
    for (day, hour), activity in schedule.items():
        week.week[day - 1].blocks[hour] = activity


my_classes = Classes()
my_classes.display_classes()
my_blockers = Blockers()
my_blockers.display_schedule()
test = Week()
satisfyConstraints(test, my_classes, my_blockers)
prompt(test)






