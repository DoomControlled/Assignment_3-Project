#########################
# Joshua Hajec
# ITEC 3265
# Professor Jongho Seol
# 10/17/2023
#########################

from time import *
from random import *


# Return the current time rounded to the nearest millisecond.
# Used for general timekeeping to keep things consistent.
def getTimeMS():
    return round(time() * 1000)


# Process class
# Accepts a Process ID, Required burst time, and Priority as initialization arguments.
class Process:

    # Set up object when initialized.
    def __init__(self, Process_ID, BurstTime, Priority):
        self.pid = Process_ID
        self.burstTime = BurstTime
        self.priority = Priority

        # Additional variables.
        self.arrivalTime = 0
        self.startTime = 0

    # Set arrival time
    def Set_Arrival_Time(self):
        self.arrivalTime = getTimeMS()

    # Set start time
    def Set_Start_Time(self):
        self.startTime = getTimeMS()

    # Get Arrival Time
    def Get_Arrival_Time(self):
        return self.arrivalTime

    # Get Start Time
    def Get_Start_Time(self):
        return self.startTime

    # Get Burst Time
    def Get_Burst_Time(self):
        return self.burstTime

    # Get Priority
    def Get_Priority(self):
        return self.priority


# Scheduler class.
# Accepts a memorySize as an initialization argument.
class Scheduler:

    # Initialize the scheduler. Running queue can be given a size (Threads) to test the simulation.
    def __init__(self, Threads=3):
        self.readyQueue = []
        self.runningQueue = [0] * Threads
        self.completedQueue = []
        self.timeStarted = 0
        self.currentTime = getTimeMS()
        self.memoryUsageSnapshots = []
        self.turnAroundTimes = []
        self.waitTimes = []

    # Append a process to the end of the ready queue.
    def Add_Process(self, process):
        self.readyQueue.append(process)

    # Check for an empty slot in the running queue (Represented by a 0).
    # If one is found, return a tuple of true and the index. Return false otherwise.
    # The value returned should always have its first tuple value checked in an if statement.
    def EmptySlot(self):
        for index, slot in enumerate(self.runningQueue):
            if slot == 0:
                return True, index
        # No empty slot found.
        return False, None

    # Run the scheduling algorithm on the ready queue and move processes to the running queue.
    # First come, First served
    # This algorithm finds the first process in the ready queue (Process at index 0).
    # This process is then moved from the ready queue to the running queue.
    def Run_Scheduling_Algorithm_FCFS(self):
        slot = self.EmptySlot()
        if slot[0]:
            if len(self.readyQueue) > 0:
                # Scheduling algorithm and move process to running queue.
                process = self.readyQueue.pop(0)
                process.Set_Start_Time()
                self.Calculate_Wait_Time(process)
                self.runningQueue[slot[1]] = process

    # Run the scheduling algorithm on the ready queue and move processes to the running queue.
    # Priority Scheduling
    # This algorithm checks all process in the ready queue. It then determines the process with the highest priority.
    # In the case of this algorithm, higher value = higher priority, so 1 goes after 2 for example.
    # If two processes have the same priority, it picks the first one found.
    # This process is then moved from the ready queue into the running queue.
    def Run_Scheduling_Algorithm_PS(self):
        slot = self.EmptySlot()
        if slot[0]:
            if len(self.readyQueue) > 0:

                # Scheduling algorithm
                # Default the chosen process to the first process in the ready queue.
                process = self.readyQueue[0]
                index = 0
                # Find the first process with the highest priority number in the ready queue.
                for spot, checkProcess in enumerate(self.readyQueue):
                    if checkProcess.Get_Priority() > process.Get_Priority():
                        process = checkProcess
                        index = spot

                # Move process to running queue.
                process = self.readyQueue.pop(index)
                process.Set_Start_Time()
                self.Calculate_Wait_Time(process)
                self.runningQueue[slot[1]] = process

    # Run the scheduling algorithm on the ready queue and move processes to the running queue.
    # Shortest Job First
    # This algorithm checks all processes in the ready queue.
    # It then determines the process with the smallest Burst time.
    # If two process have the same smallest burst time, it picks the first one found.
    # This process is then moved from the ready queue into the running queue.
    def Run_Scheduling_Algorithm_SJF(self):
        slot = self.EmptySlot()
        if slot[0]:
            if len(self.readyQueue) > 0:

                # Scheduling algorithm
                # Default the chosen process to the first process in the ready queue.
                process = self.readyQueue[0]
                index = 0

                # Find the first process with the lowest burst time in the ready queue.
                for spot, checkProcess in enumerate(self.readyQueue):
                    if checkProcess.Get_Burst_Time() < process.Get_Burst_Time():
                        process = checkProcess
                        index = spot

                # Move process to running queue.
                process = self.readyQueue.pop(index)
                process.Set_Start_Time()
                self.Calculate_Wait_Time(process)
                self.runningQueue[slot[1]] = process

    # Run the scheduling algorithm on the ready queue and move processes to the running queue.
    # Random Job
    # This algorithm selects a random process from the ready queue and puts it in the running queue.
    def Run_Random_Algorithm(self):
        slot = self.EmptySlot()
        if slot[0]:
            if len(self.readyQueue) > 0:
                # Scheduling algorithm (technically)
                index = randint(0, len(self.readyQueue) - 1)

                # Move process to running queue.
                process = self.readyQueue.pop(index)
                process.Set_Start_Time()
                self.Calculate_Wait_Time(process)
                self.runningQueue[slot[1]] = process

    # Check for completed processes within the running queue and move them to the completed queue.
    # This is done by checking whether the amount of time that has passed since the process started
    # Is more than or equal to its burst time.
    def Check_Complete(self):
        for index, process in enumerate(self.runningQueue):
            if isinstance(process, Process):
                if self.currentTime - process.Get_Start_Time() >= process.Get_Burst_Time():
                    self.Calculate_Turnaround(self.runningQueue[index])
                    # Print logging info when a process completes.
                    print(f"Process {process.pid} has completed execution at {self.currentTime - self.timeStarted}ms "
                          f"with a Turnaround time of {self.turnAroundTimes[len(self.turnAroundTimes)-1]}")
                    self.completedQueue.append(process)
                    self.runningQueue[index] = 0

    # Calculate memory usage in this instant.
    # (This is calculated by How many processes can run vs How many are running)
    # Outputs the percentage into the memoryUsageSnapshots list.
    def Calculate_Memory_Usage(self):
        count = 0
        for obj in self.runningQueue:
            if isinstance(obj, Process):
                count += 1
        if not len(self.runningQueue) == 0:
            self.memoryUsageSnapshots.append(count / len(self.runningQueue) * 100)

    # Calculate average memory usage.
    def Calculate_Average_Memory_Usage(self):
        count = 0
        total = 0
        for value in self.memoryUsageSnapshots:
            count += 1
            total += value
        if not count == 0:
            return total / count

    # Calculates turnaround time for a process in ms. This should be run on a process when it is complete.
    def Calculate_Turnaround(self, process):
        self.turnAroundTimes.append(self.currentTime - process.Get_Arrival_Time())

    # Calculates the average turnaround time for all completed processes in ms.
    def Calculate_Average_Turnaround(self):
        count = 0
        total = 0
        for value in self.turnAroundTimes:
            count += 1
            total += value
        if not count == 0:
            return total / count

    # Calculate the time a process waited before being moved from ready queue to running queue in ms.
    def Calculate_Wait_Time(self, process):
        self.waitTimes.append(self.currentTime - process.Get_Arrival_Time())

    # Calculate the average wait time for all processes in ms.
    def Calculate_Average_Wait_Time(self):
        count = 0
        total = 0
        for value in self.waitTimes:
            count += 1
            total += value
        if not count == 0:
            return total / count

    # Calculate metrics and return a tuple with (WaitTime, TurnaroundTime, MemoryUsage).
    def Calculate_Metrics(self):
        Wait = self.Calculate_Average_Wait_Time()
        Turnaround = self.Calculate_Average_Turnaround()
        Memory = self.Calculate_Average_Memory_Usage()
        return Wait, Turnaround, Memory

    # Display metrics
    def Display_Metrics(self, Metrics):
        print(f"Metrics")
        print(f"Average Process Wait Time: {round(Metrics[0])} ms")
        print(f"Average Process Turnaround Time: {round(Metrics[1])} ms")
        print(f"Average CPU Memory Usage: {round(Metrics[2])}%")

    # Execute the simulation. Accepts a list of processes to simulate running.
    # Also accepts a conditional argument algorithm to determine which algorithm to run.
    def Simulate(self, processList, algorithm=0, processAddTime=5, fullDebug=False):
        # Start the simulation clock.
        self.timeStarted = getTimeMS()

        # Time to wait before adding a new process in ms.
        lastAddedTime = self.timeStarted
        simulating = 1

        # Simulation loop
        while simulating:
            # Check memory usage every millisecond for metrics.
            if getTimeMS() - self.currentTime == 1:
                self.Calculate_Memory_Usage()

            # Get the current time for each loop to use during benchmarking).
            self.currentTime = getTimeMS()

            # Add a new process from the process list to the ready queue if enough time has passed.
            # Time required is determined by processAddTime.
            if self.currentTime - lastAddedTime >= processAddTime and not len(processList) == 0:
                process = processList.pop(0)
                process.Set_Arrival_Time()
                self.Add_Process(process)
                lastAddedTime = getTimeMS()

            # Run the scheduling algorithm on the ready queue.
            if algorithm == 0:
                self.Run_Scheduling_Algorithm_FCFS()
            elif algorithm == 1:
                self.Run_Scheduling_Algorithm_PS()
            elif algorithm == 2:
                self.Run_Scheduling_Algorithm_SJF()
            elif algorithm == 3:
                self.Run_Random_Algorithm()
            else:
                algorithm = 0

            # Check for completed processes in the running queue.
            self.Check_Complete()

            # Check for the exit condition.
            # Exit condition is reached when all of the following statements are false:
            # 1.) There is an item in the running queue
            #           -All non-zero objects in the running queue represent processes.
            # 2.) The length of the input process list is greater than 0 (There are still processes in the list)
            # 3.) The length of the ready queue is greater than 0 (There are still processes in the ready queue)
            # If all of these are false, then it is determined that all processes have completed execution.
            simulating = 0
            for item in self.runningQueue:
                if not item == 0:
                    simulating = 1
            if not len(processList) == 0:
                simulating = 1
            if not len(self.readyQueue) == 0:
                simulating = 1

        # Exit from simulation loop and print simulation results.
        # Print extra information when in full debug mode.
        print(f"\nResults\n")

        # Extra debug information that only shows if selected to be shown.
        if fullDebug:
            print(f"Turnaround times list: {self.turnAroundTimes}")
            print(f"Wait times list: {self.waitTimes}")
            print(f"Memory usage list: {self.memoryUsageSnapshots}")

        print(f"Simulation information")

        # Display the algorithm used.

        if algorithm == 0:
            print(f"Scheduling Algorithm Used: First come, First served")
        elif algorithm == 1:
            print(f"Scheduling Algorithm Used: Priority Scheduling")
        elif algorithm == 2:
            print(f"Scheduling Algorithm Used: Shortest Job First")
        elif algorithm == 3:
            print(f"Scheduling Algorithm Used: Random Scheduling.")

        # Display number of CPU threads used.
        print(f"Threads: {len(self.runningQueue)}")

        # Display total processes ran.
        print(f"Processes ran: {len(self.completedQueue)}")

        # Display wait time between processes being added to the queue.
        print(f"Wait time between each process added to the simulation: {processAddTime} ms")

        print()

        # Display simulation metrics (Wait time, Turnaround time, Memory usage).
        self.Display_Metrics(self.Calculate_Metrics())

        print()
        print(f"Total time information")

        # Calculate and display the total combined burst time of all processes.
        BurstTime = 0
        for queue in self.readyQueue, self.runningQueue, self.completedQueue:
            for process in queue:
                if isinstance(process, Process):
                    BurstTime += process.Get_Burst_Time()

        print(f"Total cumulative burst time: {BurstTime} ms")

        print(f"Average burst time per process: {BurstTime / len(self.completedQueue)}")

        print(f"Actual run time: {self.currentTime - self.timeStarted} ms")
        print()

        # Extra debug information that only shows if selected to be shown.
        if fullDebug:
            print("Ready queue process ID's: ", end="")
            for process in self.readyQueue:
                if not process == 0:
                    print(f"{process.pid}, ", end="")
            print()
            print("Running queue process ID's: ", end="")
            for process in self.runningQueue:
                if not process == 0:
                    print(f"{process.pid}, ", end="")
            print()
            print("Completed queue process ID's: ", end="")
            for process in self.completedQueue:
                if not process == 0:
                    print(f"{process.pid}, ", end="")


