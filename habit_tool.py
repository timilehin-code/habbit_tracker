from datetime import datetime, date
import json
import os
import pandas as pd
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt, FloatPrompt
from rich import print

console = Console()
prompt = Prompt()


class ProgressBar:
    @staticmethod
    def generate(percentage: float, width: int = 10) -> str:
        filled = int(width * percentage / 100)
        bar = "█" * filled + "▒" * (width - filled)
        return f"[{bar}] {percentage}%"


class Habit:
    def __init__(
        self,
        habit_name: str,
        start_date: datetime,
        goal: float,
        cost_per_day: float,
        minutes_wasted: float,
        status: str = "Ongoing",
        streak: int = 0,
        completion_dates: list = None,
    ):
        self.habit_name = habit_name
        self.start_date = start_date
        self.goal = goal
        self.cost_per_day = cost_per_day
        self.minutes_wasted = minutes_wasted
        self.status = status
        self.streak = streak
        self.completion_dates = completion_dates if completion_dates is not None else []
        self.time_since = ""
        self.days_remaining = 0
        self.minutes_saved = 0
        self.percentage_completed = ""
        self.money_saved = ""
        self.progress_bar = ""
        self.recalculate()

    def recalculate(self):
        time_elapsed = (datetime.now() - self.start_date).total_seconds()
        hours = round(time_elapsed / 60 / 60, 1)
        days = round(hours / 24, 2)
        self.minutes_saved = round(days * self.minutes_wasted, 1)
        self.days_remaining = round(self.goal - days)
        self.percentage_completed = f"{min(round(days / self.goal * 100, 2), 100)}%"
        self.money_saved = f"₦{self.cost_per_day * days:,}"
        self.progress_bar = ProgressBar.generate(
            min(round(days / self.goal * 100, 2), 100)
        )
        if hours > 48:
            self.time_since = f"{days} days"
        else:
            self.time_since = f"{hours} hours"

    def to_dict(self):
        return {
            "habit_name": self.habit_name,
            "start_date": self.start_date.isoformat(),
            "goal": self.goal,
            "cost_per_day": self.cost_per_day,
            "minutes_wasted": self.minutes_wasted,
            "status": self.status,
            "streak": self.streak,
            "completion_dates": self.completion_dates,
            "time_since": self.time_since,
            "days_remaining": self.days_remaining,
            "minutes_saved": self.minutes_saved,
            "% completed": self.percentage_completed,
            "money_saved": self.money_saved,
            "progress_bar": self.progress_bar,
        }


class FileHandler:
    @staticmethod
    def load_habits(filename: str = "habits.json") -> list:
        habits = []
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    loaded_habits = json.load(f)
                for habit_data in loaded_habits:
                    start_date = datetime.fromisoformat(habit_data["start_date"])
                    habit = Habit(
                        habit_data["habit_name"],
                        start_date,
                        habit_data.get("goal", 30),
                        habit_data.get("cost_per_day", 0),
                        habit_data.get("minutes_wasted", 0),
                        habit_data.get("status", "Ongoing"),
                        habit_data.get("streak", 0),
                        habit_data.get("completion_dates", []),
                    )
                    habits.append(habit)
                print("[blue]Loaded existing habits from 'habits.json'.[/blue]")
            except Exception as e:
                print(
                    f"[red]Error loading habits: {e}. Starting with an empty list.[/red]"
                )
        return habits

    @staticmethod
    def save_habits(habits: list, filename: str = "habits.json"):
        try:
            with open(filename, "w") as f:
                json.dump([h.to_dict() for h in habits], f, indent=4)
            print("[green]Habits saved to 'habits.json'.[/green]")
        except Exception as e:
            print(f"[red]Error saving habits to JSON: {e}[/red]")

    @staticmethod
    def save_csv(habits: list):
        try:
            file_name = f"habits{round(datetime.now().timestamp())}.csv"
            df = pd.DataFrame([h.to_dict() for h in habits])
            df.to_csv(file_name, index=False)
            print(f"[green]Habits saved as {file_name}.[/green]")
        except Exception as e:
            print(f"[red]Error saving habits to CSV: {e}[/red]")

    @staticmethod
    def archive_habit(habit: "Habit", habits: list):
        try:
            archive_file = "archive.json"
            archive_data = []
            if os.path.exists(archive_file):
                with open(archive_file, "r") as f:
                    archive_data = json.load(f)
            archive_data.append(habit.to_dict())
            with open(archive_file, "w") as f:
                json.dump(archive_data, f, indent=4)
            habits.remove(habit)
            print(f"[green]Archived '{habit.habit_name}' to '{archive_file}'.[/green]")
        except Exception as e:
            print(f"[red]Error archiving habit: {e}[/red]")


