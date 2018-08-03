from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer
import re
from .models import UserProfile, Headline, WordAndCount

from TurkishStemmer import TurkishStemmer

from rest_framework.views import APIView
from rest_framework.response import Response

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        words = dict()
        for w in WordAndCount.objects.all().order_by('-id')[:10]:
            words[w.word] = w.count
        words = dict(words)
        data = {
            "word": words.keys(),
            "count": words.values(),
        }
        return Response(data)
        
def bar_graph(request):
    return render(request, "news/plotly.html", {})
def word_count_list(request):
    all_words_and_counts = WordAndCount.objects.all().order_by('-id')[:10]
    context = {
        'object_list': all_words_and_counts
    }
    return render(request, "news/home.html", context)

def scrape(request):
    session = requests.Session()
    session.headers = {'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    url = 'https://www.birgun.net/guncel'
    main_url = 'https://www.birgun.net'
    content = session.get(url, verify=False).content
     
    soup = BeautifulSoup(content, "html.parser")
    first_news = soup.findAll("div", {"class": "aciklamali-haber haber"})
    total_text = ''
    for i in first_news:
        link = i.find('a')
        im_source = i.find('img')['src']
        
        news_detail_url =main_url + link.get('href')
        detail_content = session.get(news_detail_url, verify=False).content
        soup = BeautifulSoup(detail_content,"html.parser")
        paragraphs = soup.find('div', {"class": "body fw"}).findAll('p')
        i = 0
        for p in paragraphs:
            total_text = total_text + p.text + '\n'
    
    words = word_tokenize(total_text)
    stop_words = set(stopwords.words("turkish"))
    my_words = {"bir","Bu", "var", "sonra","yok","olarak","yapılan","değil","göre","tarafından","ardından","geri","ileri","devam","eden"
                        "hatta","bazen","ilgili", "Ben","ben","ama","Bir","olmak","üzere","bin","ton","kota"
    }
    stop_words = stop_words.union(my_words) 
    filtered_words = [w for w in words if not w in stop_words]

    non_punct = re.compile('.*[A-Za-z0-9].*')  # must contain a letter or digit
     
    # ONE LINER FOR THE SAME JOB
    #double_filtered = [w for w in filtered_words if non_punct.match(w)]
    stemmer = TurkishStemmer()

    final_list = []
    for w in filtered_words:
        if non_punct.match(w):
            std = stemmer.stem(w)
            final_list.append(std)
    #print(final_list)
    counts = Counter(final_list)

    
    fdist = FreqDist(final_list)
    common_ones = fdist.most_common(10)
    for i, (w,c) in enumerate(common_ones):
        new_word_and_count = WordAndCount()
        new_word_and_count.word = w
        new_word_and_count.count = c
        new_word_and_count.save()

    
    
    return redirect('/home/')
