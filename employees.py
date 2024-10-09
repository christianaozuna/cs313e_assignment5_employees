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
        self._performance = INITIAL_PERFORMANCE
        self.__happiness = INITIAL_HAPPINESS

    # name, read only
    @property
    def name(self):
        """
        Read only property returning name.
        """
        return self.__name

    # manager, read only
    @property
    def manager(self):
        """
        Read only property returning manager name.
        """
        return self.__manager

    @property
    def performance(self):
        """
        Read only property returning performance.
        """
        return self._performance

    # performance, clamped to 0 or 100 if out of range
    @performance.setter
    def performance(self, performance):
        """
        Setter for performance.
        """
        # less than 0 (percentage min)
        if performance < PERCENTAGE_MIN:
            self._performance = 0
        # greater than 100 (percentage max)
        elif performance > PERCENTAGE_MAX:
            self._performance = 100
        else:
            self._performance = performance

    @property
    def happiness(self):
        """
        Read only property returning happiness.
        """
        return self.__happiness

    # happiness, clamped to 0 or 100 if out of range
    @happiness.setter
    def happiness(self, happiness):
        # less than 0 (percentage min)
        if happiness < PERCENTAGE_MIN:
            self.__happiness = 0
        # greater than 100 (percentage max)
        elif happiness > PERCENTAGE_MAX:
            self.__happiness = 100
        else:
            self.__happiness = happiness

    @property
    def salary(self):
        """
        Read only property returning salary.
        """
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
        """
        Represents an interaction of one employee with another.
        """
        # if not in dictionary
        if other not in self.relationships:
            # add and initialize relationship to 0
            self.relationships[other.name] = 0
        # check if relationship > threshold
        if self.relationships[other.name] >= RELATIONSHIP_THRESHOLD:
            # employee happiness increase by 1
            self.__happiness += 1
        # if not above relationship threshold but both employees happiness > happiness threshold
        elif self.__happiness >= HAPPINESS_THRESHOLD and other.happiness >= HAPPINESS_THRESHOLD:
            # relationship improves by 1
            self.relationships[other.name] += 1
        # otherwise
        else:
            # relationshup decreases
            self.relationships[other.name] -= 1
            # happiness increases
            self.__happiness -= 1

    def daily_expense(self):
        """
        Simulates the employees daily expenses by reducing their happiness and savings.
        """
        self.__happiness -= 1
        self.savings -= DAILY_EXPENSE

    def __str__(self):
        return self.name + "\n\tSalary: $" + str(self.salary) + "\n\tSavings: $" + \
              str(self.savings) + "\n\tHappiness: " + str(self.__happiness) + \
                "%\n\tPerformance: " + str(self._performance) + "%"

class Manager(Employee):
    """
    A subclass of Employee representing a manager.
    """

    def work(self):
        change = random.randint(-5, 5)
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

    def work(self):
        change = random.randint(-15, 15)
        self.performance += change
        if change <= 0:
            self.happiness -= 2
        elif change > 0:
            self.happiness += 1

    def interact(self, other):
        super().interact(other)
        # if the other employee is the person's manger
        if other == self.manager:
            if other.happiness >= HAPPINESS_THRESHOLD and \
                self._performance >= TEMP_EMPLOYEE_PERFORMANCE_THRESHOLD:
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
    def work(self):
        change = random.randint(-10, 10)
        self.performance += change
        if change >= 0:
            self.happiness += 1

    def interact(self, other):
        super().interact(other)
        if other == self.manager:
            if other.happiness >= HAPPINESS_THRESHOLD and self._performance > \
                PERM_EMPLOYEE_PERFORMANCE_THRESHOLD:
                self.savings += MANAGER_BONUS
            elif other.happiness <= HAPPINESS_THRESHOLD:
                self.happiness -= 1
