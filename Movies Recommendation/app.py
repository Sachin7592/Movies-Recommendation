from tkinter.font import names

import streamlit as st
import pickle
import pandas as pd
import requests
import time
session = requests.Session()
session.headers.update({'User-Agent': 'MovieApp/1.0'})

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": "446b83ccb92d04775668bf43b89c0b42","langueage":"en-US"}
    for attempt in range(3):
        try:
            response = session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            return "https://image.tmdb.org/t/p/w500" + data['poster_path']
        except requests.exceptions.RequestException:
            if attempt <2:
                time.sleep(1)
                continue
            raise


    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse = True, key = lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id =movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster



movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies= pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommendation System")


Selected_movie_name = st.selectbox("Enter the name of a movie", movies['title'].values)


if st.button("Recommend"):
    names,posters = recommend(Selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
