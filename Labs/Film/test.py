import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
                  '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

url = 'https://www.imdb.com/title/tt0113497/'
response = requests.get(url, headers=headers)
html_text = response.text
print(html_text)
exit()

soup = BeautifulSoup(html_text, 'html.parser')
elements = soup.find_all('a')
print(elements)