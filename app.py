import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Add src to python path
sys.path.append(os.path.abspath('.'))

from src.data_cleaner import preprocess_netflix_data, split_multivalue_column
from src.visualization_theme import apply_netflix_theme, get_netflix_colors

# ----------------- PAGE CONFIGURATION -----------------
st.set_page_config(
    page_title="Netflix Catalog Insights Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- CUSTOM STYLING -----------------
# Premium Netflix Dark Aesthetics
st.markdown("""
    <style>
    .main {
        background-color: #111111;
        color: #F5F5F1;
    }
    div[data-testid="stSidebar"] {
        background-color: #181818;
    }
    h1, h2, h3 {
        color: #E50914 !important;
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
        font-weight: 800;
    }
    .stMetric {
        background-color: #222222;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #E50914;
    }
    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 700;
    }
    div[data-testid="stMetricLabel"] {
        color: #AAAAAA !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1c1c1c;
        border: 1px solid #333333;
        border-radius: 4px;
        color: #CCCCCC;
        padding: 8px 16px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #E50914 !important;
        color: #FFFFFF !important;
        border: 1px solid #E50914 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- DATA LOADING -----------------
@st.cache_data
def load_and_clean_data():
    raw_path = "data/netflix_titles.csv"
    cleaned_path = "data/netflix_titles_cleaned.csv"
    
    if os.path.exists(cleaned_path):
        df = pd.read_csv(cleaned_path)
    elif os.path.exists(raw_path):
        df = preprocess_netflix_data(raw_path)
        df.to_csv(cleaned_path, index=False)
    else:
        # Fallback if file paths are slightly shifted
        raw_path = "../data/netflix_titles.csv"
        cleaned_path = "../data/netflix_titles_cleaned.csv"
        if os.path.exists(cleaned_path):
            df = pd.read_csv(cleaned_path)
        else:
            df = preprocess_netflix_data(raw_path)
            df.to_csv(cleaned_path, index=False)
            
    df['date_added'] = pd.to_datetime(df['date_added'])
    return df

try:
    df = load_and_clean_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Please verify that netflix_titles.csv exists in the data/ folder.")
    st.stop()

# Apply standard dark plotting configurations
apply_netflix_theme(style='dark')
colors = get_netflix_colors()

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=180)
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.title("Dashboard Controls")

# Content Type Filter
content_type = st.sidebar.selectbox("Select Content Type", ["All Content", "Movie", "TV Show"])

# Release Year Filter
min_year = int(df['release_year'].min())
max_year = int(df['release_year'].max())
year_range = st.sidebar.slider("Select Release Year Range", min_year, max_year, (2000, max_year))

# Rating Filter
all_ratings = sorted(df['rating'].unique())
selected_ratings = st.sidebar.multiselect("Select Content Ratings", all_ratings, default=all_ratings)

# Filter Data
filtered_df = df[
    (df['release_year'] >= year_range[0]) &
    (df['release_year'] <= year_range[1]) &
    (df['rating'].isin(selected_ratings))
]

if content_type != "All Content":
    filtered_df = filtered_df[filtered_df['type'] == content_type]

# ----------------- HEADER & KPIS -----------------
st.title("🎬 Netflix Catalog Data Analysis Dashboard")
st.markdown("An interactive platform visualizing production trends, catalog growth, geographic insights, and scheduling logic.")
st.markdown("---")

# KPI Metrics Rows
col1, col2, col3, col4, col5 = st.columns(5)

total_titles = len(filtered_df)
total_movies = len(filtered_df[filtered_df['type'] == 'Movie'])
total_tv = len(filtered_df[filtered_df['type'] == 'TV Show'])

# Find top producing country in filtered subset
exploded_countries = split_multivalue_column(filtered_df, 'country')
top_country = exploded_countries['country'].value_counts().index[0] if not exploded_countries.empty else "N/A"

# Find top genre in filtered subset
exploded_genres = split_multivalue_column(filtered_df, 'listed_in')
top_genre = exploded_genres['listed_in'].value_counts().index[0] if not exploded_genres.empty else "N/A"

with col1:
    st.metric("Total Titles", f"{total_titles:,}")
with col2:
    st.metric("Total Movies", f"{total_movies:,}")
with col3:
    st.metric("Total TV Shows", f"{total_tv:,}")
with col4:
    st.metric("Top Country", top_country)
with col5:
    st.metric("Top Genre", top_genre)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- MAIN INTERFACE TABS -----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Core Distribution & Stats", 
    "📈 Release & Growth Timelines", 
    "🌍 Country & Genre Explosions", 
    "🔍 Advanced Search & Keywords"
])

# ------------- TAB 1: Core Distribution & Stats -------------
with tab1:
    st.subheader("Distribution Breakdown")
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("**Movies vs TV Shows Distribution**")
        type_counts = filtered_df['type'].value_counts()
        if not type_counts.empty:
            fig, ax = plt.subplots(figsize=(7, 4.5), facecolor=colors['dark_charcoal'])
            ax.set_facecolor(colors['medium_gray'])
            ax.pie(
                type_counts, 
                labels=type_counts.index, 
                autopct='%1.1f%%', 
                startangle=140, 
                colors=[colors['red'], '#444444'],
                textprops={'color': colors['light_gray'], 'fontweight': 'bold'}
            )
            plt.title("Catalog Composition", color=colors['light_gray'], fontweight='bold')
            st.pyplot(fig)
        else:
            st.warning("No data matches current filters.")
            
    with c2:
        st.markdown("**Ratings Distribution**")
        if not filtered_df.empty:
            fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=colors['dark_charcoal'])
            ax.set_facecolor(colors['medium_gray'])
            rating_order = filtered_df['rating'].value_counts().index
            sns.countplot(data=filtered_df, y='rating', order=rating_order, palette='Reds_r', ax=ax)
            ax.set_title("Ratings Summary", color=colors['light_gray'], fontweight='bold')
            ax.set_xlabel("Count", color=colors['light_gray'])
            ax.set_ylabel("Rating", color=colors['light_gray'])
            ax.tick_params(colors=colors['light_gray'])
            st.pyplot(fig)
        else:
            st.warning("No data matches current filters.")

    # Duration Analytics Section
    st.markdown("---")
    st.subheader("Duration Profiles")
    c3, c4 = st.columns(2)
    
    with c3:
        st.markdown("**Movie Length Distribution (in Minutes)**")
        movie_data = filtered_df[(filtered_df['type'] == 'Movie') & (filtered_df['duration_minutes'].notna())]
        if not movie_data.empty:
            fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=colors['dark_charcoal'])
            ax.set_facecolor(colors['medium_gray'])
            sns.histplot(data=movie_data, x='duration_minutes', bins=30, kde=True, color=colors['red'], ax=ax)
            ax.axvline(movie_data['duration_minutes'].mean(), color='#FFFFFF', linestyle='--', label=f"Mean: {movie_data['duration_minutes'].mean():.1f}m")
            ax.axvline(movie_data['duration_minutes'].median(), color='#FFAEAE', linestyle='-.', label=f"Median: {movie_data['duration_minutes'].median():.1f}m")
            ax.set_title("Running Time Spread", color=colors['light_gray'], fontweight='bold')
            ax.tick_params(colors=colors['light_gray'])
            ax.set_xlabel("Minutes", color=colors['light_gray'])
            ax.legend()
            st.pyplot(fig)
        else:
            st.info("Select 'Movie' or 'All Content' in sidebar to view movie lengths.")
            
    with c4:
        st.markdown("**TV Show Longevity (Season Counts)**")
        tv_data = filtered_df[(filtered_df['type'] == 'TV Show') & (filtered_df['duration_seasons'].notna())]
        if not tv_data.empty:
            fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=colors['dark_charcoal'])
            ax.set_facecolor(colors['medium_gray'])
            season_counts = tv_data['duration_seasons'].value_counts().sort_index()
            sns.barplot(x=season_counts.index.astype(int), y=season_counts.values, color=colors['red'], ax=ax)
            ax.set_title("Season Retention Count", color=colors['light_gray'], fontweight='bold')
            ax.set_xlabel("Number of Seasons", color=colors['light_gray'])
            ax.tick_params(colors=colors['light_gray'])
            st.pyplot(fig)
        else:
            st.info("Select 'TV Show' or 'All Content' in sidebar to view TV seasons.")

# ------------- TAB 2: Release & Growth Timelines -------------
with tab2:
    st.subheader("Temporal Trends & Upload Patterns")
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("**Monthly Release Seasonality**")
        df_months = filtered_df['month_name_added'].value_counts()
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December']
        df_months = df_months.reindex(month_order).fillna(0)
        
        fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=colors['dark_charcoal'])
        ax.set_facecolor(colors['medium_gray'])
        sns.barplot(x=df_months.index, y=df_months.values, palette='Oranges', ax=ax)
        ax.set_title("Additions by Month of Year", color=colors['light_gray'], fontweight='bold')
        ax.tick_params(colors=colors['light_gray'])
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
    with c2:
        st.markdown("**Day of Week Scheduling Logic**")
        df_days = filtered_df['day_name_added'].value_counts()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df_days = df_days.reindex(day_order).fillna(0)
        
        fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=colors['dark_charcoal'])
        ax.set_facecolor(colors['medium_gray'])
        sns.barplot(x=df_days.index, y=df_days.values, color=colors['red'], ax=ax)
        ax.set_title("Additions by Day of Week", color=colors['light_gray'], fontweight='bold')
        ax.tick_params(colors=colors['light_gray'])
        st.pyplot(fig)

    st.markdown("---")
    st.markdown("**Catalog Expansion Over the Years (2008–2021)**")
    df_growth = filtered_df[filtered_df['year_added'] >= 2008].groupby(['year_added', 'type']).size().reset_index(name='count')
    if not df_growth.empty:
        fig, ax = plt.subplots(figsize=(15, 5), facecolor=colors['dark_charcoal'])
        ax.set_facecolor(colors['medium_gray'])
        sns.lineplot(
            data=df_growth, 
            x='year_added', 
            y='count', 
            hue='type', 
            marker='o', 
            linewidth=3, 
            palette=[colors['red'], '#999999'], 
            ax=ax
        )
        ax.set_title("Annual Content Ingestion Growth", color=colors['light_gray'], fontweight='bold')
        ax.set_xlabel("Year Added", color=colors['light_gray'])
        ax.set_ylabel("Count of Shows", color=colors['light_gray'])
        ax.tick_params(colors=colors['light_gray'])
        st.pyplot(fig)
    else:
        st.info("Adjust the release year range filter in the sidebar to include 2008-2021.")

# ------------- TAB 3: Country & Genre Explosions -------------
with tab3:
    st.subheader("Global Distributions & Exploded Categories")
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("**Top Producing Countries**")
        if not exploded_countries.empty:
            top_countries = exploded_countries['country'].value_counts().head(10)
            fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=colors['dark_charcoal'])
            ax.set_facecolor(colors['medium_gray'])
            sns.barplot(x=top_countries.values, y=top_countries.index, palette='Reds_r', ax=ax)
            ax.set_title("Top 10 Producing Nations", color=colors['light_gray'], fontweight='bold')
            ax.set_xlabel("Contribution Count", color=colors['light_gray'])
            ax.tick_params(colors=colors['light_gray'])
            st.pyplot(fig)
        else:
            st.warning("No country data available.")
            
    with c2:
        st.markdown("**Top Catalog Genres**")
        if not exploded_genres.empty:
            top_genres = exploded_genres['listed_in'].value_counts().head(10)
            fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=colors['dark_charcoal'])
            ax.set_facecolor(colors['medium_gray'])
            sns.barplot(x=top_genres.values, y=top_genres.index, palette='Oranges_r', ax=ax)
            ax.set_title("Top 10 Categorical Genres", color=colors['light_gray'], fontweight='bold')
            ax.set_xlabel("Titles Count", color=colors['light_gray'])
            ax.tick_params(colors=colors['light_gray'])
            st.pyplot(fig)
        else:
            st.warning("No genre data available.")

# ------------- TAB 4: Advanced Search & Keywords -------------
with tab4:
    st.subheader("Narrative Words & Interactive Search")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.markdown("**Description Keyword Frequencies**")
        if not filtered_df.empty:
            all_desc = " ".join(filtered_df['description'].astype(str).str.lower())
            words = [w.strip(".,!?;:()\"'") for w in all_desc.split()]
            stopwords = {'a', 'an', 'the', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'to', 'for', 'in', 'of', 'on', 'with', 'by', 'at',
                         'from', 'his', 'her', 'their', 'this', 'that', 'who', 'whom', 'which', 'he', 'she', 'they', 'it', 'its', 'as', 'new',
                         'this', 'up', 'out', 'an', 'into', 'about', 'young', 'world', 'life', 'family', 'man', 'woman', 'one', 'two', 'finds',
                         'must', 'save', 'takes', 'turns', 'after', 'lives', 'shows', 'find', 'takes', 'sets', 'series', 'first'}
            
            filtered_words = [w for w in words if w not in stopwords and len(w) > 3]
            if filtered_words:
                word_counts = pd.Series(filtered_words).value_counts().head(12)
                fig, ax = plt.subplots(figsize=(6, 5.5), facecolor=colors['dark_charcoal'])
                ax.set_facecolor(colors['medium_gray'])
                sns.barplot(x=word_counts.values, y=word_counts.index, color=colors['red'], ax=ax)
                ax.set_title("Top Plot Keywords", color=colors['light_gray'], fontweight='bold')
                ax.tick_params(colors=colors['light_gray'])
                st.pyplot(fig)
            else:
                st.info("No description text found.")
        else:
            st.warning("No data matches current filters.")
            
    with c2:
        st.markdown("**Interactive Catalog Explorer**")
        search_query = st.text_input("🔍 Search by Title, Director, or Cast:")
        
        explorer_df = filtered_df.copy()
        if search_query:
            explorer_df = explorer_df[
                explorer_df['title'].str.contains(search_query, case=False, na=False) |
                explorer_df['director'].str.contains(search_query, case=False, na=False) |
                explorer_df['cast'].str.contains(search_query, case=False, na=False)
            ]
            
        st.write(f"Showing {len(explorer_df):,} matching rows:")
        st.dataframe(
            explorer_df[['title', 'type', 'director', 'country', 'release_year', 'rating', 'duration', 'listed_in']],
            height=400,
            use_container_width=True
        )

# ----------------- FOOTER -----------------
st.markdown("---")
st.markdown("<p style='text-align: center; color: #666666;'>Netflix Title Catalog Analysis Project | Data Analytics Curriculum</p>", unsafe_allow_html=True)
