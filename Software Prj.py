student-task-manager/
│
├── src/
│   ├── __init__.py
│   ├── task.py
│   └── task_manager.py
│
├── tests/
│   ├── __init__.py
│   └── test_task_manager.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
python -m venv .venv
.venv\Scripts\activate
pip install pytest
pip freeze > requirements.txt
from dataclasses import dataclass


@dataclass
class Task:
    title: str
    completed: bool = False
    from src.task import Task


class TaskManager:
    def __init__(self) -> None:
        self.tasks: list[Task] = []

    def add_task(self, title: str) -> Task:
        if not title.strip():
            raise ValueError("Task title cannot be empty.")

        task = Task(title=title)
        self.tasks.append(task)

        return task

    def get_tasks(self) -> list[Task]:
        return self.tasks

    def complete_task(self, index: int) -> None:
        if index < 0 or index >= len(self.tasks):
            raise IndexError("Task does not exist.")

        self.tasks[index].completed = True

    def delete_task(self, index: int) -> None:
        if index < 0 or index >= len(self.tasks):
            raise IndexError("Task does not exist.")

        self.tasks.pop(index)
        from src.task_manager import TaskManager


def display_tasks(manager: TaskManager) -> None:
    tasks = manager.get_tasks()

    if not tasks:
        print("\nNo tasks available.")
        return

    print("\n--- YOUR TASKS ---")

    for index, task in enumerate(tasks):
        status = "✓" if task.completed else " "
        print(f"{index + 1}. [{status}] {task.title}")


def main() -> None:
    manager = TaskManager()

    while True:
        print("\n=== STUDENT TASK MANAGER ===")
        print("1. Add task")
        print("2. View tasks")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Exit")

        choice = input("Choose an option: ")

        try:
            if choice == "1":
                title = input("Enter task title: ")
                manager.add_task(title)
                print("Task added successfully!")

            elif choice == "2":
                display_tasks(manager)

            elif choice == "3":
                display_tasks(manager)
                index = int(input("Enter task number: ")) - 1
                manager.complete_task(index)
                print("Task completed!")

            elif choice == "4":
                display_tasks(manager)
                index = int(input("Enter task number: ")) - 1
                manager.delete_task(index)
                print("Task deleted!")

            elif choice == "5":
                print("Goodbye!")
                break

            else:
                print("Invalid option. Please try again.")

        except ValueError as error:
            print(f"Error: {error}")

        except IndexError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
    python main.py
    import pytest

from src.task_manager import TaskManager


@pytest.fixture
def manager() -> TaskManager:
    return TaskManager()


def test_add_task(manager: TaskManager) -> None:
    task = manager.add_task("Study Python")

    assert task.title == "Study Python"
    assert task.completed is False
    assert len(manager.get_tasks()) == 1


def test_empty_task_raises_error(manager: TaskManager) -> None:
    with pytest.raises(ValueError):
        manager.add_task("")


def test_complete_task(manager: TaskManager) -> None:
    manager.add_task("Learn pytest")

    manager.complete_task(0)

    assert manager.get_tasks()[0].completed is True


def test_delete_task(manager: TaskManager) -> None:
    manager.add_task("Finish assignment")

    manager.delete_task(0)

    assert len(manager.get_tasks()) == 0


def test_invalid_task_index(manager: TaskManager) -> None:
    with pytest.raises(IndexError):
        manager.complete_task(5)
        pytest
        5 passed
        def get_completed_tasks(self) -> list[Task]:
    return [task for task in self.tasks if task.completed]
.venv/
__pycache__/
.pytest_cache/
*.pyc
git init
git add .
git commit -m "Initial project structure"
git switch -c feature/add-tasks
git add .
git commit -m "Add task creation feature"
git push -u origin feature/add-tasks
main
 │
 ├── feature/add-tasks
 ├── feature/complete-tasks
 ├── feature/delete-tasks
 └── feature/task-tests
Choose an option: Traceback (most recent call last):
  File "c:\Users\Joel-LeviOmotayo\# Student Management System.py", line 94, in <module>
    choice = input("\nChoose an option: ")
KeyboardInterrupt
PS C:\Users\Joel-LeviOmotayo\AppData\Local\Programs\Microsoft VS Code> & C:\Users\Joel-LeviOmotayo\AppData\Local\Python\pythoncore-3.14-64\python.exe c:/Users/Joel-LeviOmotayo/app.py
Traceback (most recent call last):
  File "c:\Users\Joel-LeviOmotayo\app.py", line 1, in <module>
    from flask import Flask, render_template, request, redirect, url_for, session
ModuleNotFoundError: No module named 'flask'
PS C:\Users\Joel-LeviOmotayo\AppData\Local\Programs\Microsoft VS Code> & C:\Users\Joel-LeviOmotayo\AppData\Local\Python\pythoncore-3.14-64\python.exe c:/Users/Joel-LeviOmotayo/app.py
Traceback (most recent call last):
  File "c:\Users\Joel-LeviOmotayo\app.py", line 1, in <module>
    from flask import Flask, render_template, request, redirect, url_for, session
ModuleNotFoundError: No module named 'flask'
PS C:\Users\Joel-LeviOmotayo\AppData\Local\Programs\Microsoft VS Code> & C:\Users\Joel-LeviOmotayo\AppData\Local\Python\pythoncore-3.14-64\python.exe "c:/Users/Joel-LeviOmotayo/Software Prj.py"
  File "c:\Users\Joel-LeviOmotayo\Software Prj.py", line 2
    │
    ^
SyntaxError: invalid character '│' (U+2502)
PS C:\Users\Joel-LeviOmotayo\AppData\Local\Programs\Microsoft VS Code> & C:\Users\Joel-LeviOmotayo\AppData\Local\Python\pythoncore-3.14-64\python.exe "c:/Users/Joel-LeviOmotayo/Software Prj.py"
  File "c:\Users\Joel-LeviOmotayo\Software Prj.py", line 2
    │
    ^
SyntaxError: invalid character '│' (U+2502)
PS C:\Users\Joel-LeviOmotayo\AppData\Local\Programs\Microsoft VS Code> 
PS C:\Users\Joel-LeviOmotayo\AppData\Local\Programs\Microsoft VS Code> git statugit init.venv/
>> __pycache__/
>> .pytest_cache/
>> *.pycgit statusgit add .git commit -m "Initial commit - Student Task Manager"https://github.com/YOUR-USERNAME/student-task-manager.gitgit remote add origin YOUR-REPOSITORY-URLgit remote add origin https://github.com/YourUsername/student-task-manager.gitgit branch -M maingit push -u origin maingit init
>> git add .
>> git commit -m "Initial commit - Student Task Manager"
>> git branch -M main
>> git remote add origin YOUR-REPOSITORY-URL
>> git push -u origin maingit add .
>> git commit -m "Describe what you changed"
>> git pushgit add .
>> git commit -m "Add completed task filtering"
>> git push
https://github.com/Joel-Leviom/AI-and-ML-Training.git