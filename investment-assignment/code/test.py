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
    fix_permalink_from_rounds("Boréal Bikes Incorporated", "/organization/boréal-bikes-incorporated", companies,
                              rounds2)
    fix_permalink_from_rounds("Tío Conejo", "/organization/tío-conejo", companies, rounds2)
    fix_permalink_from_rounds("Monnier Frères", "/organization/monnier-frères", companies, rounds2)
    fix_permalink_from_rounds("Affluent Attaché Club", "/organization/affluent-attaché-club-2", companies, rounds2)
    fix_permalink_from_rounds("Jean Pütz Produkte", "/organization/jean-pütz-produkte", companies, rounds2)
    fix_permalink_from_rounds("PatroFİN", "/organization/patrofi̇n", companies, rounds2)
    fix_permalink_from_rounds("Salão VIP", "/organization/salão-vip", companies, rounds2)
    fix_permalink_from_rounds("Proděti.cz", "/organization/proděti-cz", companies, rounds2)
    fix_permalink_from_rounds("LawPadi", "/organization/lawpàdí", companies, rounds2)
    fix_permalink_from_rounds("eTool.io", "/organization/etool-io", companies, rounds2)
    fix_permalink_from_rounds("Crème & Ciseaux", "/organization/crème-ciseaux", companies, rounds2)
    fix_permalink_from_rounds("Prześwietl.pl", "/organization/prześwietl-pl", companies, rounds2)
    fix_permalink_from_rounds("Capptú", "/organization/capptú", companies, rounds2)
    fix_permalink_from_rounds("Gráfica en línea", "/organization/gráfica-en-línea", companies, rounds2)
    fix_permalink_from_rounds("IGNIA Bienes Raíces", "/organization/ignia-bienes-raíces", companies, rounds2)
    fix_permalink_from_rounds("Bricoprivé.com", "/organization/bricoprivé-com", companies, rounds2)
    fix_permalink_from_rounds("Médica Santa Carmen", "/organization/médica-santa-carmen-2", companies, rounds2)
    fix_permalink_from_rounds("E CÚBICA", "/organization/e-cêbica", companies, rounds2)
    fix_permalink_from_rounds("Vá de Táxi", "/organization/vá-de-táxi", companies, rounds2)

    fix_permalink_from_companies("It’s All About Me", "S-ALL-ABOUT-ME", companies, rounds2)
    fix_permalink_from_companies("Whodat’s Spaces", "WHODAT", companies, rounds2)
    fix_permalink_from_companies("know’N’act", "KNOW", companies, rounds2)
    fix_permalink_from_companies("iProof - The Foundation for the Internet of Things™", "IPROOF---THE-FOUNDATION-FOR-THE-INTERNET-OF-THINGS", companies, rounds2)
    fix_permalink_from_companies("ÁERON", "�eron", companies, rounds2)

    # This needs some extra fixing
    fix_permalink_from_companies("Crème & Ciseaux", "e-ciseaux", companies, rounds2)

    regenerate_permalink("ZenGame", "ZenGame 禅游科技", companies, rounds2)
    regenerate_permalink("EnergyStone Games", "EnergyStone Games 灵石游戏", companies, rounds2)
    regenerate_permalink("Magnet Tech ", "Magnet Tech 磁石科技", companies, rounds2)
    regenerate_permalink("Huizuche.com", "Huizuche.com 惠租车", companies, rounds2)
    regenerate_permalink("Inveno ", "Inveno 英威诺", companies, rounds2)
    regenerate_permalink("Weiche Tech ", "Weiche Tech 喂车科技", companies, rounds2)
    regenerate_permalink("TipCat Interactive", "TipCat Interactive 沙舟信息科技", companies, rounds2)
    regenerate_permalink("Jiwu", "Jiwu 吉屋网", companies, rounds2)
    regenerate_permalink("TalentSigned", "TalentSigned™", companies, rounds2)
    regenerate_permalink("Asiansbook", "Asiansbook™", companies, rounds2)
    regenerate_permalink("Reklam-Ve-Tan", "İnovatiff Reklam ve Tanıtım Hizmetleri Tic", companies, rounds2, "")
    regenerate_permalink("thế-giới-di", "The Gioi Di Dong", companies,
                         rounds2)  # This permalink is mangled in both data sets, generated new permalink
    regenerate_permalink("k��k", "KÖÖK", companies, rounds2)

    x, y = uniques(companies, rounds2)
    print(set(y).difference(set(x)))

