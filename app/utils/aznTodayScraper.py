import math

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from getter import get_page_content
from log import get_logger

# Logger
logger = get_logger('mainlog')

'''
    AZNTODAY Data Scraper (via Headless Chrome Browser)
'''

class AznTodayScraper:

    def __init__(self):
        self.URL = "https://azn.today/"

        self.headers = []
        self.tableData = []


    '''
        Fetching the currency table
    '''

    def fetch_table(self):
        # Getting the page content
        waitComponent = EC.presence_of_element_located((By.CSS_SELECTOR, "body > div > main > div.table-wrap > table > tbody > tr:nth-child(2)"))
        content = get_page_content(self.URL, waitComponent = waitComponent)

        # Safety check for nullity
        if content is None:
            logger.info("[ERROR]: Table cannot be obtained")
            return None

        # Parser
        soup = BeautifulSoup(content, 'html.parser')

        # Table rows
        rows = soup.find("div", {"class": "table-wrap"}).find_all("tr")

        if len(rows) <= 0:
            logger.info("[ERROR]: Table Rows cannot be obtained")
            return None

        headers = [header.text for header in rows[0].find_all("th")]
        tableData = []

        # Parsing through the table
        for i, row in enumerate(rows):
            if i == 0:
                continue
            else:
                column_data = [column.text for column in row.find_all("td")]

                # Data dict for each rows: key the header - value the corresponding data
                data = {}
                for i, header in enumerate(headers):
                    data[header] = column_data[i] if column_data[i] else None

                # Keeping the column record
                tableData.append(data)

        self.headers = headers
        self.tableData = tableData

        # Returning the table data
        return tableData


    '''
        Determine the best rate from the given table data
    '''

    def get_best_rate(self):
        # Safety check for data size
        if len(self.tableData) == 0:
            logger.info("[WARNING]: Table Data is empty")
            return None

        # Sorting
        sortedBuyRates = sorted(self.tableData, key = lambda x: float(x['Buy Cash']), reverse=True)
        bestBuyRate = sortedBuyRates[0]

        sortedSellRates = sorted(self.tableData, key = lambda x: float(x['Sell Cash']) if x['Sell Cash'] != "0.0000" else math.inf)
        bestSellRate = sortedSellRates[0]

        # Returning
        return {
            'buy': bestBuyRate,
            'sell': bestSellRate
        }
