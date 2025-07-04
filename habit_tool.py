from datetime import datetime, date
import json
import os
import pandas as pd
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
from rich import print

prompt = Prompt()
console = Console()


# graphical representation of the progress made in trying to break the habit
def progress_bar(percentage, width=10):
    filled = int(width * percentage / 100)
    bar = "█" * filled + "▒" * (width - filled)
    return f"[{bar}] {percentage}%"


def recalculating_habits(
    habit_name, start_date, goal, cost_per_day, minutes_wasted, status="ongoing", streak=0, completion_dates=None
):
    """calculating habits for each time habits a new habit is add or the existing habit is viewed"""
    # total time elapsed in seconds
    time_elapsed = (datetime.now() - start_date).total_seconds()
    # converting the timestamp to both hours and days
    hours = round(time_elapsed / 60 / 60, 1)
    days = round(hours / 24, 2)
    # extra details like money saved
    money_saved = cost_per_day * days
    minutes_saved = round(days * minutes_wasted, 1)
    days_to_go = round(goal - days)
    total_percentage_completed = round(days / goal * 100, 2)

    """change hours to days if it is more than 48 hours"""
    if hours > 48:
        hours = str(days) + "days"
    else:
        hours = str(hours) + "hours"
    return {
        "habit_name": habit_name,
        "start_date": start_date.isoformat(),
        "time_since": hours,
        "days_remaining": days_to_go,
        "minutes_saved": minutes_saved,
        "% completed": f"{total_percentage_completed}%",
        "money_saved": f"₦{money_saved:,}",
        "progress_bar": progress_bar(total_percentage_completed),
        "status": status,
        "goal": goal,
        "cost_per_day": cost_per_day,
        "minutes_wasted": minutes_wasted,
         "streak": streak,
        "completion_dates": completion_dates if completion_dates is not None else []
    }


def save_csv(habits):
    """Saving file to csv using pandas"""
    try:
        file_name = f"habits{round(datetime.now().timestamp())}.csv"
        df = pd.DataFrame(habits)
        df.to_csv(file_name, index=False)
        print(f"[green]Habits saved as {file_name}.[/green]")
    except Exception as e:
        print(f"[red]Error saving habits to CSV: {e}[/red]")


def archive_habits(habit, habits):
    """Archive the completed habits"""
    try:
        archive_file = "archive.json"
        archive_data = []
        if os.path.exists(archive_file):
            with open(archive_file, "r") as archive:
                archive_data = json.load(archive)
        archive_data.append(habit)
        with open(archive_file, "w") as archive:
            json.dump(archive_data, archive, indent=4)
        habits.remove(habit)
        print(f"[green]Archived '{habit['habit_name']}' to '{archive_file}'.[/green]")
    except Exception as e:
        print(f"[red]Error archiving habit: {e}[/red]")


def delete_habits(habit, habits):
    """Removing habit from the list of habits"""
    try:
        habits.remove(habit)
        print(f"[green]Deleted '{habit['habit_name']}' from habits.[/green]")
    except Exception as e:
        print(f"[red]Error deleting habit: {e}[/red]")


