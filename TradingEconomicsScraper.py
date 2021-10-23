# Dependency imports
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd


# Array of economic indicators for 'smaller is more favourable' type regional comparison

smaller_fav_idx = ['UnemploymentRate',
                   'InflationRate',
                   'InterestRate',
                   'GovernmentDebttoGDP',
                   'CorporateTaxRate',
                   'PersonalIncomeTaxRate',
                   'UnemploymentRate',
                   'YouthUnemploymentRate',
                   'LabourCosts',
                   'SalesTaxRate'
                   ]


# Array of economic indicators for 'greater is more favourable' type regional comparison

bigger_fav_idx = [
    'GDPGrowthRate',
    'BusinessConfidence',
    'ManufacturingPMI',
    'ServicesPMI',
    'ConsumerConfidence',
    'RetailSalesMoM',
    'GDPpercapitaPPP',
    'ForeignExchangeReserves']

_table_header = ['Indicator', 'WhoseIsBetter']


# Helper function - index comparison by higher indicator value.
# compare sets of two indicators by the appropriate type; the greater indicator value in region A,the
# better the general outlook by comparison with region B.
# E.g. higher GDP growth rate in region A, than in region B.
def _compare_growth_type_favourability(indicator_set_region_1: pd.DataFrame, indicator_set_region_2: pd.DataFrame) -> dict:
    p1_vals = {}
    p2_vals = {}

    print('Scraping growth type favourable indices:\n')
    print('First dataframe... \n')
    for index, row in indicator_set_region_1.iterrows():
        for name_idx in bigger_fav_idx:
            if name_idx in row['Indicator']:
                p1_vals[name_idx] = [
                    float(row['Last']), float(row['Previous'])]
                continue

    print("Done.\n")
    print('Second dataframe... \n')
    for index, row in indicator_set_region_2.iterrows():
        for name_idx in bigger_fav_idx:
            if name_idx in row['Indicator']:
                p2_vals[name_idx] = [
                    float(row['Last']), float(row['Previous'])]
                continue

    print(p1_vals)
    print(p2_vals)
    print("Done.\n")
    df_growth_comparison = {}
    print("Beginning comparison...\n")
    for name_idx in bigger_fav_idx:
        if (p1_vals[name_idx][0] - p1_vals[name_idx][1]) > (p2_vals[name_idx][0] - p2_vals[name_idx][1]):
            df_growth_comparison[name_idx] = 'A'

        elif (p1_vals[name_idx][0] - p1_vals[name_idx][1]) < (p2_vals[name_idx][0] - p2_vals[name_idx][1]):
            df_growth_comparison[name_idx] = 'B'

        else:
            df_growth_comparison[name_idx] = 'EQUAL'

    print("Done.\n")
    return df_growth_comparison


# Helper function - index comparison by smaller indicator value.
# compare sets of two indicators by the appropriate type; the smaller indicator value in region A,the
# better the general outlook by comparison with region B.
# E.g. smaller inflation rate in region A, than in region B.
#
# input: DataFrame (Pandas module) type -> set of indicators scraped with 'scrape_data' (TradingEconomicsScraper) function.
# output: Dictionary of index comparison results
def _compare_fall_type_favourability(indicator_set_region_1: pd.DataFrame, indicator_set_region_2: pd.DataFrame) -> dict:
    p1_vals = {}
    p2_vals = {}

    print('Scraping fall type favourable indices:\n')
    print('First dataframe... \n')
    for index, row in indicator_set_region_1.iterrows():
        for name_idx in smaller_fav_idx:
            if name_idx in row['Indicator']:
                p1_vals[name_idx] = [
                    float(row['Last']), float(row['Previous'])]
                continue

    print("Done.\n")
    print('Second dataframe... \n')
    for index, row in indicator_set_region_2.iterrows():
        for name_idx in smaller_fav_idx:
            if name_idx in row['Indicator']:
                p2_vals[name_idx] = [
                    float(row['Last']), float(row['Previous'])]
                continue

    print("Done.\n")
    df_decrease_comparison = {}
    print("Beginning comparison...\n")

    for name_idx in smaller_fav_idx:
        if (p1_vals[name_idx][0] - p1_vals[name_idx][1]) > (p2_vals[name_idx][0] - p2_vals[name_idx][1]):
            df_decrease_comparison[name_idx] = 'B'

        elif (p1_vals[name_idx][0] - p1_vals[name_idx][1]) < (p2_vals[name_idx][0] - p2_vals[name_idx][1]):
            df_decrease_comparison[name_idx] = 'A'

        else:
            df_decrease_comparison[name_idx] = 'EQUAL'

    print("Done.\n")

    return df_decrease_comparison


# Compare two sets of economic indicators from two different regions.
# The result is quite arbitrarily defined 'economic stability/prosperity' (?)
# based on the outcome of the analysis, taking into consideration provided indicatiors.
#
# input: DataFrame (Pandas module) type -> set of indicators scraped with 'scrape_data' (TradingEconomicsScraper) function.
# output: Dictionary of index comparison results
def compare_dataframes(A, B, wanna_stf):
    G_type = _compare_growth_type_favourability(A, B)
    S_type = _compare_fall_type_favourability(A, B)

    print(G_type)
    print(S_type)
    A_vals = 0
    B_vals = 0

    for key in G_type:
        if G_type[key] == 'A':
            A_vals += 1
        elif G_type[key] == 'B':
            B_vals += 1

    for key in S_type:
        if S_type[key] == 'A':
            A_vals += 1
        elif S_type[key] == 'B':
            B_vals += 1

    return A_vals, B_vals

    if wanna_stf == True:
        pass


# Helper function -> updating the value of the dictionary based on the index
def _update_dict_val(idx, dict, td):
    td = td.replace("\r", "")
    td = td.replace("\n", "")

    if idx == 0:
        td = td.replace(" ", "")
        dict.update({'Indicator': td})
    elif idx == 1:
        dict.update({"Last": td})
    elif idx == 2:
        dict.update({"Reference": td})
    elif idx == 3:
        dict.update({"Previous": td})
    elif idx == 4:
        dict.update({"Range": td})
    elif idx == 5:
        dict.update({"Frequency": td})


# Obtain data from the front-end of the Trading Economics website
#
# input: string; name of the region -> indicator data of which are to be scraped
# output: DataFrame (Pandas module) -> indicator data
def scrape_data(region: str) -> pd.DataFrame:

    url = "https://tradingeconomics.com/" + region + "/indicators"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    table_head = ['Indicator', 'Last', 'Reference',
                  'Previous', 'Range', 'Frequency']

    df = pd.DataFrame(columns=table_head)

    for tr in soup.find_all('tr')[:-5]:
        tds = tr.find_all('td')
        frame_row = {'Indicator': "", 'Last': "", 'Reference': "",
                     'Previous': "", 'Range': "", 'Frequency': ""}
        i_pos = 0
        for t_tag in tds:
            _update_dict_val(i_pos, dict=frame_row, td=t_tag.text.strip())
            i_pos += 1
        df = df.append(frame_row, ignore_index=True)

    return df
