import math
import re
from functools import reduce
import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import scipy as scp
from scipy import stats

ENGLISH_COUNTRIES = ['AUS', 'NZL', 'GBR', 'USA', 'ATG', 'BHS', 'BRB', 'BLZ', 'BWA', 'BDI', 'CMR', 'CAN', 'DMA', 'SWZ', 'FJI', 'GMB', 'GHA', 'GRD', 'GUY', 'IND', 'IRL', 'JAM', 'KEN', 'KIR', 'LSO', 'LBR', 'MWI', 'MLT', 'MHL', 'MUS', 'FSM', 'NAM', 'NRU', 'NGA', 'PAK', 'PLW', 'PNG', 'PHL', 'KNA', 'LCA', 'VCT', 'WSM', 'SYC', 'SLE', 'SGP', 'SLB', 'ZAF', 'SSD', 'SDN', 'TZA', 'TON', 'TTO', 'TUV', 'VUT', 'ZMB', 'ZWE', 'BHR', 'BGD', 'BRN', 'KHM', 'CYP', 'ERI', 'ETH', 'ISR', 'JOR', 'KWT', 'MYS', 'MDV', 'MMR', 'OMN', 'QAT', 'RWA', 'LKA', 'UGA', 'ARE']
ORGANIZATION = "/organization/"
EMPTY_STRING = ""

class Columns:
    ROUNDS2_COMPANY_PERMALINK = "company_permalink"
    COMPANIES_COMPANY_PERMALINK = "permalink"
    ROUNDS2_COMPANY_PERMALINK_LOWERCASE = "company_permalink_lowercase"
    COMPANIES_COMPANY_PERMALINK_LOWERCASE = "permalink_lowercase"
    COMPANIES_NAME = "name"
    ORGANIZATION = "/organization/"
    FUNDING_ROUND_TYPE = "funding_round_type"
    RAISED_AMOUNT_USD = "raised_amount_usd"
    COUNTRY_CODE = "country_code"
    CATEGORY_LIST = "category_list"
    VALUE = "value"
    VARIABLE = "variable"
    PRIMARY_SECTOR = "primary_sector"
    MAIN_SECTOR = "main_sector"

class InvestmentTypes:
    SEED = "seed"
    ANGEL = "angel"
    VENTURE = "venture"
    PRIVATE_EQUITY = "private_equity"

def sanitized(s):
    return s.replace(" ", "-").replace(".", "-")

def with_organization_prefix(s):
    return f"{ORGANIZATION}{s}"

def pattern_for_rounds_matching(company_name):
    return f'{ORGANIZATION}{sanitized(company_name.lower())}'

def constant(x):
    return lambda company_name: x

def merge_companies_rounds(companies, rounds):
    print(f"Number of Companies: {len(companies)}")
    print(f"Number of Rounds: {len(rounds)}")
    return pd.merge(companies, rounds, left_on = Columns.COMPANIES_COMPANY_PERMALINK_LOWERCASE, right_on = Columns.ROUNDS2_COMPANY_PERMALINK_LOWERCASE)

def boxplot(investment_type, x, y, axis, stuff):
    print(f"Statistics for {investment_type} investments:")
    print(stuff.loc[investment_type, Columns.RAISED_AMOUNT_USD].describe().apply(lambda x: format(x, 'f')))
    # print(f"Number of {investment_type} investments: {len(stuff.loc[investment_type, Columns.RAISED_AMOUNT_USD])}" )
    # print(f"Median investment oof type {investment_type}: {stuff.loc[investment_type, Columns.RAISED_AMOUNT_USD].median()}" )
    axis[x,y].boxplot(stuff.loc[investment_type, Columns.RAISED_AMOUNT_USD])
    axis[x,y].set_title(investment_type)

def analyse_investment_types(master_funding):
    # Use only 4 investment types
    investments_with_4_types = master_funding[(master_funding[Columns.FUNDING_ROUND_TYPE] == InvestmentTypes.ANGEL) |
                                              (master_funding[Columns.FUNDING_ROUND_TYPE] == InvestmentTypes.SEED) |
                                              (master_funding[Columns.FUNDING_ROUND_TYPE] == InvestmentTypes.VENTURE) |
                                              (master_funding[Columns.FUNDING_ROUND_TYPE] == InvestmentTypes.PRIVATE_EQUITY)]
    print(f"Only English Investments of 4 Types: {len(investments_with_4_types)}")

    funding_amounts_with_investment_types = investments_with_4_types[[Columns.FUNDING_ROUND_TYPE, Columns.RAISED_AMOUNT_USD]]

    # Remove outliers
    funding_by_investment_type = funding_amounts_with_investment_types.groupby(Columns.FUNDING_ROUND_TYPE)
    funding_by_investment_without_outliers = funding_by_investment_type.apply(lambda g: g[(g[Columns.RAISED_AMOUNT_USD] > g[Columns.RAISED_AMOUNT_USD].quantile(q=0.05)) & (g[Columns.RAISED_AMOUNT_USD] < g[Columns.RAISED_AMOUNT_USD].quantile(q=0.90))])

    # Create boxplots
    figure, axis = plt.subplots(2, 2)
    boxplot(InvestmentTypes.SEED, 0, 0, axis, funding_by_investment_without_outliers)
    boxplot(InvestmentTypes.ANGEL, 0, 1, axis, funding_by_investment_without_outliers)
    boxplot(InvestmentTypes.VENTURE, 1, 0, axis, funding_by_investment_without_outliers)
    boxplot(InvestmentTypes.PRIVATE_EQUITY, 1, 1, axis, funding_by_investment_without_outliers)
    plt.show()

