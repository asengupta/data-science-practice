import re
from functools import reduce
import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import scipy as scp
from scipy import stats

ROUNDS2_COMPANY_PERMALINK = "company_permalink"
COMPANIES_COMPANY_PERMALINK = "permalink"

ROUNDS2_COMPANY_PERMALINK_LOWERCASE = "company_permalink_lowercase"
COMPANIES_COMPANY_PERMALINK_LOWERCASE = "permalink_lowercase"
COMPANIES_NAME = "name"

def analyse():
    global ROUNDS2_COMPANY_PERMALINK
    global COMPANIES_COMPANY_PERMALINK
    global ROUNDS2_COMPANY_PERMALINK_LOWERCASE
    global COMPANIES_COMPANY_PERMALINK_LOWERCASE

    companies = pd.read_csv("../data/companies.csv")
    mapping = pd.read_csv("../data/mapping.csv")
    rounds2 = pd.read_csv("../data/rounds2.csv")
    print(companies.columns)
    print(mapping.columns)
    print(rounds2.columns)

    # Fix case
    rounds2[ROUNDS2_COMPANY_PERMALINK_LOWERCASE] = rounds2[ROUNDS2_COMPANY_PERMALINK].str.lower()
    companies[COMPANIES_COMPANY_PERMALINK_LOWERCASE] = companies[COMPANIES_COMPANY_PERMALINK].str.lower()
    unique_companies_in_companies, unique_companies_in_rounds2 = uniques(companies, rounds2)
    # How many unique companies are present in rounds2?
    print(len(unique_companies_in_rounds2))

    # How many unique companies are present in companies?
    print(len(unique_companies_in_companies))

    # In the companies data frame, which column can be used as the unique key for each company? Write the name of the column.
    # permalink

    # Are there any companies in the rounds2 file which are not present in companies? Answer yes or no: Y/N
    companies_not_in_companies = set(unique_companies_in_rounds2).difference(set(unique_companies_in_companies))
    companies_not_in_rounds2 = set(unique_companies_in_companies).difference(set(unique_companies_in_rounds2))
    print(len(companies_not_in_companies))
    print(companies_not_in_companies)
    # print(len(companies_not_in_rounds2))
    # YES

    #Fix inconsistent Data
    # Fix BORéAL-BIKES-INCORPORATED

    fix("Boréal Bikes Incorporated", "/organization/boréal-bikes-incorporated", rounds2, companies)
    fix("Tío Conejo", "/organization/tío-conejo", rounds2, companies)
    fix("Monnier Frères", "/organization/monnier-frères", rounds2, companies)
    fix("Affluent Attaché Club", "/organization/affluent-attaché-club-2", rounds2, companies)
    fix("Jean Pütz Produkte", "/organization/jean-pütz-produkte", rounds2, companies)
    fix("PatroFİN", "/organization/patrofi̇n", rounds2, companies)
    fix("Salão VIP", "/organization/salão-vip", rounds2, companies)
    fix("Proděti.cz", "/organization/proděti-cz", rounds2, companies)
    fix("LawPadi", "/organization/lawpàdí", rounds2, companies)
    fix("eTool.io", "/organization/etool-io", rounds2, companies)
    fix("Crème & Ciseaux", "/organization/crème-ciseaux", rounds2, companies)
    fix("Prześwietl.pl", "/organization/prześwietl-pl", rounds2, companies)
    fix("Capptú", "/organization/capptú", rounds2, companies)
    fix("Gráfica en línea", "/organization/gráfica-en-línea", rounds2, companies)
    fix("IGNIA Bienes Raíces", "/organization/ignia-bienes-raíces", rounds2, companies)
    fix("Bricoprivé.com", "/organization/bricoprivé-com", rounds2, companies)
    fix("Médica Santa Carmen", "/organization/médica-santa-carmen-2", rounds2, companies)
    fix("Weiche Tech 喂车科技", "/organization/weiche-tech-喂车科暀", rounds2, companies)
    # fix("Magnet Tech 磁石科技", "/organization/magnet-tech-磁??科暀", rounds2, companies)
    # fix("iProof - The Foundation for the Internet of Things", "/organization/affluent-attaché-club-2", rounds2, companies)
    fix_zengame(companies, rounds2, "ZenGame", "ZenGame 禅游科技")
    fix_zengame(companies, rounds2, "EnergyStone Games", "EnergyStone Games 灵石游戏")
    fix_zengame(companies, rounds2, "Magnet Tech ", "Magnet Tech 磁石科技")

    x, y = uniques(companies, rounds2)
    print(set(y).difference(set(x)))

def fix_zengame(companies, rounds2, company_name_prefix, full_company_name):
    global ROUNDS2_COMPANY_PERMALINK
    global COMPANIES_NAME

    zengame = companies[companies[COMPANIES_NAME].str.startswith(company_name_prefix, na=False)]
    correct_name = zengame.iloc[0][COMPANIES_NAME]
    # result = re.compile(f"{original_company_name_prefix} (.*)").search(correct_name)
    dashed_company_name_prefix = company_name_prefix.replace(' ', '-')
    dashed_lowercase_full_company_name = full_company_name.replace(' ', '-').lower()
    corrected_permalink_lowercase = (f'/organization/{dashed_lowercase_full_company_name}').lower()
    print(corrected_permalink_lowercase)
    companies.loc[companies[COMPANIES_NAME].str.contains(full_company_name, na=False), COMPANIES_COMPANY_PERMALINK_LOWERCASE] = corrected_permalink_lowercase
    rounds2.loc[rounds2[ROUNDS2_COMPANY_PERMALINK].str.contains(dashed_company_name_prefix,
                                                                na=False, case=False), ROUNDS2_COMPANY_PERMALINK_LOWERCASE] = corrected_permalink_lowercase
    # print(companies.iloc[65778])
    print(companies[companies[COMPANIES_COMPANY_PERMALINK_LOWERCASE].str.contains(corrected_permalink_lowercase, na=False, case=False)])
    print(rounds2[rounds2[ROUNDS2_COMPANY_PERMALINK_LOWERCASE].str.contains(corrected_permalink_lowercase, na=False, case=False)])

def fix(company_name, company_permalink, truth, corrupted):
    global COMPANIES_NAME

    correct_value_rows = truth[truth[ROUNDS2_COMPANY_PERMALINK_LOWERCASE] == company_permalink]
    # print(correct_value_rows.iloc[0][ROUNDS2_COMPANY_PERMALINK_LOWERCASE])
    corrected_value = correct_value_rows.iloc[0][ROUNDS2_COMPANY_PERMALINK_LOWERCASE]
    corrupted.loc[corrupted[COMPANIES_NAME] == company_name, COMPANIES_COMPANY_PERMALINK_LOWERCASE] = corrected_value
    print(corrupted[corrupted[COMPANIES_NAME] == company_name].to_string())
    print(truth[truth[ROUNDS2_COMPANY_PERMALINK_LOWERCASE] == corrected_value].to_string())

def uniques(companies, rounds2):
    global ROUNDS2_COMPANY_PERMALINK_LOWERCASE
    global COMPANIES_COMPANY_PERMALINK_LOWERCASE

    unique_companies_in_rounds2 = rounds2[ROUNDS2_COMPANY_PERMALINK_LOWERCASE].unique()
    unique_companies_in_companies = companies[COMPANIES_COMPANY_PERMALINK_LOWERCASE].unique()
    return unique_companies_in_companies, unique_companies_in_rounds2

analyse()

