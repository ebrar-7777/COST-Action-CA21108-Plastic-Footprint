import csv
import requests
from bs4 import BeautifulSoup
import time,os
from urllib.parse import quote_plus
import random
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com/',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
}

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def extract_co2_values(paragraph):
    co2_values = []
    para_list = paragraph.split(" ")
    for i in range(len(para_list) - 1):
        #print(para_list[i], para_list[i + 1])
        if is_float(para_list[i]) and ('kg' in para_list[i + 1] or 'co2' in para_list[i + 1].lower()):
            last_data = para_list[i + 1]
            if last_data.lower() == 'kgco':
                last_data = 'kg'
            co2_values.append((float(para_list[i]), last_data))
        #process kg
        elif 'kg' in para_list[i]:
            split_value = para_list[i].replace('kg', '').strip()
            if is_float(split_value):
                co2_values.append((float(split_value), 'kg'))
        elif is_float(para_list[i]):
            lst_1 = ['million']
            lst_2 = ['tons', 'ton']
            if (para_list[i + 1].lower() in lst_1) and (para_list[i + 2].lower() in lst_2):
                co2_values.append((float(para_list[i]), f'{para_list[i + 1]} {para_list[i + 2]}'))
    return co2_values

def wait_for_random_time(min_seconds, max_seconds):
    interval = random.randint(min_seconds, max_seconds)
    print('[+] Script is sleeping for {} seconds ...'.format(interval))
    time.sleep(interval)

def convert_to_url_format(string, query_format):
    #string = f"CO2 emissions of {string} production"
    #string = f"{string} co2 emissions"
    string = query_format.format(polymer=string)
    encoded_string = quote_plus(string)
    return encoded_string


def google_search_engine(polymer, encoded_query, start):
    json_data = {
        'polymer': polymer,
        'domain': 'google.com',
    }

    response = requests.get(
        f'https://www.google.com/search?vet=12ahUKEwiq9PHc4YaCAxUScGwGHTcFCEU4KBDErwJ6BAgBEAM..i&ved=2ahUKEwirotDN4YaCAxUWl5UCHaGxA0cQ_skCegQIAxAG&bl=p8DK&s=web&opi=89978449&yv=3&q={encoded_query}&sca_esv=575405473&ei=KJEzZavuLZau1sQPoeOOuAQ&start={start}&sa=N&asearch=arc&cs=0&async=arc_id:srp_150,ffilt:all,ve_name:MoreResultsContainer,use_ac:false,inf:1,_id:arc-srp_150,_pms:s,_fmt:pc',
        headers=headers,
    )

    html_data = response.text

    html_data = html_data.split('[2]e022;')[-1]
    bs_data = BeautifulSoup(html_data, 'html.parser')

    #print(html_data)

    page_data = []

    for card_div in bs_data.find_all('div', {'class': CURRENT_PROCCESS_LOOKUP}):
            
            #get headline ...
            try:
                head_line = card_div.find('h3').text.strip()
            except AttributeError:
                head_line =  None

            if not head_line:
                continue

            #url
            try:
                data_link = card_div.find('a').get('href')
            except AttributeError:
                data_link = ''

            #description
            try:
                description = ''
                for span in card_div.find_all('span'):
                    description += span.text.strip() + ' '
            except AttributeError:
                description = ''

            co2_values = extract_co2_values(description)
            co2_data = []
            for i, co2 in enumerate(co2_values, start=1):
                if i == 2:
                    break
                co2_data.append(str(co2[0]) + ' ' + str(co2[1]))
            co2_string = ' - '.join(co2_data)

            #uncomment this when to skip empty data
            if not co2_string:
                continue

            page_data.append({
                'polymer': polymer,
                'link': data_link,
                'co2_value': co2_string,
                
            })

    print('[+] Writing Data to File ....')
    with open(query_data_csv, 'a') as o_file:
        csv_writer = csv.DictWriter(o_file, fieldnames=CSV_HEADERS)
        csv_writer.writerows(page_data)

    # this line is important in long run
    wait_for_random_time(2, 5)

def work_on_indi_query(polymer, query):
    global MAX_PAGES
    max_pages = MAX_PAGES

    print('[+] Query : {}'.format(polymer))
    print('[+] Max Pages Set : {}'.format(max_pages))

    page_counter = 1
    while True:
        #out_json_path = op_dir + polymer + f'_PAGE_{page_counter}.json' #no-need

        """ if os.path.exists(out_json_path):
            page_counter += 1
            continue """

        if page_counter > max_pages:
            print('[+ Max Pages Reached ///]')
            break
            
        data_start = 20 *(page_counter - 1)

        encoded_query = convert_to_url_format(polymer, query)
        google_search_engine(polymer, encoded_query, data_start)
        page_counter += 1

        if page_counter > max_pages:
            print('[+ Max Pages Reached ///]')
            break

    #it's important in long run
    wait_for_random_time(4, 5)


def work_on_query_data(query):
    for polymer in PL_LIST:
        print(f'[+] Getting {polymer} ...')
        work_on_indi_query(polymer, query)


"""
CAN MODIFY
"""
MAX_PAGES = 5

#"{polymer} carbon footprint",
#"{polymer} CO2 impact",
#"carbon emissions of {polymer}",
#"CO2 emissions of {polymer} production",
#"{polymer} CO2 emission value"
QUERY_LIST = [
    "co2 emissions per kg of {polymer} polymer",
]

#list of polymers
PL_LIST = [
    'Low Density Polypropylene', 'High Density Polypropylene',
    'Polystyrene','Polycarbonate','Polypropylene','Silicone',
    'Polyethylene','LD Polyethylene', 'HD Polyethylene',
    'Acetal','Polyester','Borosilicate glass','Polyethylene',
    'Polyethylene Terephthalate','Polyvinyl chloride','Nitrile'
]
query_data_csv = 'query_dbv2_queryv2.csv'


#op_dir = 'raw_data/' #no-need
CURRENT_PROCCESS_LOOKUP = 'MjjYud'
CSV_HEADERS = ['polymer', 'co2_value', 'link'] 
#os.makedirs(op_dir, exist_ok=True) #no-need

if __name__ == "__main__":
    print('[+] Preparing CSV File ....')
    with open(query_data_csv, 'w') as csv_f:
        csv_writer = csv.DictWriter(csv_f, fieldnames=CSV_HEADERS)
        csv_writer.writeheader()
    
    for query in QUERY_LIST:
        print(f'[+] Using query {query} ...')
        work_on_query_data(query)