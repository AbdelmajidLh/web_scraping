import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import os

# insert the product name
search_query = input('insert your product name :')

search_query = search_query.replace(' ', '+')
base_url = 'https://www.amazon.com/s?k={0}'.format(search_query)

# user agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept-Language': 'en-US, en;q=0.5'
}

# disable your proxies in your requests
proxies = {
  "http": None,
  "https": None,
}

# save products in the items list
items = []
for i in range(1, 5):
    print('Processing {0}...'.format(base_url + '&page={0}'.format(i)))
    response = requests.get(base_url + '&page={0}'.format(i), headers=headers, proxies=proxies)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    for result in results:
        product_name = result.h2.text

        try:
            rating = result.find('i', {'class': 'a-icon'}).text
            rating_count = result.find_all('span', {'aria-label': True})[1].text
        except AttributeError:
            continue

        try:
            price1 = result.find('span', {'class': 'a-price-whole'}).text
            price2 = result.find('span', {'class': 'a-price-fraction'}).text
            price = float(price1 + price2)
            product_url = 'https://amazon.com' + result.h2.a['href']
            # print(rating_count, product_url)
            items.append([product_name, rating, rating_count, price, product_url])
        except AttributeError:
            continue
    sleep(1.5)
    
# créer le dataframe
df = pd.DataFrame(items, columns=['produit', 'note', 'nombre_de_notes', 'prix', 'lien produit'])

# create the RES directory if it doesn't ixist
path = "RES"
isExist = os.path.exists(path)
if not isExist:
   # Create a new directory because it does not exist
   os.makedirs(path)

 # export  results
df.to_excel('{0}/{1}.xlsx'.format(path, search_query), index=False)