class HabitTracker:
    def __init__(self):
        self.habits = FileHandler.load_habits()

    def add_habit(self):
        try:
            habit_name = (
                prompt.ask(
                    "[bold cyan]Enter the habit you want to break (e.g., smoking)[/bold cyan]"
                )
                .strip()
                .title()
            )
            if not habit_name:
                raise ValueError("Habit cannot be empty")
            start_date_input = prompt.ask(
                "[bold cyan]Input the day and time you started (YYYY-MM-DD HH:MM, e.g., 1980-04-01 16:15)[/bold cyan]"
            ).strip()
            start_date = datetime.strptime(start_date_input, "%Y-%m-%d %H:%M")
            if start_date > datetime.now():
                raise ValueError("[yellow]Date cannot be in the future[/yellow]")
            goal = FloatPrompt.ask(
                "[bold cyan]Input the days you want to spend breaking the habit[/bold cyan]"
            )
            if goal <= 0:
                raise ValueError("Goal must be a positive number")
            cost_per_day = FloatPrompt.ask(
                "[bold cyan]Enter the cost per day (e.g., 40 for ₦40)[/bold cyan]"
            )
            if cost_per_day < 0:
                raise ValueError("Cost cannot be negative")
            minutes_wasted = FloatPrompt.ask(
                "[bold cyan]Enter minutes wasted per day (e.g., 20)[/bold cyan]"
            )
            if minutes_wasted < 0:
                raise ValueError("Minutes wasted cannot be negative")
            habit = Habit(habit_name, start_date, goal, cost_per_day, minutes_wasted)
            self.habits.append(habit)
            FileHandler.save_habits(self.habits)
        except ValueError as e:
            print(f"[red]Error: {e}[/red]")
        except Exception as e:
            print(f"[red]Unexpected error: {e}[/red]")

    def update_streaks(self):
        today = date.today()
        for habit in self.habits:
            if str(today) not in habit.completion_dates:
                yesterday = (datetime.now() - pd.Timedelta(days=1)).date()
                if str(yesterday) in habit.completion_dates:
                    completed = (
                        prompt.ask(
                            f"[bold cyan]Did you complete '{habit.habit_name}' today? (y/n)[/bold cyan]"
                        )
                        .strip()
                        .lower()
                        == "y"
                    )
                    if completed:
                        habit.completion_dates.append(str(today))
                        habit.streak += 1
                    else:
                        habit.streak = 0
                else:
                    habit.streak = 0
            habit.recalculate()

    def update_status(self, index: int):
        try:
            habit = self.habits[index]
            print(f"\nUpdating status for habit: {habit.habit_name}")
            status = (
                input("Enter status ('Ongoing', 'Defaulted', or 'Completed'): ")
                .strip()
                .title()
            )
            if status not in ["Ongoing", "Defaulted", "Completed"]:
                raise ValueError(
                    "[yellow]Status must be 'Ongoing', 'Defaulted', or 'Completed'.[/yellow]"
                )
            if status == "Completed":
                days_elapsed = (datetime.now() - habit.start_date).total_seconds() / (
                    60 * 60 * 24
                )
                if days_elapsed < habit.goal - 0.01:
                    raise ValueError(
                        f"[yellow]Warning: your {habit.habit_name} Habit is only {habit.percentage_completed} complete. ({days_elapsed:.2f} days is less than goal {habit.goal}).[/yellow]"
                    )
                archive_option = (
                    prompt.ask(
                        "[bold cyan]Do you want to archive this habit? ('y' for yes, 'n' for no)[/bold cyan]"
                    )
                    .strip()
                    .upper()
                )
                if archive_option == "Y":
                    FileHandler.archive_habit(habit, self.habits)
                    FileHandler.save_habits(self.habits)
                    return
            habit.status = status
            habit.recalculate()
            FileHandler.save_habits(self.habits)
        except ValueError as e:
            print(f"[red]Error: {e}[/red]")
        except Exception as e:
            print(f"[red]Unexpected error: {e}[/red]")

    def edit_habit(self, index: int):
        try:
            habit = self.habits[index]
            console.print(f"\nEditing habit: [cyan]{habit.habit_name}[/cyan]")
            habit_name = (
                prompt.ask(
                    f"[bold cyan]Enter new habit name (current: {habit.habit_name}, press Enter to keep):[/bold cyan]"
                )
                .strip()
                .title()
                or habit.habit_name
            )
            if not habit_name:
                raise ValueError("[yellow]Habit name cannot be empty.[/yellow]")
            start_date_input = prompt.ask(
                f"[bold cyan]Enter new start date (YYYY-MM-DD HH:MM, current: {habit.start_date}, press Enter to keep):[/bold cyan]"
            ).strip()
            start_date = (
                datetime.strptime(start_date_input, "%Y-%m-%d %H:%M")
                if start_date_input
                else habit.start_date
            )
            if start_date > datetime.now():
                raise ValueError("[yellow]Date cannot be in the future.[/yellow]")
            goal = FloatPrompt.ask(
                f"[bold cyan]Enter new goal in days (current: {habit.goal}, press Enter to keep):[/bold cyan]",
                default=habit.goal,
            )
            if goal <= 0:
                raise ValueError("[yellow]Goal must be a positive number.[/yellow]")
            cost_per_day = FloatPrompt.ask(
                f"[bold cyan]Enter new cost per day (current: {habit.cost_per_day}, press Enter to keep):[/bold cyan]",
                default=habit.cost_per_day,
            )
            if cost_per_day < 0:
                raise ValueError("[yellow]Cost cannot be negative.[/yellow]")
            minutes_wasted = FloatPrompt.ask(
                f"[bold cyan]Enter new minutes wasted per day (current: {habit.minutes_wasted}, press Enter to keep):[/bold cyan]",
                default=habit.minutes_wasted,
            )
            if minutes_wasted < 0:
                raise ValueError("[yellow]Minutes wasted cannot be negative.[/yellow]")
            for i, h in enumerate(self.habits):
                if (
                    i != index
                    and h.habit_name == habit_name
                    and h.start_date.isoformat() == start_date.isoformat()
                ):
                    raise ValueError(
                        f"[yellow]Habit '{habit_name}' with start date {start_date} already exists.[/yellow]"
                    )
            habit.habit_name = habit_name
            habit.start_date = start_date
            habit.goal = goal
            habit.cost_per_day = cost_per_day
            habit.minutes_wasted = minutes_wasted
            habit.recalculate()
            FileHandler.save_habits(self.habits)
            print(f"[green]Updated '{habit_name}' successfully.[/green]")
        except ValueError as e:
            print(f"[red]Error: {e}[/red]")
        except Exception as e:
            print(f"[red]Unexpected error: {e}[/red]")

    def delete_habit(self, index: int):
        try:
            habit = self.habits[index]
            confirm = (
                prompt.ask(
                    f"[bold cyan]Confirm deletion of '{habit.habit_name}'? ('y' for yes, 'n' for no)[/bold cyan]"
                )
                .strip()
                .upper()
            )
            if confirm == "Y":
                self.habits.remove(habit)
                FileHandler.save_habits(self.habits)
                print(f"[green]Deleted '{habit.habit_name}' from habits.[/green]")
            elif confirm != "N":
                raise ValueError("[red]Invalid input: Please enter 'y' or 'n'.[/red]")
        except ValueError as e:
            print(f"[red]Error: {e}[/red]")
        except Exception as e:
            print(f"[red]Unexpected error: {e}[/red]")

    def display_habits(self, summary: bool = True):
        if not self.habits:
            print("[cyan]No habits entered.[/cyan]")
            return
        table = Table(
            show_header=True,
            title="Current Habits" if summary else "Your Habit-Breaking Progress",
            header_style="bold magenta",
        )
        table.add_column("S/N", style="red")
        table.add_column("Habit", style="cyan")
        if not summary:
            table.add_column("Start Date", style="cyan")
            table.add_column("Time Since", justify="right")
            table.add_column("Days Remaining", justify="right")
            table.add_column("Minutes Saved", justify="right")
            table.add_column("% Completed", justify="right")
            table.add_column("Money Saved", justify="right")
            table.add_column("Progress", justify="left", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Streak", style="blue")
        for i, habit in enumerate(self.habits, 1):
            if summary:
                table.add_row(
                    str(i), habit.habit_name, habit.status, f"{habit.streak} days"
                )
            else:
                table.add_row(
                    str(i),
                    habit.habit_name,
                    habit.start_date.isoformat(),
                    habit.time_since,
                    str(habit.days_remaining),
                    str(habit.minutes_saved),
                    habit.percentage_completed,
                    habit.money_saved,
                    habit.progress_bar,
                    habit.status,
                    f"{habit.streak} days",
                )
        console.print(table)


def main():
    tracker = HabitTracker()
    while True:
        tracker.update_streaks()
        tracker.display_habits(summary=True)
        if not tracker.habits:
            action = (
                prompt.ask(
                    "[blue]\nEnter 'add' to add a new habit or 'done' to finish: [/blue]"
                )
                .strip()
                .lower()
            )
        else:
            action = (
                prompt.ask(
                    "[blue]\nEnter habit number to update status, 'add' to add a new habit, 'done' to finish, 'edit' to edit a habit, or 'delete' to delete a habit: [/blue]"
                )
                .strip()
                .lower()
            )
        if action == "done":
            if tracker.habits:
                save_option = (
                    prompt.ask(
                        "[cyan bold]Do you want to save file as a csv file? ('y' for yes, 'n' for no)[/cyan bold]"
                    )
                    .strip()
                    .upper()
                )
                if save_option == "Y":
                    FileHandler.save_csv(tracker.habits)
                    print("[green]File saved successfully![/green]")
                elif save_option == "N":
                    print("[yellow]File did not save as csv[/yellow]")
                else:
                    print("[red]Invalid input[/red]")
            break
        elif action == "add":
            tracker.add_habit()
        elif action == "edit" and tracker.habits:
            try:
                index = (
                    int(
                        prompt.ask(
                            "[bold cyan]Enter habit number to edit:[/bold cyan]"
                        ).strip()
                    )
                    - 1
                )
                if index < 0 or index >= len(tracker.habits):
                    raise ValueError("[yellow]Invalid habit number.[/yellow]")
                tracker.edit_habit(index)
            except ValueError as e:
                print(f"[red]Error: {e}[/red]")
        elif action == "delete" and tracker.habits:
            try:
                index = (
                    int(
                        prompt.ask(
                            "[bold cyan]Enter habit number to delete:[/bold cyan]"
                        ).strip()
                    )
                    - 1
                )
                if index < 0 or index >= len(tracker.habits):
                    raise ValueError("[yellow]Invalid habit number.[/yellow]")
                tracker.delete_habit(index)
            except ValueError as e:
                print(f"[red]Error: {e}[/red]")
        elif tracker.habits:
            try:
                index = int(action) - 1
                if index < 0 or index >= len(tracker.habits):
                    raise ValueError("[yellow]Invalid habit number.[/yellow]")
                tracker.update_status(index)
            except ValueError as e:
                print(f"[red]Error: {e}[/red]")
        tracker.display_habits(summary=False)


if __name__ == "__main__":
    main()
