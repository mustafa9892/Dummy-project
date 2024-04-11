import streamlit as st
import requests
import pandas as pd
import pickle

def fetch_poster(movie_id):

    response = requests.get('https://api.themoviedb.org/3/movie/'
                            '{}?api_key=062c68e0b5a666dc35778aa9f9475489'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/original" + data['poster_path']


movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    recommended_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_posters, recommended_movies


st.title('Movie recommender')

option = st.selectbox(
    'Recommend',
    movies['title'])

if st.button('Recommend'):
    posters, names = recommend(option)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.header(names[0])
        st.image(posters[0])

    with col2:
        st.header(names[1])
        st.image(posters[1])

    with col3:
        st.header(names[2])
        st.image(posters[2])

    with col4:
        st.header(names[3])
        st.image(posters[3])

    with col5:
        st.header(names[4])
        st.image(posters[4])

