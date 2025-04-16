from pickletools import genops
import sreamlit as st
import pandas as pd
import json
import os
from datatime import datetime
import time
import random
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests

# set page configuration

st.set_page_config(
    page_title="Personal Library Management System",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

#custom css for styling
st.markdown("""
<style>
        .main-header{
            font-size:3rem !important;
            color: #1E3A8A;
            font-weight: 700;
            margin-bottom: 1rem;
            text-alight: center;
            text-shadow: 2px 2px 4px rbga(0,0,0,0.1);
       }
            
        .sub_header {
             font-size: 1.8rem !important;
             color:3882F6;
             margin-top: 1rem;
             margin-bottom:1rem
        }
        
        .sucess-message {
            padding:1rem;
            background-color: #ECFDFS;
            border-left: 5px solid #108981;
            border-radius: 0.375rem;
        }
        .warning-message {
            padding: 1rem;
            background-color: #FEF3c7;
            border-left: 5px solid #F59E0B;
            border-radius:0.375rem;
        }
        .book-card {
            background-color: #F3F4F6;
            border-redius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 5px solidd 03B82F6;
            transition: transform 0.3s ease;
        }
        
        .book-card-hover{
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
            
        }
        .read-badge {
            background-color: #10B981;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.758rem;
            font-weight: 600;
            
            
        }
        .unread-badge {
            background-color: #F87171;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.758rem;
            font-weight: 600;
            
        }
        .action-button {
            margin-right: 0.5rem;
            
        }
        .stButton>button{
            border-radius: 0.375rem;
        }
</style>
"""), unsafe_allow_html=True

def load_lottieur(url):
    try:
        r=request.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None
    
if 'library' not in st.session_state:
    st.session_state.library = []
if 'search_result' not in st.session_state:
    st.session.state.search_result = []
if 'book_added' not in st.session.state:
    st.session_state.book_added = False;
if 'book_removed' not in st.session.state:    
    st.session_sate.book_removed = false;
if 'current_view' not in st.session_state:
    st.session_state.current_view = "library"
    
def load_library():
    try:
        if os.path.exists('library.json'):
            with open('library.json', 'r') as file:
                st.session_state.library = json.load(file)
                return True
            return False
    except Exception as e:
        st.error(f"Error loading library: (e)")
        return False
    
   # save library
def save_library():
    try:
        with open('library.json', 'w') as file:
            json.dump(st.session_stae.library, file)
            return True
    except Exception as e:
        st.error(f"Error loading library: (e)")
        return False 
    
# add a book to library
def add_bood(title, author, publication_year, genre, read_status):
    book=(
        'title': title, 
        'authoor':autho,
        'publication_year':publation_year,
        'genre': genre,
        'read_status'=:ead_status,
        'added_date': datetime.now().strftime("%y-%m-%d %M:%H:%S")
    )
    st.session_state.library.append(book)
    save_library()
    st.session_state.book_added = True
    time.sleep(0.5) #maintain deley
    
def remove_book(index):
    if 0 <= index < len(st.session_sate.library):
        st.session_state.book_removed = True
        return True
    return False
#search book
def search_books(search_term, search_by):
    search_term = search_term.lower()
    result = []
    for book in st.session_state.library:
        if search_by == "Title" and search_term in book['title'].lower():
            result.append(book)   
        elif search_by == "Author" and search_term in book['author'].lower(): 
            result.append(book)
        elif search_by == "Genre" and search_term in book['author'].lower():
            result.append(book)            
    st.session_state.search_results = results
    #calculate liberary states
    
def get_library_stats():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book['read status'])
    percent_read = (read_books / total_books * 100) if total_books > 0 else 0
    
    generes = ()
    authors = ()
    decades = ()
    
    for book in st.session_state.library:
        if book['genre'] in generes:
            generes[book['genre']] += 1
        else:
            generes[book['genre']] = 1
            
        # Count author
        if book['author'] in authors:
                authors[book['author']] += 1
        else:
            authors[book['author']] = 1   
          #count decades
        decades = (book['publication_year'] // 10) * 10
        if decades in decades:
            decades[decades] += 1
        else:
            decades[decades] = 1
            
#sort by count
    generes = dict(sorted(generes.items(), key=lambda x: x[1] , reverse= True))            
    authors = dict(sorted(authors.items(), key=lambda x: x[1] , reverse= True)) 
    decades = dict(sorted(decades.items(), key=lambda x: x[1] ))   
    return {
    'total_books': total_books,
    'read_books': read_books,
    'percent_read': percent_read,
    'generes' :generes,
    'authors' :authors,
    'decades' :decades
}              
    
def create_visulations(stats):
    if stats['total_books'] > 0:
        fig_read_status = go.Figure(data = [go.Pie(
            labels = ['Read', 'Unread'],
            values=[stats['read_books'], stats['total_books'] - stats['read_books']],
            hole =.4,
            marker_colors=['#103981', '#f87171']
        )])    
        fig_read_status.update_layout(
            title_text ='Read vs Unread Books',
            showlegends = True,
            helght = 400
        )
        st.plotly_chart(fig_read_status, use_container_width = True)
        #bar chart genres
        if stats['genres']:
            genres_df = pd.DataFrame((
                
                'Genre': list(stats['genres'].keys()),
                'Count' : list(stats['genres'].values())
            ))
            fig_genres = px.bar(
                genres_df,
                x='Genre',
                y='Count',
                color= 'Count',
                color_continous_scale=px.colors.sequential.Blues[]
            )
            fig_genres.update_layout(
                title_text = 'Book by publication genres',
                xaxis_title = 'Genres',
                yaxis_title = 'Number of books',
                height = 400
            )
            st.plotly_chart(fig_decades, use_container_width=True)
        if stats['decades']:
            decades_df=pd.DataFrame((
                'Decade':[f"(decade)s" for decade in sats['decades'].keys()],
                "count': list(stats["decades'].values())"
            ))  
            fig_decades = px.line(
                decades_df,
                x='Decade',
                y='Count'
                markers=True,
                line_shape='spline'
            )  
            fig_decades.update_layout(
                title_text = 'Book by publication decades',
                xaxis_title = 'Decades',
                yaxis_title = 'Number of books',
                height=400
                
            )
            st.plotly_chart(fig_decades, use_container_width=True)
            
            #load library
            
load_library()
st.sidebar.markdown("<h1 style ='text-alighn: center;'> Navigation</h1>", unsafe_allow_html = True)
lottle_book = load_lottieurl("https://assests9.lottiefiles.com/temp/1f20_avafin.json")
if lottie_book:
   with st.sidebar:
        st.lotties(lottie_book, height=200, key="book_animation")
nav_options=st.sidebar.radion(
    "Choose an option:,"
    ["view library","Search book", "Add Book", "Library Statistic"]
)            
if nav_options == "view library":
   st.session_state.current_view = 'library'
elif nav_options == "Add bool":
   st.session_state.current_view = 'Add'
elif nav_options == "Search Book":
   st.session_state.current_view = 'Search'
elif nav_options == "Library Statistics":
   st.session_state.current_view = "Stats"   
   
   
st.markdown("<h1 class='main_header'> Personal Library Manager </h1>" unsafe_allow_html=True)
if st.session_state.current_view == "Add":
    st.markdown("<h2 class = 'sub-header'> Add  a New Book</h2>", unsafe_allow_html=True)
    
    # adding books input form
    
    with st.form(key='add_book_form'):
         col1, col2 = st.columns(2)
         
         with col1:
              title = st.text_input("Book Title", max_chars=100)
              author = st.text_input("Author",max_chars = 100)
              publication_year = st.number_input("publication Year", min_value = 1000, max_value = datetime.now().year, step=1, value=2023)
        
         with col2:
              genre = st.selectbox("Genre", ["Friction", "None-Frictionj", "Science", "Technology", "Finance", "Poetry", "Heallth", "Art Books", "Religion", "History", "Others"])
              read_status = st.radio("Read Status",["Read", "Unread"], horizontal=True)
              read_bool = read_status == "Read"
              
              submit_button = st.form_submit_button(label = " Add Book")
              
              if submit_button and title and author:
                  add_book(title, author, publication_year, genre, read_bool)
    if st.session_state.book_added:
       st.markdown("<div class = 'sucess-message'> Book Added sussussfully!</div>", unsafe_allow_html= True)
       st.baloons()
       st.session_state.book_added = False
    elif st.session_state.current_view == "library":
        st.markdown("<h2 class = 'sub-header'> Your Library </h2>", unsafe_allow_html=True)
        
        if not st.session_state.library:
            st.markdown("<div class='warning-message'> Your library is empty, Add some books to  get started !</div>", unsafe_allow_html=True)
        else:
             cols=st.column(2)
             for i, book in enumerate(st.session_state.library):
                 with cols[i % 2]:
                      st.markdown(f"""<div class = 'book-card'>
                      <h3>{book['title']}</h3>
                      <p><strong>Author:,/strong>{book['author']}</p>
                         <p><strong>Publication Year:,/strong>{book['publication_year']}</p>
                            <p><strong>Genre:,/strong>{book['genre']}</p>
                            <p><span class = '{"read-badge" if book["read_status"] else "unread-badge"}'>{
                                "Read" if book["read_status"] else "Unread"
                            }</s[am></p>
                            </div>]
                      """, unsafe_allow_htmal=True)
                      
             col1, col2 = st.columns(2)    
             with col1:
              if st.button(f"Remove", key=f"remove_{i}", use_container_width=True):
                  if remove_book(i):
                      st.rerun()
             with col2:
                    new_status = not book['read_status']
                    status_label = "mark as read" if not book['read_status'] else "Mark as unread"
                    if st.button(status_label, key=f"status_{i}", use_container_width=True):
                        st.session_state.library[i]['read_status'] = new_status
                        save_library()
                        st.reruun()
        if st.session_state.book_removed:
            st.markdown("div class ='sucess-message'> Book removed sucessfully!</div>", unsafe_allow_html=True)
            st.session_state.book_removed = False
        elif st.session_state.current_view == "search":
             st.markdown("<h2 class ='sub-header'>Search Books</h2>",unsafe_allow_html=True)     
             
             search_by = st.selectbox("Search by:", ["Title", "Author", "Genre"])
             search_tem = st.text_input("Enter search term:")
             
             if st.button("Search", use_container_width=False):
                 
                if search_term: 
                
                   with st.spinner("Searching..."):
                         time.sleep(0.5)
                         search_books(search_term, search_by)
             if hasattr(st.session_state, 'search_results'):
                if st.session_state.search_results:
                   st.markdown(f"<h3> Found {len(st.session_state.search_results:</h3>", unsafe_allow_html=True)          
                        
                   for i, book in enumerate(st.session_state.search_result):
                       st.markdown(f"""
                                  <div class = 'book-card'>
                                   <p><strong>Author:,/strong>{book['author']}</p>
                                  <p><strong>Publication Year:,/strong>{book['publication_year']}</p>
                                   <p><strong>Genre:,/strong>{book['genre']}</p>
                                  <p><span class = '{"read-badge" if book["read_status"] else "unread-badge"}'>{
                                 "Read" if book["read_status"] else "Unread"
                             }</span></p>
                            </div>
                      """, unsafe_allow_htmal=True)
                       
                elif search_term:
                    st.markdown("<div class ='warning'>No Books Found Matching Your Search</div>",unsafe_allow_html=True)
elif st.session_state.current_view=="status":
     st.markdown("<h2 class ='sub-header'>Library Status</h2>", unsafe_allow_html=True)
     
     if not st.session_state.library:
         st.markdown("<div class = 'warnig-message'>Your library is empty. Add some books to see stae</div>", unsafe_allow_html=True)
     else:
         stats = get_library_stats()
         col1, col2,col3 = st.column(3)
         with col1:
              st.metric("Total Books", stats['total_books'])
         with col2:
              st.metric( "Book Read", stats['read_books'])      
         with col3:
              st.metric("Percentage Read", f"{stats['percentage_read']%")      
         create_visulations()
         
         if stats['authors']:
             st.markdown("<h3> Top Authors,</h3>",unsafe_allow_html=True)
             top_authors = dict(list(stats['authors'].items()[:5]))       
         
             for author, count in top_authors.items():
                 st.markdown(f"**{author}**: {count} books's' if count > 1 else ''}")
                 st.markdown("----")
                 st.markdown("copyright @ 2025 Farhat Naz Personal Library Manager", unsafe_allow_html=True)                    
                               
