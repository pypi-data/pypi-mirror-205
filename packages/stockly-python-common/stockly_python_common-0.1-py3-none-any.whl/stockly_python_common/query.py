
class Query:

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_stock_current_price(ticker: str, api_key: str) -> str:
        return f"""
        query {{
        getStockCurrentPrice(ticker: "{ticker}" apiKey: "{api_key}"){{
            price
            message
            status
        }}
        }}"""

    @staticmethod
    def get_stock_peers(ticker: str ,apikey: str) -> str:
        return f"""
            query {{
            getStockPeers(symbol: "{ticker}", apiKey: "{apikey}") {{
            data {{
                symbol
                peersList
            }}
            message
            status
        }}
        }}"""



    @staticmethod
    def get_ticker_search_data(ticker:str,exchange:str,apikey:str)->str:

        return f"""query {{
        getTickerSearchData(
            searchTicker: "{ticker}"
            exchange: "{exchange}"
            apiKey: "{apikey}"
        ) {{
            data {{
            currency
            exchangeShortName
            name
            stockExchange
            symbol
            }}
            message
            status
        }}
        }}"""







    @staticmethod
    def get_exchange_screener(exchange:str,market_capital:int,beta:int,volume:int,limit:int,apikey:str)->str:
        return f"""
        query {{
        getExchangeScreener(
            exchange: "{exchange}"
            marketCapital: {market_capital}
            beta: {beta}
            volume: {volume}
            limit: {limit}
            apiKey: "{apikey}"
        ) {{
            data {{
                symbol
                volume
                beta
                lastAnnualDividend
                exchangeShortName
                isEtf
                price
                marketCap
                isActivelyTrading
                companyName
                sector
            }}
            message
            status
        }}
        }}"""


    @staticmethod
    def get_sector_screener(exchange:str,sector:str,market_capital:int,beta:int,volume:int,limit:int,apikey:str)->str:
     return f"""
        query {{
        getSectorScreener(
            exchange: "{exchange}"
            sector: "{sector}"
            marketCapital: {market_capital}
            beta: {beta}
            volume: {volume}
            limit: {limit}
            apiKey: "{apikey}"
        ) {{
            data {{
                symbol
                volume
                beta
                lastAnnualDividend
                exchangeShortName
                isEtf
                price
                marketCap
                isActivelyTrading
                companyName
                sector
            }}
            message
            status
        }}
        }}"""



    @staticmethod
    def percent_change_data(ticker:str,apikey:str)->str:
        return f"""
        query {{
        percentChangeData(
            symbol: "{ticker}"
            apiKey: "{apikey}"
        ) {{
            message
            status
            data {{
                d1
                d5
                m1
                m3
                m6
                ytd
                y1
                y3
                y5
                y10
                max
            }}
        }}
        }}"""

    @staticmethod
    def get_stock_price_screener(price:int,country:str,type:str,apikey:str)->str:
        return f"""
        query {{
        getStockPriceScreener(
            price: {price}
            country: "{country}"
            type: "{type}"
            apiKey: "{apikey}"
        ) {{
            data {{
                symbol
                volume
                beta
                lastAnnualDividend
                exchangeShortName
                isEtf
                price
                marketCap
                isActivelyTrading
                companyName
                sector
            }}
            message
            status
        }}
        }}"""
    
    @staticmethod
    def get_sectors_ratio_data(exchange:str,date:str,apikey:str)->str:
        return f"""
        query {{
        getSectorsRatioData(
            exchange: "{exchange}"
            date: "{date}"
            apiKey: "{apikey}"
        ) {{
            data {{
                exchange
                pe
                date
                sector
            }}
            message
            status
        }}
        }}"""

    @staticmethod
    def get_industries_pe_ratio(exchange:str,date:str,apikey:str)->str:
    
     return f"""
        query {{
        getIndustriesPERatio(
            date: "{date}"
            exchange: "{exchange}"
            apiKey: "{apikey}"
        ) {{
            message
            status
            data {{
                date
                industry
                exchange
                pe
            }}
        }}
        }}
        """
    @staticmethod
    def get_stock_market_performance_data(apiKey)->str:
        return f"""
        query {{
        getStockMarketPerformanceData(apiKey: "{apiKey}") {{
            data{{
            sector
            changesPercentage
            }}
            message
            status
        }}
        }}"""

    @staticmethod
    def get_financial_ratios_of_companies(ticker:str,apikey:str)->str:
        return f"""
        query{{
        getFinancialRatiosOfCompanies(
            symbol: "{ticker}"
            apiKey: "{apikey}"
        ) {{
            data {{
                dividendYielTTM
                dividendYielPercentageTTM
                peRatioTTM
                pegRatioTTM
                payoutRatioTTM
                currentRatioTTM
                quickRatioTTM
                cashRatioTTM
                daysOfSalesOutstandingTTM
                daysOfInventoryOutstandingTTM
                operatingCycleTTM
                daysOfPayablesOutstandingTTM
                cashConversionCycleTTM
                grossProfitMarginTTM
                operatingProfitMarginTTM
                pretaxProfitMarginTTM
                netProfitMarginTTM
                effectiveTaxRateTTM
                returnOnAssetsTTM
                returnOnEquityTTM
                returnOnCapitalEmployedTTM
                netIncomePerEBTTTM
                ebtPerEbitTTM
                ebitPerRevenueTTM
                debtRatioTTM
                debtEquityRatioTTM
                longTermDebtToCapitalizationTTM
                totalDebtToCapitalizationTTM
                interestCoverageTTM
                cashFlowToDebtRatioTTM
                companyEquityMultiplierTTM
                receivablesTurnoverTTM
                payablesTurnoverTTM
                inventoryTurnoverTTM
                fixedAssetTurnoverTTM
                assetTurnoverTTM
                operatingCashFlowPerShareTTM
                freeCashFlowPerShareTTM
                cashPerShareTTM
                operatingCashFlowSalesRatioTTM
                freeCashFlowOperatingCashFlowRatioTTM
                cashFlowCoverageRatiosTTM
                shortTermCoverageRatiosTTM
                capitalExpenditureCoverageRatioTTM
                dividendPaidAndCapexCoverageRatioTTM
                priceBookValueRatioTTM
                priceToBookRatioTTM
                priceToSalesRatioTTM
                priceEarningsRatioTTM
                priceToFreeCashFlowsRatioTTM
                priceToOperatingCashFlowsRatioTTM
                priceCashFlowRatioTTM
                priceEarningsToGrowthRatioTTM
                priceSalesRatioTTM
                dividendYieldTTM
                enterpriseValueMultipleTTM
                priceFairValueTTM
                dividendPerShareTTM
            }}
            message
            status
        }}
        }}
    """




    @staticmethod
    def get_target_price_summary(ticker:str,apikey:str)->str:
        return f"""
        query{{
        getTargetPriceSummary(symbol: "{ticker}", apiKey: "{apikey}"){{
            message
            status
            data{{
                symbol
                lastMonth
                lastMonthAvgPriceTarget
                lastQuarter
                lastQuarterAvgPriceTarget
                lastYear
                lastYearAvgPriceTarget
                allTime
                allTimeAvgPriceTarget
                publishers
            }}
        }}
    }}
    """

    @staticmethod
    def get_target_price(symbol:str,country:str,apikey:str)->str:
        return f"""
        query{{
        getTargetPrice(symbol: "{symbol}", country: "{country}", apiKey: "{apikey}"){{
            data{{
            price_target{{
                high
                median
                low
                average
                current
            }}
            }}
            status
            message
        }}
        }}
        """

    @staticmethod
    def get_end_of_day_price(apikey:str,country:str,symbol:str)->str:
        return f"""
        query{{
        getEndOfDayPrice(apiKey: "{apikey}", country: "{country}", symbol: "{symbol}"){{
            status
            message
            data{{
                symbol
                exchange
                mic_code
                currency
                datetime
                close
            }}
        }}
        }}"""



    @staticmethod
    def get_current_price(apikey:str,country:str,symbol:str)->str:
        return f"""
        query{{
        getCurrentPrice(symbol: "{symbol}", country: "{country}", apiKey: "{apikey}"){{
            data{{
            price
            }}
            message
            status
        }}
        }}"""



    @staticmethod
    def get_insider_traders(symbol:str,country:str,apikey:str)->str:
        return f"""
        query{{
        getInsiderTraders(symbol: "{symbol}", country: "{country}", apiKey: "{apikey}"){{
            data{{
                meta{{
                    symbol
                    name
                    currency
                    exchange
                    mic_code
                    exchange_timezone
            }}
                insider_transactions{{
                    full_name
                    position
                    date_reported
                    is_direct
                    shares
                    value
                    description
            }}
            }}
            message
            status
        }}
        }}
        """
    

    @staticmethod
    def get_delisted_companies(apkey:str)->str:
        return f"""
            query {{
            getDelistedCompanies(apiKey: "{apkey}") {{
                data {{
                    symbol
                    exchange
                    companyName
                    delistedDate
                    ipoDate
                }}
                message
                status
            }}
            }}"""


    @staticmethod
    def get_symbol_change(apikey:str)->str:
        return f"""
        query {{
        getSymbolChange(apiKey: "{apikey}") {{
            data {{
                date
                name
                newSymbol
                oldSymbol
            }}
            message
            status
        }}
        }}"""
    
    @staticmethod
    def get_s_and_p_companies(apikey:str)->str:
        return f"""
        query {{
        getSpCompanies(apiKey: "{apikey}") {{
            data {{
            cik
            dateFirstAdded
            founded
            headQuarter
            name
            sector
            subSector
            symbol
            }}
            message
            status
        }}
        }}"""

    @staticmethod
    def get_nasdaq_companies(apikey:str)->str:
        return f"""
        query {{
        getNasdaqCompanies(apiKey: "{apikey}") {{
            data {{
            cik
            dateFirstAdded
            founded
            headQuarter
            name
            sector
            subSector
            symbol
            }}
            message
            status
        }}
        }}
        """

    @staticmethod
    def get_crypto_symbol(apikey:str)->str:
        return f"""query {{
        getCryptoSymbol(
            apiKey: "{apikey}"
        ) {{
            data {{
                symbol
                price
                changesPercentage
                change
                dayLow
                dayHigh
                yearHigh
                yearLow
                marketCap
                priceAvg50
                priceAvg200
                volume
                avgVolume
                exchange
            }}
            message
            status
        }}
        }}"""
 

    @staticmethod
    def get_forex_symbol(apikey:str)->str:
        return f"""
        query {{
        getForexSymbol(apiKey: "{apikey}") {{
            data {{
            ticker
            ask
            bid
            changes
            date
            high
            low
            open
            }}
            message
            status
        }}
        }}"""

    @staticmethod
    def get_dow_jones_companies(apikey:str)->str:
        return f"""
        query {{
        getDowjonesCompanies(
            apiKey: "{apikey}"
        ) {{
            data {{
                cik
                dateFirstAdded
                founded
                headQuarter
                name
                sector
                subSector
                symbol
            }}

            message
            status
        }}
        }}"""


    @staticmethod
    def get_etf_list_data(apikey:str)->str:
        return f"""
        query {{
        getETFListData(apiKey: "{apikey}") {{
            data {{
                asset
                cusip
                isin
                marketValue
                name
                sharesNumber
                weightPercentage
            }}
            message
            status
        }}
        }}"""



    @staticmethod
    def get_esg_score_data(symbol:str,apikey:str)->str:
        return f"""
        query
        {{
        getESGScoreData(symbol:"{symbol}", apiKey: "{apikey}")
        {{
            data{{
            ESGScore
            acceptedDate
            cik
            companyName
            date
            environmentalScore
            formType
            governanceScore
            socialScore
            symbol
            url
            }}
            message
            status
        }}
        }}"""



    @staticmethod
    def get_esg_bench_marking_by_sector_and_year(year:str,apikey:str)->str:
        return f"""
        query{{
        getESGBenchmarkingBySectorAndYear(year: "{year}", apiKey: "{apikey}"){{
            data{{
            year
            sector
            environmentalScore
            socialScore
            governanceScore
            ESGScore
            }}
            message
            status
        }}
        }}"""


    @staticmethod
    def get_company_esg_risk_rating(symbol:str,apikey:str)->str:
        return f"""
        query{{
        getCompanyEsgRiskRating(symbol: "{symbol}", apiKey: "{apikey}"){{
            message
            status
            data{{
                symbol
                cik
                companyName
                industry
                year
                ESGRiskRating
                industryRank
            }}
        }}
        }}"""

    

    @staticmethod
    def get_company_enterprise_value(symbol:str,apikey:str)->str:
        return f"""
        query {{
        getCompanyEnterpriseValue(
            symbol: "{symbol}"
            apiKey: "{apikey}"
    ) {{
        data {{
            symbol
            date
            stockPrice
            numberOfShares
            marketCapitalization
            minusCashAndCashEquivalents
            addTotalDebt
            enterpriseValue
        }}
        message
        status
    }}
    }}"""


    @staticmethod
    def get_company_notes_due_by_stock_name(symbol:str,apikey:str)->str:
        return f"""
        query {{
        getCompanyNotesDueByStockName(
            stockName: "{symbol}"
            apiKey: "{apikey}"
        ) {{
            message
            status
            data {{
            cik
            exchange
            title
            symbol
            }}
        }}
        }}"""

    @staticmethod
    def get_company_quote_by_stock_name(ticker:str,country:str,apikey:str)->str:
        return f"""query {{
        getCompanyQuoteByStockName(
            stockName: "{ticker}"
            country: "{country}"
            apiKey: "{apikey}"
        ) {{
            message
            status
            data {{
            symbol
            name
            exchange
            mic_code
            currency
            datetime
            timestamp
            open
            high
            low
            close
            volume
            previousClose
            change
            percentChange
            averageVolume
            isMarketOpen
            fifty_two_week {{
                lowChange
                highChange
                high
                low
                lowChangePercent
                highChangePercent
                range
            }}
            }}
        }}
        }}"""


    @staticmethod
    def get_company_outlook(ticker:str,country:str,apikey:str)->str:
        return f"""
        query {{
        getCompanyOutlook(
            symbol: "{ticker}"
            country: "{country}"
            apiKey: "{apikey}"
        ) {{
            message
            status
            data {{
                symbol
                name
                exchange
                mic_code
                sector
                employees
                website
                description
                type
                ceo
                address
                city
                zip
                state
                country
                phone
            }}
        }}
        }}"""



    @staticmethod
    def get_company_rating_by_stock_name(symbol:str,apikey:str)->str:
        return f"""
        query {{
        getCompanyRatingByStockName(
            stockName: "{symbol}"
            apiKey: "{apikey}"
        ) {{
            message
            status
            data {{
            symbol
            date
            rating
            ratingDetailsDCFRecommendation
            ratingDetailsROERecommendation
            ratingDetailsROARecommendation
            ratingDetailsDERecommendation
            ratingDetailsPERecommendation
            ratingDetailsPBRecommendation
            ratingDetailsDCFScore
            ratingDetailsROEScore
            ratingDetailsROAScore
            ratingDetailsDEScore
            ratingDetailsPEScore
            ratingDetailsPBScore
            }}
        }}
    }}"""

    @staticmethod
    def get_company_core_information(symbol:str,apikey:str)->str:
        return f"""
        query {{
        getCompanyCoreInformation(
            stockName: "{symbol}"
            apiKey: "{apikey}"
        ) {{
            data {{
                businessAddress
                cik
                exchange
                fiscalYearEnd
                mailingAddress
                registrantName
                sicCode
                sicDescription
                sicGroup
                stateLocation
                stateLocation
                stateOfIncorporation
                symbol
                taxIdentificationNumber
            }}
            message
            status
        }}
        }}
        """
    @staticmethod
    def get_company_key_metrics(symbol:str,apikey:str)->str:
        return f"""
            query {{
            getCompanyKeyMetrics(
                symbol: "{symbol}"
                apiKey: "{apikey}"
            ) {{
                data {{
                revenuePerShareTTM
                netIncomePerShareTTM
                operatingCashFlowPerShareTTM
                freeCashFlowPerShareTTM
                cashPerShareTTM
                bookValuePerShareTTM
                tangibleBookValuePerShareTTM
                shareholdersEquityPerShareTTM
                interestDebtPerShareTTM
                marketCapTTM
                enterpriseValueTTM
                peRatioTTM
                priceToSalesRatioTTM
                pocfratioTTM
                pfcfRatioTTM
                pbRatioTTM
                ptbRatioTTM
                evToSalesTTM
                enterpriseValueOverEBITDATTM
                evToOperatingCashFlowTTM
                evToFreeCashFlowTTM
                earningsYieldTTM
                freeCashFlowYieldTTM
                debtToEquityTTM
                debtToAssetsTTM
                netDebtToEBITDATTM
                currentRatioTTM
                interestCoverageTTM
                incomeQualityTTM
                dividendYieldTTM
                dividendYieldPercentageTTM
                payoutRatioTTM
                salesGeneralAndAdministrativeToRevenueTTM
                researchAndDevelopementToRevenueTTM
                intangiblesToTotalAssetsTTM
                capexToOperatingCashFlowTTM
                capexToRevenueTTM
                capexToDepreciationTTM
                stockBasedCompensationToRevenueTTM
                grahamNumberTTM
                roicTTM
                returnOnTangibleAssetsTTM
                grahamNetNetTTM
                workingCapitalTTM
                tangibleAssetValueTTM
                netCurrentAssetValueTTM
                investedCapitalTTM
                averageReceivablesTTM
                averagePayablesTTM
                averageInventoryTTM
                daysSalesOutstandingTTM
                daysPayablesOutstandingTTM
                daysOfInventoryOnHandTTM
                receivablesTurnoverTTM
                payablesTurnoverTTM
                inventoryTurnoverTTM
                roeTTM
                capexPerShareTTM
                dividendPerShareTTM
                debtToMarketCapTTM
                }}
                status
                message
            }}
            }}
            """
    @staticmethod
    def get_market_capitalization_stock_data(symbol:str,apikey:str)->str:
        return f"""
        query{{
            getMarketCapitalizationStockData(symbol:"{symbol}", apiKey:"{apikey}")
            {{
            data{{
                date
                marketCap
                symbol
            }}    
            status
            message
            }}
        }}"""
    
    @staticmethod
    def get_key_executives(symbol:str,country:str,apikey:str)->str:
        return f"""
        query {{
        getKeyExecutives(
            symbol: "{symbol}"
            country: "{country}"
            apiKey: "{apikey}"
        ) {{
            data {{
                meta {{
                    symbol
                    name
                    currency
                    exchange
                    mic_code
                    exchange_timezone
                }}
                keyExecutives {{
                    name
                    title
                    age
                    year_born
                    pay
                }}
            }}
            status
            message
        }}
        }}"""
    

    @staticmethod
    def get_company_disc_cash_flow(symbol:str,apikey:str)->str:
        return f"""
        query {{
        getCompanyDiscCashflow(
            symbol: "{symbol}"
            apiKey: "{apikey}"
        ) {{
            data {{
            symbol
            date
            dcf
            stockPrice
            }}
            status
            message
        }}
        }}"""


    @staticmethod
    def get_financial_statement(symbol:str,country:str,apikey:str)->str:
        return f"""
        query{{
        getFinancialStatement(symbol: "{symbol}", country: "{country}", apiKey: "{apikey}"){{
            status
            message
            data{{
            meta{{
            symbol
            name
            currency
            exchange
            mic_code
            exchange_timezone
            period
        }}
        income_statement{{
            fiscal_date
            quarter
            sales
            cost_of_goods
            gross_profit
            operating_expense{{
                research_and_development
                selling_general_and_administrative
                other_operating_expenses
            }}
            operating_income
            non_operating_interest{{
            income
            expense
            }}
            other_income_expense
            pretax_income
            income_tax
            net_income
            eps_basic
            eps_diluted
            basic_shares_outstanding
            diluted_shares_outstanding
            ebitda
            net_income_continuous_operations
            minority_interests
            preferred_stock_dividends
            }}
            }}
        }}
        }}
        """
    
    @staticmethod
    def get_balance_sheet(symbol:str,country:str,apikey:str)->str:
        return f"""
        query{{
        getBalanceSheet(symbol: "{symbol}", country: "{country}", apiKey: "{apikey}"){{
            status
            message
            data{{
                    meta{{
                    symbol
                    name
                    currency
                    exchange
                    mic_code
                    exchange_timezone
                    period
                }}
        balance_sheet{{
            fiscal_date
            assets{{
                current_assets{{
                    cash
                    cash_equivalents
                    cash_and_cash_equivalents
                    other_short_term_investments
                    accounts_receivable
                    other_receivables
                    inventory
                    prepaid_assets
                    restricted_cash
                    assets_held_for_sale
                    hedging_assets
                    other_current_assets
                    total_current_assets
                }}
            non_current_assets{{
                properties
                land_and_improvements
                machinery_furniture_equipment
                construction_in_progress
                leases
                accumulated_depreciation
                goodwill
                investment_properties
                financial_assets
                intangible_assets
                investments_and_advances
                other_non_current_assets
                total_non_current_assets
            }}
            total_assets
            }}
            liabilities{{
            current_liabilities{{
                accounts_payable
                accrued_expenses
                short_term_debt
                deferred_revenue
                tax_payable
                pensions
                other_current_liabilities
                total_current_liabilities
            }}
            non_current_liabilities{{
                long_term_provisions
                long_term_debt
                provision_for_risks_and_charges
                deferred_liabilities
                derivative_product_liabilities
                other_non_current_liabilities
                total_non_current_liabilities
            }}
            total_liabilities
            }}
            shareholders_equity {{
            common_stock
            retained_earnings
            other_shareholders_equity
            total_shareholders_equity
            additional_paid_in_capital
            treasury_stock
            minority_interest
            }}
        }}
            }}
        }}
        }}"""





    #analysis bot
    @staticmethod
    def get_earnings_estimate(symbol:str,country:str,apikey:str)->str:
        return f"""
        query {{
        getEarningsEstimate(
            apiKey: "{apikey}"
            symbol: "{symbol}"
            country: "{country}"
        ) {{
            data {{
                avg_estimate
                date
                low_estimate
                number_of_analysts
                period
                year_ago_eps
                high_estimate
            }}
            message
            status
        }}
        }}"""


    @staticmethod
    def get_revenue_estimate(symbol:str,country:str,apikey:str)->str:
        return f"""
        query {{
        getRevenueEstimate(
            apiKey: "{apikey}"
            symbol: "{symbol}"
            country: "{country}"
        ) {{
            data {{
            avg_estimate
            date
            low_estimate
            number_of_analysts
            period
            year_ago_eps
            sales_growth
            high_estimate
            }}
            message
            status
        }}
        }}
        """
    
    @staticmethod
    def get_cash_flow(symbol:str,country:str,apikey:str)->str:
        return f"""
        query{{
        getCashFlow(symbol: "{symbol}", country: "{country}", apiKey: "{apikey}"){{
        message
        status
        data{{
            meta{{
            symbol
            name
            currency
            exchange
            mic_code
            exchange_timezone
            period
        }}
        cash_flow{{
            fiscal_date
            quarter
            operating_activities{{
            net_income
            depreciation
            deferred_taxes
            stock_based_compensation
            other_non_cash_items
            accounts_receivable
            accounts_payable
            other_assets_liabilities
            operating_cash_flow
            }}
            investing_activities{{
            capital_expenditures
            net_intangibles
            net_acquisitions
            purchase_of_investments
            sale_of_investments
            other_investing_activity
            investing_cash_flow
            }}
            financing_activities{{
            long_term_debt_issuance
            long_term_debt_payments
            short_term_debt_issuance
            common_stock_issuance
            common_stock_repurchase
            common_dividends
            other_financing_charges
            financing_cash_flow
            }}
            end_cash_position
            income_tax_paid
            interest_paid
            free_cash_flow
        }}
        }}
        }}
        }}
        """
    @staticmethod
    def get_financial_score(symbol:str,apikey:str)->str:
        return f"""
        query{{
        getStockFinancialScores(symbol: "{symbol}", apiKey: "{apikey}"){{
            message
            status
            data{{
                symbol
                altmanZScore
                piotroskiScore
                workingCapital
                totalAssets
                retainedEarnings
                ebit
                marketCap
                totalLiabilities
                revenue
            }}
        }}
        }}"""
    
    @staticmethod
    def get_financial_growth(symbol:str,limit:int,apikey:str)->str:
        return f"""
        query{{
        getFinancialGrowth(symbol: "{symbol}", limit: {limit}, apiKey: "{apikey}"){{
            message
            status
            data{{
            symbol
            date
            period
            revenueGrowth
            grossProfitGrowth
            ebitgrowth
            operatingIncomeGrowth
            netIncomeGrowth
            epsgrowth
            epsdilutedGrowth
            weightedAverageSharesGrowth
            weightedAverageSharesDilutedGrowth
            dividendsperShareGrowth
            operatingCashFlowGrowth
            freeCashFlowGrowth
            tenYRevenueGrowthPerShare
            fiveYRevenueGrowthPerShare
            threeYRevenueGrowthPerShare
            tenYOperatingCFGrowthPerShare
            fiveYOperatingCFGrowthPerShare
            threeYOperatingCFGrowthPerShare
            tenYNetIncomeGrowthPerShare
            fiveYNetIncomeGrowthPerShare
            threeYNetIncomeGrowthPerShare
            tenYShareholdersEquityGrowthPerShare
            fiveYShareholdersEquityGrowthPerShare
            threeYShareholdersEquityGrowthPerShare
            tenYDividendperShareGrowthPerShare
            fiveYDividendperShareGrowthPerShare
            threeYDividendperShareGrowthPerShare
            receivablesGrowth
            inventoryGrowth
            assetGrowth
            bookValueperShareGrowth
            debtGrowth
            rdexpenseGrowth
            sgaexpensesGrowth
            }}
        }}
        }}"""

    @staticmethod
    def get_stock_financial_statement(symbol:str,limit:int,apikey:str)->str:
        return f"""
        query{{
        getStockFinancialStatement(symbol: "{symbol}", limit: {limit}, apiKey: "{apikey}"){{
            message
            status
            data{{
            date
            symbol
            period
            growthRevenue
            growthCostOfRevenue
            growthGrossProfit
            growthGrossProfitRatio
            growthResearchAndDevelopmentExpenses
            growthGeneralAndAdministrativeExpenses
            growthSellingAndMarketingExpenses
            growthOtherExpenses
            growthOperatingExpenses
            growthCostAndExpenses
            growthInterestExpense
            growthDepreciationAndAmortization
            growthEBITDA
            growthEBITDARatio
            growthOperatingIncome
            growthOperatingIncomeRatio
            growthTotalOtherIncomeExpensesNet
            growthIncomeBeforeTax
            growthIncomeBeforeTaxRatio
            growthIncomeTaxExpense
            growthNetIncome
            growthNetIncomeRatio
            growthEPS
            growthEPSDiluted
            growthWeightedAverageShsOut
            growthWeightedAverageShsOutDil
            }}
        }}
        }}
        """




















    @staticmethod
    def get_social_sentiment_of_stock(symbol:str,apikey:str)->str:
        return f"""
        query {{
        getSocialSentimentOfStock(
            symbol: "{symbol}"
            apiKey: "{apikey}"
        ) {{
        message
        status
        data {{
            date
            symbol
            stocktwitsPosts
            twitterPosts
            stocktwitsComments
            twitterComments
            stocktwitsLikes
            twitterLikes
            stocktwitsImpressions
            twitterImpressions
            stocktwitsSentiment
            twitterSentiment
        }}
    }}
    }}"""


    @staticmethod
    def get_market_news(symbol:str,news_type:str,apikey:str)->str:
        return f"""
        query {{
        getMarketNews(
            symbol: "{symbol}"
            newsType: "{news_type}"
            apiKey: "{apikey}"
        ) {{
            message
            status
            data {{
            symbol
            publishedDate
            title
            image
            site
            text
            url
            }}
        }}
        }}"""


    @staticmethod
    def get_eps_trend(symbol:str,country:str,apikey:str)->str:
        return f"""
        query {{
        getEpsTrend(
            apiKey: "{apikey}"
            symbol: "{symbol}"
            country: "{country}"
        ) {{
            data {{
            period
            current_estimate
            date
            ninety_days_ago
            seven_days_ago
            sixty_days_ago
            thirty_days_ago
            }}
            message
            status
        }}
        }}"""

    @staticmethod
    def get_eps_revision(symbol:str,country:str,apikey:str)->str:
        return f"""
            query {{
            getEpsRevision(
                apiKey: "{apikey}"
                symbol: "{symbol}"
                country: "{country}"
            ) {{
                data {{
                date
                down_last_month
                down_last_week
                period
                up_last_month
                up_last_week
                }}
                message
                status
            }}
            }}"""

    @staticmethod
    def get_growth_estimates(symbol:str,country:str,apikey:str)->str:
        return f"""
        query {{
        getGrowthEstimates(
                apiKey: "{apikey}"
                symbol: "{symbol}"
                country: "{country}"
        ) {{
            data {{
            current_quarter
            current_year
            next_5_years_pa
            next_quarter
            next_year
            past_5_years_pa
            }}
            message
            status
        }}
        }}"""

    @staticmethod
    def get_stock_recommendation(symbol:str,country:str,apikey:str)->str:
            return f"""
            query {{
        getStockRecommendation(
                apiKey: "{apikey}"
                symbol: "{symbol}"
                country: "{country}"
        ) {{
            data {{
            trends {{
                current_month {{
                buy
                hold
                sell
                strong_buy
                strong_sell
                }}
                previous_month {{
                buy
                hold
                sell
                strong_buy
                strong_sell
                }}
                three_months_ago {{
                buy
                hold
                sell
                strong_buy
                strong_sell
                }}
                two_months_ago {{
                buy
                hold
                sell
                strong_buy
                strong_sell
                }}
            }}

            rating
            }}
            message
            status
        }}
        }}"""
    
    @staticmethod
    def get_analyst_ratings_light_data(symbol:str,country:str,apikey:str)->str:
        return f"""
        query {{
        getAnalystRatingsLightData(
            apiKey: "{apikey}"
            symbol: "{symbol}"
            country: "{country}"
        ) {{
            data {{
                date
                firm
                rating_change
                rating_current
                rating_prior
            }}
            message
            status
        }}
        }}"""


    @staticmethod
    def get_analyst_estimates(symbol:str,apikey:str)->str:
        return f"""
        query {{
        getAnalystEstimates(
            symbol: "{symbol}"
            apiKey: "{apikey}"
        ) {{
            message
            status
            data {{
            symbol
            date
            estimatedRevenueLow
            estimatedRevenueHigh
            estimatedRevenueAvg
            estimatedEbitdaLow
            estimatedEbitdaHigh
            estimatedEbitdaAvg
            estimatedEbitLow
            estimatedEbitHigh
            estimatedEbitAvg
            estimatedNetIncomeLow
            estimatedNetIncomeHigh
            estimatedNetIncomeAvg
            estimatedSgaExpenseLow
            estimatedSgaExpenseHigh
            estimatedSgaExpenseAvg
            estimatedEpsAvg
            estimatedEpsHigh
            estimatedEpsLow
            numberAnalystEstimatedRevenue
            numberAnalystsEstimatedEps
            }}
        }}
        }}"""

    @staticmethod
    def get_stock_earnings_surprises(symbol:str,apikey:str)->str:
        return f"""
        query {{
        getStockEarningsSurprises(symbol: "{symbol}"
        apiKey: "{apikey}") {{
            message
            status
            data {{
            actualEarningResult
            date
            estimatedEarning
            symbol
            }}
        }}
        }}
        """
    
    @staticmethod
    def get_overall_statistics(symbol:str,country:str,apikey:str)->str:
        return f"""
        query {{
    getOverallStatistics(
        symbol: "{symbol}"
        country: "{country}"
        apiKey: "{apikey}"
    ) {{
        message
        status
        data {{
        meta {{
            symbol
            name
            currency
            exchange
            mic_code
            exchange_timezone
        }}
        statistics {{
            valuations_metrics {{
            market_capitalization
            enterprise_value
            trailing_pe
            forward_pe
            peg_ratio
            price_to_sales_ttm
            price_to_book_mrq
            enterprise_to_revenue
            enterprise_to_ebitda
            }}
            financials {{
            fiscal_year_ends
            most_recent_quarter
            profit_margin
            operating_margin
            return_on_assets_ttm

            return_on_equity_ttm
            income_statement {{
                revenue_ttm
                revenue_per_share_ttm
                quarterly_revenue_growth
                gross_profit_ttm
                ebitda
                net_income_to_common_ttm
                diluted_eps_ttm
                quarterly_earnings_growth_yoy
            }}
            balance_sheet {{
                total_cash_mrq
                total_cash_per_share_mrq
                total_debt_mrq
                total_debt_to_equity_mrq
                current_ratio_mrq
                book_value_per_share_mrq
            }}
            cash_flow {{
                operating_cash_flow_ttm
                levered_free_cash_flow_ttm
            }}
            }}
            stock_statistics {{
            shares_outstanding
            float_shares
            avg_10_volume
            avg_30_volume
            shares_short
            short_ratio
            short_percent_of_shares_outstanding
            percent_held_by_insiders
            percent_held_by_institutions
            }}
            stock_price_summary {{
            fifty_two_week_low
            fifty_two_week_high
            fifty_two_week_change
            beta
            day_50_ma
            day_200_ma
            }}
            dividends_and_splits {{
            forward_annual_dividend_rate
            forward_annual_dividend_yield
            trailing_annual_dividend_rate
            trailing_annual_dividend_yield
            
            payout_ratio
            dividend_date
            five_year_average_dividend_yield
            ex_dividend_date
            last_split_factor
            last_split_date
            }}
        }}
        }}
    }}
    }}
    """

    @staticmethod
    def get_mutual_fund_holders(symbol:str, country: str, apikey: str)->str:
        return f"""
        query{{
        getMutualFundHolders(symbol: "{symbol}", country: "{country}", apiKey: "{apikey}"){{
        message
        status
            data{{
                meta{{
                    symbol
                    name
                    currency
                    exchange
                    mic_code
                    exchange_timezone
                }}
                fund_holders{{
                    entity_name
                    date_reported
                    shares
                    value
                    percent_held
                }}
            }}
        }}
        }}"""

    @staticmethod
    def get_institutional_holders(symbol:str, country: str, apikey: str)->str:
        return f"""
        query{{
        getInstitutionalHolders(symbol: "{symbol}", country: "{country}", apiKey: "{apikey}"){{
            message
            status
            data{{
            meta{{
                symbol
                name
                currency
                exchange
                mic_code
                exchange_timezone
            }}
            institutional_holders{{
                entity_name
                date_reported
                shares
                value
                percent_held
            }}
            }}
        }}
        }}"""

    @staticmethod
    def get_stock_ownership_by_holders(symbol:str, date: str, apikey: str)->str:
        return f"""
        query{{
        getStockOwnershipByHolders(symbol: "{symbol}", date: "{date}", apiKey: "{apikey}"){{
            message
            status
            data{{
                date
                cik
                filingDate
                investorName
                symbol
                securityName
                typeOfSecurity
                securityCusip
                sharesType
                putCallShare
                investmentDiscretion
                industryTitle
                weight
                lastWeight
                changeInWeight
                changeInWeightPercentage
                marketValue
                lastMarketValue
                changeInMarketValue
                changeInMarketValuePercentage
                sharesNumber
                lastSharesNumber
                changeInSharesNumber
                changeInSharesNumberPercentage
                quarterEndPrice
                avgPricePaid
                isNew
                isSoldOut
                ownership
                lastOwnership
                changeInOwnershipPercentage
                holdingPeriod
                firstAdded
                performance
                performancePercentage
                lastPerformance
                changeInPerformance
                isCountedForPerformance
            }}
        }}
        }}"""

    @staticmethod
    def get_etf_holders(apikey: str)->str:
        return f"""
        query{{
        getETFHolders(apiKey: "{apikey}"){{
        message
        status
        data{{
            asset
            name
            isin
            cusip
            sharesNumber
            weightPercentage
            marketValue
             updated
            }}
        }}
        }}"""
    
    @staticmethod
    def get_stock_response(symbol:str ,apikey:str)->str:
        return f"""
        query{{
        getStockResponse(symbol: "{symbol}", apiKey: "{apikey}"){{
            message
            status
            data{{
                symbol
                date
                freeFloat
                floatShares
                outstandingShares
                source
            }}
        }}
        }}"""

    
    @staticmethod
    def get_etf_sector_weightings(apikey:str)->str:
        return f"""
        query{{
        getETFSectorWeightings(apiKey: "{apikey}"){{
            message
            status
            data{{
                sector
                weightPercentage
            }}
        }}
        }}"""

    @staticmethod
    def get_time_series(symbol:str,interval:str,start_date:str,end_date:str,apikey:str)->str:
        return f"""
        query{{
        getTimeSeries(symbol:"{symbol}",interval:"{interval}",startDate:"{start_date}",endDate:"{end_date}",apiKey:"{apikey}")
        {{
        data{{
            close
            datetime
            high
            low
            open
            volume
        }}
        message
        status
        }}
        }}"""
    

    @staticmethod
    def get_gainers_or_losers(type:str,apikey:str,country:str)->str:
        return f"""query {{
        getGainersOrLosers(
            type: "{type}"
            country:"{country}"
            apiKey: "{apikey}"
        ) {{
            data {{
                symbol
                change
                name
                changesPercentage
            }}
            message
            status
        }}
        }}"""


    @staticmethod
    def get_stock_market_holiday_data(year:int,apikey:str)->str:
        return f"""
        query {{
        getStockMarketHolidayData(
            year: {year}
            apiKey: "{apikey}"
        ) {{
            data {{
            year
            holidays {{
                date
                name
            }}
            }}
            message
            status
        }}
        }}"""
    



    @staticmethod
    def get_market_status_data(exchange:str,country:str,apikey:str)->str:
        return f"""
        query {{
        getMarketStatusData(
            exchangeName: "{exchange}"
            country: "{country}"
            apiKey: "{apikey}"
        ) {{
            data {{
            exchange_name
            is_market_open
            time_to_close
            time_to_open
            country
            time_after_open
            code
            }}
            message
            status
        }}
        }}"""


    @staticmethod
    def get_dividend_calendar(apikey:str,symbol:str,limit:str)->str:
        return f"""
        query {{
        getDividendCalendar(
            apiKey: "{apikey}"
            symbol: "{symbol}"
            limit:{limit}
        ) {{
            data {{
            symbol
            historical {{
                date
                label
                adjDividend
                dividend
                recordDate
                paymentDate
                declarationDate
            }}
            }}
            message
            status
        }}
        }}"""


    @staticmethod
    def get_earning_calendar(from_date:str,to_date:str,apikey:str)->str:
        return f"""
        query {{
        getEarningCalendar(
            fromDate: "{from_date}"
            toDate: "{to_date}"
            apiKey: "{apikey}"
        ) {{
            data {{
                symbol
                fiscalDateEnding
                time
                revenue
                date
                revenueEstimated
                eps
                updatedFromDate
                epsEstimated
            }}
            status
            message
        }}
        }}"""

    @staticmethod
    def get_economic_calendar(from_date:str,to_date:str,apikey:str)->str:
        return f"""
        query {{
        getEconomicCalendar(
            fromDate: "{from_date}"
            toDate: "{to_date}"
            apiKey: "{apikey}"
        ) {{
            data {{
                country
                impact
                event
                date
                actual
                previous
                changePercentage
                change
                estimate
            }}
            status
            message
        }}
        }}
        """
    
    @staticmethod
    def get_split_calendar(from_date:str,to_date:str,apikey:str)->str:
        return f"""
        query {{
        getSplitCalendar(
            fromDate: "{from_date}"
            toDate: "{to_date}"
            apiKey: "{apikey}"
        ) {{
            data {{
                symbol
                label
                date
                denominator
                numerator
            }}
            status
            message
        }}
        }}"""


    @staticmethod
    def get_technical_indicators(apikey:str,ticker:str,interval:str,indicator:str,limit)->str:
        return f"""query {{
            getTechnicalIndicators(
            apiKey: "{apikey}"
            ticker: "{ticker}"
            interval: "{interval}"
            indicator: "{indicator}"
            limit: {limit}
        ) {{
            data {{
            meta {{
                currency
                exchange
                indicator {{
                name
                }}
                interval
                exchange_timezone
                mic_code
                type
            }}
            values 
            }}
            message
            status
        }}
        }}"""
    
    @staticmethod
    def get_ipo_stock_data(start_time:str,end_time:str,limit:int,apikey:str)->str:
        return f"""
        query {{
        getIPOStockData(
            startTime: "{start_time}"
            endTime: "{end_time}"
            limit: {limit}
            apiKey: "{apikey}"
        ) {{
            data {{
                actions
                company
                date
                exchange
                marketCap
                priceRange
                shares
                symbol
            }}
            message
            status
        }}
        }}"""
    
    @staticmethod
    def get_times_series_data(symbol:str,country:str,interval:str,limit:str,apikey:str)->str:
        return f"""
        query {{
        getTimesSeriesData(
            apiKey: "{apikey}"
            symbol: "{symbol}"
            country: "{country}"
            interval: "{interval}",
            limit:{limit}
        ) {{
            data {{
            meta {{
                currency
                exchange
                interval
                exchange_timezone
                mic_code
                type
            }}
            values {{
                datetime
                open
                high
                low
                close
                volume
            }}
            }}

            message
            status
        }}
        }}
        """

    @staticmethod
    def get_times_series_data_by_date(symbol:str,country:str,interval:str,limit:int,apikey:str,start_date:str,
                                      end_date:str
                                      
                                      )->str:
        return f"""query {{
        getTimesSeriesData(
            apiKey: "{apikey}"
            symbol: "{symbol}"
            country: "{country}"
            interval: "{interval}",
            limit:{limit}
            startDate:"{start_date}",
            endDate:"{end_date}"
        ) {{
            data {{
            meta {{
                currency
                exchange
                interval
                exchange_timezone
                mic_code
                type
            }}
            values {{
                datetime
                open
                high
                low
                close
                volume
            }}
            }}

            message
            status
        }}
        }}"""
    
        
    @staticmethod
    def get_stock_trends_chart_data( symbol: str,
                                    interval: str,
                                    type: str,
                                    chart_type: str,
                                    exchange: str,
                                    country_id: str,
                                    api_key: str):
        return f"""
            query {{
            getStockTrendsChartData(
            symbol: "{symbol}"
            interval: "{interval}"
            type: "{type}"
            chartType: "{chart_type}"
            exchange: "{exchange}"
            countryId: {country_id}
            apiKey: "{api_key}"
            ){{
                message
                status
                data {{
                date
                close
                high
                open
                low
                tradeCount
                VWAP
                y
            }}
        }}
        }}
    """
    
    @staticmethod
    def get_bot_user_permission_list(list_type:str,stockly_userid:int,bot_id:str,apikey:str):
        return f"""
            query {{
            getBotUserPermissionList(
                type: "{list_type}"
                userId: {stockly_userid}
                botMatrixId: "{bot_id}"
                apiKey: "{apikey}"
            ) {{
                status
                message
                data {{
                s2_bot_permission {{
                    description
                    id
                    name
                }}
                list {{
                    response {{
                    ticker_id
                    ticker_name
                    ticker_symbol
                    
                    }}
                    }}
                }}
                }}
            }}"""




    @staticmethod
    def get_stock_details_data(country:str,page_no:int,records_required:int,apikey:str):
        return f"""

            query {{
            getStocksDetailsData(
                country: "{country}"
                pageNumber: {page_no}
                pageSize:{records_required}
                apiKey: "{apikey}"
            ) {{
                status
                message
                data {{
                    company_name
                    id_s2_stock_type
                    s2_stock_type {{
                        name
                }}
                    ticker_symbol
                    s2_exchange {{
                    name
                }}
                s2_sectors {{
                name
            }}
            }}
        }}
        }}
        """
    
    @staticmethod
    def add_bot_user_specific_configs(stockly_user_id:int,bot_id:str,data:str,apikey:str)->str:
        return f'''mutation {{
        addBotUserSpecificConfigs(
            userId: {stockly_user_id}
            botMatrixId: "{bot_id}"
            config: """{data}"""
            apiKey: "{apikey}"
        ) {{
            message
            status
        }}
        }}
        '''

    @staticmethod
    def get_bot_user_specific_configs(bot_id:str,apikey:str,stockly_user_id:int=None)->str:
        if stockly_user_id:
            return f"""
                query{{
                getBotUserSpecificConfigs(
                    userId: {stockly_user_id}
                    botMatrixId: "{bot_id}"
                    apiKey: "{apikey}"
                    ){{
                    data{{
                        config
                        id_s2_users
                    }}
                    message
                    status
                }}
                }}
                """
        return f"""
            query{{
            getBotUserSpecificConfigs(
                botMatrixId: "{bot_id}"
                apiKey: "{apikey}"
                ){{
                data{{
                    config
                    id_s2_users
                }}
                message
                status
            }}
            }}
            """
    
    def get_bot_subscribe_user_developer(bot_id:str,apikey:str)->str:
        return f"""
        query {{
        getBotSubscribeUserDeveloper(
            matrixId: "{bot_id}"
            apiKey: "{apikey}"
        ) {{
            status
            message
            data {{
            bot_matrix_room_detail {{
             room_id
            }}
            s2_users {{
                id
                cts
                full_name
                username
            }}
            }}
        }}
        }}
        """
