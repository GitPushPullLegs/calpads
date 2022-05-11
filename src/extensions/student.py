import datetime
import json
import re

from src.extensions import BaseAPIExt


class Student(BaseAPIExt):
    def list_by_enrollment(
            self,
            reporting_lea: int,
            school_of_attendance: int,
            enrollment_status: str,
            grade: str = None,
            enrolled_on_or_after: datetime.datetime = None
    ):
        if enrolled_on_or_after:
            enrolled_on_or_after = enrolled_on_or_after.strftime("%M %D %Y").replace(" ", "%2F")
        if enrollment_status not in ["All", "Previous", "Current"]:
            raise ValueError("enrollment status must be 'All', 'Previous', or 'Current'.")

        response = self.api._session.get(
            "https://www.calpads.org/Student/EnrollmentSearch"
            f"?ReportingLEA={reporting_lea}"
            f"&SchoolOfAttendence={school_of_attendance}"
            f"&Grade={grade if grade else ''}"
            f"&EnrolledOnOrAfter={enrolled_on_or_after if enrolled_on_or_after else ''}"
            f"&EnrollmentStatus={enrollment_status}"
            f"&format=JSON")
        data = re.search(r'(?<={"Data":\[)([\w\W]+)(?=],"Total":)', response.text)
        if data:
            return json.loads(f"[{data.groups()[-1]}]")

        if "There are more than 1000 records matching your criteria. Please narrow your search." in response.text:
            raise MemoryError("There are more than 1000 records matching your criteria. Please narrow your search.")

        return []

    def list_by_demographics(
            self,
            last_name: str = None,
            first_name: str = None,
            middle_name: str = None,
            birth_year: int = None,
            birth_country: str = "US",
            gender: str = None
    ):
        """ For first, middle, or last name you can use an asterisks as a wildcard. E.g. Joe Agui* """
        response = self.api._session.get(
            "https://www.calpads.org/Student/DemographicSearch"
            f"?LastName={last_name if last_name else ''}"
            f"&FirstName={first_name if first_name else ''}"
            f"&MiddleName={middle_name if middle_name else ''}"
            f"&BirthDate={birth_year if birth_year else ''}"
            f"&BirthCountry={birth_country if birth_country else ''}"
            f"&Gender={gender if gender else ''}")
        data = re.search(r'(?<={"Data":\[)([\w\W]+)(?=],"Total":)', response.text)
        if data:
            return json.loads(f"[{data.groups()[-1]}]")

        if "There are more than 100 records matching your criteria. Please narrow your search." in response.text:
            raise MemoryError("There are more than 100 records matching your criteria. Please narrow your search.")

        return []

    def enrollment_history(self, ssid: str):
        return self.api.get_resource(f"/Student/{ssid}/Enrollment?format=JSON")

    def demographics(self, ssid: str):
        return self.api.get_resource(f"/Student/{ssid}/Demographics?format=JSON")

    def address_history(self, ssid: str):
        return self.api.get_resource(f"/Student/{ssid}/Address?format=JSON")

    def ela(self, ssid: str):
        return self.api.get_resource(f"/Student/{ssid}/EnglishLanguageAcquisition?format=JSON")

    def program_history(self, ssid: str):
        return self.api.get_resource(f"/Student/{ssid}/Program?format=JSON")

    def student_course_section_history(self, ssid: str):
        return self.api.get_resource(f"/Student/{ssid}/StudentCourseSection?format=JSON")

    def career_technical_education(self, ssid: str):
        return self.api.get_resource(f"/Student/{ssid}/CareerTechnicalEducation?format=JSON")

    def absence_summary(self, ssid: str):
        return self.api.get_resource(f"/Student/{ssid}/StudentAbsenceSummary?format=JSON")

    def incident_history(self, ssid: str):
        return self.api.get_resource(f"/Student/{ssid}/StudentIncidentResult?format=JSON")

    def offence_history(self, ssid: str):
        return self.api.get_resource(f"/Student/{ssid}/Offense?format=JSON")

    def assessment_history(self, ssid: str):
        return self.api.get_resource(f"/Student/{ssid}/Assessment?format=JSON")

    def sped_history(self, ssid: str):
        return self.api.get_resource(f"/Student/{ssid}/SPED?format=JSON")

    def sped_service_history(self, ssid: str):
        return self.api.get_resource(f"/Student/{ssid}/SSRV?format=JSON")

    def postsecondary_status(self, ssid: str):
        return self.api.get_resource(f"/Student/{ssid}/PSTS?format=JSON")
