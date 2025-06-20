# Habit Tracker

## Overview
The Habit Tracker is a lightweight Python tool designed to help users monitor and break habits. It tracks the time elapsed since starting to break a habit, calculates money saved by avoiding the habit, and estimates minutes saved daily based on time previously spent on the habit.

## Features
- Track habits by name and start date.
- Calculate time elapsed in days and hours since quitting the habit.
- Estimate money saved based on the daily cost of the habit.
- Estimate total minutes saved based on daily time spent on the habit.
- Tabulated display of habits 
- saving of habits being tracked

## Requirements
- **Python**: Version 3.7 or later
- Intermidate Understanding of python
- understanding of python `rich` module
- understanding of `pandas` module
- understanding of `json` module

## dependecies
- datetime module
- pandas module
- rich module
- json module
- os module

## Installation
1. Ensure Python 3.7 or higher is installed on your machine. Verify with:
   ```bash
   python --version
   ```
2. Clone the repository (replace `yourusername` with the actual repository owner):
   ```bash
   git clone https://github.com/yourusername/habit-tracker.git
   ```
3. Navigate to the project directory:
   ```bash
   cd habit-tracker
   ```
4. make sure the python rich module is installed on your machine. to install run the following command on your terminal:
 ```bash
   pip install rich
 ```
 4. make sure the python pandas module is installed on your machine. to install run the following command on your terminal:
 ```bash
   pip install pandas
 ```
## Usage
The Habit Tracker is implemented in the `habit_tracker.py` file, which contains the `break_habits` function. To use it, run the script or import the function into your Python code.


#### Example
Create a Python script or use the interactive Python shell to call the function:

```python
from datetime import datetime
from habit_tracker import break_habits

```



This will prompt for inputs or use hardcoded values (depending on the script’s implementation).

## Project Structure
```
habit-tracker/
│
├── habit_tool.py  # Main script with the break_habits function
├── README.md         # This file
└── LICENSE           # MIT License file
```

## Notes
- The `start_date` must be in the past relative to the current date and time.
- The `cost_per_day` and `minutes_wasted` should be non-negative numbers. The function does not currently validate inputs, so ensure valid values are provided.
- The output format may vary depending on the implementation of `break_habits` (e.g., string or dictionary).

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please report issues or suggest features via the [GitHub Issues page](https://github.com/yourusername/habit-tracker/issues).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.