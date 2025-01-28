import requests
from bs4 import BeautifulSoup
import pandas as pd
from random import sample
import spacy
import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from spacytextblob.spacytextblob import SpacyTextBlob


link_html = requests.get(
  'https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html', 
  verify=False
  )

link_content = BeautifulSoup(link_html.content, 'html.parser')

link_list = link_content.select('a[href*="last"]')

link_list = [link_list[i].get('href') for i in range(len(link_list))]

link_list = ['https://www.tdcj.texas.gov/death_row/'+link_list[i] for i in range(len(link_list))]

link_list = [link_list[i].replace('//death_row', '') for i in range(len(link_list))]

link_list = [link_list[i] for i in range(len(link_list)) if 'no_last_statement' not in link_list[i]]

link_list = sample(link_list, 50)

for i in range(len(link_list)):
    link_html = requests.get(link_list[i], verify=False)
    link_content = BeautifulSoup(link_html.content, 'html.parser')
    link_list[i] = link_content.select('p:contains("Last Statement:")~*')
    link_list[i] = [link_list[i][j].getText() for j in range(len(link_list[i]))]
    link_list[i] = ' '.join(link_list[i])
    
len(link_list)


#Stemming
stemmer = PorterStemmer()

death_words = link_list

[stemmer.stem(word) for word in death_words]


#Lemmatization
nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('spacytextblob') 

docs = list(nlp.pipe(death_words)) 
statements = []
for i in range(len(docs)):
    #docs[i] = [token.lemma_ for token in docs[i] if not token.is_stop and not token.is_space and not token.is_punct]
    statements.append([token.lemma_ for token in docs[i] if not token.is_stop and not token.is_space and not token.is_punct])

#statements is an array of lists with lematized words for each statement

#statements1 = [' '.join(statement) for statement in statements]
# death_row = pd.DataFrame(data = statements, columns = ['Statement'])


df = pd.DataFrame(link_list)
df = df.map(lambda x: x.lower() if isinstance(x, str) else x)

# #TF-IDF
tfidf_vec = TfidfVectorizer()

tfidf = tfidf_vec.fit_transform(link_list)

tfidf_tokens = tfidf_vec.get_feature_names_out()


df_countvect = pd.DataFrame(data = tfidf.toarray(), 
 columns = tfidf_tokens)
df_countvect