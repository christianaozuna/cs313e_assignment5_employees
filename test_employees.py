"""
Employees testing suite.
"""

import unittest
import random
import sys
from employees import Employee, Manager, TemporaryEmployee, PermanentEmployee


class TestEmployee(unittest.TestCase):
    """Employee Class Test Suite"""

    def test_employee_1(self):
        """Test that Employee cannot be instantiated (abstract class)."""
        with self.assertRaises(TypeError):
            Employee("A", None, 200, 10000)


class TestManager(unittest.TestCase):
    """Manager Class Test Suite"""

    def test_manager_1(self):
        """Test initialization of Manager attributes."""
        e = Manager("A", None, 200, 10000)
        self.assertEqual(e.name, "A")
        self.assertEqual(e.manager, None)
        self.assertEqual(e.salary, 200)
        self.assertEqual(e.savings, 10000)
        self.assertEqual(e.happiness, 50)
        self.assertEqual(e.performance, 75)
        self.assertTrue(e.is_employed)

    def test_manager_2(self):
        """Test setting performance to a normal value."""
        e = Manager("A", None, 200, 10000)
        e.performance = 85
        self.assertEqual(e.performance, 85)

    def test_manager_3(self):
        """Test performance value below zero should set to 0."""
        e = Manager("A", None, 200, 10000)
        e.performance -= 101
        self.assertEqual(e.performance, 0)

    def test_manager_4(self):
        """Test performance value above 100 should set to 100."""
        e = Manager("A", None, 200, 10000)
        e.performance = 150
        self.assertEqual(e.performance, 100)

    def test_manager_5(self):
        """Test setting happiness to a normal value."""
        e = Manager("A", None, 200, 10000)
        e.happiness = 70
        self.assertEqual(e.happiness, 70)

    def test_manager_6(self):
        """Test changing name."""
        e = Manager("A", None, 200, 10000)
        with self.assertRaises(AttributeError):
            e.name = "B"

    def test_manager_7(self):
        """Test happiness value above 100 should set to 100."""
        e = Manager("A", None, 200, 10000)
        e.happiness = 120
        self.assertEqual(e.happiness, 100)

    def test_manager_8(self):
        """Test setting salary to a normal value."""
        e = Manager("A", None, 200, 10000)
        e.salary = 6000
        self.assertEqual(e.salary, 6000)

    def test_manager_9(self):
        """Test negative salary should raise ValueError."""
        e = Manager("A", None, 200, 10000)
        with self.assertRaises(ValueError):
            e.salary = -1

    def test_manager_10(self):
        """Test savings set to a normal value."""
        e = Manager("A", None, 200, 0)
        e.savings += 15000
        self.assertEqual(e.savings, 15000)

    def test_manager_11(self):
        """Test decrementing savings to negative value."""
        e = Manager("A", None, 200, 0)
        e.savings -= 500
        self.assertEqual(e.savings, -500)

    def test_manager_12(self):
        """Test daily expense deduction on happiness and savings."""
        e = Manager("A", None, 200, 10000)
        e.daily_expense()
        self.assertEqual(e.happiness, 49)
        self.assertEqual(e.savings, 9940)

    def test_manager_13(self):
        """Test daily expense results in negative savings."""
        e = Manager("A", None, 200, 50)
        e.daily_expense()
        self.assertEqual(e.savings, -10)

    def test_manager_14(self):
        """Test interaction creates a new relationship."""
        e1 = Manager("A", None, 200, 10000)
        e2 = Manager("B", e1, 6000, 15000)
        e1.interact(e2)
        self.assertIn("B", e1.relationships)
        self.assertEqual(e1.relationships["B"], 1)

    def test_manager_15(self):
        """Test interaction increases happiness when relationship score is high."""
        e1 = Manager("A", None, 200, 10000)
        e2 = Manager("B", e1, 6000, 15000)
        e1.relationships["B"] = 15
        e1.interact(e2)
        self.assertEqual(e1.happiness, 51)

    def test_manager_16(self):
        """Test interaction decreases happiness when both employees are unhappy."""
        e1 = Manager("A", None, 200, 10000)
        e2 = Manager("B", e1, 6000, 15000)
        e1.happiness = 40
        e2.happiness = 40
        e1.interact(e2)
        self.assertEqual(e1.happiness, 39)
        self.assertEqual(e1.relationships["B"], -1)

    def test_manager_17(self):
        """Test manager work increases performance."""
        e = Manager("A", None, 200, 10000)
        random.seed(999)
        e.work()
        self.assertGreaterEqual(e.performance, 80)

    def test_manager_18(self):
        """Test manager work decreases performance."""
        e = Manager("A", None, 200, 10000)
        random.seed(123)
        e.work()
        self.assertEqual(e.performance, 70)

    def test_manager_19(self):
        """Test string representation of a manager."""
        e = Manager("A", None, 500, 100000)
        self.assertEqual(
            str(e),
            "A\n\tSalary: $500\n\tSavings: $100000\n\tHappiness: 50%\n\tPerformance: 75%",
        )

    def test_manager_20(self):
        """Test work when performance is at zero."""
        e = Manager("A", None, 200, 10000)
        e.performance = 1
        random.seed(123)
        e.work()
        self.assertGreaterEqual(e.performance, 0)

    def test_manager_21(self):
        """Test work when performance is at maximum (100)."""
        e = Manager("A", None, 200, 10000)
        e.performance = 100
        random.seed(1)
        e.work()
        self.assertLessEqual(e.performance, 100)

    def test_manager_22(self):
        """Test salary deduction after daily expense."""
        e = Manager("A", None, 200, 100)
        e.daily_expense()
        self.assertEqual(e.savings, 40)

    def test_manager_23(self):
        """Test savings can become negative after daily expense."""
        e = Manager("A", None, 200, 50)
        e.daily_expense()
        self.assertEqual(e.savings, -10)

    def test_manager_24(self):
        """Test happiness decreases after daily expense."""
        e = Manager("A", None, 200, 5000)
        e.daily_expense()
        self.assertEqual(e.happiness, 49)

    def test_manager_25(self):
        """Test interaction does not increase happiness when both employees are unhappy."""
        e1 = Manager("A", None, 200, 10000)
        e2 = Manager("B", e1, 6000, 15000)
        e1.happiness = 45
        e2.happiness = 45
        e1.interact(e2)
        self.assertEqual(e1.happiness, 44)

    def test_manager_26(self):
        """Test interaction with a new employee starts with 0 relationship score."""
        e1 = Manager("A", None, 200, 10000)
        e2 = Manager("B", e1, 6000, 15000)
        e1.interact(e2)
        e2.interact(e1)
        self.assertEqual(e1.relationships["B"], 1)
        self.assertEqual(e2.relationships["A"], 1)

    def test_manager_27(self):
        """Test work maintains performance at boundary when it reaches zero."""
        e = Manager("A", None, 200, 10000)
        e.performance = 0
        random.seed(6)
        e.work()
        self.assertGreaterEqual(e.performance, 0)

    def test_manager_28(self):
        """Test performance does not exceed 100 when increased."""
        e = Manager("A", None, 200, 10000)
        e.performance = 100
        random.seed(0)
        e.work()
        self.assertLessEqual(e.performance, 100)

    def test_manager_29(self):
        """Test that relationships decrease if manager performance decreases."""
        e = Manager("A", None, 200, 10000)
        e.relationships = {"B": 3}
        random.seed(2)  # Ensure performance decreases
        e.work()
        self.assertEqual(e.relationships["B"], 2)


