import argparse
import json
import operator
import os
import questionary


def save_to_json(entries):
    if not entries:
        print("No entries to save")
        return

    filename = questionary.text("Enter filename:").ask()
    if not filename:
        print("Filename not provided. Cancelled")
        return
    
    if not filename.endswith(".json"):
        filename += ".json"
    
    with open(filename, 'w') as file:
        json.dump(entries, file, indent=2)

    print(f"Saved {len(entries)} entries to '{filename}'")

def show_entries_paginate(entries):
    page = 0
    page_size = 10 #CHANGE THIS

    while True:
        start = page * page_size
        end = start + page_size
        current_entries = entries[start:end]

        print(f"\n <--- Page №{page + 1} of {(len(entries) // 10) + 1} --->")
        for i, entry in enumerate(current_entries, start=1):
            #print(f"\n--- Showing entries {start + 1} to {min(end, len(entries))} of {len(entries)} ---")
            #print(f"[{start + i}] {entry['url']}\n\tstatus: {entry['status']}\n\tlength: {entry['length']}\n\twords: {entry['words']}\n\tlines: {entry['lines']}\n\tduration: {entry['duration']}")
            print(f"#{start + i}")
            print(f"URL:      {entry.get('url', '-')}")
            print(f"HOST:     {entry.get('host', '-')}")
            print(f"Status:   {entry.get('status', '-')}")
            print(f"Length:   {entry.get('length', '-')}")
            print(f"Words:    {entry.get('words', '-')}")
            print(f"Lines:    {entry.get('lines', '-')}")
            print(f"Duration: {entry.get('duration', '-')}")
            print("-" * 50)

        # Menu
        choices = []
        if page > 0:
            choices.append("Previous page")
        if end < len(entries):
            choices.append("Next page")
        choices.append("Main Menu")

        navigation = questionary.select("Navigation", choices=choices).ask()

        if navigation == "Next page":
            page += 1
        elif navigation == "Previous page":
            page -= 1
        else:
            break

def show_menu(filtered_entries):
    print(f"Found: {len(filtered_entries)} records")

    choice = questionary.select(
        "Choose an action",
        choices=[
            "Change filters",
            "Show entries",
            "Save as JSON",
            "Quit"
        ] 
    ).ask()

    return choice

def apply_filters(entries, active_filter):
    filtered = []
    ops_map = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}

    for entry in entries:
        passed = True

        for field, condition in active_filter.items():
            if condition is None:
                continue # Skip, if condition doesn`t specify

            parsed = parse_condition(condition)
            if not parsed:
                continue # Skip, if something wrong input

            op_str, value = parsed
            op_func = ops_map[op_str]

            # Is there a field or not
            if field not in entry:
                passed = False
                break

            #Apply filter
            if not op_func(entry[field], value):
                passed = False
                break

        if passed:
            filtered.append(entry)

    return filtered

def parse_condition(condition_str):
    valid_ops = ['==', '!=', '<', '>', '>=', '<=']
    condition_str = condition_str.strip()
    split_str = condition_str.strip().split()

    if len(split_str) == 1:
        try:
            return ("==", int(split_str[0]))
        except ValueError:
            return None  # Input string, not int

    # Regular format: ">= 100", "< 500", etc.
    if len(split_str) == 2:
        op, value = split_str
        if op not in valid_ops:
            return None
        try:
            return (op, int(value))
        except ValueError:
            return None

    # Wrong format
    return None

def ask_for_filters(active_filters, filters):
    print("\nUpdate filters (leave blank to skip). Use format like '> 100', '== 200'\n")

    field_questions = {}
    for field in filters:
        current = active_filters.get(field)
        default = current if current else ""
        field_questions[field] = questionary.text(f"{field}", default=default)

    answers = questionary.form(**field_questions).ask()

    for field in filters:
        user_input = answers.get(field)
        active_filters[field] = user_input.strip() if user_input else None
    
def load_file(path):
    with open(path, 'r') as file:
        return json.load(file) # To parse JSON format

def get_args():
    parser = argparse.ArgumentParser(description="Filter for JSON results")
    parser.add_argument("file", help="Path to JSON file")
    return parser.parse_args()

args = get_args()
if not os.path.exists(args.file):
    print("File not found.")
    exit(1)

data = load_file(args.file)
entries = data['results'] # To straight access to objects
filter_fields = ['status', 'length', 'words', 'lines', 'duration'] # CHANGE THIS
active_filters = {field: None for field in filter_fields} # {'status': None, 'length': None,...

# Main loop
while True:
    filtered = apply_filters(entries, active_filters)
    choice = show_menu(filtered)

    if choice == "Change filters":
        ask_for_filters(active_filters, filter_fields)
    elif choice == "Show entries":
        show_entries_paginate(filtered)
    elif choice == "Save as JSON":
        save_to_json(filtered)
    else:
        break
