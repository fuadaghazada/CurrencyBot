from aznTodayScraper import AznTodayScraper

# TEST
scraper = AznTodayScraper()
scraper.fetch_table()
print(scraper.get_best_rate())