class TestTemporaryEmployee(unittest.TestCase):
    """Temporary Employee Test Suite"""

    def test_temp_employee_1(self):
        """Test temporary employee work increases performance."""
        e = TemporaryEmployee("A", None, 200, 10000)
        random.seed(3)
        e.work()
        self.assertEqual(e.performance, 67)

    def test_temp_employee_2(self):
        """Test temporary employee work decreases performance."""
        e = TemporaryEmployee("A", None, 200, 10000)
        random.seed(4)
        e.work()
        self.assertLessEqual(e.performance, 75)

    def test_temp_employee_3(self):
        """Test temp employee interaction gives bonus when performance is high."""
        manager = Manager("M", None, 10000, 20000)
        employee = TemporaryEmployee("A", manager, 200, 10000)
        employee.performance = 60
        manager.happiness = 60
        employee.interact(manager)
        manager.interact(employee)
        self.assertEqual(employee.savings, 11000)

    def test_temp_employee_4(self):
        """Test temp employee salary halves and becomes unemployed if performance is low."""
        manager = Manager("M", None, 10000, 20000)
        employee = TemporaryEmployee("A", manager, 200, 10000)
        employee.performance = 40
        manager.happiness = 40
        employee.interact(manager)
        manager.interact(employee)
        self.assertEqual(employee.salary, 100)
        self.assertTrue(employee.is_employed)

    def test_temp_employee_5(self):
        """Test interaction with a non-manager employee does not change salary or savings."""
        manager = Manager("M", None, 10000, 20000)
        employee = TemporaryEmployee("A", manager, 200, 10000)
        other_employee = TemporaryEmployee("B", manager, 4000, 8000)
        employee.interact(other_employee)
        self.assertEqual(employee.savings, 10000)
        self.assertEqual(employee.salary, 200)

    def test_temp_employee_6(self):
        """Test work does not modify savings."""
        e = TemporaryEmployee("A", None, 200, 10000)
        random.seed(6)
        e.work()
        self.assertEqual(e.savings, 10000)

    def test_temp_employee_7(self):
        """Test daily expense reduces savings but not salary."""
        e = TemporaryEmployee("A", None, 200, 1000)
        e.daily_expense()
        self.assertEqual(e.savings, 940)
        self.assertEqual(e.salary, 200)

    def test_temp_employee_8(self):
        """Test temp employee does not get bonus if manager happiness is low."""
        manager = Manager("M", None, 10000, 20000)
        employee = TemporaryEmployee("A", manager, 200, 10000)
        employee.performance = 60
        manager.happiness = 40
        employee.interact(manager)
        manager.interact(employee)
        self.assertEqual(employee.savings, 10000)

    def test_temp_employee_9(self):
        """Test temp employee becomes unemployed when salary is halved to 0."""
        manager = Manager("M", "Bob", 10000, 20000)
        employee = TemporaryEmployee("A", manager, 1, 10000)
        manager.happiness = 40
        employee.performance = 40
        employee.interact(manager)
        manager.interact(employee)
        self.assertFalse(employee.is_employed)

    def test_temp_employee_10(self):
        """Test string representation of a temp employee."""
        e = TemporaryEmployee("A", None, 200, 10000)
        self.assertEqual(
            str(e),
            "A\n\tSalary: $200\n\tSavings: $10000\n\tHappiness: 50%\n\tPerformance: 75%",
        )

    def test_temp_employee_11(self):
        """Test temporary employee performance increase does not exceed 100."""
        e = TemporaryEmployee("A", None, 200, 10000)
        e.performance = 100
        random.seed(3)
        e.work()
        self.assertEqual(e.performance, 92)

    def test_temp_employee_12(self):
        """Test temporary employee performance at minimum remains non-negative."""
        e = TemporaryEmployee("A", None, 200, 10000)
        e.performance = 0
        random.seed(4)
        e.work()
        self.assertGreaterEqual(e.performance, 0)

    def test_temp_employee_13(self):
        """Test temporary employee daily expense decreases both savings and happiness."""
        e = TemporaryEmployee("A", None, 200, 10000)
        e.daily_expense()
        self.assertEqual(e.savings, 9940)
        self.assertEqual(e.happiness, 49)

    def test_temp_employee_14(self):
        """Test that temporary employee does not lose employment if salary is positive."""
        manager = Manager("M", None, 10000, 20000)
        employee = TemporaryEmployee("A", manager, 200, 10000)
        employee.performance = 40
        manager.happiness = 40
        employee.interact(manager)
        self.assertTrue(employee.is_employed)

    def test_temp_employee_15(self):
        """Test temporary employee does not get bonus if performance is below threshold."""
        manager = Manager("M", None, 10000, 20000)
        employee = TemporaryEmployee("A", manager, 200, 10000)
        employee.performance = 40
        manager.happiness = 60
        employee.interact(manager)
        self.assertEqual(employee.savings, 10000)