def english_speaking_countries(fundings):
    only_english_company_investments = fundings[fundings[Columns.COUNTRY_CODE].isin(ENGLISH_COUNTRIES)]
    print(f"English Company Investments: {len(only_english_company_investments)}")
    print(f"Non-English Company Investments: {len(fundings) - len(only_english_company_investments)}")
    return only_english_company_investments

def top_9_countries(investments):
    aggregator = {}
    aggregator[Columns.RAISED_AMOUNT_USD] = "sum"
    investments_by_country = investments.groupby(Columns.COUNTRY_CODE)
    sorted_countrywise_investments = investments_by_country.agg(aggregator).reset_index(level=0, inplace=False).sort_values(by=Columns.RAISED_AMOUNT_USD, ascending = False)
    print(f"Countrywise Investments:")
    print(sorted_countrywise_investments)
    return sorted_countrywise_investments.head(9)


def with_sectors(english_venture_investments_with_outliers):
    pass

def analyse():
    global ROUNDS2_COMPANY_PERMALINK
    global COMPANIES_COMPANY_PERMALINK
    global ROUNDS2_COMPANY_PERMALINK_LOWERCASE
    global COMPANIES_COMPANY_PERMALINK_LOWERCASE

    companies = pd.read_csv("../data/companies.csv")
    rounds = pd.read_csv("../data/rounds2.csv")
    mapping = pd.read_csv("../data/mapping.csv")
    print(companies.columns)
    print(mapping.columns)
    print(rounds.columns)

    sector_map = mapping_dict(mapping)

    # Fix case
    rounds[Columns.ROUNDS2_COMPANY_PERMALINK_LOWERCASE] = rounds[Columns.ROUNDS2_COMPANY_PERMALINK].str.lower()
    companies[Columns.COMPANIES_COMPANY_PERMALINK_LOWERCASE] = companies[Columns.COMPANIES_COMPANY_PERMALINK].str.lower()
    unique_companies_in_companies, unique_companies_in_rounds2 = unique_companies(companies, rounds)
    # How many unique companies are present in rounds?
    print(len(unique_companies_in_rounds2))

    # How many unique companies are present in companies?
    print(len(unique_companies_in_companies))

    # In the companies data frame, which column can be used as the unique key for each company? Write the name of the column.
    # permalink

    # Are there any companies in the rounds file which are not present in companies? Answer yes or no: Y/N
    companies_not_in_companies = set(unique_companies_in_rounds2).difference(set(unique_companies_in_companies))
    companies_not_in_rounds2 = set(unique_companies_in_companies).difference(set(unique_companies_in_rounds2))
    print(len(companies_not_in_companies))
    print(companies_not_in_companies)
    # print(len(companies_not_in_rounds2))
    # YES

    clean_permalinks(companies, rounds)
    master_funding = merge_companies_rounds(companies, rounds)
    master_funding[Columns.PRIMARY_SECTOR] = master_funding[Columns.CATEGORY_LIST].str.split("|").apply(lambda splits: splits[0] if isinstance(splits, list) else EMPTY_STRING)
    master_funding[Columns.MAIN_SECTOR] = master_funding[Columns.PRIMARY_SECTOR].apply(lambda primary_sector: sector_map[primary_sector])
    print("MASTER FUNDING")
    print(master_funding.head(10))
    print("-----------------------------------------")
    english_master_funding = english_speaking_countries(master_funding)
    print(f"Only English Investments: {len(english_master_funding)}")
    analyse_investment_types(english_master_funding)

    # Calculate the most representative value of the investment amount for each of the four funding types (venture, angel, seed, and private equity) and report the answers in Table 2.1
    # Fill in Table
    # Based on the most representative investment amount calculated above, which investment type do you think is the most suitable for Spark Funds?
    # Venture Investments
    english_venture_investments_with_outliers = english_master_funding[english_master_funding[Columns.FUNDING_ROUND_TYPE] == InvestmentTypes.VENTURE]
    print(f"English-only Venture Investments Selected: {len(english_venture_investments_with_outliers)}")
    top9 = top_9_countries(english_venture_investments_with_outliers)
    print("Top 9 Countrywise Investments:")
    print(top9)
    # Fill Top 3 Countries from the Above List
    english_venture_investments_with_outliers_with_sectors = with_sectors(english_venture_investments_with_outliers)


