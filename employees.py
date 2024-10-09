"""
Student information for this assignment:

On my/our honor, Christiana Ozuna and Jessica North, this
programming assignment is my own work and I have not provided this code to
any other student.

I have read and understand the course syllabus's guidelines regarding Academic
Integrity. I understand that if I violate the Academic Integrity policy (e.g.
copy code from someone else, have the code generated by an LLM, or give my
code to someone else), the case shall be submitted to the Office of the Dean of
Students. Academic penalties up to and including an F in the course are likely.

UT EID 1: cmo2388
UT EID 2: jan3557
"""

from abc import ABC, abstractmethod
import random

DAILY_EXPENSE = 60
HAPPINESS_THRESHOLD = 50
MANAGER_BONUS = 1000
TEMP_EMPLOYEE_PERFORMANCE_THRESHOLD = 50
PERM_EMPLOYEE_PERFORMANCE_THRESHOLD = 25
RELATIONSHIP_THRESHOLD = 10
INITIAL_PERFORMANCE = 75
INITIAL_HAPPINESS = 50
PERCENTAGE_MAX = 100
PERCENTAGE_MIN = 0
SALARY_ERROR_MESSAGE = "Salary must be non-negative."

class Employee(ABC):
    """
    Abstract base class representing a generic employee in the system.
    """

    def __init__(self, name, manager, salary, savings):
        self.relationships = {}
        self.savings = savings
        self.__salary = salary
        self.is_employed = True
        self.__name = name
        self.__manager = manager
        self.__performance = INITIAL_PERFORMANCE
        self.happiness = INITIAL_HAPPINESS

    # name, read only
    @property
    def name(self):
        return self.__name

    # manager, read only
    @property
    def manager(self):
        return self.__manager

    @property
    def performance(self):
        return self.__performance

    # performance, clamped to 0 or 100 if out of range
    @performance.setter
    def performance(self, performance):
        # less than 0 (percentage min)
        if performance < PERCENTAGE_MIN:
            self.__performance = 0
        # greater than 100 (percentage max)
        elif performance > PERCENTAGE_MAX:
            self.__performance = 100
        else:
            self.__performance = performance

    @property
    def happiness(self):
        return self.happiness

    # happiness, clamped to 0 or 100 if out of range
    @happiness.setter
    def happiness(self, happiness):
        # less than 0 (percentage min)
        if happiness < PERCENTAGE_MIN:
            self.happiness = 0
        # greater than 100 (percentage max)
        elif happiness > PERCENTAGE_MAX:
            self.happiness = 100
        else:
            self.happiness = happiness

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, value):
        # salary must be non-negative
        if value >= 0:
            self.__salary = value
        else:
            raise ValueError

    @abstractmethod
    def work(self):
        pass

    def interact(self, other):
        # if not in dictionary
        if other.name not in self.relationships:
            # add and initialize relationship to 0
            self.relationships[other.name] = 0
        # if in dictionary
        elif other.name in self.relationships:
            # check if relationship > threshold
            if self.relationships[other.name] >= RELATIONSHIP_THRESHOLD:
                # employee happiness increase by 1
                self.happiness += 1
            # if not above relationship threshold but both employees happiness > happiness threshold
            elif self.happiness >= HAPPINESS_THRESHOLD and other.happiness >= HAPPINESS_THRESHOLD:
                # relationship improves by 1
                self.relationships[other.name] += 1
            # otherwise
            else:
                # relationshup decreases
                self.relationships[other.name] -= 1
                # happiness increases
                self.happiness -= 1

    def daily_expense(self):
        self.happiness -= 1
        self.savings -= DAILY_EXPENSE

    def __str__(self):
        return self.name + "\n\tSalary: $" + str(self.salary) + "\n\tSavings: $" + \
              str(self.savings) + "\n\tHappiness: " + str(self.happiness) + "%\n\tPerformance: " + \
                str(self.__performance) + "%"

class Manager(Employee):
    """
    A subclass of Employee representing a manager.
    """
    def __init__(self, name, manager, salary, savings):
        super().__init__(name, manager, salary, savings)

    def work(self):
        change = random.randint(-5, 6)
        self.performance += change
        if change <= 0:
            self.happiness -= 1
            for employee in self.relationships:
                self.relationships[employee] -= 1
        elif change > 1:
            self.happiness += 1

class TemporaryEmployee(Employee):
    """
    A subclass of Employee representing a temporary employee.
    """

    def __init__(self, name, manager, salary, savings):
        super().__init__(name, manager, salary, savings)

    def work(self):
        change = random.randint(-15, 16)
        self.__performance += change
        if change <= 0:
            self.happiness -= 2
        elif change > 1:
            self.happiness += 1

    def interact(self, other):
        # if the other employee is the person's manger
        if other.name == self.manager:
            if other.happiness >= HAPPINESS_THRESHOLD and \
                self.__performance >= TEMP_EMPLOYEE_PERFORMANCE_THRESHOLD:
                self.savings += MANAGER_BONUS
            elif other.happiness <= HAPPINESS_THRESHOLD:
                self.salary = self.salary // 2
                self.happiness -= 5

        if self.salary <= 0:
            self.is_employed = False

class PermanentEmployee(Employee):
    """
    A subclass of Employee representing a permanent employee.
    """
    def __init__(self, name, manager, salary, savings):
        super().__init__(name, manager, salary, savings)

    def work(self):
        change = random.randint(-10, 11)
        if change >= 0:
            self.happiness += 1

    def interact(self, other):
        if other.name == self.manager:
            if other.happiness >= HAPPINESS_THRESHOLD and self.__performance > \
                PERM_EMPLOYEE_PERFORMANCE_THRESHOLD:
                self.savings += MANAGER_BONUS
            elif other.happiness <= HAPPINESS_THRESHOLD:
                self.happiness -= 1
