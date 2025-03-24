import requests
from bs4 import BeautifulSoup
import mysql.connector
from urllib.parse import urljoin 


conn = mysql.connector.connect(
    host='localhost',
    user='root',  
    password='', 
    database='web_scraper'
)
cursor = conn.cursor()


base_url = "http://localhost:8000/"


visited = set()


def dfs(url):
    """ Fungsi DFS untuk merayapi halaman web """
    if url in visited:
        return
    
    visited.add(url)
    print(f"Mengunjungi: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

    
        title = soup.title.text.strip() if soup.title else "No Title"
        paragraph = soup.p.text.strip() if soup.p else "No Content"

        cursor.execute("INSERT INTO pages (url, title, paragraph) VALUES (%s, %s, %s)",
                       (url, title, paragraph))
        conn.commit()


        for link in soup.find_all('a', href=True):
            next_url = urljoin(base_url, link['href'])  # Pastikan URL yang benar
            dfs(next_url)

    except requests.exceptions.RequestException as e:
        print(f"Gagal mengakses {url}: {e}")


dfs(base_url + "index.html")


cursor.close()
conn.close()
print("Scraping selesai dan data telah disimpan di database!")
