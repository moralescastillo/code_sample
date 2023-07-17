#-----------------------------------------------------------------------------------------------------------------------
#
# this code scrapes the following sites for the following purposes
#
#   * https://www.speedtest.net/global-index
#       finding median fixed broadband internet speed in different countries
#
#   * https://www.numbeo.com/cost-of-living/rankings_by_country.jsp
#       finding updated Cost of Living Plus Rent index
#
#   * https://www.worldsurfleague.com/events?all=1&year=
#       finding countries where tour stops took place in different years
#
# created by Paulo Morales Castillo (hello@paulomoralescastillo.com)
#-----------------------------------------------------------------------------------------------------------------------


from bs4 import BeautifulSoup
from plotnine import *
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd
import pycountry


# start of functions ---------------------------------------------------------------------------------------------------

def find_country_code(country_list):

    '''
    for each country name in country list, find the equivalent international 3-letter
    country code, whenever available, using package pycountry
    :param country_list: a list containing names of countries
    :return: a list with three-letter country codes
    '''

    country_code_list = []

    for country in country_list:
        country = country.replace('(', '').replace(')', '')
        country_object = pycountry.countries.get(name=country)

        if country_object is None:
            try:
                country_object = pycountry.countries.search_fuzzy(country)[0]
            except Exception:
                country_object = None

        if country_object is not None:
            country_code = country_object.alpha_3

        else:
            country_code = None

        country_code_list.append(country_code)

    return(country_code_list)

# create beautiful object
def cook_soup(url):

    '''
    Create a BeautifulSoup object based on the website passed onto the object url
    :param url: a string with the url to be converted into a beautifulsoup object
    :return: beautifulsoup object
    '''

    req=Request(url, headers={'User-Agent': 'Mozilla/6.0'})
    page=urlopen(req)
    html=page.read().decode("utf-8")
    soup=BeautifulSoup(html, "html.parser")

    return (soup)


# end of functions ---------------------------------------------------------------------------------------------------

# start of speedtest ---------------------------------------------------------------------------------------------------

soup = cook_soup("https://www.speedtest.net/global-index")

# find all listed countries and their results' type (fixed broadband vs mobile)

country_list = []
type_list = []
country_html = soup.find_all(name='td', class_='country')

for country_raw in country_html:

    # find all countries first

    country=country_raw.get_text().strip()
    country_list.append(country)

    # then find all results types within country information
    for a in country_raw.find_all(name = 'a', href = True):
        href = a['href']
        result_type = href.split("#", 1)[1]
        type_list.append(result_type)

# find the location of all results

result_location_list = []
results_html = soup.find_all(name='tr', class_='data-result results')

for result in results_html:

    result_str = str(result)
    location_index = str(soup).find(result_str)
    result_location_list.append(location_index)
    print(location_index)

# find mean and median locations

index_mobile_mean = str(soup).find('global-mobileMean-graph')

index_mobile_median = str(soup).find('global-mobileMedian-graph')

index_fixed_mean = str(soup).find('global-fixedMean-graph')

index_fixed_median = str(soup).find('global-fixedMedian-graph')

index_last = max(result_location_list)


# find all countries' ranks

rank_list=[]
rank_html = soup.find_all('td', class_='rank actual-rank')

for rank_raw in rank_html:

    rank=rank_raw.get_text().strip()
    rank_list.append(rank)

# find all countries's speed results
speed_list=[]
speed_html=soup.find_all('td', class_='speed')

for speed_raw in speed_html:

    speed=speed_raw.get_text().strip()
    speed_list.append(speed)

# categorize all results into mobile vs fixed and median vs mobile

bin_range = [index_mobile_mean, index_mobile_median, index_fixed_mean, index_fixed_median, index_last]

bin_label = ['mobile mean', 'mobile median', 'fixed mean', 'fixed median', 'last']

df_bin = pd.DataFrame({'bin_range': bin_range,
                       'bin_label': bin_label})

df_bin = df_bin.sort_values(by=['bin_range'], ascending=True)

classification_list = pd.cut(result_location_list, bins=df_bin.bin_range, labels=df_bin.bin_label[:-1])

# bind all lists into a preliminary df

df = pd.DataFrame({'rank':rank_list,
                   'country':country_list,
                   'type': type_list,
                   'speed': speed_list,
                   #'location': result_location_list,
                   'classification': classification_list})


# keep only those results for median fixed broadband
df = df.query("classification == 'fixed median'")

# have pandas display all content
#print(df.to_string(max_rows=None, max_cols=None))


# find an international code for each country in the list
country_code_list = []
for country in df['country']:

    country = country.replace('(', '').replace(')', '')
    print(country)
    country_object = pycountry.countries.get(name=country)
    print("<---------->")
    if country_object is None:
        #print(country_object)
        try:
            country_object = pycountry.countries.search_fuzzy(country)[0]
            print(country_object)
        except Exception:
            country_object = None

    if country_object is not None:
        country_code = country_object.alpha_3

    else:
        country_code = None

    country_code_list.append(country_code)