def mapping_dict(mapping):
    mapping = mapping.melt([Columns.CATEGORY_LIST])

    # Cleaning data
    # mapping.loc[mapping[Columns.CATEGORY_LIST] == "A0lytics", Columns.CATEGORY_LIST] = "Analytics"
    mapping[Columns.CATEGORY_LIST] = mapping[Columns.CATEGORY_LIST].str.replace("0", "na")
    mapping.loc[mapping[Columns.CATEGORY_LIST] == "nanotechnology", Columns.CATEGORY_LIST] = "Nanotechnology"

    mapping = mapping[mapping[Columns.VALUE] == 1][[Columns.CATEGORY_LIST, Columns.VARIABLE]]
    mappings_as_list = mapping.values.tolist()
    mapping_as_dict = {}
    for pair in mappings_as_list:
        print(pair)
        mapping_as_dict[pair[0] if isinstance(pair[0], str) else EMPTY_STRING] = pair[1]
    print("Mapping is:")
    print(mapping_as_dict)
    return mapping_as_dict

def clean_permalinks(companies, rounds):
    # Fix inconsistent Data
    fix_permalink_from_rounds = fix_permalink_from_rounds_builder(pattern_for_rounds_matching, companies, rounds)
    fix_permalink_from_rounds("Boréal Bikes Incorporated")
    fix_permalink_from_rounds("Tío Conejo")
    fix_permalink_from_rounds("Monnier Frères")
    fix_permalink_from_rounds("Affluent Attaché Club", locator=constant(with_organization_prefix("affluent-attaché-club-2")))
    fix_permalink_from_rounds("Jean Pütz Produkte")
    fix_permalink_from_rounds("PatroFİN")
    fix_permalink_from_rounds("Salão VIP")
    fix_permalink_from_rounds("Proděti.cz")
    fix_permalink_from_rounds("LawPadi", locator=constant(with_organization_prefix("lawpàdí")))
    fix_permalink_from_rounds("eTool.io")
    fix_permalink_from_rounds("Crème & Ciseaux", locator=constant(with_organization_prefix("crème-ciseaux")))
    fix_permalink_from_rounds("Prześwietl.pl")
    fix_permalink_from_rounds("Capptú")
    fix_permalink_from_rounds("Gráfica en línea")
    fix_permalink_from_rounds("IGNIA Bienes Raíces")
    fix_permalink_from_rounds("Bricoprivé.com")
    fix_permalink_from_rounds("Médica Santa Carmen", locator=constant(with_organization_prefix("médica-santa-carmen-2")))
    fix_permalink_from_rounds("E CÚBICA", locator=constant(with_organization_prefix("e-cêbica")))
    fix_permalink_from_rounds("Vá de Táxi")
    fix_permalink_from_companies("It’s All About Me", "S-ALL-ABOUT-ME", companies, rounds)
    fix_permalink_from_companies("Whodat’s Spaces", "WHODAT", companies, rounds)
    fix_permalink_from_companies("know’N’act", "KNOW", companies, rounds)
    fix_permalink_from_companies("iProof - The Foundation for the Internet of Things™",
                                 "IPROOF---THE-FOUNDATION-FOR-THE-INTERNET-OF-THINGS", companies, rounds)
    fix_permalink_from_companies("ÁERON", "�eron", companies, rounds)
    # This needs some extra fixing
    fix_permalink_from_companies("Crème & Ciseaux", "e-ciseaux", companies, rounds)
    regenerate_permalink("ZenGame", "ZenGame 禅游科技", companies, rounds)
    regenerate_permalink("EnergyStone Games", "EnergyStone Games 灵石游戏", companies, rounds)
    regenerate_permalink("Magnet Tech ", "Magnet Tech 磁石科技", companies, rounds)
    regenerate_permalink("Huizuche.com", "Huizuche.com 惠租车", companies, rounds)
    regenerate_permalink("Inveno ", "Inveno 英威诺", companies, rounds)
    regenerate_permalink("Weiche Tech ", "Weiche Tech 喂车科技", companies, rounds)
    regenerate_permalink("TipCat Interactive", "TipCat Interactive 沙舟信息科技", companies, rounds)
    regenerate_permalink("Jiwu", "Jiwu 吉屋网", companies, rounds)
    regenerate_permalink("TalentSigned", "TalentSigned™", companies, rounds)
    regenerate_permalink("Asiansbook", "Asiansbook™", companies, rounds)
    regenerate_permalink("Reklam-Ve-Tan", "İnovatiff Reklam ve Tanıtım Hizmetleri Tic", companies, rounds, EMPTY_STRING)
    regenerate_permalink("thế-giới-di", "The Gioi Di Dong", companies,
                         rounds)  # This permalink is mangled in both data sets, generated new permalink
    regenerate_permalink("k��k", "KÖÖK", companies, rounds)
    x, y = unique_companies(companies, rounds)
    print(set(y).difference(set(x)))
    print(set(x).difference(set(y)))