def edit_habit(habit, habits, index):
    """Edit habit details and update the habits list."""
    try:
        console.print(f"\nEditing habit: [cyan]{habit['habit_name']}[/cyan]")
        # Prompt for new values, allowing empty input to keep existing values
        habit_name = (
            prompt.ask(
                f"[bold cyan]Enter new habit name (current: {habit['habit_name']}, press Enter to keep):[/bold cyan]"
            )
            .strip()
            .title()
            or habit["habit_name"]
        )
        if not habit_name:
            raise ValueError("[yellow]Habit name cannot be empty.[/yellow]")

        start_date_input = prompt.ask(
            f"[bold cyan]Enter new start date (YYYY-MM-DD HH:MM, current: {habit['start_date']}, press Enter to keep):[/bold cyan]"
        ).strip()
        start_date = (
            datetime.strptime(start_date_input, "%Y-%m-%d %H:%M")
            if start_date_input
            else datetime.fromisoformat(habit["start_date"])
        )
        if start_date > datetime.now():
            raise ValueError("[yellow]Date cannot be in the future.[/yellow]")

        goal_input = prompt.ask(
            f"[bold cyan]Enter new goal in days (current: {habit['goal']}, press Enter to keep):[/bold cyan]"
        ).strip()
        goal = float(goal_input) if goal_input else habit["goal"]
        if goal <= 0:
            raise ValueError("[yellow]Goal must be a positive number.[/yellow]")

        cost_input = prompt.ask(
            f"[bold cyan]Enter new cost per day (current: {habit['cost_per_day']}, press Enter to keep):[/bold cyan]"
        ).strip()
        cost_per_day = float(cost_input) if cost_input else habit["cost_per_day"]
        if cost_per_day < 0:
            raise ValueError("[yellow]Cost cannot be negative.[/yellow]")

        minutes_input = prompt.ask(
            f"[bold cyan]Enter new minutes wasted per day (current: {habit['minutes_wasted']}, press Enter to keep):[/bold cyan]"
        ).strip()
        minutes_wasted = (
            float(minutes_input) if minutes_input else habit["minutes_wasted"]
        )
        if minutes_wasted < 0:
            raise ValueError("[yellow]Minutes wasted cannot be negative.[/yellow]")

        for i, h in enumerate(habits):
            if (
                i != index
                and h["habit_name"] == habit_name
                and h["start_date"] == start_date.isoformat()
            ):
                raise ValueError(
                    f"[yellow]Habit '{habit_name}' with start date {start_date} already exists.[/yellow]"
                )

        updated_habit = recalculating_habits(
            habit_name, start_date, goal, cost_per_day, minutes_wasted, habit["status"]
        )
        habits[index] = updated_habit
        print(f"[green]Updated '{habit_name}' successfully.[/green]")
    except ValueError as e:
        print(f"[red]Error: {e}[/red]")
        raise
    except Exception as e:
        print(f"[red]Unexpected error: {e}[/red]")
        raise


