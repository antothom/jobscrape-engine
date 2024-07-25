import xml.etree.ElementTree as ET
import requests

# Sa

response = requests.get('https://smacc.jobs.personio.de/xml?language=de')

# Parse the XML data
root = ET.fromstring(response.text)
data = root.findall('position')
# Extracting specific data
for position in data:
    id_ = position.find('id').text
    office = position.find('office').text
    department = position.find('department').text
    recruiting_category = position.find('recruitingCategory').text
    name = position.find('name').text

    print(f"ID: {id_}")
    print(f"Office: {office}")
    print(f"Department: {department}")
    print(f"Recruiting Category: {recruiting_category}")
    print(f"Name: {name}")

    print("\nJob Descriptions:")
    for job_description in position.find('jobDescriptions').findall('jobDescription'):
        job_name = job_description.find('name').text
        job_value = job_description.find('value').text.strip()
        print(f"  {job_name}: {job_value}")

    employment_type = position.find('employmentType').text
    seniority = position.find('seniority').text
    schedule = position.find('schedule').text
    years_of_experience = position.find('yearsOfExperience').text
    occupation = position.find('occupation').text
    occupation_category = position.find('occupationCategory').text
    created_at = position.find('createdAt').text

    print(f"\nEmployment Type: {employment_type}")
    print(f"Seniority: {seniority}")
    print(f"Schedule: {schedule}")
    print(f"Years of Experience: {years_of_experience}")
    print(f"Occupation: {occupation}")
    print(f"Occupation Category: {occupation_category}")
    print(f"Created At: {created_at}")

