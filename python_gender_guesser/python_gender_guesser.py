import pandas as pd
import pycountry
import pyodbc
import gender_guesser.detector as gender


'''
import data
'''

server = 'servername'
database = 'databasename'
username = 'username'
password = 'password'
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER='+server+
                      ';DATABASE='+database+
                      ';UID='+username+
                      ';PWD='+ password)

my_query = '''
SELECT 
    first_name,
    country,
    freq
FROM 
    customer.first_name_table
'''

df = pd.read_sql(my_query, conn)

print(df)
print(type(df))

'''
find country names
'''

df['country_name'] = [pycountry.countries.get(alpha_2=ii).name.lower().replace(' ', '_') for ii in df['country']]

'''
user gender detector based on first name and country
'''

d = gender.Detector(case_sensitive=False)

gender_found = []

for ii,jj in zip(df['first_name'], df['country_name']):
    try:
        gender_result = d.get_gender(ii, jj)
    except:
        gender_result = d.get_gender(ii)
    print(gender_result)
    gender_found.append(gender_result)

df['gender_v1'] = gender_found

'''
user gender detector based on first name only
'''

df['gender_ v2'] = [d.get_gender(ii) for ii in df['first_name']]                

'''
turn partial results into either male or female
'''

df = df.replace({'mostly_male': 'male'}, regex=True)

df = df.replace({'mostly_female': 'female'}, regex=True)

'''
take whichever gender version is more specific, with priority on gender v1
'''

df['gender_final'] = df.apply(lambda x: x['gender_alternative'] 
                                if x['gender_found'] not in ['male', 'female'] 
                                else x['gender_found'], 
                                axis = 1)


'''
export list
'''

df.to_csv('gender_list.csv', sep=';', index=False, encoding='utf-8-sig')
