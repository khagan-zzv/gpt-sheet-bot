def find_cell(sheet_data: str, search_for: str, sheet_name: str = "Sheet1") -> str:
    lines = sheet_data.splitlines()
    for row_idx, line in enumerate(lines):
        cells = line.split("|")
        for col_idx, cell in enumerate(cells):
            if search_for.lower() in cell.lower():
                col_letter = chr(65 + col_idx)  # 65 = 'A'
                row_number = row_idx + 1  # Google Sheets is 1-indexed
                print(f"{sheet_name}!{col_letter}{row_number}")
                return f"{sheet_name}{col_letter}{row_number}"
    return "Not found"