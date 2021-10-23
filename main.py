import TradingEconomicsScraper as tes

# Exemplary usage -> obtain data published on the Trading Economics website,
#                    compare indications in terms of 'generalised' favourability.
#                    The result of such an analysis may be used e.g. as the
#                    suggestion to what bet to make in case of Forex trading?
#
#                    Display


def main():
    # Obtaining dataframes with indicators
    print('Begin scraping data...\n')
    euro = tes.scrape_data('euro-area')
    us = tes.scrape_data('united-states')
    print('Done!\n')

    # Saving dataframes
    print('Saving dataframe to .tex files...\n')
    f1 = open("euro_area.tex", 'w')
    f2 = open('united-states.tex', 'w')

    f1.write(euro.to_latex(index=False))
    f2.write(us.to_latex(index=False))

    f1.close()
    f2.close()
    print('Done!\n')

    # Comparing dataframes
    print('Begin Comparison...\n')
    EUR_uh, US_uh = tes.compare_dataframes(euro, us, True)
    print("\nComparison results number of indications of higher economic performance in:\n")
    print("Eurozone (A)  = " + str(EUR_uh))
    print("United States (B) = " + str(US_uh))

    print('Done.\n')


if __name__ == '__main__':
    main()
