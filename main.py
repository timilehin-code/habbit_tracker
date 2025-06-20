# from datetime import datetime

# from rich.table import Table
# import habbit_tool as ht
# import pandas as pd
from rich import print

# from rich.console  import Console
# console = Console()
# table = Table(title="testing")
# table.add_column("habbit", justify="right", style="green", no_wrap=True)
# table.add_column("habbit", style="red")
# table.add_column("habbit", justify="right", style="cyan")


# table.add_row("1", "smoking", "40mins")
# table.add_row("1", "smoking", "40mins")
# table.add_row("1", "smoking", "40mins")
details = {
    "habbit": "habbit_name",
    "time_since": "hours",
    "days_remaining": "days_to_go",
    "minutes_saved": "minutes_saved",
    "% completed": f"%",
    "money_saved": "total_money_saved",
}
for key, value in details.items():
    print(f"{key.title().replace("_", " ")} -- {value}")
