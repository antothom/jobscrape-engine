from abc import abstractmethod

from bs4 import BeautifulSoup

from fetcher import DataFetcher

import requests

class Extractor:
    def __init__(self, data_fetcher: DataFetcher) -> None:
        self.url = data_fetcher.url
        self.data = data_fetcher.data
        self.jobs_list = []
        self.company_name = data_fetcher.company_name

    @classmethod
    def create(cls, data_fetcher) -> 'Extractor':
        if ('greenhouse' in data_fetcher.url[0]) or ('traderepublic' in data_fetcher.url[0]):
            return GreenhouseExtractor(data_fetcher)
        elif 'personio' in data_fetcher.url[0]:
            return PersonioExtractor(data_fetcher)
        elif 'ashbyhq' in data_fetcher.url[0]:
            return AshbyExtractor(data_fetcher)
        elif 'recruitee' in data_fetcher.url[0]:
            return RecruiteeExtractor(data_fetcher)
        elif 'lever' in data_fetcher.url[0]:
            return LeverExtractor(data_fetcher)
        elif 'smartrecruiters' in data_fetcher.url[0]:
            return SmartRecruitersExtractor(data_fetcher)
        elif 'polymer' in data_fetcher.url[0]:
            return PolymerExtractor(data_fetcher)
        elif 'join.com' in data_fetcher.url[0]:
            return JoinExtractor(data_fetcher)
        else:
            raise ValueError('There is no extractor for the given Job Board')

    @abstractmethod
    def extract_job_list(self) -> None:
        pass


class PersonioExtractor(Extractor):
    def __init__(self, data_fetcher):
        super().__init__(data_fetcher)

    def extract_job_list(self) -> None:

        for position in self.data:
            id = position.find('id').text
            title = position.find('name').text
            # url = position.find('id').text
            departments = position.find('department')
            if departments is not None:
                departments = departments.text
            location = position.find('office').text
            employmentType = position.find('employmentType').text
            job_description = ''
            for job_desc in position.find('jobDescriptions').findall('jobDescription'):
                job_name = job_desc.find('name').text
                job_value = job_desc.find('value').text.strip()
                job_description += f"{job_name}\n{job_value}\n\n"
            published_on = position.find('createdAt').text

            job = {
                'company': self.company_name,
                'id': id,
                'title': title,
                'url': f"https://finway.jobs.personio.de/job/{id}",
                'departments': departments,
                'location': location,
                'employment_type': employmentType,
                'description': job_description,
                'published_on': published_on
            }

            self.jobs_list.append(job)


class AshbyExtractor(Extractor):
    def __init__(self, data_fetcher):
        super().__init__(data_fetcher)

    def extract_job_list(self) -> None:
        jobs_elements = self.data['jobs']

        # Extract job details and store in a list of dictionaries
        jobs_list = [
            {
                'company': self.company_name,
                'id': job['id'],
                'title': job['title'],
                'url': job['jobUrl'],
                'departments': job['department'],
                'location': job['location'],
                'employment_type': job['employmentType'],
                'description': job['descriptionPlain'],
                'published_on': job['publishedAt']
            }
            for job in jobs_elements
        ]

        self.jobs_list = jobs_list


class RecruiteeExtractor(Extractor):
    def __init__(self, data_fetcher):
        super().__init__(data_fetcher)

    def extract_job_list(self) -> None:
        pass


class GreenhouseExtractor(Extractor):
    def __init__(self, data_fetcher):
        super().__init__(data_fetcher)

    def extract_job_list(self) -> None:
        jobs_elements = self.data['jobs']

        # Extract job details and store in a list of dictionaries
        jobs_list = [
            {
                'company': self.company_name,
                'id': job['id'],
                'title': job['title'],
                'url': job['absolute_url'],
                # return None if departments does not exist
                # check if there is a department key in the job dictionary
                # if it exists, return the department name
                # if it does not exist, return None
                'departments': job['departments'] if 'departments' in job else None,
                'location': job['location']['name'],
                'employment_type': job['metadata'][0]['value'] if job['metadata'] is not None else None,
                'description': job['content'] if 'content' in job else None,
                'published_on': job['updated_at']
            }
            for job in jobs_elements
        ]

        self.jobs_list = jobs_list


