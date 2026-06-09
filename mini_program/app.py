from datetime import date, timedelta
from typing import List, Dict


class WorkingDay:
    def __init__(self, is_working: bool, reason: str,  pattern_day: int = None):
        self.is_working_day = is_working
        self.reason = reason
        self.pattern_day_number = pattern_day

    def __repr__(self):
        return f"WorkingDay(working={self.is_working_day}, reason='{self.reason}')"


class DutyPatternStrategy:
    def __init__(self, pattern: List[str], start_date: date):
        self.pattern = pattern
        self.start_date = start_date

    def calculate(self, target_date: date) -> WorkingDay:
        days_diff = (target_date - self.start_date).days
        pattern_idx = days_diff % len(self.pattern)
        status = self.pattern[pattern_idx]
        day_num = pattern_idx + 1
        return WorkingDay(
            is_working=(status == "ON"),
            reason=f"Duty pattern day {day_num} is {status}",
            pattern_day=day_num
        )


class Employee:
    def __init__(self, id: str, name: str, strategy):
        self.id = id
        self.name = name
        self.strategy = strategy

    def working_day(self, target_date: date) -> WorkingDay:
        result = self.strategy.calculate(target_date)

        status_word = "working" if result.is_working_day else "off"
        new_reason = f"{target_date} for {self.name} is {status_word}"
        result.reason = new_reason + f" - {result.reason}"
        return result


class EmployeeFactory:
    @staticmethod
    def create_nurse_with_duty_roster(id: str, name: str, start_date: date) -> Employee:
        pattern = ["ON", "ON", "OFF", "ON", "OFF"]
        strategy = DutyPatternStrategy(pattern, start_date)
        return Employee(id, name, strategy)

def attendance_checking(check_date: date, employees: List[Employee]) -> None:
    for emp in employees:
        result = emp.working_day(check_date)
        if result.is_working_day:
            print(f"[ATTEND] {emp.name} ({emp.id}) has to work. Reason: {result.reason}")
        else:
            print(f"[OFF]   {emp.name} ({emp.id}) is duty off. Reason: {result.reason}")


if __name__ == "__main__":
    employees = [
        EmployeeFactory.create_nurse_with_duty_roster("E001", "David", date(2026, 6, 3)),
        EmployeeFactory.create_nurse_with_duty_roster("E002", "Emily", date(2026, 6, 1)),
        EmployeeFactory.create_nurse_with_duty_roster("E003", "Ivy", date(2026, 6, 7)),

    ]
    check_date = date(2026, 6, 8) 
    attendance_checking(check_date, employees)