def regenerate_permalink(company_name_prefix, full_company_name, companies, rounds2,
                         optional_organization_prefix=ORGANIZATION):
    global ROUNDS2_COMPANY_PERMALINK
    global COMPANIES_NAME

    dashed_company_name_prefix = sanitized(company_name_prefix)
    dashed_lowercase_full_company_name = sanitized(full_company_name).lower()
    corrected_permalink_lowercase = (f'/organization/{dashed_lowercase_full_company_name}').lower()
    print(corrected_permalink_lowercase)
    companies.loc[companies[Columns.COMPANIES_NAME].str.contains(full_company_name, na=False), Columns.COMPANIES_COMPANY_PERMALINK_LOWERCASE] = corrected_permalink_lowercase
    rounds2.loc[rounds2[Columns.ROUNDS2_COMPANY_PERMALINK].str.contains(f'{optional_organization_prefix}{dashed_company_name_prefix}',
                                                                na=False, case=False, regex=False), Columns.ROUNDS2_COMPANY_PERMALINK_LOWERCASE] = corrected_permalink_lowercase
    print(companies[companies[Columns.COMPANIES_COMPANY_PERMALINK_LOWERCASE].str.contains(corrected_permalink_lowercase, na=False, case=False)])
    print(rounds2[rounds2[Columns.ROUNDS2_COMPANY_PERMALINK_LOWERCASE].str.contains(corrected_permalink_lowercase, na=False, case=False)])

def fix_permalink_from_rounds_builder(company_permalink_locator_in_round, companies, rounds):
    def fix_permalink_from_rounds_inner(company_name, locator = company_permalink_locator_in_round):
        company_permalink_from_rounds = locator(company_name)
        global COMPANIES_NAME

        correct_value_rows = rounds[rounds[Columns.ROUNDS2_COMPANY_PERMALINK_LOWERCASE] == company_permalink_from_rounds]
        corrected_value = correct_value_rows.iloc[0][Columns.ROUNDS2_COMPANY_PERMALINK_LOWERCASE]
        companies.loc[companies[Columns.COMPANIES_NAME] == company_name, Columns.COMPANIES_COMPANY_PERMALINK_LOWERCASE] = corrected_value
        print(companies[companies[Columns.COMPANIES_NAME] == company_name].to_string())
        print(rounds[rounds[Columns.ROUNDS2_COMPANY_PERMALINK_LOWERCASE] == corrected_value].to_string())

    return fix_permalink_from_rounds_inner

def fix_permalink_from_companies(company_name, rounds_permalink_fragment, companies, rounds, truth_column = Columns.COMPANIES_COMPANY_PERMALINK_LOWERCASE):
    global COMPANIES_NAME

    correct_value_rows = companies[companies[Columns.COMPANIES_NAME] == company_name]
    lowercase_corrected_value = correct_value_rows.iloc[0][truth_column].lower()
    rounds.loc[rounds[Columns.ROUNDS2_COMPANY_PERMALINK_LOWERCASE].str.contains(rounds_permalink_fragment, na=False, case=False, regex=False), Columns.ROUNDS2_COMPANY_PERMALINK_LOWERCASE] = lowercase_corrected_value
    print(companies[companies[truth_column] == lowercase_corrected_value].to_string())
    print(rounds[rounds[Columns.ROUNDS2_COMPANY_PERMALINK_LOWERCASE] == lowercase_corrected_value].to_string())

def unique_companies(companies, rounds2):
    global ROUNDS2_COMPANY_PERMALINK_LOWERCASE
    global COMPANIES_COMPANY_PERMALINK_LOWERCASE

    unique_companies_in_rounds2 = rounds2[Columns.ROUNDS2_COMPANY_PERMALINK_LOWERCASE].unique()
    unique_companies_in_companies = companies[Columns.COMPANIES_COMPANY_PERMALINK_LOWERCASE].unique()
    return unique_companies_in_companies, unique_companies_in_rounds2

analyse()

