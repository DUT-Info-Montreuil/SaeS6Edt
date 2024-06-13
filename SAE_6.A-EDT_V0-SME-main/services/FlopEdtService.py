import requests
from database.config import db

class FlopEdtService:

    @staticmethod
    def get_FlopEdt_courses(dept, week, year, work_copy):
        url = f"https://flopedt.iut.univ-paris8.fr/fr/api/fetch/scheduledcourses/?dept={dept}&week={week}&year={year}&work_copy={work_copy}"

        try:
            response = requests.get(url)
            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None