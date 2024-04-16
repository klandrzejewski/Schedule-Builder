from tabulate import tabulate
#README FIRST
#We need to have a a constraint satisfaction algorithm
#We should also add errors if the input is not in the correct format 

# Ok so what we need to work on right now is above the line "prompt(test)" we need
# to change the schedule array to have their sleep times, work, classes and what not

class Classes:
    classes = []
    def __init__(self):
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

    
    def edit(self):
        print("Working on this")
 
class CSP: 
	def __init__(self, variables, Domains,constraints): 
		self.variables = variables 
		self.domains = Domains 
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

def prompt(test):
    print(" ")
    print("Choose an action:")
    action = input("(1) Edit Timeslots    (2) Provide Feedback    (3) Print Schedule    (4) Quit \n\n")
    if action == "Print Schedule" or action == "1":
        test.printWeek()
        prompt()
    elif action == "Edit Timeslots" or action == "2":
        test.edit()
        prompt()
    elif action == "Provide Feedback" or action == "3":
        print("Still working on this function")
        prompt()
    elif action == "Quit" or action == "4":
        print("Exiting program")
    else:
        print("Invalid command")
        prompt()

def satisfyConstraints(week, classes):
    print("This is where the algorithm will go")

def convertTime(time):
    pm = 'PM' in time
    time = time.replace('AM', '').replace('PM', '')
    hour, minute = map(int, time.split(":"))

    if pm and hour != 12:
        hour += 12

    return hour

def convertDays(dayOrig):
    days = []
    for day in dayOrig:
        day = day.strip().lower()  
        if day == 'sun' or day == 'sunday':
            days.append(1)
        elif day == 'mon' or day == 'monday':
            days.append(2)
        elif day == 'tues' or day == 'tuesday':
            days.append(3)
        elif day == 'wed' or day == 'wednesday':
            days.append(4)
        elif day == 'thurs' or day == 'thursday':
            days.append(5)
        elif day == 'fri' or day == 'friday':
            days.append(6)
        elif day == 'sat' or day == 'saturday':
            days.append(7)
        else:
            # Warning 
            pass

    return days

# Create arrays for the schedule with 24 hours and 7 days
schedule = [[0 for _ in range(24)] for _ in range(7)]
scheduleWords = [[0 for _ in range(24)] for _ in range(7)]

# Print the array
#for row in schedule:
    #print(row)
my_classes = Classes()
my_classes.display_classes()
my_blockers = Blockers()
my_blockers.display_schedule()
test = Week()
#satisfyConstraints(test, my_classes)


bedtime = convertTime(my_blockers.bedtime)
waketime = convertTime(my_blockers.wakeup_time)
timeBed = 24-bedtime

worktimeStart = []
worktimeEnd = []
timeWork = []
worktimeDays = []
index = 0
for work in my_blockers.work:     
    worktimeStart.append(convertTime(work['start_time']))
    worktimeEnd.append(convertTime(work['end_time']))
    timeWork.append(worktimeEnd[index] - worktimeStart[index])
    worktimeDays.append(convertDays(work['days']))
    index += 1


classtimeStart = []
classtimeEnd = []
timeClass = []
classtimeDays = []
index2 = 0

for classes in my_blockers.classes:     
    classtimeStart.append(convertTime(classes['start_time']))
    classtimeEnd.append(convertTime(classes['end_time']))
    timeClass.append(classtimeEnd[index2] - classtimeStart[index2])
    classtimeDays.append(convertDays(classes['days']))
    index2 += 1

othertimeStart = []
othertimeEnd = []
timeOther = []
othertimeDays = []
index3 = 0

for other in my_blockers.other_commitments:     
    othertimeStart.append(convertTime(other['start_time']))
    othertimeEnd.append(convertTime(other['end_time']))
    timeOther.append(othertimeEnd[index3] - othertimeStart[index3])
    othertimeDays.append(convertDays(other['days']))
    index3 += 1

# Fix if bedtime is post midnight
for i in range(7): 
    for j in range(timeBed):
        schedule[i][bedtime+j] = 1
        scheduleWords[i][bedtime+j] = "Sleep"
    for k in range(waketime):
        schedule[i][k] = 1  
        scheduleWords[i][k] = "Sleep"

for work in range(index):
    for i in worktimeDays[work]:
        for l in range(timeWork[work]):
            schedule[i-1][worktimeStart[work]+l] = 2
            scheduleWords[i-1][worktimeStart[work]+l] = "Work " + str(work+1)

for classes in range(index2):
    for i in classtimeDays[classes]:
        for l in range(timeClass[classes]):
            schedule[i-1][classtimeStart[classes]+l] = 3
            scheduleWords[i-1][classtimeStart[classes]+l] = "Class " + str(classes+1)

for other in range(index3):
    for i in othertimeDays[other]:
        for l in range(timeOther[other]):
            schedule[i-1][othertimeStart[other]+l] = 3
            scheduleWords[i-1][othertimeStart[other]+l] = "Other " + str(other+1)
 
for row in scheduleWords:
    print(row)

prompt(test)
	
# Variables 
variables = [(i, j) for i in range(7) for j in range(24)] 

classNum = index2+1

# Domains: sleep = 1, work = 2, class = 3, other = 4, study = 5+
Domains = {var: set(range(5, classNum+1)) if schedule[var[0]][var[1]] == 0
						else {schedule[var[0]][var[1]]} for var in variables} 

def add_constraint(var): 
    constraints[var] = [] 
    for i in range(7): 
        # No two study sessions can occur at the same time
        if i != var[0]:
            constraints[var].append((i, var[1]))
    # No two study sessions for the same subject on the same day
    current_day_schedule = schedule[var[0]]  
    if var[1] in current_day_schedule:
        for time_slot in current_day_schedule[var[1]]:
            if time_slot != var:
                constraints[var].append(time_slot)
                  
constraints = {} 
for i in range(7): 
    for j in range(24): 
        add_constraint((i, j)) 

csp = CSP(variables, Domains, constraints) 
sol = csp.solve() 

solution = [[0 for i in range(24)] for i in range(7)] 
for i,j in sol: 
	solution[i][j]=sol[i,j] 
	
for row in solution:
    print(row)

          
