import json

from src.client import CALPADS


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client = CALPADS(username="reynolds.r@monet.k12.ca.us", password="As3UBPpF7d7Nc#Y")
    # for lea in client.core.get_leas():
    #     if "modesto" in lea.text.lower():
    #         print(lea)
    print(client.student.list_by_enrollment(reporting_lea=5071175, school_of_attendance=5031380,
                                       enrollment_status="Current", grade=12))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
