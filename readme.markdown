# Habit Tracker

## Overview
The Habit Tracker is a lightweight Python tool designed to help users monitor and break habits. It tracks the time elapsed since starting to break a habit, calculates money saved by avoiding the habit, and estimates minutes saved daily based on time previously spent on the habit.

## Features
- Track habits by name and start date.
- Calculate time elapsed in days and hours since quitting the habit.
- Estimate money saved based on the daily cost of the habit.
- Estimate total minutes saved based on daily time spent on the habit.
- Tabulated display of habits 
- Saving of habits being tracked
- Saving of habits as a `CSV` or `JSON` file
- Archiving of the **completed** habits
- deleting of habit 
- Updating of habit details
- Streak counting.

## Requirements
- **Python**: Version 3.7 or later
- Intermidate Understanding of python
- Understanding of python `rich` module
- Understanding of `pandas` module
- Understanding of `json` module

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
[![uml image](https://img.plantuml.biz/plantuml/svg/bLNHJjim57sFb7-uucKWqX-eKCKOJ7i02J7sD4tMhNDfFH8xifr2DUtVPpjEuvG4j9UgkUVuNf_Za_ZIMDIshIluXcjXuL4ZVoODF-vkuLhWHcETPtds2UvT7JTau4bfe5TBMc859JKaIv9SaCcpfkF0oKsFtugrHkt04_YJPm2yGcEWH4jMr0GN5rKWx5Uh0Vrjb9n6b9ckDoXBdC6quDinyhSJrEbrMq4mLhVSjfhoh5lKOM77Ywt_poJMjFJ4K0kcCIzZg7b1p0Z9arg9UyCqrIYaa9ibF5KARK1g8LjBXXdSKPa23MbEqZeR6LTrKv7rUD-mLfBs_QA-s6YrqMGCMwCUxT6sPdZUAApIGLmPozmq9sC_jRCND3RPMdJjpac1CD078t6h3qvYcXiUe9-_VEryhGcVMOUSdeqnDwCyGA62PIp4vxRnThDELQnHwKuc9PNa_HgLKFEjs8rhtZzc5UDcvojHsjTMSYjSze8gd-TEtdsqzmgZklFKyDFXmA9N1Ro8qcwN8AGzY_w74Lsxxsxue_fYTh5PkfaZsyv62pztIf9i7eaBlt5n0U_skWv6fQr6rlr7fmVYMF6sGkiI7XWcTjGfqX_kqTjKGFegzT-50fAm5Z2Hr08cOnhQzQbt6rUjhlQESZYRFdOZ2JSkHgaLIQpUDQ9m9rpIQtVGXnWza5UifDcAncLez78i5gluRLawLIuqGavHqiGjeGrPV4CQSZHB6ILcbfLcOPOqTSopvC7Gdf9dG-sZTgDTVqGUNF3CU17CTWfNIuzEjVMam-qqgo_SARFeQCWRL9d4b4jtURgxDy_-0G00)](https://editor.plantuml.com/uml/bLNHJjim57sFb7-uucKWqX-eKCKOJ7i02J7sD4tMhNDfFH8xifr2DUtVPpjEuvG4j9UgkUVuNf_Za_ZIMDIshIluXcjXuL4ZVoODF-vkuLhWHcETPtds2UvT7JTau4bfe5TBMc859JKaIv9SaCcpfkF0oKsFtugrHkt04_YJPm2yGcEWH4jMr0GN5rKWx5Uh0Vrjb9n6b9ckDoXBdC6quDinyhSJrEbrMq4mLhVSjfhoh5lKOM77Ywt_poJMjFJ4K0kcCIzZg7b1p0Z9arg9UyCqrIYaa9ibF5KARK1g8LjBXXdSKPa23MbEqZeR6LTrKv7rUD-mLfBs_QA-s6YrqMGCMwCUxT6sPdZUAApIGLmPozmq9sC_jRCND3RPMdJjpac1CD078t6h3qvYcXiUe9-_VEryhGcVMOUSdeqnDwCyGA62PIp4vxRnThDELQnHwKuc9PNa_HgLKFEjs8rhtZzc5UDcvojHsjTMSYjSze8gd-TEtdsqzmgZklFKyDFXmA9N1Ro8qcwN8AGzY_w74Lsxxsxue_fYTh5PkfaZsyv62pztIf9i7eaBlt5n0U_skWv6fQr6rlr7fmVYMF6sGkiI7XWcTjGfqX_kqTjKGFegzT-50fAm5Z2Hr08cOnhQzQbt6rUjhlQESZYRFdOZ2JSkHgaLIQpUDQ9m9rpIQtVGXnWza5UifDcAncLez78i5gluRLawLIuqGavHqiGjeGrPV4CQSZHB6ILcbfLcOPOqTSopvC7Gdf9dG-sZTgDTVqGUNF3CU17CTWfNIuzEjVMam-qqgo_SARFeQCWRL9d4b4jtURgxDy_-0G00)
