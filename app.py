import pickle
import streamlit as st
import requests
import pandas as pd
from streamlit import components

# Create a footer component with your name and copyright symbol
footer_component = """
<div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #ffffff; padding: 10px; text-align: center;">
    <p style="font-size: 12px; color: #777;">Made by Ananya Prasad &#169;</p>
</div>
"""

# Add the footer component to the app
st.markdown(footer_component, unsafe_allow_html=True)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=889bf1e9df11f468ee1f8e27e5410896&language=en-US".format(movie_id)
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('model/movie_dict.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))
movies = pd.DataFrame(movies_dict)

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Enter the name of the movie',
    movies['title'].values
)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie_name)
    container = st.container()
    columns = st.columns(5)

    for i in range(5):
        with container:
            with columns[i]:
                st.text(names[i])
                st.image(posters[i])

    

    