def regenerate_permalink(company_name_prefix, full_company_name, companies, rounds2,
                         optional_organization_prefix="/organization/"):
    global ROUNDS2_COMPANY_PERMALINK
    global COMPANIES_NAME

    dashed_company_name_prefix = company_name_prefix.replace(' ', '-').replace('.', '-')
    dashed_lowercase_full_company_name = full_company_name.replace(' ', '-').replace('.', '-').lower()
    corrected_permalink_lowercase = (f'/organization/{dashed_lowercase_full_company_name}').lower()
    print(corrected_permalink_lowercase)
    companies.loc[companies[COMPANIES_NAME].str.contains(full_company_name, na=False), COMPANIES_COMPANY_PERMALINK_LOWERCASE] = corrected_permalink_lowercase
    rounds2.loc[rounds2[ROUNDS2_COMPANY_PERMALINK].str.contains(f'{optional_organization_prefix}{dashed_company_name_prefix}',
                                                                na=False, case=False, regex=False), ROUNDS2_COMPANY_PERMALINK_LOWERCASE] = corrected_permalink_lowercase
    print(companies[companies[COMPANIES_COMPANY_PERMALINK_LOWERCASE].str.contains(corrected_permalink_lowercase, na=False, case=False)])
    print(rounds2[rounds2[ROUNDS2_COMPANY_PERMALINK_LOWERCASE].str.contains(corrected_permalink_lowercase, na=False, case=False)])

def fix_permalink_from_rounds(company_name, company_permalink, companies, rounds):
    global COMPANIES_NAME

    correct_value_rows = rounds[rounds[ROUNDS2_COMPANY_PERMALINK_LOWERCASE] == company_permalink]
    corrected_value = correct_value_rows.iloc[0][ROUNDS2_COMPANY_PERMALINK_LOWERCASE]
    companies.loc[companies[COMPANIES_NAME] == company_name, COMPANIES_COMPANY_PERMALINK_LOWERCASE] = corrected_value
    print(companies[companies[COMPANIES_NAME] == company_name].to_string())
    print(rounds[rounds[ROUNDS2_COMPANY_PERMALINK_LOWERCASE] == corrected_value].to_string())

def fix_permalink_from_companies(company_name, rounds_permalink_fragment, companies, rounds, truth_column = COMPANIES_COMPANY_PERMALINK_LOWERCASE):
    global COMPANIES_NAME

    correct_value_rows = companies[companies[COMPANIES_NAME] == company_name]
    lowercase_corrected_value = correct_value_rows.iloc[0][truth_column].lower()
    rounds.loc[rounds[ROUNDS2_COMPANY_PERMALINK_LOWERCASE].str.contains(rounds_permalink_fragment, na=False, case=False, regex=False), ROUNDS2_COMPANY_PERMALINK_LOWERCASE] = lowercase_corrected_value
    print(companies[companies[truth_column] == lowercase_corrected_value].to_string())
    print(rounds[rounds[ROUNDS2_COMPANY_PERMALINK_LOWERCASE] == lowercase_corrected_value].to_string())

def uniques(companies, rounds2):
    global ROUNDS2_COMPANY_PERMALINK_LOWERCASE
    global COMPANIES_COMPANY_PERMALINK_LOWERCASE

    unique_companies_in_rounds2 = rounds2[ROUNDS2_COMPANY_PERMALINK_LOWERCASE].unique()
    unique_companies_in_companies = companies[COMPANIES_COMPANY_PERMALINK_LOWERCASE].unique()
    return unique_companies_in_companies, unique_companies_in_rounds2

analyse()
