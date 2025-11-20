#!/usr/bin/env python3

def extract_datetime_string(file_path):
    """Reads the first line of a file and extracts the YYYYMMDDHHMMSS string."""
    try:
        with open(file_path, "r") as f:
            # Read only the first line of the file
            first_line = f.readline().strip()

        # Split the line by spaces
        # Example line: "PDE 2024 12 5 18 44 21.00 40.3600 ..."
        parts = first_line.split()

        # Extract and format the components:
        # Index 1: Year (2024)
        # Index 2: Month (12) -> padded
        # Index 3: Day (5) -> padded
        # Index 4: Hour (18)
        # Index 5: Minute (44)
        # Index 6: Seconds (21.00) -> integer part only, padded

        year = parts[1]
        month = parts[2].zfill(2)
        day = parts[3].zfill(2)
        hour = parts[4].zfill(2)
        minute = parts[5].zfill(2)

        # Take the integer part of the seconds and pad it
        second = parts[6].split(".")[0].zfill(2)

        # Concatenate and return the string
        return f"{year}{month}{day}{hour}{minute}{second}"

    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    except IndexError:
        return (
            "Error: Could not parse the date/time components "
            "from the first line. Check file format."
        )
    except Exception as e:
        return f"An unexpected error occurred: {e}"


# Assuming the file is named 'data/cmtsolution'
file_name = "data/cmtsolution"
result = extract_datetime_string(file_name)

print(result)
