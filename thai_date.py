from datetime import datetime

thai_months = {
    "ม.ค.": "01", "ก.พ.": "02", "มี.ค.": "03", "เม.ย.": "04",
    "พ.ค.": "05", "มิ.ย.": "06", "ก.ค.": "07", "ส.ค.": "08",
    "ก.ย.": "09", "ต.ค.": "10", "พ.ย.": "11", "ธ.ค.": "12"
}


def parse_thai_date(thai_date_str):
    # Split the date into day, month, and year
    day, thai_month, thai_year = thai_date_str.split()

    # Convert the Thai month to month number
    month = thai_months[thai_month]

    # Convert the Buddhist year to Gregorian year
    year = str(int(thai_year) - 543)

    # Construct the Gregorian date string
    gregorian_date_str = f"{day}-{month}-{year}"

    # Parse the date string to a datetime object
    return datetime.strptime(gregorian_date_str, '%d-%m-%Y')