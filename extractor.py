from abc import abstractmethod

from bs4 import BeautifulSoup

from fetcher import DataFetcher

import re
import requests
import json

class Extractor:
    def __init__(self, data_fetcher: DataFetcher) -> None:
        self.url = data_fetcher.url
        self.data = data_fetcher.data
        self.jobs_list = []
        self.company_name = data_fetcher.company_name
        self.ats_platform = data_fetcher.ats_platform.lower()
        with open('mappings.txt', 'r') as file:
            self.mappings = json.load(file)
    
    @classmethod
    def create(cls, data_fetcher) -> 'Extractor':
        if data_fetcher.ats_platform.lower() == 'greenhouse':
            return GreenhouseExtractor(data_fetcher)
        elif data_fetcher.ats_platform.lower() == 'personio':
            return PersonioExtractor(data_fetcher)
        elif data_fetcher.ats_platform.lower() == 'ashby':
            return AshbyExtractor(data_fetcher)
        elif data_fetcher.ats_platform.lower() == 'recruitee':
            return RecruiteeExtractor(data_fetcher)
        elif data_fetcher.ats_platform.lower() == 'lever':
            return LeverExtractor(data_fetcher)
        elif data_fetcher.ats_platform.lower() == 'smartrecruiters':
            return SmartRecruitersExtractor(data_fetcher)
        elif data_fetcher.ats_platform.lower() == 'polymer':
            return PolymerExtractor(data_fetcher)
        elif data_fetcher.ats_platform.lower() == 'join':
            return JoinExtractor(data_fetcher)
        elif data_fetcher.ats_platform.lower() == 'teamtailor':
            return TeamtailorExtractor(data_fetcher)
        elif data_fetcher.ats_platform.lower() == 'dover':
            return DoverExtractor(data_fetcher)
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
            # Get the id of the job
            id = position.find('id').text

            # Get the title of the job
            title = position.find('name').text
            
            # Get the url of the job
            url = f"https://{re.search(r'https:\/\/([a-zA-Z0-9-]+)\.jobs\.personio\.de', self.url[0]).group(1)}.jobs.personio.de/job/{id}/"

            # Get the departments of the job
            departments = position.find('department')
            if departments is not None:
                departments = departments.text

            # Get the location of the job
            location = position.find('office').text
            
            # Get the employment type of the job
            employment_type = position.find('employmentType').text
            employment_type = self.mappings['employment_type'][employment_type] if employment_type in self.mappings['employment_type'] else None

            # Get the description of the job
            job_description = ''
            for job_desc in position.find('jobDescriptions').findall('jobDescription'):
                job_name = job_desc.find('name').text
                job_value = job_desc.find('value').text.strip()
                job_description += f"{job_name}\n{job_value}\n\n"
            
            # Get the publishing date of the job
            published_on = position.find('createdAt').text

            job = {
                'company': self.company_name,
                'id': id,
                'title': title,
                'url': url,
                'departments': departments,
                'location': location,
                'employment_type': employment_type,
                'description': job_description,
                'published_on': published_on
            }

            self.jobs_list.append(job)


class AshbyExtractor(Extractor):
    def __init__(self, data_fetcher):
        super().__init__(data_fetcher)

    def extract_job_list(self) -> None:
        jobs_elements = self.data['jobs']

        for position in jobs_elements:
            # Get the id of the job
            job_id = position['id']

            # Get the title of the job
            title = position['title']

            # Get the url of the job
            url = position['jobUrl']

            # Get the departments of the job
            departments = position['department']

            # Get the location of the job
            location = position['location']

            # Get the employment type of the job
            employment_type = position['employmentType']
            employment_type = self.mappings['employment_type'][employment_type] if employment_type in self.mappings['employment_type'] else None

            # Get the description of the job
            description = position['descriptionPlain']

            # Get the publishing date of the job
            published_on = position['publishedAt']

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


class GreenhouseExtractor(Extractor):
    def __init__(self, data_fetcher):
        super().__init__(data_fetcher)

    def extract_job_list(self) -> None:
        jobs_elements = self.data['jobs']

        for position in jobs_elements:
            # Get the id of the job
            job_id = position['id']

            # Get the title of the job
            title = position['title']

            # Get the url of the job
            url = position['absolute_url']

            # Get the departments of the job
            departments = position['departments'] if 'departments' in position else None

            # Get the location of the job
            location = position['location']['name']

            # Get the employment type of the job
            employment_type = position['metadata'][0]['value'] if position['metadata'] is not None else None
            employment_type = self.mappings['employment_type'][employment_type] if employment_type in self.mappings['employment_type'] else None

            # Get the description of the job
            description = position['content'] if 'content' in position else None

            # Get the publishing date of the job
            published_on = position['updated_at']

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