def break_habits():
    # list to store all habits
    habits = []

    """Load existing habits from habits.json if it exists"""
    if os.path.exists("habits.json"):
        try:
            with open("habits.json", "r") as json_file:
                loaded_habits = json.load(json_file)
            for habit in loaded_habits:
                start_date = datetime.fromisoformat(habit["start_date"])
                updated_habit = recalculating_habits(
                    habit["habit_name"],
                    start_date,
                    habit.get("goal", 30),  # Default goal if missing
                    habit.get("cost_per_day", 0),  # Default cost if missing
                    habit.get("minutes_wasted", 0),  # Default minutes if missing
                    habit.get("status", "Ongoing"),  # Retain status
                    habit.get("streak", 0),
                    habit.get("completion_dates", [])
                )
                habits.append(updated_habit)
            print("[blue]Loaded existing habits from 'habits.json'.[/blue]")
        except Exception as e:
            print(
                f"[red]Error loading habits from file: {e}. Starting with an empty list.[/red]"
            )
    today = date.today()
    for habit in habits:
        if str(today) not in habit["completion_dates"]:
            yesterday = (datetime.now() - pd.Timedelta(days=1)).date()
            if str(yesterday) in habit["completion_dates"]:
                completed = (
                    prompt.ask(
                        f"[bold cyan]Did you complete '{habit['habit_name']}' today? (y/n)[/bold cyan]"
                    )
                    .strip()
                    .lower()
                    == "y"
                )
                if completed:
                    habit["completion_dates"].append(str(today))
                    habit["streak"] += 1
                else:
                    habit["streak"] = 0
            else:
                habit["streak"] = 0
        start_date = datetime.fromisoformat(habit["start_date"])
        habit.update(
            recalculating_habits(
                habit["habit_name"],
                start_date,
                habit["goal"],
                habit["cost_per_day"],
                habit["minutes_wasted"],
                habit["status"],
                habit["streak"],
                habit["completion_dates"],
            )
        )
    # getting the  user input using try except
    while True:
        try:
            habit_name = (
                prompt.ask(
                    "[bold cyan]enter the habit you want to break (e.g, smoking) or done to finish[/bold cyan]"
                )
                .strip()
                .title()
            )
            # check if habit name is empty
            if not habit_name:
                raise ValueError("habit cannot be empty")
            if habit_name.lower() == "done":
                break
            start_date_input = prompt.ask(
                "[bold cyan]input the day and time you started format(YYYY-MM-DD HH:MM, e.g., 1980-04-01 16:15) [/bold cyan]"
            ).strip()
            # converting the  date to a defined format
            start_date = datetime.strptime(start_date_input, "%Y-%m-%d %H:%M")
            # check if date is greater than todays date
            if start_date > datetime.now():
                raise ValueError(
                    "[yellow]date cannot be more than today's date[/yellow]"
                )
            # day you want to use in trying to break the habit
            goal = int(
                prompt.ask(
                    "[bold cyan]input the days you want to spend breaking the habit[/bold cyan]"
                ).strip()
            )
            # check if  days is less than zero
            if goal < 0:
                raise ValueError("must be a positive number!")
            # check if user input is a string or a float
            elif isinstance(goal, (str, float)):
                raise ValueError("goal must be a number!")

            cost_per_day = float(
                prompt.ask(
                    "[bold cyan]enter the cost per day for the e.g., 40 for ₦40[bold cyan]"
                ).strip()
            )
            # check if  cost per day is less than 0
            if cost_per_day < 0:
                raise ValueError("cost cannot be empty")
            minutes_wasted = float(
                prompt.ask(
                    "[bold cyan]Enter minutes wasted per day (e.g., 20)[bold cyan]"
                ).strip()
            )
            # check if  minutes wasted is less than 0
            if minutes_wasted < 0:
                raise ValueError("Minutes wasted cannot be negative.")

            # Append new habit
            habits.append(
                recalculating_habits(
                    habit_name, start_date, goal, cost_per_day, minutes_wasted
                )
            )
            # Save habits to JSON and CSV file after adding a new habit
            try:
                # save to json
                with open("habits.json", "w") as json_file:
                    json.dump(habits, json_file, indent=4)

            except Exception as e:
                print(f"Error saving habits to file: {e}")
        except ValueError as e:
            if "cannot be" in str(e) or "must be" in str(e):
                print(f"Error: {e}")
            else:
                print(
                    "Error: Invalid input. Ensure date is in YYYY-MM-DD HH:MM format and numbers are valid."
                )
                print("Please try again or enter 'done' to finish.")
                continue
        except Exception as e:
            print(f"Unexpected error: {e}")
            print("Please try again or enter 'done' to finish.")
            continue

        # Save habits to as JSON file

    while habits:
        table = Table(
            show_header=True, title="Current Habits", header_style="bold magenta"
        )
        table.add_column("S/N", style="red")
        table.add_column("Habit", style="cyan")
        table.add_column("Status", style="yellow")
        table.add_column("% Completed", style="green")
        table.add_column("Streak", style="blue")
        for i, habit in enumerate(habits, 1):
            table.add_row(
                str(i), habit["habit_name"], habit["status"], habit["% completed"], f"{habit['streak']} days"
            )
        console.print(table)
        action = (
            prompt.ask(
                "[blue]\nEnter habit number to update status, 'add' to add a new habit, 'done' to finish, 'edit' to edit a habit, or 'delete' to delete a habit [/blue]"
            )
            .strip()
            .lower()
        )

        if action == "done":
            break
        if action == "add":
            continue
        if action == "delete":
            try:
                habit_index = (
                    int(
                        prompt.ask(
                            "[bold cyan]Enter habit number to delete:[/bold cyan]"
                        ).strip()
                    )
                    - 1
                )
                if habit_index < 0 or habit_index >= len(habits):
                    raise ValueError("[yellow]Invalid habit number.[/yellow]")
                habit = habits[habit_index]
                confirm = (
                    prompt.ask(
                        f"[bold cyan]Confirm deletion of '{habit['habit_name']}'? ('y' for yes, 'n' for no)[/bold cyan]"
                    )
                    .strip()
                    .upper()
                )
                if confirm == "Y":
                    delete_habits(habit, habits)
                    # Save updated habits list after deletion
                    try:
                        with open("habits.json", "w") as json_file:
                            json.dump(habits, json_file, indent=4)
                        print("[green]Habits saved to 'habits.json'.[/green]")
                    except Exception as e:
                        print(f"[red]Error saving habits to JSON: {e}[/red]")
                elif confirm != "N":
                    raise ValueError(
                        "[red]Invalid input: Please enter 'y' or 'n'.[/red]"
                    )
            except ValueError as e:
                print(f"[red]Error: {e}[/red]")
                continue
            except Exception as e:
                print(f"[red]Unexpected error: {e}[/red]")
                continue
            continue
        if action == "edit":
            try:
                habit_index = (
                    int(
                        prompt.ask(
                            "[bold cyan]Enter habit number to edit:[/bold cyan]"
                        ).strip()
                    )
                    - 1
                )
                if habit_index < 0 or habit_index >= len(habits):
                    raise ValueError("[yellow]Invalid habit number.[/yellow]")
                habit = habits[habit_index]
                edit_habit(habit, habits, habit_index)
                try:
                    with open("habits.json", "w") as json_file:
                        json.dump(habits, json_file, indent=4)
                    print("[green]Habits saved to 'habits.json'.[/green]")
                except Exception as e:
                    print(f"[red]Error saving habits to JSON: {e}[/red]")
            except ValueError as e:
                print(f"[red]Error: {e}[/red]")
                continue
            except Exception as e:
                print(f"[red]Unexpected error: {e}[/red]")
                continue
            continue
        try:
            habit_index = int(action) - 1
            if habit_index < 0 or habit_index >= len(habits):
                raise ValueError("Invalid habit number.")

            habit = habits[habit_index]
            print(f"\nUpdating status for habit: {habit['habit_name']}")
            status = (
                input("Enter status ('Ongoing','Defaulted', or 'Completed'): ")
                .strip()
                .title()
            )
            if status not in ["Ongoing", "Defaulted", "Completed"]:
                raise ValueError(
                    "[yellow]Status must be 'Ongoing','Defaulted' or 'Completed'.[/yellow]"
                )
            if status == "Completed":
                #  checking if habit is truly completed
                days_elapsed = (
                    datetime.now() - datetime.fromisoformat(habit["start_date"])
                ).total_seconds() / (60 * 60 * 24)
                if days_elapsed < habit["goal"] - 0.01:
                    raise ValueError(
                        f"[yellow]Warning: your {habit[habit_name]} Habit is only {habit['% completed']} complete. ({days_elapsed:.2f}) Days is less than goal ({habit['goal']}).[/yellow]"
                    )
                # archiving of comppleted habits
                archive_option = (
                    prompt.ask(
                        "[bold cyan]Do you want to archive this habit? ('y' for yes, 'n' for no)[/bold cyan]"
                    )
                    .strip()
                    .upper()
                )
                if archive_option == "Y":
                    archive_habits(habit, habits)
                    # Save updated habits list after archiving
                    try:
                        with open("habits.json", "w") as json_file:
                            json.dump(habits, json_file, indent=4)
                        print("[green]Habits saved to 'habits.json'.[/green]")
                    except Exception as e:
                        print(f"[red]Error saving habits to JSON: {e}[/red]")
                    continue  # Skip updating the habit since it's archived

            # Recalculate habit details with updated status
            start_date = datetime.fromisoformat(habit["start_date"])
            updated_habit = recalculating_habits(
                habit["habit_name"],
                start_date,
                habit["goal"],
                habit["cost_per_day"],
                habit["minutes_wasted"],
                status,
                habit["streak"], 
                habit["completion_dates"]
            )
            habits[habit_index] = updated_habit
            # save habits to JSON file
            try:
                with open("habits.json", "w") as json_file:
                    json.dump(habits, json_file, indent=4)
            except Exception as e:
                print(f"[red]Error saving habits to file JSON: {e}[/red]")
        except ValueError as e:
            print(f"Error: {e}")
            continue
        except Exception as e:
            print(f"Unexpected error: {e}")
            continue
    # prompt to save as csv or
    if habits:
        save_option = (
            prompt.ask(
                "[cyan bold]Do you want to save file as a csv file? ('y' for yes, 'n' for no)[/cyan bold]"
            )
            .strip()
            .upper()
        )
        if save_option == "Y":
            save_csv(habits)
            print("[green]File saved successfully![/green]")
        elif save_option == "N":
            print("[yellow]File did not save as csv[/yellow]")
        else:
            raise ValueError("[red]Invalid input[/red]")

    return habits


result = break_habits()
if result:
    table = Table(
        title="Your Habit-Breaking Progress",
        show_header=True,
        header_style="bold Magenta",
    )
    table.add_column("S/N", style="Red")
    table.add_column("Habit", style="cyan")
    table.add_column("Start Date", style="cyan")
    table.add_column("Time Since", justify="right")
    table.add_column("Days Remaining", justify="right")
    table.add_column("Minutes Saved", justify="right")
    table.add_column("% Completed", justify="right")
    table.add_column("Money Saved", justify="right")
    table.add_column("Progress", justify="left", style="green")
    table.add_column(
        "Status",
        justify="left", style="yellow"
    )
    table.add_column("Streak", style="blue")
    for i, habit in enumerate(result, 1):
        table.add_row(
            str(i),
            habit["habit_name"],
            habit["start_date"],
            str(habit["time_since"]),
            str(habit["days_remaining"]),
            str(habit["minutes_saved"]),
            habit["% completed"],
            habit["money_saved"],
            habit["progress_bar"],
            habit["status"],
            f"{habit['streak']} days"
            
        )

    console.print(table)

else:
    print("[cyan]\nNo habits entered.[/cyan]")
