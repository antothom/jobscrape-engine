from abc import abstractmethod

import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET
import re




class DataFetcher:
    def __init__(self, url: list, source_type: str, company_name: str) -> None:
        self.url = url
        self.source_type = source_type
        self.data = None
        self.company_name = company_name

    @classmethod
    def create(cls, url, source_type, company_name):
        if source_type == 'html':
            return HTMLDataFetcher(url, source_type, company_name)
        elif source_type == 'xml':
            return XMLDataFetcher(url, source_type,company_name)
        elif source_type == 'json':
            return JSONDataFetcher(url, source_type,company_name)
        else:
            raise ValueError('Invalid source type')
        x


class HTMLDataFetcher(DataFetcher):
    def __init__(self, url, source_type, company_name):
        super().__init__(url, source_type, company_name)

    def get_data(self):
        response = requests.get(self.url[0])
        soup = BeautifulSoup(response.text, 'html.parser')
        self.data = soup


class XMLDataFetcher(DataFetcher):
    def __init__(self, url, source_type, company_name):
        super().__init__(url, source_type, company_name)

    def get_data(self):
        headers = {"accept": "application/xml"}

        response = requests.get(self.url[0], headers=headers)
        # Parse the XML data
        try:
            root = ET.fromstring(response.text)
        except ET.ParseError:
            raise ValueError('Invalid XML data')

        self.data = root.findall('position')


class JSONDataFetcher(DataFetcher):
    def __init__(self, url, source_type, company_name):
        super().__init__(url, source_type, company_name)

    def get_data(self):
        response = requests.get(self.url[0])
        self.data = response.json()