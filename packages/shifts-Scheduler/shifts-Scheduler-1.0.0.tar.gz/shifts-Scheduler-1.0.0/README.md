Employee Shift Scheduler
This is a Python script for scheduling employees into shifts based on their net salaries. The script reads employee data from a JSON file, sorts the employees by net salary, divides them into groups, shuffles the groups randomly, and assigns employees to shifts. The total cost of each shift is calculated based on the net salaries of the employees in the shift.

Usage
To use the script, follow these steps:

Install Python 3.x on your computer if it is not already installed.
Clone this repository to your local machine or download the script employee_shift_scheduler.py.
Create a JSON file with employee data. The file should have the following structure:

{
    "employees": [
        {
            "name": "John Smith",
            "position": "Manager",
            "net_salary": 50000
        },
        {
            "name": "Jane Doe",
            "position": "Assistant",
            "net_salary": 35000
        },
        ...
    ]
}

Edit the file_path variable in employee_shift_scheduler.py to point to your employee data file.
Run the script using the following command in your terminal:

python employee_shift_scheduler.py

The script will output the employees assigned to each shift and the total cost of each shift.

Hourly Labor Cost Version
If you want to use an hourly labor cost instead of net salary, you can use the employee_shift_scheduler_hourly.py script instead. This script reads employee data with hourly wage and working hours from a CSV file, calculates the net salary based on the working hours, and then schedules employees into shifts based on their net salaries.

To use the hourly labor cost version, follow the same steps as above, but edit the file_path variable in employee_shift_scheduler_hourly.py to point to your CSV file with employee data.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Feel free to modify and use this script as you see fit. If you find any bugs or issues, please report them to the repository issue tracker.

To be honest I didn't spend much time on this and I feel someone can do it better, would love to see someone perfect it.