df['country_code'] = country_code_list

# keep only countries and remove cities and non found countries
df = df[~df['country_code'].isna()].reset_index(drop=True)

df.to_csv(path_or_buf='ranking.csv', sep=';', index=False)

# end of speedtest -----------------------------------------------------------------------------------------------------

# start of numbeo  -----------------------------------------------------------------------------------------------------
soup_cost = cook_soup("https://www.numbeo.com/cost-of-living/rankings_by_country.jsp")

table_column_html = soup_cost.find_all(name='thead')
table_column_list = []

for column_name_raw in table_column_html:

    column_name_list = column_name_raw.find_all(name="div", style="font-size: 90%;")

    for column_raw in column_name_list:

        column_name = column_raw.get_text().strip()
        table_column_list.append(column_name)
        print(column_name)


column_selected = 'Cost of Living Plus Rent Index'

column_index_selected = [i for i, x in enumerate(table_column_list) if x == column_selected][0]

table_html_cost = soup_cost.find_all(name='tr', style="width: 100%" )
country_list_cost = []
index_list_cost = []

for country_row_raw in table_html_cost:

    print(country_row_raw)
    country_raw = country_row_raw.find_all(name='td', class_='cityOrCountryInIndicesTable')[0]

    #print(country_raw)
    # find all countries first
    country=country_raw.get_text().strip()
    country_list_cost.append(country)

    print("<------------------->")

    index_raw = country_row_raw.find_all(name='td', style='text-align: right')[column_index_selected]

    index_value = index_raw.get_text().strip()
    index_list_cost.append(index_value)

    print(index_value)

    print("<------------------->")


df_cost_index = pd.DataFrame({'country': country_list_cost,
                              'index_cost': index_list_cost})



# find an international code for each country in the list

df_cost_index['country_code'] = find_country_code(df_cost_index['country'])

df_cost_index.to_csv('cost_index.csv', index=False, sep=';')

# end of numbeo  -------------------------------------------------------------------------------------------------------

# start of wsl  --------------------------------------------------------------------------------------------------------

wsl_year = [2019, 2020, 2021, 2022, 2023]
wsl_html = []

for year in wsl_year:
    url_string = "https://www.worldsurfleague.com/events?all=1&year="+str(year)
    wsl_html.append(cook_soup(url_string))

location_list_surf = []

for soup_wsl in wsl_html:

    location_html_surf = soup_wsl.find_all(name='span', class_="event-schedule-details__location" )
    location_list_surf_year = []

    for location_raw in location_html_surf:

        location = location_raw.get_text().split(', ')
        location_list_surf_year.append(location[-1])

    location_list_surf.extend(location_list_surf_year)

location_list_surf = list(dict.fromkeys(location_list_surf))

country_code_surf = find_country_code(location_list_surf)

df_surf = pd.DataFrame({'location': location_list_surf,
                        'country_code': country_code_surf})

df_surf = df_surf.query('country_code.notnull()', engine='python')

df_surf = df_surf.drop_duplicates(subset='country_code', keep='first')
# end of wsl  ----------------------------------------------------------------------------------------------------------

# start of consolidate and plot  ---------------------------------------------------------------------------------------

df_internet_cost = pd.merge(df, df_cost_index, on='country_code', how='outer')

df_internet_cost = df_internet_cost[['country_code', 'speed', 'index_cost']]

df_internet_cost = df_internet_cost.query(expr='speed.notnull() and index_cost.notnull()', engine='python')

df_final = pd.merge(left=df_internet_cost, right=df_surf, on='country_code', how='left')

df_final['if_surf'] = df_final['location'].notnull()

df_final = df_final[['country_code', 'speed', 'index_cost', 'if_surf']]

df_final[['speed', 'index_cost']] = df_final[['speed', 'index_cost']].apply(pd.to_numeric)

find_country_code(['taiwan'])

df_final['speed'].median()

df_final['index_cost'].median()

label_logic = np.where(df_final['speed'] > 100, df_final['country_code'], None)

print(df.to_string(max_rows=None, max_cols=None))
print(df_final.to_string(max_rows=None, max_cols=None))



d1 = (
    ggplot(df_final)
    + aes(x='index_cost', y='speed')
    + aes(shape='if_surf')
    + geom_point()
    + geom_vline(xintercept = 45, size=0.2, linetype='dotted')
    + geom_hline(yintercept = 100, size=0.2)
    + labs(x = 'Cost of Living Plus Rent Index',
           y = 'Median Fixed Broadband Download Speed (Mbps)',
           shape='good surf is likely')
    + geom_text(aes(label=label_logic), nudge_x=2, nudge_y=2)
    + ggtitle(title="Workation Trifecta")
    + theme_tufte(base_size=11, base_family="serif", ticks=True)
)


print(d1)

# end of consolidate and plot  -----------------------------------------------------------------------------------------

