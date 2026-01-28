import csv
import os

REQUIRED_COLUMNS = {"process", "action", "resource"}
VALID_ACTIONS = {"request", "hold", "release"}


class CSVFormatError(Exception):
    pass


def load_csv(file_path="input/input.csv"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    data = []

    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        # Validate CSV header
        if not REQUIRED_COLUMNS.issubset(reader.fieldnames):
            raise CSVFormatError(
                f"CSV is missing required columns. Required: {REQUIRED_COLUMNS}"
            )

        # Read and validate each row
        for line_num, row in enumerate(reader, start=2):
            process = row["process"].strip()
            action = row["action"].strip().lower()
            resource = row["resource"].strip()

            if not process or not resource:
                raise CSVFormatError(
                    f"Line {line_num}: process or resource is empty"
                )

            if action not in VALID_ACTIONS:
                raise CSVFormatError(
                    f"Line {line_num}: invalid action '{action}'"
                )

            data.append({
                "process": process,
                "action": action,
                "resource": resource
            })

    if not data:
        raise CSVFormatError("CSV file is empty")

    return data
##test cases
# if __name__ == "__main__":
#     try:
#         operations = load_csv("input.csv")
#         for op in operations:
#             print(op)
#         print("CSV loaded successfully.")
#     except Exception as e:
#         print(e)