class TestPermanentEmployee(unittest.TestCase):
    """Permanent Employee Test Suite"""

    def test_perm_employee_1(self):
        """Test permanent employee work can sometimes not change performance."""
        e = PermanentEmployee("A", None, 200, 10000)
        initial_performance = e.performance
        random.seed(5)
        e.work()
        self.assertGreaterEqual(e.performance, initial_performance)

    def test_perm_employee_2(self):
        """Test permanent employee work decreases performance."""
        e = PermanentEmployee("A", None, 200, 10000)
        random.seed(6)
        e.work()
        self.assertLessEqual(e.performance, 83)

    def test_perm_employee_3(self):
        """Test perm employee interaction gives bonus when performance is high."""
        manager = Manager("M", None, 10000, 20000)
        employee = PermanentEmployee("A", manager, 200, 10000)
        employee.performance = 30
        manager.happiness = 60
        employee.interact(manager)
        self.assertEqual(employee.savings, 11000)

    def test_perm_employee_4(self):
        """Test perm employee does not get bonus when performance is low."""
        manager = Manager("M", None, 10000, 20000)
        employee = PermanentEmployee("A", manager, 200, 10000)
        employee.performance = 20
        manager.happiness = 60
        employee.interact(manager)
        self.assertEqual(employee.savings, 10000)

    def test_perm_employee_5(self):
        """Test interaction with a non-manager employee does not give bonus."""
        manager = Manager("M", None, 10000, 20000)
        employee = PermanentEmployee("A", manager, 200, 10000)
        other_employee = PermanentEmployee("B", manager, 4000, 8000)
        employee.interact(other_employee)
        self.assertEqual(employee.savings, 10000)

    def test_perm_employee_6(self):
        """Test work does not modify savings."""
        e = PermanentEmployee("A", None, 200, 10000)
        e.work()
        self.assertEqual(e.savings, 10000)

    def test_perm_employee_7(self):
        """Test work does not modify salary."""
        e = PermanentEmployee("A", None, 200, 10000)
        e.work()
        self.assertEqual(e.salary, 200)

    def test_perm_employee_8(self):
        """Test permanent employee does not get bonus if manager happiness is low."""
        manager = Manager("M", None, 10000, 20000)
        employee = PermanentEmployee("A", manager, 200, 10000)
        employee.performance = 30
        manager.happiness = 40
        employee.interact(manager)
        manager.interact(employee)
        self.assertEqual(employee.savings, 10000)

    def test_perm_employee_9(self):
        """Test permanent employee does not become unemployed after interaction."""
        manager = Manager("M", None, 10000, 20000)
        employee = PermanentEmployee("A", manager, 200, 10000)
        manager.happiness = 40
        employee.performance = 20
        employee.interact(manager)
        manager.interact(employee)
        self.assertTrue(employee.is_employed)

    def test_perm_employee_10(self):
        """Test string representation of a perm employee."""
        e = PermanentEmployee("A", None, 300, 1000)
        self.assertEqual(
            str(e),
            "A\n\tSalary: $300\n\tSavings: $1000\n\tHappiness: 50%\n\tPerformance: 75%",
        )

    def test_perm_employee_11(self):
        """Test permanent employee performance does not exceed 100."""
        e = PermanentEmployee("A", None, 200, 10000)
        e.performance = 99
        random.seed(5)
        e.work()
        self.assertEqual(e.performance, 100)

    def test_perm_employee_12(self):
        """Test permanent employee performance remains non-negative at boundary."""
        e = PermanentEmployee("A", None, 200, 10000)
        e.performance = 1
        random.seed(6)
        e.work()
        self.assertGreaterEqual(e.performance, 0)

    def test_perm_employee_13(self):
        """Test permanent employee happiness decreases after daily expense."""
        e = PermanentEmployee("A", None, 200, 10000)
        e.daily_expense()
        self.assertEqual(e.happiness, 49)

    def test_perm_employee_14(self):
        """Test permanent employee savings decreases after daily expense."""
        e = PermanentEmployee("A", None, 200, 10000)
        e.daily_expense()
        self.assertEqual(e.savings, 9940)

    def test_perm_employee_15(self):
        """Test permanent employee does not lose employment with low performance."""
        manager = Manager("M", None, 10000, 20000)
        employee = PermanentEmployee("A", manager, 200, 10000)
        employee.performance = 0
        employee.interact(manager)
        manager.interact(employee)
        self.assertTrue(employee.is_employed)


