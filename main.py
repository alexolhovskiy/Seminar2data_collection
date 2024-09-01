import requests
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint
ua=UserAgent()

# print(ua.safari)
# print(ua.chrome)
# print(ua.edge)
# print(ua.random)
#'https://books.toscrape.com/catalogue/category/books_1/page-2'

headers={"User-Agent":ua.random}
# params={"ref_":"bo_nb_hm_tab"}

session=requests.session()



# print(rows)
url_first='https://books.toscrape.com/catalogue'

books=[]
n=1
while True:

    url=f'https://books.toscrape.com/catalogue/category/books_1/page-{n}.html'
    response=session.get(url,headers=headers)
    soup=BeautifulSoup(response.text,"html.parser")
    rows=soup.find_all('li',{'class':'col-xs-6 col-sm-4 col-md-3 col-lg-3'})
    
    if not rows:
        break

    for row in rows:
        book={}

        try:
            link=row.find('div',{'class':'image_container'}).findChildren()[0]

            page_response=session.get(url_first+link.get('href')[5:],headers=headers)
            soup=BeautifulSoup(page_response.text,"html.parser")
            page=soup.find('article',{'class':'product_page'})

            book['title']=page.find('div',{'class':'product_main'}).findChildren()[0].getText()
            book['price']=page.find('p',{'class':'price_color'}).getText()
            book['in_stock']=page.find('p',{'class':'instock availability'}).getText().split('(')[1].split(' ')[0]
            book['description']=page.find('div',{'id':'product_description'}).next_sibling.next_sibling.getText()
        except:
            book['link']='None'
        
        books.append(book)   
    print(n) 
    n+=1



pprint(books)
print(len(books))
print(n)

with open("books.json", "w") as f:
    json.dump(books,f)