class LeverExtractor(Extractor):
    def __init__(self, data_fetcher):
        super().__init__(data_fetcher)

    def extract_job_list(self) -> None:
        if 'error' in self.data:
            if self.data['error'] == 'Document not found':
                self.jobs_list = []
                return None

        for position in self.data:
            # Get the job ID
            job_id = position['id']

            # Get the job title
            title = position['text']

            # Get the job URL
            url = position['hostedUrl']

            # Get the departments
            departments = None

            # Get the location
            location = position['categories']['location']

            # Get the employment type
            employment_type = position['categories']['commitment'] if 'commitment' in position['categories'] else None
            employment_type = self.mappings['employment_type'][employment_type] if employment_type in self.mappings['employment_type'] else None

            # Get the job description
            description = position['descriptionPlain']

            # Get the publishing date of the job
            published_on = position['createdAt']

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


class SmartRecruitersExtractor(Extractor):
    def __init__(self, data_fetcher):
        super().__init__(data_fetcher)

    def extract_job_list(self) -> None:
        for position in self.data['content']:
            # Get the job ID
            job_id = position['id']

            # Get the job title 
            title = position['name']

            # Get the job URL
            url = position['ref']

            # Get the departments
            departments = position['department']['label'] if 'label' in position['department'] else None

            # Get the location
            location = position['location']['city']

            # Get the employment type
            employment_type = position['experienceLevel']['label']
            employment_type = self.mappings['employment_type'][employment_type] if employment_type in self.mappings['employment_type'] else None

            # Get the job description
            description = None

            # Get the publishing date of the job
            published_on = position['releasedDate']

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
        for position in self.data['offers']:
            # Get the job ID
            job_id = position['id']

            # Get the job title
            title = position['sharing_title']

            # Get the job URL
            url = position['careers_url']

            # Get the departments
            departments = position['department']

            # Get the location
            location = position['location']

            # Get the employment type
            employment_type = position['employment_type_code']
            employment_type = self.mappings['employment_type'][employment_type] if employment_type in self.mappings['employment_type'] else None
            
            # Get the job description
            description = position['description']

            # Get the publishing date of the job
            published_on = position['published_at']

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
            job_elements = soup.find_all('a', class_=lambda x: x and x.startswith('JobTile___StyledJobLink-sc-'))

            for job_element in job_elements:
                title_element = job_element.find('h3')
                detail_element = job_element.find('div', class_='sc-hLseeU jtGHbV')
                # Find all the div elements with the relevant class
                info_divs = detail_element.find_all('div',
                                          class_=lambda x: x and x.startswith('JobTile-elements___StyledText-sc-'))

                # Initialize variables to store the extracted information
                location = employment_type = department = None
                location = detail_element.find

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


class TeamtailorExtractor(Extractor):
    def __init__(self, data_fetcher):
        super().__init__(data_fetcher)

    def extract_job_list(self) -> None:
        jobs = []

        show_more = True
        page = 1
        while show_more:
           
            response = requests.get(f'{self.url[0]}?page={page}')
            
            soup = BeautifulSoup(response.content, 'html.parser')
            show_more_button = soup.find('div', id='show_more_button')
            if show_more_button is not None:
                page += 1
            else:
                show_more = False

            job_list = soup.find('ul', id='jobs_list_container')
            job_elements = job_list.find_all('li')

            for job_element in job_elements:
                title_element = job_element.find('span', class_='text-block-base-link').get_text(strip=True)
                url = job_element.find('a', href=True)['href']
                detail_information = job_element.find('div', class_='mt-1 text-md').get_text(' ', strip=True).split('·')
                
                department = detail_information[0] if len(detail_information) > 0 else None
                location = detail_information[1] if len(detail_information) > 1 else None 

                job = {
                    'id': url.split('/')[-1][:7],
                    'company': self.company_name,
                    'title': title_element,
                    'url': url,
                    'departments': department,
                    'location': location,
                    'employment_type': None,
                    'description': None,
                    'published_on': None
                }
                jobs.append(job)

         

        self.jobs_list = jobs


class DoverExtractor(Extractor):
    def __init__(self, data_fetcher):
        super().__init__(data_fetcher)

    def extract_job_list(self) -> None:
        jobs_elements = self.data['results']

        for position in jobs_elements:
            # Get the id of the job
            job_id = position['id']

            # Get the title of the job
            title = position['title']

            # Get the url of the job
            url = f"https://app.dover.com/apply/{self.company_name}/"+position['id']

            # Get the departments of the job
            departments = None

            # Get the location of the job
            location = position['locations'][0]['location_option']['city']

            # Get the employment type of the job
            employment_type = None
            employment_type = self.mappings['employment_type'][employment_type] if employment_type in self.mappings['employment_type'] else None

            # Get the description of the job
            description = None

            # Get the publishing date of the job
            published_on = None

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