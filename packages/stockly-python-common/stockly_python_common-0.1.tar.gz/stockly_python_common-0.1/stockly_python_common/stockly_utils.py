import requests
from stockly_python_common.query import Query



def _common(url:str,key:str,query:str,subkey="data",res:bool=False,return_type=[]):
    try:
        response = requests.post(url,json={"query": query}, timeout=15)
        if response.status_code == 200:
            response = response.json()
            status=response["data"][key]["status"]
            if res and status !=400: 
                return response["data"][key]
            elif response["data"][key]["message"] == "Success":
                return response["data"][key][subkey]
            return response["data"][key]
        return return_type
    except Exception as error:
        print(error)
        return return_type


class StocklyUtilsClient:

    def __init__(self, api_key: str, auth_url: str, api_url: str) ->None:
        self.api_key = api_key
        self.auth_url = auth_url
        self.api_url = api_url



    def get_stock_current_price(self, symbol: str)->list:
        """_summary_: This function is used to get the current or real time price of the stock.

        Args:
            symbol (str): Stock symbol

        Returns:
            str: Current or real time price of the stock.
        """
        query = Query.get_stock_current_price(
            ticker=symbol, api_key=self.api_key)
        return _common(url=self.api_url,key="getStockCurrentPrice",query=query,subkey="price",return_type=[])


    def get_stock_peers(self,symbol: str)->list:
        """_summary_: This function is used to get the stock peers which is the group 
        of companies that trade on the same exchange,are in the same industry and have
        a similar market capitalizations.
        
        Args:
            symbol (str): Stock symbol
        
        Returns:
            list: List having dict with keys as symbol and peersList.
        """
        query = Query.get_stock_peers(
            ticker=symbol, apikey=self.api_key)
        return _common(url=self.api_url, key="getStockPeers",query=query,return_type=[])


    def get_ticker_search_data(self,symbol:str,exchange:str)->list:
        """_summary_:This function is used to search ticker by it's symbol or character from particular exchange.

        Args:
            symbol (str): stock symbol
            
            exchange (str): Values for exchange are ETF, MUTUAL_FUND, COMMODITY, INDEX, CRYPTO,
            FOREX, TSX, AMEX, NASDAQ, NYSE, EURONEXT, XETRA, NSE and LSE

        Returns:
            list: List of dictionaries having keys as symbol,stockExchange,currency and exchangeShortName.
        """
        query = Query.get_ticker_search_data(
            ticker=symbol,exchange=exchange, apikey=self.api_key)
        return _common(url=self.api_url, key="getTickerSearchData",query=query,return_type=[])


    def get_exchange_screener(self,exchange:str,market_capital:int,beta:int,volume:int,limit:int)->list:
        """_summary_: This function is used to search the stocks with particular exchange.

        Args:
            exchange (str): Values for exchange are nyse, nasdaq, amex, euronext, tsx, etf and mutual_fund
            
            market_capital (int): Market capital of the stock
            
            beta (int): Beta describes the movement in a stock
            
            volume (int): Volume of the stock
            
            limit (int): Number of results required as per requirement

        Returns:
            list: List of dictionaries having keys as symbol, volume, beta, lastAnnualDividend, exchangeShortName
            isEtf, price, marketCap, isActivelyTrading, companyName and sector.
        """
        query = Query.get_exchange_screener(exchange=exchange,limit=limit, apikey=self.api_key,market_capital=market_capital,beta=beta,
                                            volume=volume
                                            )
        return _common(url=self.api_url, key="getExchangeScreener",query=query,return_type=[])


    def get_sector_screener(self,exchange:str,sector:str,market_capital:int,beta:int,volume:int,limit:int)->list:
        """_summary_: This function is used to search the stocks with particular sector.

        Args:
            exchange (str): Values for exchange are nyse, nasdaq, amex, euronext, tsx, etf and mutual_fund
            
            sector (str): Values for Consumer Cyclical, Energy, Technology, Industrials, Financial Services,
            Basic Materials, Communication Services, Consumer Defensive, Healthcare, Real Estate, Utilities,
            Industrial Goods, Financial, Services and Conglomerates
            
            market_capital (int): Market capital of the stock
            
            beta (int): Beta describes the movement in a stock
            
            volume (int): Volume of the stock
            
            limit (int): Number of results required as per requirement

        Returns:
            list: List of dictionaries having keys as symbol, volume, beta, lastAnnualDividend, exchangeShortName
            isEtf, price, marketCap, isActivelyTrading, companyName and sector.
        """
        query = Query.get_sector_screener(exchange=exchange,limit=limit, apikey=self.api_key,
                                        market_capital=market_capital,beta=beta,
                                        volume=volume,sector=sector
                                        )
        return _common(url=self.api_url, key="getSectorScreener",query=query,return_type=[])
        

    def percent_change_data(self,symbol:str)->list:
        """_summary_: This function is used to get the price percentage change for multiple timeframes.

        Args:
            symbol (str): Stock symbol

        Returns:
            list: List of price change for different timeframes.
        """
        query = Query.percent_change_data(ticker=symbol,apikey=self.api_key)
        return _common(url=self.api_url, key="percentChangeData",query=query,return_type=[])


    def get_stock_price_screener(self,price:int,country:str,type:str)->list:
        """_summary_: This function is used to filter the stocks on the basis of stock price as per requirements. 

        Args:
            price (int): Required price to filter the stocks
            
            country (str): Required country to filter the stock
            
            type (str): Values for type are priceMoreThan(to get the stocks having price more than) and
            priceLowerThan(to get the stocks having price less than) 

        Returns:
            list: List of dictionaries having keys as symbol, volume, beta, lastAnnualDividend, exchangeShortName,
            isEtf, price, marketCap, isActivelyTrading, companyName and sector.
        """
        query = Query.get_stock_price_screener(price=price,country=country,type=type,apikey=self.api_key)
        return _common(url=self.api_url, key="getStockPriceScreener",query=query,return_type=[])


    def get_sectors_ratio_data(self,exchange:str,date:str)->list:
        """_summary_: This function is used to get the PE ratio for sectors.
        PE ratio is the average price to earnings ratio.

        Args:
            exchange (str): Stock exchange
            
            date (str): Date(to get sector pe ratio on particular date)

        Returns:
            list: List of dictionaries for various sectors with keys as exchange, pe, date and sector.
        """
        query = Query.get_sectors_ratio_data(exchange=exchange,date=date,apikey=self.api_key)
        return _common(url=self.api_url, key="getSectorsRatioData",query=query,return_type=[])
    

    def get_industries_pe_ratio(self,exchange:str,date:str)->list:
        """_summary_: This function is used to get the PE ratio for industries.
        PE ratio is the average price to earnings ratio.

        Args:
            exchange (str): Stock exchange
            
            date (str): Date(to get industries pe ratio on particular date)

        Returns:
            list: List of dictionaries for various industries with keys as exchange, pe, date and industry.
        """
        query = Query.get_industries_pe_ratio(exchange=exchange,date=date,apikey=self.api_key)
        return _common(url=self.api_url, key="getIndustriesPERatio",query=query,return_type=[])
    

    def get_stock_market_performance_data(self)->list:
        """_summary_: This function is used to get the percent change in each sector's companies.

        Returns:
            list: List of dictionaries for various sectors with their pecent change.
        """
        query = Query.get_stock_market_performance_data(self.api_key)
        return _common(url=self.api_url, key="getStockMarketPerformanceData",query=query,return_type=[])


    def get_financial_ratios_of_companies(self,symbol:str)->list:
        """_summary_: This function is used to get the ratios for each financial statement.

        Args:
            symbol (str): Stock symbol

        Returns:
            list: List of ratios for each financial statement.
        """
        query = Query.get_financial_ratios_of_companies(ticker=symbol,apikey=self.api_key)
        return _common(url=self.api_url, key="getFinancialRatiosOfCompanies",query=query,return_type=[])


    def get_target_price_summary(self,symbol:str)->list:
        """_summary_: This function is used to get the target price summary for the stock. 

        Args:
            symbol (str): Stock symbol

        Returns:
            list: List if dict having keys as symbol, lastMonth, lastMonthAvgPriceTarget, lastQuarter,
            lastQuarterAvgPriceTarget, lastYear, lastYearAvgPriceTarget, allTime, allTimeAvgPriceTarget
            and publishers.
        """
        query = Query.get_target_price_summary(ticker=symbol,apikey=self.api_key)
        return _common(url=self.api_url, key="getTargetPriceSummary",query=query,return_type=[])


    def get_target_price(self,symbol:str,country:str)->dict:
        """_summary_: This function is used to get the analysts' projection of a security's future price.

        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock

        Returns:
            dict: Dict having high, median, low, average and current price.
        """
        query = Query.get_target_price(symbol=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getTargetPrice",query=query,return_type={})
    
    
    def get_end_of_day_price(self,country:str,symbol:str)->dict:
        """_summary_: This function is used to get the latest end of the day price for the stock.

        Args:
            country (str): Required country to filter the stock
            
            symbol (str): Stock symbol

        Returns:
            dict: Dict having keys as symbol, exchange, mic_code, currency, datetime and close.
        """
        query = Query.get_end_of_day_price(symbol=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getEndOfDayPrice",query=query,return_type={})
    
    
    def get_current_price(self,country:str,symbol:str)->dict:
        """_summary_: This function is used to get the real time price or current price of the stock.

        Args:
            country (str): Required country to filter the stock
            
            symbol (str): Stock symbol

        Returns:
            dict: Dict having key as price.
        """
        query = Query.get_current_price(symbol=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getCurrentPrice",query=query,return_type={})
    

    def get_insider_traders(self,symbol:str,country:str)->dict:
        """_summary_: This function is used to get the trading information performed by insiders.

        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock

        Returns:
            dict: Dict having keys as meta and values.
            Metaobject consists of general information about the given symbol.
        """
        query = Query.get_insider_traders(symbol=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getInsiderTraders",query=query,return_type={})


    def get_delisted_companies(self)->list:
        """_summary_: This function is used to get the list of delisted companies from the US exchanges.

        Returns:
            list: List of dictionaries having keys as symbol, companyName, exchange, ipoDate and delistedDate.
        """
        query = Query.get_delisted_companies(apkey=self.api_key)
        return _common(url=self.api_url ,key="getDelistedCompanies",query=query,return_type=[])

    
    def get_etf_list_data(self)->list:
        """_summary_: This function is used to get the all ETF symbols.

        Returns:
            list: List of dictionaries having keys as symbol, name, price, exchange and exchangeShortName.
        """
        query = Query.get_etf_list_data(self.api_key)
        return _common(url=self.api_url, key="getETFListData",query=query,return_type=[])


    def get_symbol_change(self)->list:
        """_summary_: This function is used to get the get the info if there is any symbol change happened.

        Returns:
            list: List of dictionaries having keys as symbol, name, oldSymbol and newSymbol.
        """
        query = Query.get_symbol_change(apikey=self.api_key)
        return _common(url=self.api_url, key="getSymbolChange",query=query,return_type=[])
    

    def get_s_and_p_companies(self)->list:
        """_summary_: This function is used to get the all S&P 500 constituents.

        Returns:
            list: List of dictionaries for S & p 500 stock symbols having keys as
            cik, dateFirstAdded, founded, headQuarter, name, sector, subSector and symbol.
        """
        query = Query.get_s_and_p_companies(apikey=self.api_key)
        return _common(url=self.api_url, key="getSpCompanies",query=query,return_type=[])


    def get_nasdaq_companies(self)->list:
        """_summary_: This function is used to get the all NASDAQ companies.

        Returns:
            list: List of dictionaries for NASDAQ stock symbols having keys as
            cik, dateFirstAdded, founded, headQuarter, name, sector, subSector and symbol.
        """
        query = Query.get_nasdaq_companies(apikey=self.api_key)
        return _common(url=self.api_url, key="getNasdaqCompanies",query=query,return_type=[])


    def get_crypto_symbol(self)->list:
        """_summary_: This function is used to get all major crypto currencies, price are updated in realtime.
        Major crypto included Bitcoins, Ethereum, Ripple, EOS, Cardano, Bitcoin Cash.

        Returns:
            list: List of dictionaries for crypto currencies having keys as symbol ,price, changesPercentage,
            change, dayLow, dayHigh, yearHigh, yearLow, marketCap, priceAvg50, priceAvg200, volume, avgVolume
            and exchange.
        """
        query = Query.get_crypto_symbol(apikey=self.api_key)
        return _common(url=self.api_url, key="getCryptoSymbol",query=query,return_type=[])


    def get_forex_symbol(self)->list:
        """_summary_: This function is used to get all major forex currencies.

        Returns:
            list: List of dictionaries for crypto currencies having keys as ask, bid, changes,
            date, high, low, open and ticker.
        """
        query = Query.get_forex_symbol(apikey=self.api_key)
        return _common(url=self.api_url, key="getForexSymbol",query=query,return_type=[])
    
    
    def get_dow_jones_companies(self)->list:
        """_summary_: This function is used to get companies in the Dow Jones.

        Returns:
            list: List of dictionaries for companies in the Dow Jones having keys cik, dateFirstAdded,
            founded, headQuarter, name, sector, subSector and symbol.
        """
        query = Query.get_dow_jones_companies(apikey=self.api_key)
        return _common(url=self.api_url, key="getDowjonesCompanies",query=query,return_type=[])


    def get_esg_score_data(self,symbol:str)->list:
        """_summary_: This function is used to get ESG score for the stock. 
        A company's ESG rating essentially represents its exposure to prolonged governance, social
        and environmental risks

        Args:
            symbol (str): Stock symbol

        Returns:
            list: List of dictionaries for different datetime having keys as ESGScore, acceptedDate, cik,
            companyName, date, environmentalScore, formType, governanceScore, socialScore, symbol and url.
        """
        query = Query.get_esg_score_data(symbol=symbol,apikey=self.api_key)
        return _common(url=self.api_url, key="getESGScoreData",query=query,return_type=[])


    def get_company_esg_risk_rating(self,symbol:str)->list:
        """_summary_: This function is used to get esg risk rating or industry rank for given stock symbol.

        Args:
            symbol (str): Stock symbol

        Returns:
            list: List of dictionaries for current year and previous years having keys as
            symbol, cik, companyName, industry, year, ESGRiskRating and industryRank.
        """
        query = Query.get_company_esg_risk_rating(symbol=symbol,apikey=self.api_key)
        return _common(url=self.api_url, key="getCompanyEsgRiskRating",query=query,return_type=[])


    def get_esg_bench_marking_by_sector_and_year(self,year:str)->list:
        """_summary_: This function is used to get sector's ESG benchmarking for given year.

        Args:
            year (str): Year for which ESG bechmarking required

        Returns:
            list: List of dictionaries for different sectors having keys as year, sector, environmentalScore,
            socialScore, governanceScore and ESGScore.
        """
        query = Query.get_esg_bench_marking_by_sector_and_year(year=year,apikey=self.api_key)
        return _common(url=self.api_url, key="getESGBenchmarkingBySectorAndYear",query=query,return_type=[])

    
    def get_company_quote_by_stock_name(self,symbol:str,country:str)->dict:
        """_summary_: This function is used to get the company quote for given stock symbol and country.

        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock

        Returns:
            dict: Dict having keys as symbol, name, exchange, mic_code, currency, datetime, timestamp,
            open, high, low, close, volume, previousClose, change, percentChange, averageVolume, 
            isMarketOpen and fifty_two_week.
        """
        query = Query.get_company_quote_by_stock_name(ticker=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getCompanyQuoteByStockName",query=query,return_type={})

    
    def get_company_outlook(self,symbol:str,country:str)->dict:
        """_summary_: This function is used to get the general information about the company.

        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock

        Returns:
            dict: Dict having keys as symbol, name, exchange, mic_code, sector, employees, website and description.
        """
        query = Query.get_company_outlook(ticker=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getCompanyOutlook",query=query,return_type={})
    

    def get_company_rating_by_stock_name(self,symbol:str)->list:
        """_summary_: This function is used to get the rating of a company based on its financial statement,
        discounted cash flow analysis, financial rations and its intrinsic value.

        Args:
            symbol (str): Stock symbol

        Returns:
            list: List of comapany ratings details and recommendation based on rating. 
        """
        query = Query.get_company_rating_by_stock_name(symbol=symbol,apikey=self.api_key)
        return _common(url=self.api_url, key="getCompanyRatingByStockName",query=query,return_type=[])
    
    
    def get_company_core_information(self,symbol:str)->list:
        """_summary_: This function is used to get the companies core information. 

        Args:
            symbol (str): Stock symbol

        Returns:
            list: List contains businessAddress, cik,exchange, fiscalYearEnd, mailingAddress,
            registrantName, sicCode, sicDescription, sicGroup, stateLocationstateLocation, 
            stateOfIncorporationsymbol and taxIdentificationNumber.
        """
        query = Query.get_company_core_information(symbol=symbol,apikey=self.api_key)
        return _common(url=self.api_url, key="getCompanyCoreInformation",query=query,return_type=[])
    

    def get_company_enterprise_value(self,symbol:str)->list:
        """_summary_: This function is used to get a company enterprise value. 

        Args:
            symbol (str): Stock symbol

        Returns:
            list: List contains symbol, date, stockPrice, numberOfShares, marketCapitalization,
            minusCashAndCashEquivalents, addTotalDebt and enterpriseValue.
        """
        query = Query.get_company_enterprise_value(symbol=symbol,apikey=self.api_key)
        return _common(url=self.api_url, key="getCompanyEnterpriseValue",query=query,return_type=[])


    def get_company_notes_due_by_stock_name(self,symbol:str)->list:
        """_summary_: This function is used to get a company notes due. 

        Args:
            symbol (str): Stock symbol

        Returns:
            list: List of dictionaries having keys as cik, exchange, title and symbol.
        """
        query = Query.get_company_notes_due_by_stock_name(symbol=symbol,apikey=self.api_key)
        return _common(url=self.api_url, key="getCompanyNotesDueByStockName",query=query,return_type=[])


    def get_company_key_metrics(self,symbol:str)->dict:
        """_summary_: This function is used to get the company key metrics.
        The change in company metrics is essential for valuating a company.

        Args:
            symbol (str): Stock symbol

        Returns:
            dict: Dict having keys as revenuePerShareTTM, netIncomePerShareTTM, operatingCashFlowPerShareTTM, 
            freeCashFlowPerShareTTM,cashPerShareTTM, bookValuePerShareTTM, tangibleBookValuePerShareTTM,
            shareholdersEquityPerShareTTM,interestDebtPerShareTTM, marketCapTTM, enterpriseValueTTM, peRatioTTM,
            priceToSalesRatioTTM, pocfratioTTM,pfcfRatioTTM, pbRatioTTM, ptbRatioTTM, evToSalesTTM, 
            enterpriseValueOverEBITDATTM, evToOperatingCashFlowTTM, evToFreeCashFlowTTM, earningsYieldTTM,
            freeCashFlowYieldTTM, debtToEquityTTM, debtToAssetsTTM, netDebtToEBITDATTM,currentRatioTTM,
            interestCoverageTTM, incomeQualityTTM, dividendYieldTTM, dividendYieldPercentageTTM, payoutRatioTTM, 
            salesGeneralAndAdministrativeToRevenueTTM, researchAndDevelopementToRevenueTTM, intangiblesToTotalAssetsTTM, 
            capexToOperatingCashFlowTTM, capexToRevenueTTM, capexToDepreciationTTM, stockBasedCompensationToRevenueTTM, 
            grahamNumberTTM, roicTTM, returnOnTangibleAssetsTTM, grahamNetNetTTM, workingCapitalTTM, tangibleAssetValueTTM, 
            netCurrentAssetValueTTM, investedCapitalTTM, averageReceivablesTTM, averagePayablesTTM, averageInventoryTTM, 
            daysSalesOutstandingTTM, daysPayablesOutstandingTTM, daysOfInventoryOnHandTTM, receivablesTurnoverTTM, 
            payablesTurnoverTTM, inventoryTurnoverTTM, roeTTM, capexPerShareTTM, dividendPerShareTTM and debtToMarketCapTTM.
        """
        query = Query.get_company_key_metrics(symbol=symbol,apikey=self.api_key)
        return _common(url=self.api_url, key="getCompanyKeyMetrics",query=query,return_type={})
    
    
    def get_market_capitalization_stock_data(self,symbol:str)->list:
        """_summary_: This function is used to get the market capitalization for given stock symbol.

        Args:
            symbol (str): Stock symbol

        Returns:
            list: List with date and market capitalization fot stock.
        """
        query = Query.get_market_capitalization_stock_data(symbol=symbol,apikey=self.api_key)
        return _common(url=self.api_url, key="getMarketCapitalizationStockData",query=query,return_type=[])
    
    
    def get_key_executives(self,symbol:str,country:str)->dict:
        """_summary_: This function is used to get the key executives of the company.
        Key executives are the people at the top of a company who make critical decisions that affect the company.

        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock

        Returns:
            dict: Dict having keys as meta and keyExecutives.
            Metaobject consists of general information about the given symbol.
        """
        query = Query.get_key_executives(symbol=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getKeyExecutives",query=query,return_type={})
    

    def get_company_disc_cash_flow(self,symbol:str)->dict:
        """_summary_: This function is used to get the stock discounted cash flow value.
        This value represents a stock intrinsic value calculated from its free cash flow analysis.

        Args:
            symbol (str): Stock symbol

        Returns:
            dict: Dict having keys as symbol, date, dcf and stockPrice.
        """
        query = Query.get_company_disc_cash_flow(symbol=symbol,apikey=self.api_key)
        return _common(url=self.api_url, key="getCompanyDiscCashflow",query=query,return_type={})


    def get_financial_statement(self,symbol:str,country:str)->dict:
        """_summary_: This function is used to get the complete income statement of a company and
        shows the company's revenues and expenses during a period (annual or quarter).

        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock

        Returns:
            dict: Dict having keys as meta and income_statement.
            Metaobject consists of general information about the given symbol.
        """
        query = Query.get_financial_statement(symbol=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getFinancialStatement",query=query,return_type={})
    

    def get_balance_sheet(self,symbol:str,country:str)->dict:
        """_summary_: This function is used to get the balance sheet of a company showing the summary of assets,
        liabilities, and shareholders' equity.

        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock

        Returns:
            dict: Dict having keys as meta and income_statement.
            Metaobject consists of general information about the given symbol.
        """
        query = Query.get_balance_sheet(symbol=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getBalanceSheet",query=query,return_type={})
    

    def get_earnings_estimate(self,symbol:str,country:str)->list:
        """_summary_: This function is used to get the analysts' estimate for a company's future
        quarterly and annual earnings per share (EPS).

        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock

        Returns:
            list: List of dictionaries which gives the earning estimate quarterly and annually.
        """
        query = Query.get_earnings_estimate(symbol=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getEarningsEstimate",query=query,return_type=[])
    
    
    def get_revenue_estimate(self,symbol:str,country:str)->list:
        """_summary_: This function is used to get the analysts' estimate for a company's future
        quarterly and annual sales (total revenue).

        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock

        Returns:
            list: List of dictionaries which gives the revenue estimate quarterly and annually.
        """
        query = Query.get_revenue_estimate(symbol=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getRevenueEstimate",query=query,return_type=[])
    

    def get_cash_flow(self,symbol:str,country:str)->dict:
        """_summary_: This function is used to get the cash flow of a company showing the net amount
        of cash and cash equivalents being transferred into and out of business.

        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock

        Returns:
            dict: Dict having keys as meta and cash_flow.
            Metaobject consists of general information about the given symbol.
        """
        query = Query.get_cash_flow(symbol=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getCashFlow",query=query,return_type={})


    def get_financial_score(self,symbol:str)->list:
        """_summary_: This function is used to get the financial score for the given stock symbol.

        Args:
            symbol (str): Stock symbol

        Returns:
            list: List of dict having keys as symbol, altmanZScore, piotroskiScore, workingCapital,
            totalAssets, retainedEarnings, ebit, marketCap, totalLiabilities and revenue.
        """
        query = Query.get_financial_score(symbol=symbol,apikey=self.api_key)
        return _common(url=self.api_url, key="getStockFinancialScores",query=query,return_type=[])
    
    
    def get_social_sentiment_of_stock(self,symbol:str)->list:
        """_summary_: This function is used to get the social sentiment about the stock.
        Sentiment indicates overall percentage of positive activity.

        Args:
            symbol (str): Stock symbol

        Returns:
            list: List of dict having keys as date, symbol, stocktwitsPosts, twitterPosts, stocktwitsComments,
            twitterComments, stocktwitsLikes, twitterLikes, stocktwitsImpressions, twitterImpressions,
            stocktwitsSentiment and twitterSentiment.
        """
        query = Query.get_social_sentiment_of_stock(symbol=symbol,apikey=self.api_key)
        return _common(url=self.api_url, key="getSocialSentimentOfStock",query=query,return_type=[])
    
    
    def get_market_news(self,symbol:str,news_type:str)->list:
        """_summary_: This function is used to get the most recent stock, crypto, forex and general news
        with parameters like publish date, image or url of the original article.

        Args:
            symbol (str): Stock symbol
            
            news_type (str): Values for news_type are stock_news, crypto_news, forex_news, general_news

        Returns:
            list: List of dictionaries with different news having keys as symbol, publishedDate, title,
            image, site, text and url.
        """
        query = Query.get_market_news(symbol=symbol,news_type=news_type,apikey=self.api_key)
        return _common(url=self.api_url, key="getMarketNews",query=query,return_type=[])
    
    
    def get_eps_trend(self,symbol:str,country:str)->list:
        """_summary_: This function is used to get the breakdown of estimated historical EPS changes at a given period.

        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock

        Returns:
            list: List of dictionaries for diffrent time periods having keys as period, current_estimate,
            date, ninety_days_ago, seven_days_ago, sixty_days_ago and thirty_days_ago.
        """ 
        query = Query.get_eps_trend(symbol=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getEpsTrend",query=query,return_type=[])
    

    def get_eps_revision(self,symbol:str,country:str)->list:
        """_summary_: This function is used to get the analysts' revisions of a company's future quarterly
        and annual earnings per share (EPS) over the last week and month.

        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock

        Returns:
            list: List of dictionaries for diffrent time periods having keys as date, down_last_month,
            down_last_week, period, up_last_month and up_last_week.
        """
        query = Query.get_eps_revision(symbol=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getEpsRevision",query=query,return_type=[])
    

    def get_growth_estimates(self,symbol:str,country:str)->dict:
        """_summary_: This function is used to get the analyst estimates over the company's growth
        rates for various periods.

        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock

        Returns:
            dict: Dict with keys as current_quarter, current_year, next_5_years_pa, next_quarter,
            next_year and past_5_years_pa.
        """
        query = Query.get_growth_estimates(symbol=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getGrowthEstimates",query=query,return_type={})
    
    
    def get_stock_recommendation(self,symbol:str,country:str)->dict:
        """_summary_: This function is used to get the average of all analyst recommendations 
        and classifies them as Strong Buy, Buy, Hold, or Sell. Also, it returns a recommendation score.

        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock

        Returns:
            dict: Dict with keys as trend and rating.
        """
        query = Query.get_stock_recommendation(symbol=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getStockRecommendation",query=query,return_type={})
    

    def get_analyst_ratings_light_data(self,symbol:str,country:str)->list:
        """_summary_: This function is used to get the ratings issued by analyst firms.

        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock

        Returns:
            list: List of dict having keys as date, firm, rating_change, rating_current and rating_prior.
        """
        query = Query.get_analyst_ratings_light_data(symbol=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getAnalystRatingsLightData",query=query,return_type=[])


    def get_analyst_estimates(self,symbol:str)->list:
        """_summary_: This function is used to get the annual analyst estimates of a stock.

        Args:
            symbol (str): Stock symbol

        Returns:
            list: List of dict having keys as symbol, date, estimatedRevenueLow, estimatedRevenueHigh,
            estimatedRevenueAvg, estimatedEbitdaLow, estimatedEbitdaHigh, estimatedEbitdaAvg,estimatedEbitLow,
            estimatedEbitHigh, estimatedEbitAvg, estimatedNetIncomeLow, estimatedNetIncomeHigh, estimatedNetIncomeAvg,
            estimatedSgaExpenseLow, estimatedSgaExpenseHigh, estimatedSgaExpenseAvg, estimatedEpsAvg, estimatedEpsHigh,
            estimatedEpsLow, numberAnalystEstimatedRevenue and numberAnalystsEstimatedEps.
        """
        query = Query.get_analyst_estimates(symbol=symbol,apikey=self.api_key)
        return _common(url=self.api_url, key="getAnalystEstimates",query=query,return_type=[])
    
    
    def get_stock_earnings_surprises(self,symbol:str)->list:
        """_summary_: This function is used to get the estimated and actual EPS.

        Args:
            symbol (str): Stock symbol

        Returns:
            list: List of dict having keys as actualEarningResult, date, estimatedEarning and symbol.
        """
        query = Query.get_stock_earnings_surprises(symbol=symbol,apikey=self.api_key)
        return _common(url=self.api_url, key="getStockEarningsSurprises",query=query,return_type=[])
    
    
    def get_overall_statistics(self,symbol:str,country:str)->dict:
        """_summary_: This function is used to get the overall statistics for stock symbol.

        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock

        Returns:
            dict: Dict having keys as meta and statistics.
            Metaobject consists of general information about the given symbol.
        """
        query = Query.get_overall_statistics(symbol=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getOverallStatistics",query=query,return_type={})


    def get_mutual_fund_holders(self,symbol:str, country: str)->dict:
        """_summary_: This function is used to get the a list of mutual funds.

        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock

        Returns:
            dict: Dict having keys as meta and fund_holders.
            Metaobject consists of general information about the given symbol.
        """
        query = Query.get_mutual_fund_holders(symbol=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getMutualFundHolders",query=query,return_type={})
    

    def get_institutional_holders(self,symbol:str, country: str)->dict:
        """_summary_: This function is used to get the amount of the company's available stock owned by 
        institutions (pension funds, insurance companies, investment firms, private foundations, endowments
        or other large entities that manage funds on behalf of others).

        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock

        Returns:
            dict: Dict having keys as meta and institutional_holders.
            Metaobject consists of general information about the given symbol.
        """
        query = Query.get_institutional_holders(symbol=symbol,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getInstitutionalHolders",query=query,return_type={})


    def get_stock_ownership_by_holders(self,symbol:str, date: str)->dict:
        """_summary_: This function is used to get the stock ownership by holders.

        Args:
            symbol (str): Stock symbol
            
            date (str): Date must be YYYY-09-30. To get the stock owenership by holders data for particular year,
            in place of 'YYYY' write the required year.

        Returns:
            dict: Dict having keys as date, cik, filingDate, investorName, symbol, securityName, typeOfSecurity,
            securityCusip, sharesType, putCallShare, investmentDiscretion, industryTitle, weight, lastWeight,
            changeInWeight, changeInWeightPercentage, marketValue, lastMarketValue, changeInMarketValue,
            changeInMarketValuePercentage, sharesNumber, lastSharesNumber, changeInSharesNumber,
            changeInSharesNumberPercentage, quarterEndPrice, avgPricePaid, isNew, isSoldOut, ownership,
            lastOwnership, changeInOwnershipPercentage, holdingPeriod, firstAdded, performance,
            performancePercentage, lastPerformance, changeInPerformance and isCountedForPerformance.
        """
        query = Query.get_stock_ownership_by_holders(symbol=symbol,date=date,apikey=self.api_key)
        return _common(url=self.api_url, key="getStockOwnershipByHolders",query=query,return_type={})
    
    
    def get_etf_holders(self)->list:
        """_summary_: This function is used to get the all stocks held by a specific ETF.

        Returns:
            list: list of dictionaries for different etf holders having keys as asset, name, isin, cusip,
            sharesNumber, weightPercentage, marketValue and updated.
        """
        query = Query.get_etf_holders(apikey=self.api_key)
        return _common(url=self.api_url, key="getETFHolders",query=query,return_type=[])
    
    
    def get_stock_response(self,symbol:str)->list:
        """_summary_: This function is used to get the shares float for stock symbol.

        Args:
            symbol (str): Stock symbol

        Returns:
            list: List having dict having keys as date, freeFloat, floatShares, outstandingShares and source.
        """
        query = Query.get_stock_response(symbol=symbol, apikey=self.api_key)
        return _common(url=self.api_url, key="getStockResponse",query=query,return_type=[])
    
    
    def get_etf_sector_weightings(self)->list:
        """_summary_: This function is used to get the sector weight for each ETF holder.

        Returns:
            list: List having dict having keys as sector and weightPercentage.
        """
        query = Query.get_etf_sector_weightings(apikey=self.api_key)
        return _common(url=self.api_url, key="getETFSectorWeightings",query=query,return_type=[])
    
    
    def get_gainers_or_losers(self,type:str,country:str)->list:
        """_summary_: This function is used to get the list of today's top gaining, losing and actives stocks.

        Args:
            type (str): Get the different market movers as per required type.
            Values for type are actives, gainers and losers.
            
            country (str): Required country to filter the stock

        Returns:
            list: List dictionaries for top gainers/losers/actives having keys as change, datetime, exchange,
            high, last, low, mic_code, name, percent_change, volume and symbol.
        """
        query = Query.get_gainers_or_losers(type=type,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getGainersOrLosers",query=query,return_type=[])


    def get_stock_market_holiday_data(self,year:int)->dict:
        """_summary_: This function is used to get the days when the stock market is closed,
        such as New Year's Day or Christmas.

        Args:
            year (int): Year for which holidays required.

        Returns:
            dict: Dict having keys as year and holidays.  
        """
        query = Query.get_stock_market_holiday_data(year=year,apikey=self.api_key)
        return _common(url=self.api_url, key="getStockMarketHolidayData",query=query,return_type={})
    

    def get_market_status_data(self,exchange:str,country:str)->dict:
        """_summary_: This function is used to get the current market status like trading hours.

        Args:
            exchange (str): Stock exchange
            
            country (str): Required country to filter the stock

        Returns:
            dict: Dict having keys as exchange_name, is_market_open, time_to_close, time_to_open
            country and time_after_open and code.
        """
        query = Query.get_market_status_data(exchange=exchange,country=country,apikey=self.api_key)
        return _common(url=self.api_url, key="getMarketStatusData",query=query,return_type={})
    

    def get_dividend_calendar(self,symbol:str,limit:str)->dict:
        """_summary_: This function is used to get the info about dividend and adjacent dividend for stocks.

        Args:
            symbol (str): Stock symbol
            
            limit (str): required no. of records for dividend calendar

        Returns:
            dict: Dict having keys as symbol and historical. 
            Historical contents the detailed data about dividends.
        """
        query = Query.get_dividend_calendar(symbol=symbol,limit=limit,apikey=self.api_key)
        return _common(url=self.api_url, key="getDividendCalendar",query=query,return_type={})


    def get_earning_calendar(self,from_date:str,to_date:str)->list:
        """_summary_: This function is used to get the Earnings Calendar with time period
        (between the "from_date" and "to_date" parameters the maximum time interval can be 3 months.

        Args:
            from_date (str): earning report required from (YYYY-MM-DD)
            
            to_date (str): earning report required upto (YYYY-MM-DD)

        Returns:
            list: List of dictionaries for various stock symbols having keys as symbol, fiscalDateEnding,
            time, revenue, date, revenueEstimated, eps, updatedFromDate and epsEstimated.
        """
        query = Query.get_earning_calendar(from_date=from_date,to_date=to_date,apikey=self.api_key)
        return _common(url=self.api_url, key="getEarningCalendar",query=query,return_type={})
    

    def get_economic_calendar(self,from_date:str,to_date:str)->list:
        """_summary_: This function is used to get the all of the world's major economic events for time period 
        (between the "from_date" and "to_date" parameters the maximum time interval can be 3 months).

        Args:
            from_date (str): economic calendar required from (YYYY-MM-DD)
            
            to_date (str): economic calendar required upto (YYYY-MM-DD)

        Returns:
            list: List of dict for various economic events having keys as country, impact, event,
            date, actual, previous, changePercentage, change and estimate.
        """
        query = Query.get_economic_calendar(from_date=from_date,to_date=to_date,apikey=self.api_key)
        return _common(url=self.api_url, key="getEconomicCalendar",query=query,return_type=[])
    
    
    def get_split_calendar(self,from_date:str,to_date:str)->list:
        """_summary_: This function is used to get Stock Split Calendar for time period 
        (between the "from_date" and "to_date" parameters the maximum time interval can be 3 months).

        Args:
            from_date (str): split calendar required from (YYYY-MM-DD)
            
            to_date (str): split calendar required upto (YYYY-MM-DD)

        Returns:
            list: List of dict for various stock symbols having keys as symbol, label, date,
            denominator and numerator.
        """
        query = Query.get_split_calendar(from_date=from_date,to_date=to_date,apikey=self.api_key)
        return _common(url=self.api_url, key="getSplitCalendar",query=query,return_type=[])
    
    
    def get_technical_indicators(self,symbol:str,interval:str,indicator:str,limit:int)->dict:
        """_summary_: This function is used to get real-time and historical values of the demanded
        indicator at the selected interval.

        Args:
            symbol (str): Stock symbol
            
            interval (str): Interval between two consecutive points in time series.(Candle interval)
                            Supports: 1min, 5min, 15min, 30min, 45min, 1h, 2h, 4h, 1day, 1week, 1month
                            
            indicator (str): To get the indicator value for stock symbol, the values for indicator are
            ad, adosc, adx, adxr, apo, aroon, aroonosc, atr, avg, avgprice, bbands, beta, bop, cci, ceil,
            cmo, coppock, correl, crsi, dema, div, dpo, dx, ema, exp, floor, heikinashicandles, hlc3,
            ht_dcperiod, ht_dcphase, ht_phasor, ht_sine, ht_trendline, ht_trendmode, ichimoku, kama,
            keltner, kst, linearreg, linearregangle, linearregintercept, linearregslope, ln, log10, ma,
            macd, macd_slope, macdext, mama, max, maxindex, mcginley_dynamic, medprice, mfi, midpoint,
            midprice, mfi, min, minindex, minmax, minmaxindex, minus_di, minus_dm, mom, mult, natr, obv,
            percent_b, pivot_points_hl, plus_di, plus_dm, ppo, roc, rocp, rocr, rocr100, rsi, rvol, sar,
            sarext, sma, sqrt, stddev, stoch, stochf, stochrsi, sub, sum, supertrend, supertrend_heikinashicandles,
            t3ma, tema, trange, trima, tsf, typprice, ultosc, var, vwap, wclprice, willr and wma
            
            limit (str): Number of records required for the given indicator

        Returns:
            dict:  Dict having keys as meta and values. Metaobject consists of general information 
            about the given indicator and values consist of the datetime and indicator value for given stock symbol. 
        """
        query = Query.get_technical_indicators(ticker=symbol,interval=interval,indicator=indicator,limit=limit , apikey=self.api_key)
        return _common(url=self.api_url, key="getTechnicalIndicators",query=query,return_type={})
    
    
    def get_ipo_stock_data(self,start_time:str,end_time:str,limit:int)->list:
        """_summary_: This function is used to get IPO Calendar for time period 
        (between the "start_time" and "end_time" parameters the maximum time interval can be 3 months).

        Args:
            start_time (str): Start Date (ipo required from) (YYYY-MM-DD)
            
            end_time (str): End Date (ipo required upto) (YYYY-MM-DD)
            
            limit (int): Number of required records

        Returns:
            list: List of dict for different stock symbols having keys as actions, company, date,
            exchange, marketCap, priceRange, shares and symbol.
        """
        query = Query.get_ipo_stock_data(start_time=start_time,end_time=end_time,limit=limit, apikey=self.api_key)
        return _common(url=self.api_url, key="getIPOStockData",query=query,return_type=[])
    
    
    def get_times_series_data(self,symbol:str,country:str,interval:str,limit:str)->dict:
        """_summary_: This function is used to get timeseries data or historical data.
        By giving the limit value, get the required number of records only.

        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock
            
            interval (str): Interval between two consecutive points in time series.(Candle interval)
                            Supports: 1min, 5min, 15min, 30min, 45min, 1h, 2h, 4h, 1day, 1week, 1month
            
            limit (str): Number of required records

        Returns:
            dict: Dict having keys as meta and values.Metaobject consists of general information 
            about the given symbol and values contain timeseries data.
        """
        query = Query.get_times_series_data(symbol=symbol,country=country,limit=limit,interval=interval, apikey=self.api_key)
        return _common(url=self.api_url, key="getTimesSeriesData",query=query,return_type={})
    

    def get_times_series_data_by_date(self,symbol:str,country:str,interval:str,limit:int,start_date:str,
                                      end_date:str)->dict:
        """_summary_: This function is used to get the timeseries data or historical data.
        By giving the start_date and end_date , get the records only for given time period.
        
        Args:
            symbol (str): Stock symbol
            
            country (str): Required country to filter the stock
            
            interval (str): Interval between two consecutive points in time series.(Candle interval)
                            Supports: 1min, 5min, 15min, 30min, 45min, 1h, 2h, 4h, 1day, 1week, 1month
                            
            limit (str): Number of required records
            
            start_date (str): timeseries data required from (YYYY-MM-DD)
            
            end_date (str): timeseries data required upto (YYYY-MM-DD)

        Returns:
            dict: Dict having keys as meta and values.Metaobject consists of general information 
            about the given symbol and values contain timeseries data.
        """
        query = Query.get_times_series_data_by_date(symbol=symbol,country=country,limit=limit,interval=interval,
                                                    start_date=start_date,
                                                    end_date=end_date,
                                                    apikey=self.api_key)
        return _common(url=self.api_url, key="getTimesSeriesData",query=query,return_type={})
    

    def get_financial_growth(self,symbol:str,limit:int)->list:
        """_summary_: This function is used to get the financial growth of the company.

        Args:
            symbol (str): Stock symbol
            
            limit (str): Number of required records

        Returns:
            list: List of dict having keys as symbol, date, period, revenueGrowth, grossProfitGrowth, ebitgrowth,
            operatingIncomeGrowth, netIncomeGrowth, epsgrowth, epsdilutedGrowth, weightedAverageSharesGrowth,
            weightedAverageSharesDilutedGrowth, dividendsperShareGrowth, operatingCashFlowGrowth, freeCashFlowGrowth,
            tenYRevenueGrowthPerShare, fiveYRevenueGrowthPerShare, threeYRevenueGrowthPerShare, tenYOperatingCFGrowthPerShare,
            fiveYOperatingCFGrowthPerShare, threeYOperatingCFGrowthPerShare, tenYNetIncomeGrowthPerShare,
            fiveYNetIncomeGrowthPerShare, threeYNetIncomeGrowthPerShare, tenYShareholdersEquityGrowthPerShare,
            fiveYShareholdersEquityGrowthPerShare, threeYShareholdersEquityGrowthPerShare, tenYDividendperShareGrowthPerShare,
            fiveYDividendperShareGrowthPerShare, threeYDividendperShareGrowthPerShare, receivablesGrowth
            inventoryGrowth, assetGrowth, bookValueperShareGrowth, debtGrowth, rdexpenseGrowth and sgaexpensesGrowth
        """
        query = Query.get_financial_growth(symbol=symbol,limit=limit,apikey=self.api_key)
        return _common(url=self.api_url, key="getFinancialGrowth",query=query,return_type=[])


    def get_stock_financial_statement(self,symbol:str,limit:int)->list:
        """_summary_: This function is used to get the annual income statements of the company.

        Args:
            symbol (str): Stock symbol
            
            limit (str): Number of required records

        Returns:
            list: List of dict having keys as date, symbol, period, growthRevenue, growthCostOfRevenue,
            growthGrossProfit, growthGrossProfitRatio, growthResearchAndDevelopmentExpenses,
            growthGeneralAndAdministrativeExpenses, growthSellingAndMarketingExpenses, growthOtherExpenses,
            growthOperatingExpenses, growthOperatingExpenses, growthCostAndExpenses, growthInterestExpense,
            growthDepreciationAndAmortization, growthEBITDA, growthEBITDARatio, growthOperatingIncome,
            growthOperatingIncomeRatio, growthTotalOtherIncomeExpensesNet, growthIncomeBeforeTax,
            growthIncomeBeforeTaxRatio, growthIncomeTaxExpense, growthNetIncome, growthNetIncomeRatio,
            growthEPS, growthEPSDiluted, growthWeightedAverageShsOut and growthWeightedAverageShsOutDil
        """
        query = Query.get_stock_financial_statement(symbol=symbol,limit=limit,apikey=self.api_key)
        return _common(url=self.api_url, key="getStockFinancialStatement",query=query,return_type=[])
    
    
    def get_stock_trends_chart_data(self,
                                    symbol: str,
                                    interval: str,
                                    type: str,
                                    chart_type: str,
                                    exchange: str,
                                    country_id: str)->list:
        """
        This function is used to get stock trends chart data
        
        Args:
            symbol (str): stock symbol
            interval (str): market data interval 
            type (str): type of data
            chartType (str): type of chart
            exchange (str): stock exchange
            countryId (str): country Id

        Returns:
            list: List of dict having keys as date, close, high, open,low, tradeCount, VWAP, y.
        """
        query = Query.get_stock_trends_chart_data(
            symbol,interval,type,chart_type,exchange,country_id,api_key=self.api_key)
        return _common(url=self.api_url, key="getStockTrendsChartData",query=query,return_type=[])


    
    def get_stock_details_data(self,country:str,page_no:int,records_required:int)->dict:
        """_summary_: This function is used to get stock details for given country.

        Args:
            country (str): Required country
            page_no (int): page no.
            records_required (int): Number of records required(no. of stock's details)

        Returns:
            dict: _description_
        """
        query = Query.get_stock_details_data(country=country,page_no=page_no,records_required=records_required,apikey=self.api_key)
        return _common(url=self.api_url, key="getStocksDetailsData",query=query,return_type={})
