import os
import re
import time
import requests
from tqdm import tqdm
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class WebScraper:
    def __init__(self, chrome_driver_path):
        self.driver = self.create_driver(chrome_driver_path)

    def create_driver(self, chrome_driver_path):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
        return driver

    def create_folder(self, url):
        self.url = url
        parsed_url = urlparse(self.url)
        website_name = re.sub(r'\W+', '', parsed_url.netloc)
        timestamp = time.strftime("%Y%m%d%H%M%S")
        folder_name = f"{website_name}_{timestamp}"
        os.makedirs(folder_name, exist_ok=True)
        return folder_name

    def is_valid(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def download(self, url, pathname):
        if not os.path.isdir(pathname):
            os.makedirs(pathname)

        try:
            response = requests.get(url, stream=True)
            file_size = int(response.headers.get("Content-Length", 0))
            filename = os.path.join(pathname, url.split("/")[-1])

            progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)

            with open(filename, "wb") as f:
                for data in progress.iterable:
                    # write data read to the file
                    f.write(data)
                    # update the progress bar manually
                    progress.update(len(data))
        except Exception as e:
            print(f"Error occurred while downloading {url}. Error: {e}")
            pass

    def get_all_images(self, attribute):
        driver = self.driver
        soup = BeautifulSoup(driver.page_source, "lxml")
        urls = []

        for img in tqdm(soup.find("body").find_all("img"), "Extracting images"):
            img_url = img.attrs.get(attribute)
            if not img_url:
                continue

            img_url = urljoin(self.url, img_url)
            try:
                pos = img_url.index("?")
                img_url = img_url[:pos]
            except ValueError:
                pass

            try:
                if self.is_valid(img_url):
                    urls.append(img_url)
            except Exception as e:
                print(f"Error occurred while processing image URL: {img_url}. Error: {e}")
                pass

        return urls

    def save_images(self):
        images_folder = os.path.join(self.folder_name, "images")
        os.makedirs(images_folder, exist_ok=True)

        imgs = self.get_all_images("src") + self.get_all_images("data-srcset")

        if not imgs:
            print("No images found on the page.")
            return

        for img in imgs:
            self.download(img, images_folder)

        return images_folder

    def save_tables(self):
        driver = self.driver
        try:
            WebDriverWait(driver, 10).until(
                lambda d: d.find_elements_by_css_selector("table") or d.find_elements_by_css_selector(".dataTables_wrapper")
            )
        except TimeoutException:
            print("No tables found on the page.")
            return

        tables_standard = driver.find_elements_by_css_selector("table")
        tables_special = driver.find_elements_by_css_selector(".dataTables_wrapper")
        tables = tables_standard + tables_special

        for i, table in tqdm(enumerate(tables), desc="Saving tables", total=len(tables)):
            table_html = table.get_attribute("outerHTML")
            try:
                table_df = pd.read_html(table_html, header=0)[0]
                table_path = os.path.join(self.folder_name, f"table_{i}.csv")
                table_df.to_csv(table_path, index=False)
                print(f"Table {i} saved as: {table_path}")
            except ValueError:
                print(f"Table {i} could not be saved. Skipping...")

    def beautifulsoup_extract_text_fallback(self, response_content):
        soup = BeautifulSoup(response_content, 'lxml')
        text = soup.find_all(string=True)
        cleaned_text = ''
        blacklist = [
            '[document]', 'Sign Up',
            'noscript',
            'header',
            'html',
            'meta',
            'head',
            'input', 'footer',
            'script',
            'style', ]
        for item in text:
            if item.parent.name not in blacklist:
                cleaned_text += '{} '.format(item)
        cleaned_text = cleaned_text.replace('\t', '')
        return cleaned_text.strip()

    def save_extracted_text(self):
        text_folder = os.path.join(self.folder_name, "text")
        if not os.path.isdir(text_folder):
            os.makedirs(text_folder)
        extracted_text = self.beautifulsoup_extract_text_fallback(self.driver.page_source)

        file_name = os.path.join(text_folder, "extracted_text.txt")
        with tqdm(total=1, desc="Saving text") as pbar:
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(extracted_text)
                pbar.update(1)

        print(f"Text saved as extracted_text.txt in the {text_folder} folder")

    def process_website(self, url):
        self.folder_name = self.create_folder(url)
        self.driver.get(self.url)

        print("********************* DOWNLOADING BEGINS *********************")
        print("--------------------------- TABLES ---------------------------")
        self.save_tables()
        print("--------------------------- IMAGES ---------------------------")
        self.save_images()
        print("--------------------------- TEXT ---------------------------")
        self.save_extracted_text()

        self.driver.quit()