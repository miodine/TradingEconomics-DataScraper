# TradingEconomics-DataScraper
## About 
Data scraping python utility allowing to aggregate data from TradingEconomics. Not related to the TradingEconomicsAPI; allows one to access only the data
directly accessible on the website, functionality built solemnly on the data presented for free to the public. 

## Functionality 
Current functionality allows one to scrape macroeconomic data from any region available on TradingEconomics, store it in DataFrame format (Pandas module), 
and to compare two such sets in terms of 'economic strenght' of any two regions, taking into consideration change in available indicators (e.g. change
in inflation rate, GDP, consumer confidence etc.). 

## Installation
Dependencies:
* Pandas 
* NumPy (unused for now)
* Requests
* BeautifulSoup (4)
The module is not yet published on pip, so for now - copy and paste the 'TradingEconomicsScraper.py' to your working directory, 
and use the import directive to access its functions (by filename, if unchanged, see the *Usage* section).

## Usage 

### Scraping data: 

```Python3
import TradingEconomicsScraper as tes

def main():
    euro = tes.scrape_data('euro-area')
``` 
Result:

![image](https://user-images.githubusercontent.com/48156138/138557573-7487a4f4-46ef-4f55-b1df-7bebe5bee69e.png)

### DataFrame comparison
See current main.py
## Todo:
- xD
