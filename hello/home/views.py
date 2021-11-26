from django.shortcuts import render,HttpResponse
import pandas as pd
import numpy as np
import json
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#preprocessing the csv file and extarcting th reequired features like director name and producer name
"""
df1 = pd.read_csv("D:/credits.csv")
df2 = pd.read_csv("D:/movies_metadata.csv")

#dropping data not having mivie id as integer
df2 = df2.drop(19730)
df2 = df2.drop(29503)
df2 = df2.drop(35587)

substring = '-'
for i in range(10, 45170):
    if substring in str(df2["id"].iloc[i]):
        df2.drop(i)

#merging 2 csv files on column movie id

df2['id'] = df2['id'].astype('int64')
dfinal = df1.merge(df2, on="id")


#merging the required features in a single column
for j in range(0, 45538):
    d = dfinal['genres'].iloc[j]
    if (len(d) != 0):
        res = list(eval(d))

    else:
        res = []

    string = ""
    for i in res:
        string = string + i['name']
        string = string + ' '
        
    d = str(dfinal['production_companies'].iloc[j])
    print(j)
    if (len(d) > 5):
        res = list(eval(dfinal['production_companies'].iloc[j]))

    else:
        res = []
    for i in res:
        string = string + i['name']

    d = dfinal['cast'].iloc[j]
    if (len(d) != 0):
        res = list(eval(dfinal['cast'].iloc[j]))

    else:
        res = []
    count = 1
    for i in res:
        if count > 3:
            break
        string = string + i['name']
        count = count + 1

    d = dfinal['crew'].iloc[j]
    if (len(d) != 0):
        res = list(eval(dfinal['crew'].iloc[j]))

    else:
        res = []

    linew = ['Director', 'Producer', 'Editor', 'Original Story', 'Production Coordinator']
    for i in res:

        if 'job' in i.keys() and i['job'] in linew:
            string = string + i['name']

    li.append(string)

#saving the csv file
dfinal['extracted_features'] = li
dfinal.to_csv('D:/moviedatafinal.csv')

#creating the cosine similarity matrix 
cv = CountVectorizer()
count_matrix = cv.fit_transform(dfinal["extracted_features"])

#matrix has no of rows and columns same as no of movies or entries in the csv file
#each entry in the matrix corresponds to a number between 0 and 1 telling the similarity
#more the number more the similarity
cosine_sim = cosine_similarity(count_matrix)
name = "D:/numpy1/numpy"

#saving the each row of matrix as numpy array because size of matrix is huge(15GB) and cant be processed every time 
#we search 
for i in range(0, 45538):
    name1 = name + str(i) + '.npy'
    np.save(name1, cosine_sim[i])
"""

# Create your views here.
def index(request):
    return render(request,'index.html')


def search(request):
   res=request.GET['query']
   finallist=[]

   df = pd.read_csv("D:/csv/moviedatafinal.csv")

   currentindex=df[df['title']==res].index.values

#checking if the movie is in the csv file or not
   if currentindex.size == 0:
       pass

   else:
       #loading the numpy array which has same name as the row number of the movie
     datatoload="D:/numpy1/numpy"+str(currentindex[0])+".npy"
     #lis1=lis[0]
     lis1=np.load(datatoload)
     print(lis1)
     numbers = np.array(lis1)
     n = 10

     #getting index of top 10 values
     indices = (-numbers).argsort()[:n]
     
     newindices=list(indices)
     print(type(newindices))

     print(newindices)
     list_movies=[]

     #creting list of movies from the indexes
     for i in newindices:
      list_movies.append(df['title'][i])
     dict={'a':list_movies}
     finallist=list_movies


   finallistremdup=[]
   print(finallist, 'finallist')

   #appending some details to movies
   for i in finallist:
      movie_data=[]
      url = "https://imdb-internet-movie-database-unofficial.p.rapidapi.com/film/"+i

      headers = {
         'x-rapidapi-host': "imdb-internet-movie-database-unofficial.p.rapidapi.com",
         'x-rapidapi-key': "344962b5b9msh94666562b67e3f1p1e93eajsn9e027aa0e267"
      }
      response = requests.request("GET", url, headers=headers)
      json_data = json.loads(response.text)
      movie_data.append(json_data['title'])

      movie_data.append(json_data['poster'])
      movie_data.append(json_data['year'])
      # print(json_data)
      finallistremdup.append(movie_data) 
      
       
   finallist=finallistremdup

   dict={'a':finallist}
   if len(finallist)==0:
       return HttpResponse('No movie found please search again with different keywords')

   return render(request, 'search.html', dict)
