import csv
from pathlib import Path
from typing import Literal, Dict, List
import openpyxl
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment, PatternFill

def parse_csv(category: Literal['web', 'pwn', 'crypto', 'reverse', 'forensics'] = "web", file_path: str = "") -> list:
    """Parses the given csv file into list

    Args:
        category (Literal['web', 'pwn', 'crypto', 'reverse', 'forensics'], optional): Name of the category. Defaults to "web".
        file_path (str, optional): The path of the csv file. Defaults to "".

    Raises:
        Exception: If the file_path is invalid.
        Exception: If the given CSV is empty.

    Returns:
        list:  Returns the parsed list with all the challenges of the given category.
    """
    
    path_check = Path(file_path)
    details = []

    if (path_check.exists() and path_check.is_file()):
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)

            for row in reader:
                if ("Challenge Name" in row):
                    continue
                elif (category in row[1]):
                    details.append(row)
    else:
        raise Exception(f"Invalid file path. Did you give /bin/sudo? Never mind, it was '{file_path}'")
    
    if len(details) > 0:
        return details
    else:
        raise Exception(f"The CSV contains no data? Why did you give me an empty file? T_T")
    
def sort_challs(data: List) -> list:
    """Sorts the given challenge list into solved and unsolved. Also provides CTF name.

    Args:
        data (List): The list of challenges

    Returns:
        dict: The sorted list with the solved, unsolved and CTF name.
    """

    result = []
    solved = []
    unsolved = []

    for details in data:
        current = {}

        detail = details[0].split("-")
        ctf_name = detail[0]
        chall_name = detail[1]
        time = details[-1]
        details = details[2:-1]
        solved_by = details

        current["name"] = chall_name
        current["solved_by"] = solved_by

        if time != 'Nil':
            current["time"] = time
            solved.append(current)
        else:
            current["time"] = None
            unsolved.append(current)

    result.append(solved)
    result.append(unsolved)
    result.append(ctf_name)

    return result

def append_ctf_data_to_excel(workbook_path: str, data: List[Dict]):
    """Appends CTF challenge data to an Excel workbook, creating it if it doesn't exist, with styled data and sectioned headers.

    Args:
        workbook_path (str): Path to the Excel workbook.
        data (list): Parsed data with solved and unsolved challenges, and the CTF name.
    """
    workbook_file = Path(workbook_path)
    if workbook_file.exists():
        workbook = openpyxl.load_workbook(workbook_path)
        sheet = workbook.active
    else:
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "CTF Challenges"

    solved_challenges, unsolved_challenges, ctf_name = data

    ctf_name_cell = sheet.append([ctf_name])
    sheet.merge_cells(start_row=sheet.max_row, start_column=1, end_row=sheet.max_row, end_column=6)
    header_cell = sheet.cell(row=sheet.max_row, column=1)
    header_cell.font = Font(bold=True, size=16, color="000000") 
    header_cell.alignment = Alignment(horizontal="center")
    header_cell.fill = PatternFill(start_color="A9A9A9", end_color="A9A9A9", fill_type="solid") 

    table_header = ["Challenge Name", "Status", "Solved By", "Time Taken", "References", "Writeup"]
    sheet.append(table_header)

    for cell in sheet[sheet.max_row]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid") 

    for index, challenge in enumerate(solved_challenges):
        row = [
            challenge["name"],
            "Solved",
            ', '.join(challenge["solved_by"]),
            challenge["time"],
            "",
            ""
        ]
        sheet.append(row)

        fill_color = PatternFill(start_color="EAEAEA", end_color="EAEAEA", fill_type="solid") if index % 2 == 0 else PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
        for cell in sheet[sheet.max_row]:
            cell.fill = fill_color
   
    for index, challenge in enumerate(unsolved_challenges):
        row = [
            challenge["name"],
            "Unsolved",
            "N/A",
            "N/A",
            "",
            ""
        ]
        sheet.append(row)
       
        fill_color = PatternFill(start_color="EAEAEA", end_color="EAEAEA", fill_type="solid") if (index + len(solved_challenges)) % 2 == 0 else PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
        for cell in sheet[sheet.max_row]:
            cell.fill = fill_color

    sheet.append([" " * 10]) 
    sheet.merge_cells(start_row=sheet.max_row, start_column=1, end_row=sheet.max_row, end_column=6)
    separator_cell = sheet.cell(row=sheet.max_row, column=1)
    separator_cell.alignment = Alignment(horizontal="center")
    separator_cell.font = Font(color="808080") 
    separator_cell.fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid") 
    separator_cell.value = " " 

    min_widths = [20, 10, 15, 15, 25, 25]
    for i in range(1, 7): 
        max_length = 0
        column = [sheet.cell(row=j, column=i).value for j in range(1, sheet.max_row + 1)] 
        for value in column:
            if value is not None:
                max_length = max(max_length, len(str(value)))
        adjusted_width = max(max_length + 2, min_widths[i - 1]) 
        sheet.column_dimensions[get_column_letter(i)].width = adjusted_width 

    workbook.save(workbook_path)
    print(f"Data appended to {workbook_path}")

data = sort_challs(parse_csv(file_path="challs.csv"))
append_ctf_data_to_excel("websheet.xlsx", data)
