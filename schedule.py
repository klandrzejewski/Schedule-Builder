from tabulate import tabulate
#README FIRST
#We need to have a a constraint satisfaction algorithm
#We should also add errors if the input is not in the correct format 

# Ok so what we need to work on right now is above the line "prompt(test)" we need
# to change the schedule array to have their sleep times, work, classes and what not

class Classes:
    classes = []
    def __init__(self):
        self.numClass = int(input("How many classes do you want to study for?\n"))
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
        self.work = self.get_timings("work shift")
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

    def __init__(self, day, schedule):
        self.day = day
        self.blocks = schedule

class Week: 
    def __init__(self, schedule):
        self.week = [Day(day, schedule[day-1]) for day in range(1, 8)]

    def printWeek(self, value):
        table = []
        for day in self.week:
            row = [str(day.day)]
            row.extend(day.blocks)
            table.append(row)

        headers = ["Day", "12:00am", "1:00am", "2:00am", "3:00am", "4:00am", "5:00am", "6:00am", "7:00am",
                   "8:00am", "9:00am", "10:00am", "11:00am", "12:00pm", "1:00pm", "2:00pm", "3:00pm", "4:00pm",
                   "5:00pm", "6:00pm", "7:00pm", "8:00pm", "9:00pm", "10:00pm", "11:00pm"]

        print(tabulate(table, headers=headers, tablefmt="grid"))
        if value == 1:
            with open("schedule.txt", "w") as file:
                file.write(tabulate(table, headers=headers, tablefmt="grid"))

    
    def edit(self):
        print("Working on this")
 
class CSP: 
	def __init__(self, variables, Domains,classHour): 
		self.variables = variables 
		self.domains = Domains 
		self.classHour = classHour
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
		domain_values = self.domains[var]

        # Separate values >= 5 from other values
		greater_than_five = [value for value in domain_values if value >= 5]
		other_values = [value for value in domain_values if value < 5]

        # Combine the two lists with the ones >= 5 first
		ordered_values = greater_than_five + other_values
		
		return ordered_values

	def is_consistent(self, var, value, assignment):
        # Copy the assignment into a new one and add in the value
		updated = assignment.copy()
		updated[var] = value

		# Calculate total study hours assigned for the specific day
		day_of_assignment = var[0] 
		total_study_hours = sum(1 for (day, hour) in updated.keys() if day == day_of_assignment and updated[(day, hour)] >= 5)
		total_limit = 0
          
		#if value != 0 and (((var[0], var[1]-1) in updated and updated[(var[0], var[1]-1)] <= 4) or ((var[0], var[1]+1) in updated and updated[(var[0], var[1]+1)] <= 4)):
			#return False
                           
        # Go over each class hour to ensure the limit is not 
		for index, limit in enumerate(self.classHour):
			class_hour_count = sum(1 for assigned_value in updated.values() if assigned_value == (index + 5))
			class_hour_countDay = sum(1 for (day, hour) in updated.keys() if day == day_of_assignment and updated[(day, hour)] == (index + 5))
			total_limit += limit			
			if class_hour_count > limit:
				return False
			if limit < 5 and class_hour_countDay > 1:
				return False
			elif class_hour_countDay > ((limit // 5)+1):
				return False
		if total_limit < 5:
			if total_study_hours > 2:
				return False  
		else:
			if total_study_hours > ((total_limit // 5)+1):
				return False  
		return True

def editSchedule(words, nums, my_classes, schedule, scheduleWords, className, classHour):
    for i,j in nums:
        if nums[i, j] >= 5:
            schedule[i][j] = 4
            scheduleWords[i][j] = ""
    final, nums = satisfyConstraints(my_classes, schedule, scheduleWords, className, classHour)
    return final, nums
    


def prompt(test, nums, my_classes, schedule, scheduleWords, className, classHour):
    print(" ")
    print("Choose an action:")
    action = input("(1) Edit Timeslots    (2) Generate New Schedule    (3) Print Schedule to File   (4) Quit \n\n")
    if action == "Print Schedule" or action == "3":
        test.printWeek(1)
        prompt(test, nums, my_classes, schedule, scheduleWords, className, classHour)
    elif action == "Edit Timeslots" or action == "1":
        test.edit()
        prompt(test, nums, my_classes, schedule, scheduleWords, className, classHour)
    elif action == "Generate New Schedule" or action == "2":
        test, nums = editSchedule(test, nums, my_classes, schedule, scheduleWords, className, classHour)
        prompt(test, nums, my_classes, schedule, scheduleWords, className, classHour)
    elif action == "Quit" or action == "4":
        print("Exiting program")
    else:
        print("Invalid command")
        prompt(test, nums, my_classes, schedule, scheduleWords, className, classHour)

def satisfyConstraints(my_classes, schedule, scheduleWords, className, classHour):
    # Variables 
    variables = [(i, j) for i in range(7) for j in range(24)] 
    with open("variables.txt", "w") as file:
                for var in variables:
                    file.write(str(var) + '\n')

    classNum = my_classes.numClass + 5

    # Domains: sleep = 1, work = 2, class = 3, other = 4, study = 5+ set(range(5, classNum+1)) 
    Domains = {var: set(range(5, classNum)) | set([0]) if schedule[var[0]][var[1]] == 0
                            else {schedule[var[0]][var[1]]} for var in variables}

    with open("domain.txt", "w") as file:
                for key, value in Domains.items():
                    file.write(f"{key}: {value}\n")

    # Store how long to study for each class
    classHours = []
    for i in range(index2):
        classHours.append(my_classes.classes[i]['study_hours'])

    csp = CSP(variables, Domains, classHour) 
    sol = csp.solve() 

    solution = [[0 for i in range(24)] for i in range(7)] 
    for i,j in sol: 
        if (sol[i,j] >= 5): 
            scheduleWords[i][j] = "Study " + str(className[sol[i,j]-5])
        elif (sol[i,j] == 0):
            scheduleWords[i][j] = " "
        solution[i][j]=sol[i,j] 
    final = Week(scheduleWords)
    final.printWeek(0)  
    return final, sol
    #for row in scheduleWords:
        #print(row)


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
#test = Week()
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

className = []
classHour = []
for num in my_classes.classes:
     className.append(num['name'])
     classHour.append(num['study_hours'])

final, nums = satisfyConstraints(my_classes, schedule, scheduleWords, className, classHour)
prompt(final, nums, my_classes, schedule, scheduleWords, className, classHour)
