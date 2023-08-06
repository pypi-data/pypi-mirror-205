from typing import List
from bs4 import BeautifulSoup
from requests import get
import os
import zipfile


def is_zip(file_path):
    try:
        with zipfile.ZipFile(file_path) as zip_file:
            # If we can open the file as a zip file, then it was probably saved as a zip
            return True
    except zipfile.BadZipFile:
        # If opening the file as a zip file raises a BadZipFile exception, then it's not a zip file
        return False


def search_baiscope(query):
    url = f'https://www.baiscopelk.com/?s={query}'
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.findAll('article')
    if not articles:
        return 'Empty'
    return_list = []
    for article in articles:
        return_list.append({'title': article.h2.get_text().strip(), 'page_url': article.h2.a['href']})
    return return_list


def search_cineru(query):
    url = f'https://cineru.lk/?s={query}'
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.findAll('article')
    if not articles:
        return 'Empty'
    return_list = []
    for article in articles:
        return_list.append({'title': article.h2.get_text().strip(), 'page_url': article.h2.a['href']})
    return return_list


def download_baiscope(page_url, path=None):
    try:
        os.mkdir(path)
        print(f'{path} folder created\n\n')
    except:
        pass
    response = get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    file_url = soup.find('p', {'style': "padding: 0px; text-align: center;"}).a['href']
    file_name = file_url.split('/')[-1]
    if '?' in file_name:
        file_name = file_url.split('/')[-2]
    if '.zip' not in file_name:
        file_name = file_name.replace('-zip', '') + '.zip'
    try:
        if path:
            file_path = f"{path}/{file_name}"
        else:
            file_path = file_name
        file = open(file_path, 'wb')
        file.write(get(file_url).content)
        file.close()
        if not is_zip(file_path):
            os.rename(file_path, file_path.replace('.zip', '.rar'))
        return f'Downloaded : {file_name}\nfrom baiscopelk.com\n'
    except:
        return 'Error in download_baiscope()'


def download_cineru(page_url, path=None):
    try:
        os.mkdir(path)
        print(f'{path} folder created\n\n')
    except:
        pass
    response = get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    file_url = soup.find('a', {'id': "btn-download"})['data-link']
    file_name = file_url.split('/')[-1]
    if '?' in file_name:
        file_name = file_url.split('/')[-2]
    if '.zip' not in file_name:
        file_name = file_name.replace('-zip', '') + '.zip'
    try:
        if path:
            file_path = f"{path}/{file_name}"
        else:
            file_path = file_name
        file = open(file_path, 'wb')
        file.write(get(file_url).content)
        file.close()
        if not is_zip(file_path):
            os.rename(file_path, file_path.replace('.zip', '.rar'))
        return f'Downloaded : {file_name}\nfrom cineru.lk\n'
    except:
        return 'Error in download_cineru()'


def bulk_cineru(bulk_url):
    response = get(bulk_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    path = soup.title.get_text()
    episode_links = soup.findAll('a', {'class': 'epi_item'})
    for episode in episode_links:
        print(download_cineru(episode['href'], path))
    print('Done!')
    return True


def bulk_baiscope(bulk_url):
    response = get(bulk_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    path = soup.title.get_text()
    episode_links = soup.findAll('td')
    for episode in episode_links:
        try:
            print(download_baiscope(episode.a['href'], path))
        except:
            pass
    print('Done!')
    return True


class SinhalaSubtitles:
    def search(query: str, site: str = None) -> List[dict]:
        """
        Search for Sinhala subtitles using a given query and website.

        Args:
            query (str): The search query.
            site (str, optional): The website to search for subtitles on. Can be 'baiscopelk', 'cineru', or None to
                                  search both websites. Defaults to None.

        Returns:
            A list of dictionaries, where each dictionary represents a Sinhala subtitle file and contains the following
            keys:
            - 'title': The title of the subtitle file.
            - 'url': The URL of the subtitle file.
            - 'site': The website the subtitle file is from ('baiscopelk' or 'cineru').
        """
        if site == 'baiscopelk':
            return search_baiscope(query)
        elif site == 'cineru':
            return search_cineru(query)
        elif site is not None:
            text = 'Only baiscopelk and cineru can be use as site parameter. Then you search only on the given website. ' \
                   'Default searches both sites.'
            print(text)
        else:
            return search_baiscope(query) + search_cineru(query)

    def download(page_url: str) -> bool:
        """
        Download a Sinhala subtitle file for a given URL.

        Args:
            page_url (str): The URL of the webpage containing the subtitle file.

        Returns:
            A boolean indicating whether the download was successful or not.
        """
        if 'cineru' in page_url:
            return download_cineru(page_url, 'Downloads')
        elif 'baiscopelk' in page_url:
            return download_baiscope(page_url, 'Downloads')
        else:
            print('Wrong url. first search subtitle. and use returning links')
            return False

    def bulk(bulk_url: str) -> bool:
        """
        Download a bulk of Sinhala subtitle files for a TV series.

        Args:
            bulk_url (str): The URL of the webpage containing the Sinhala subtitle files.

        Returns:
            A boolean indicating whether the download was successful or not.
        """
        if 'cineru' in bulk_url:
            return bulk_cineru(bulk_url)
        elif 'baiscopelk' in bulk_url:
            return bulk_baiscope(bulk_url)
        else:
            print('Wrong url.')
            return False