# Main function to call
def Main():
    # Create the basic processes that will be used within the simulation.
    Processes = [Process(1, 10, 1),
                 Process(2, 5, 1),
                 Process(3, 15, 2),
                 Process(4, 5, 3),
                 Process(5, 10, 1),
                 Process(6, 30, 1),
                 Process(7, 100, 1),
                 Process(8, 100, 2),
                 Process(9, 30, 2),
                 Process(10, 5, 3)]

    # User selection for algorithm to use.
    userInput = input("Select an algorithm to use by typing the corresponding number."
                      "\n(1) First come, First served"
                      "\n(2) Priority Queue"
                      "\n(3) Shortest Job First"
                      "\n(4) Random Job Selection\n")

    # Default algorithm to 0 if enter is presses with no selection.
    if userInput == "":
        userInput = 0
    Algorithm = int(userInput) - 1

    # Default algorithm to 0 if an incorrect number is given.
    if not -1 < Algorithm < 4:
        Algorithm = 0

    # Default settings if no options are chosen.
    simthreads = 3
    AddTime = 5
    Debug = False

    # Additional Options
    userInput = input("Would you like to see additional options? (y/n)\n")
    if userInput == 'y' or userInput == "yes":
        # Allow for the generation of additional random processes to stress test the simulation if desired.
        # Default for anything besides yes is no.
        userInput = input("Would you like to generate additional random processes for the simulation? (y/n)\n")
        if userInput == 'y' or userInput == 'yes':
            Number = input("Type a number of processes to add (Maximum is 10,000).\n")
            Number = int(Number)
            if Number < 0:
                Number = 0
            if Number > 10000:
                Number = 10000
            BurstRange = input("Type a number for the maximum burst time in milliseconds (Maximum is 1000)."
                               "\nBurst time values will be between 0 and this number.\n")
            BurstRange = int(BurstRange)

            OriginalSize = len(Processes)
            for i in range(Number):
                # Create random processes with given parameters.
                Processes.append(Process(i + OriginalSize, randint(0, BurstRange), randint(1, 5)))

        # Change number of threads used.
        userInput = input("Would you like to change the number of threads used? Default is 3. (y/n)\n")
        if userInput == 'y' or userInput == 'yes':
            userInput = input("Please input the number of threads\n")
            simthreads = int(userInput)

        # Change the time between adding processes
        userInput = input("Would you like to change the time between inserting processes to the waiting queue?"
                          "Default is 5ms. (y/n)\n")
        if userInput == 'y' or userInput == 'yes':
            userInput = input("Please input an integer time (milliseconds).\n")
            AddTime = int(userInput)

        # User selection for advanced results. Default is false.
        userInput = input("See advanced result information? (y/n)"
                          "\nNote: May be hard to read with a large number of processes.\n")
        if userInput == "y" or userInput == "yes":
            Debug = True

    # Initialize the Scheduler for the simulation.
    Simulation = Scheduler(simthreads)

    print("\nRunning Simulation...")
    # Run the simulation with the given process list, algorithm, add to simulation time, and advanced debug settings.
    Simulation.Simulate(Processes, Algorithm, AddTime, Debug)

Main()