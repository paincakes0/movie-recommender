import streamlit as st
import pickle
import pandas as pd
import requests
import time
import os
import gdown

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=7214d9dddd6bd497b2aefd97e7fe844b&language=en-US'
    tries = 5
    for attempt in range(tries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return "http://image.tmdb.org/t/p/w500/" + poster_path
            else:
                return "https://via.placeholder.com/300x450?text=No+Image"
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(1)  # wait before retry
    # If all retries fail
    return "https://via.placeholder.com/300x450?text=No+Image"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch poster from web api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


if not os.path.exists('similarity.pkl'):
    url = 'https://drive.google.com/uc?id=13yPr36INevUChufCT1HvxofaaY5722nR'
    gdown.download(url, 'similarity.pkl', quiet=False)

similarity = pickle.load(open('similarity.pkl', 'rb'))


st.title('Movie Recommender')

selected_movie_name = st.selectbox(
    'Which movie would you like to know recommendation for?',
    options=[''] + list(movies['title'].values),
    index=0)

if st.button('Get recommendation', disabled=(selected_movie_name == '')):
    names, poster = recommend(selected_movie_name)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(poster[idx])


