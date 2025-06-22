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
- saving of habits as a `CSV` or `JSON` file
- Archiving of the **completed** habits
- deleting of habit feature
- updating of habit details

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
2. Clone the repository (replace `oluwatimilehin` with the actual repository owner):
   ```bash
   git clone https://github.com/oluwatimilehin/habit-tracker.git
   ```
3. Navigate to the project directory:
   ```bash
   cd habit-tracker
   ```
4. make sure the python rich module is installed on your machine. to install run the following command on your terminal:
 ```bash
   pip install rich
 ```
 4. make sure the python pandas module is installed on your machine. to install, run the following command on your terminal:
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

## Issues

Please report issues or suggest features via the [GitHub Issues page](https://github.com/oluwatimilehin/habit-tracker/issues).


## UML
[![](https://img.plantuml.biz/plantuml/svg/bLNHQjim57qt-1ykVLb371Xx35tejdRieONITKzZc1lvDj5gIqQIquQnVvyaox6Ss2rx2V4zHrSwvnvRbzgWCarLmZTSSmCF2jaJAVXnUmDN73SAgpH9atTmP-ku8GsFKW6z6582IoYe9b6GO9nqcjGj1ywkE_o6hnKg2vx1dpG1O2Lg3GKQChmYkBWeFM6_MlNeRot5E2BrUBr6KU04fZZR3f6_hQ1MhpqAWZQgOQPHb2RjeXRp9rvitVzSO4LBH_GrRrhkPFGr9oZNNB2eLk1Uvuegv8ABpH8UIud68nKNZI6TQznH4GCrAKR2M1jp9gkw9EFmhc4b1UsxHLsnLdAZIEjyZMfmHjFe_daZiOmtObARtEvcPUp7JlQCsaH72wxTMYdWDtJ1YDpgWXEPPZVtqCzVRKqsgjpRlXiANU4ZV7ZliFbQ4JxbxQhpsM3Tt3AB0-GhM8H2U6vgDugyLHngLDYfnQI2d9U34YgsvRjXpNcR6vaplNEL8Fjh8vZXDfTUiSjwA_qkMFyPW_9vF8ppVfX1SGRFl33R9N1XPc4sVekstNUx-OFyedUXMNoO8qjdWuMVMYLHRe_4-T-mE8DNUrrve-9M0-l-ezCzCInPKwAnwVSC7Jgg6Ec6U_IcPH2_Pjqt8uCeo1cCf3Y3qGZxTjqROGz-aiOkTWC9rpP6iHLHh5ur8hCJBkYb7VGXHlVa54kXjxos6HgyE8l5AdntbbQL3GqNOvGuSKjeV1PFI7sE9Yc3n4oouYnCaiR6F4dk3UqeQTBNtcetEFLRvDu5nmoNn6GdV-rqw5XRHphSN9Fw_7qpYGusEK6bZaovj1UhlPVJv1y0)](https://editor.plantuml.com/uml/bLNHQjim57qt-1ykVLb371Xx35tejdRieONITKzZc1lvDj5gIqQIquQnVvyaox6Ss2rx2V4zHrSwvnvRbzgWCarLmZTSSmCF2jaJAVXnUmDN73SAgpH9atTmP-ku8GsFKW6z6582IoYe9b6GO9nqcjGj1ywkE_o6hnKg2vx1dpG1O2Lg3GKQChmYkBWeFM6_MlNeRot5E2BrUBr6KU04fZZR3f6_hQ1MhpqAWZQgOQPHb2RjeXRp9rvitVzSO4LBH_GrRrhkPFGr9oZNNB2eLk1Uvuegv8ABpH8UIud68nKNZI6TQznH4GCrAKR2M1jp9gkw9EFmhc4b1UsxHLsnLdAZIEjyZMfmHjFe_daZiOmtObARtEvcPUp7JlQCsaH72wxTMYdWDtJ1YDpgWXEPPZVtqCzVRKqsgjpRlXiANU4ZV7ZliFbQ4JxbxQhpsM3Tt3AB0-GhM8H2U6vgDugyLHngLDYfnQI2d9U34YgsvRjXpNcR6vaplNEL8Fjh8vZXDfTUiSjwA_qkMFyPW_9vF8ppVfX1SGRFl33R9N1XPc4sVekstNUx-OFyedUXMNoO8qjdWuMVMYLHRe_4-T-mE8DNUrrve-9M0-l-ezCzCInPKwAnwVSC7Jgg6Ec6U_IcPH2_Pjqt8uCeo1cCf3Y3qGZxTjqROGz-aiOkTWC9rpP6iHLHh5ur8hCJBkYb7VGXHlVa54kXjxos6HgyE8l5AdntbbQL3GqNOvGuSKjeV1PFI7sE9Yc3n4oouYnCaiR6F4dk3UqeQTBNtcetEFLRvDu5nmoNn6GdV-rqw5XRHphSN9Fw_7qpYGusEK6bZaovj1UhlPVJv1y0)