class LeverExtractor(Extractor):
    def __init__(self, data_fetcher):
        super().__init__(data_fetcher)

    def extract_job_list(self) -> None:
        jobs_elements = self.data

        if 'error' in jobs_elements:
            if jobs_elements['error'] == 'Document not found':
                self.jobs_list = []
                # TODO: REMOVE THIS
                return None

        # Extract job details and store in a list of dictionaries
        jobs_list = [
            {
                'company': self.company_name,
                'id': job['id'],
                'title': job['text'],
                'url': job['hostedUrl'],
                'departments': job['categories']['department'],
                'location': job['categories']['location'],
                'employment_type': job['categories']['commitment'],
                'description': job['descriptionPlain'],
                'published_on': job['createdAt']
            }
            for job in jobs_elements
        ]

        self.jobs_list = jobs_list


class SmartRecruitersExtractor(Extractor):
    def __init__(self, data_fetcher):
        super().__init__(data_fetcher)

    def extract_job_list(self) -> None:
        for job in self.data['content']:
            job_id = job['id']
            title = job['name']
            url = job['ref']
            departments = job['department']['label']
            location = job['location']['city']
            employment_type = job['experienceLevel']['label']
            description = None
            published_on = job['releasedDate']

            job = {
                'company': self.company_name,
                'id': job_id,
                'title': title,
                'url': url,
                'departments': departments,
                'location': location,
                'employment_type': employment_type,
                'description': description,
                'published_on': published_on
            }

            self.jobs_list.append(job)


class PolymerExtractor(Extractor):
    def __init__(self, data_fetcher):
        super().__init__(data_fetcher)

    def extract_job_list(self) -> None:
        for job in self.data['items']:
            job_id = job['id']
            title = job['title']
            url = job['job_post_url']
            departments = None
            location = job['display_location']
            employment_type = job['kind_pretty']
            description = None
            published_on = job['published_at']

            job = {
                'company': self.company_name,
                'id': job_id,
                'title': title,
                'url': url,
                'departments': departments,
                'location': location,
                'employment_type': employment_type,
                'description': description,
                'published_on': published_on
            }

            self.jobs_list.append(job)


class RecruiteeExtractor(Extractor):
    def __init__(self, data_fetcher):
        super().__init__(data_fetcher)

    def extract_job_list(self) -> None:
        for job in self.data['offers']:
            job_id = job['id']
            title = job['sharing_title']
            url = job['careers_url']
            departments = job['department']
            location = job['location']
            employment_type = job['employment_type_code']
            description = job['description']
            published_on = job['published_at']

            job = {
                'company': self.company_name,
                'id': job_id,
                'title': title,
                'url': url,
                'departments': departments,
                'location': location,
                'employment_type': employment_type,
                'description': description,
                'published_on': published_on
            }

            self.jobs_list.append(job)


class JoinExtractor(Extractor):
    def __init__(self, data_fetcher):
        super().__init__(data_fetcher)

    def extract_job_list(self) -> None:
        jobs = []

        try:
            total_results_text = self.data.find('div', {'data-testid': 'PaginationSummary'}).text
            total_results = int(total_results_text.split(' ')[-2])
        except AttributeError:
            total_results = 0

        page = 1
        while (page - 1) * 5 < total_results:
            response = requests.get(f'{self.url[0]}?page={page}')
            soup = BeautifulSoup(response.text, 'html.parser')
            job_elements = soup.find_all('a', class_='JobTile___StyledJobLink-sc-de57a1d0-0')

            for job_element in job_elements:
                title_element = job_element.find('h3')
                detail_element = job_element.find('div', class_='sc-hLseeU jtGHbV')
                # Find all the div elements with the relevant class
                info_divs = detail_element.find_all('div',
                                          class_="sc-hLseeU JobTile-elements___StyledText-sc-e7e7aa1d-4 fyJRsY kPLurW")

                # Initialize variables to store the extracted information
                location = employment_type = department = None

                # Iterate through the div elements and extract the information based on the presence of icons
                for div in info_divs:
                    text = div.get_text(strip=True)
                    if 'LocationPinIcon' in str(div):
                        location = text
                    elif 'BriefcaseIcon' in str(div):
                        employment_type = text
                    elif 'FolderIcon' in str(div):
                        department = text

                job = {
                    'id': job_element['href'].split('/')[-1][:8],
                    'company': self.company_name,
                    'title': title_element.text,
                    'url': job_element['href'],
                    'departments': department,
                    'location': location,
                    'employment_type': employment_type,
                    'description': None,
                    'published_on': None
                }
                jobs.append(job)

            page += 1

        self.jobs_list = jobs
