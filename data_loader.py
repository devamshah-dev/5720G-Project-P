# data_loader.py
import csv

def load_scenarios(filename="scenarios.csv"):
    """
    Args:
        filename (str): The name of the CSV file to load.
    Returns:
        list: A list of dictionaries, where each dictionary represents a scenario.
    """
    scenarios = []
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # numeric types: from string to number
                row['time'] = int(row['time'])
                row['touch_pattern_base'] = float(row['touch_pattern_base'])
                scenarios.append(row)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        print("Please make sure 'scenarios.csv' is in the same directory.")
        return None
    return scenarios