def main():
    """Main function to run tests based on command-line arguments."""
    test_cases = {
        "employee": TestEmployee,
        "manager": TestManager,
        "temporary": TestTemporaryEmployee,
        "permanent": TestPermanentEmployee,
    }

    usage_string = (
        "Usage: python test_employees.py [test_type] [test_number]\n"
        "Examples:\n"
        "    python test_employees.py manager 1\n"
        "    python test_employees.py temporary 5\n"
        "Valid options for [test_type]: " + ", ".join(test_cases.keys()) + "\n"
        "Test cases range from 1 for employee, 1-29 for manager, 1-15 for temporary and permanent."
    )

    if len(sys.argv) > 3:
        print(usage_string)
        return
    if len(sys.argv) == 1:
        unittest.main()
        return
    sys.argv = sys.argv[1:]
    test_name = sys.argv[0]
    if test_name not in test_cases:
        print(
            f"Invalid test name: {test_name}. Valid options are: {', '.join(test_cases.keys())}"
        )
        return
    if len(sys.argv) == 1:
        # Extract test case based on the first command-line argument
        suite = unittest.TestLoader().loadTestsFromTestCase(test_cases[test_name])
    else:
        test_num = sys.argv[1]
        loader = unittest.TestLoader()

        # Load all tests from the test case class
        all_tests = loader.loadTestsFromTestCase(test_cases[test_name])
        suite = unittest.TestSuite()
        for test in all_tests:
            if test.id().split(".")[-1].split("_")[-1] == test_num:
                suite.addTest(test)
        if not suite.countTestCases():
            print(usage_string)
            return
    unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
    main()
