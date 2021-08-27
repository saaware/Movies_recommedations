import streamlit as st
import pickle
import pandas as pd
import requests 
import base64

# this app is created using streamlit library

# =========Show back ground image code==================start
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('image.jpg')

# =========Show back ground image code==================Ending==========
 
similarity = pickle.load(open('similarity.pkl','rb'))

movies_list = pickle.load(open('Movies_dict.pkl','rb'))
Movies_Names=pd.DataFrame(movies_list)

st.title('Ganesha! ..Movie Recommendation System')
Selected_movie_name = st.selectbox( "",(Movies_Names['original_title']))

#st.write('You selected Movie :', option)

# create function which take movie name and recomend 5 movies from model
def recommend(movie1):
    # finding index value of user provided movie and based on rec movie
    movie_index= Movies_Names[Movies_Names['original_title']==movie1].index[0] 
    distance = similarity[movie_index]
    movies_list =sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
    
    # now take movies list and find the index of recomend movies
    recomend_list=[]  # strong rec movie names
    rec_movie_poster=[]  # taking poster by caaling api TMDB

    for i in movies_list:
        movie_id =Movies_Names.iloc[i[0]].id #storing movie id for API poster fetching
        recomend_list.append(Movies_Names.iloc[i[0]].original_title)  #Now dont want index of the , we want name of the movies
        
        #fetch API call using movie id to get poster of movies
        rec_movie_poster.append(fetch_poster(movie_id))
    return recomend_list,rec_movie_poster


#now using movie_id fetch the movie poster from TMDB web site where all data present
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))  
    data=response.json()
    #st.text(data)  # to check response data on ui
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

if st.button('Recommend'):
    names,poster = recommend(Selected_movie_name)

    col1, col2, col3 ,col4,col5 = st.columns(5)
    with col1:
     st.image(poster[0])
     st.header(names[0]) 
     st.text("")
     st.text("")
   
    with col2:
     st.image(poster[1])
     st.header(names[1])
     st.text("")
     st.text("")
   
    with col3:
     st.image(poster[2])
     st.header(names[2])
     st.text("")
     st.text("")

    with col4:
     st.image(poster[3])
     st.header(names[3])
     

    with col5:
     st.image(poster[4])
     st.header(names[4])





