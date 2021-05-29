from bs4 import BeautifulSoup

f1 = open("../data/country-codes.html", "r")
f = open("../data/language-countries.html", "r")
languages_html = f.read()
country_codes_html = f1.read()
languages_soup = BeautifulSoup(languages_html, 'html.parser')
country_codes_soup = BeautifulSoup(country_codes_html, 'html.parser')
all_language_tables = languages_soup.find_all("table", "wikitable sortable jquery-tablesorter")
all_country_code_tables = country_codes_soup.find_all("table", "wikitable sortable jquery-tablesorter")

all_country_codes = all_country_code_tables[1].tbody.find_all("tr")
# print(all_country_codes[0].find_all("td"))
a = map(lambda tr: (tr.td.a.text.strip(), tr.find_all("td")[2].span.text.strip()), all_country_codes)
country_code_dict = dict(list(a))
print(country_code_dict)
print("---------------------------------------------")


defacto_official_english_countries = all_language_tables[0].tbody.find_all("tr")
# print(defacto_official_english_countries)
# print(defacto_official_english_countries[0].find_all("td"))
# x = map(lambda tr: tr.find_children()[1].text, defacto_official_english_countries)
x = map(lambda tr: tr.find_all("td")[1].text.strip(), defacto_official_english_countries)
x1 = list(x)
print(x1)
print("---------------------------------------------")

other_countries = all_language_tables[1].tbody.find_all("tr")
# print(other_countries[0].find_all("td"))
general_only_english_countries = filter(lambda tr: "Yes" in tr.find_all("td")[4].text.strip(), other_countries)
y = map(lambda tr: tr.find_all("td")[1].text.strip(), general_only_english_countries)
y1 = list(y)
print(y1)
print("---------------------------------------------")

english_non_primary_countries = all_language_tables[2].tbody.find_all("tr")
# print(english_non_primary_countries[0].td.a.text)
z = map(lambda tr: tr.td.a.text.strip(), english_non_primary_countries)
z1 = list(z)
print(z1)
print("---------------------------------------------")
