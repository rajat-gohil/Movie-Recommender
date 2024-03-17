import streamlit as st
import pickle
from imdb import IMDb

movies = pickle.load(open('movies_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list=movies['title'].values

def fetch_poster(movie_title):
    ia = IMDb()
    search_results = ia.search_movie(movie_title)
    if search_results:
        movie_id = search_results[0].movieID
        movie = ia.get_movie(movie_id)
        if 'cover url' in movie:
            return movie['cover url']
    return None

st.header('ScreenSage: Your Wise Movie Advisor')
st.write("Bringing you cinematic gems, one recommendation at a time.")


selectvalue=st.selectbox('Select Movie', movies_list)

def recommend (movie):
    index=movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movie=[]
    for i in distance[1:6]:
        recommend_movie.append(movies.iloc[i[0]].title)
    return recommend_movie


if st.button("I Recommend"):
    movie_names = recommend(selectvalue)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        if i < len(movie_names):
            col.image(fetch_poster(movie_names[i]), caption=movie_names[i])