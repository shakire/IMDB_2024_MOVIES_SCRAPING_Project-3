import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error


host = "localhost"
user = "root"
password = "tonystark"
database = "imdb"

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page:", ["IMDB_SCARP", "FILTERS"])


def check_connection():
    conn = None
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if conn.is_connected():
            st.success("Connection to the database is successful!")
        else:
            st.error("Failed to connect to the database.")
    except Error as e:
        st.error(f"Error connecting to the database: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()

check_connection()
def execute_query(query):
    conn = None  
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if conn.is_connected():
            df = pd.read_sql(query, conn)
            return df
    except Error as e:
        st.error(f"Error connecting to the database: {e}")
        return pd.DataFrame()
    finally:
        if conn and conn.is_connected():
            conn.close()

if page == "IMDB_SCARP":
    st.title("Project-1")
    st.header("IMDB_MOVIES_SCRAPING")

    check_connection()

    menu_options = ["Select an option", 
                    "Top 10 movies by rating and voting count",
                    "Genre Distribution - count of movies in each genre",
                    "Average duration by genre on each genre",
                    "Voting Trends by Genre",
                    "Rating Distribution by Genre",
                    "top-rated movie for each genre",
                    "Most Popular Genres by Voting",
                    "shortest and longest movies duration",
                    "Ratings by genre",]


    selected_option = st.selectbox("Choose a query to run:", menu_options)

    query_1 = """select Titile, Ratings, Voting_count from scarb_imdb order by Ratings desc, Voting_count desc limit 10"""
    if selected_option == "Top 10 movies by rating and voting count":
        st.info("Fetching Top 10 movies by rating and voting count...")
        result_data = execute_query(query_1)
        if not result_data.empty:
            st.table(result_data)
        else:
            st.warning("No data found.")

    query_2 = """select Genre,count(*) as movies_genre_distribution from scarb_imdb group by Genre"""
    if selected_option == "Genre Distribution - count of movies in each genre":
        st.info("Fetching Genre Distribution - count of movies in each genre...")
        result_data = execute_query(query_2)
        if not result_data.empty:
            st.table(result_data)
        else:
            st.warning("No data found.")

    query_3 = """select Genre,Avg(Timings) as average_duration from scarb_imdb group by Genre"""
    if selected_option == "Average duration by genre on each genre":
        st.info("Fetching Average duration by genre on each genre...")
        result_data = execute_query(query_3)
        if not result_data.empty:
            st.table(result_data)
        else:
            st.warning("No data found.")

    query_4 = """select Genre,Avg(Voting_count) as Voting_trends from scarb_imdb group by Genre"""
    if selected_option == "Voting Trends by Genre":
        st.info("Fetching Voting Trends by Genre...")
        result_data = execute_query(query_4)
        if not result_data.empty:
            st.table(result_data)
        else:
            st.warning("No data found.")

    query_5 = """select Genre,avg(Ratings) as Rating_distribution  from scarb_imdb group by Genre"""
    if selected_option == "Rating Distribution by Genre":
        st.info("Fetching Rating Distribution by Genre...")
        result_data = execute_query(query_5)
        if not result_data.empty:
            st.table(result_data)
        else:
            st.warning("No data found.")

    query_6 = """select Titile, Genre, Ratings from scarb_imdb s
                where (Genre, Ratings) in (select Genre, MAX(Ratings) from scarb_imdb group by Genre)
                order by Ratings desc"""
    if selected_option == "top-rated movie for each genre":
        st.info("Fetching top-rated movie for each genre...")
        result_data = execute_query(query_6)
        if not result_data.empty:
            st.table(result_data)
        else:
            st.warning("No data found.")

    query_7 = """select Genre,avg(Voting_count) as popular_genre from scarb_imdb group by Genre"""
    if selected_option == "Most Popular Genres by Voting":
        st.info("Fetching Most Popular Genres by Voting...")
        result_data = execute_query(query_7)
        if not result_data.empty:
            st.table(result_data)
        else:
            st.warning("No data found.")

    query_8 = """select Titile, Timings, case 
                when Timings = (select max(Timings) from scarb_imdb) then 'Highest Timing'
                when Timings = (select min(Timings) from  scarb_imdb) then 'Lowest Timing' end as Timing_Type
                from  scarb_imdb where Timings = (select max(Timings) from  scarb_imdb) or Timings = (select MIN(Timings) from  scarb_imdb)"""
    if selected_option == "shortest and longest movies duration":
        st.info("Fetching shortest and longest movies duration...")
        result_data = execute_query(query_8)
        if not result_data.empty:
            st.table(result_data)
        else:
            st.warning("No data found.")

    query_9 = """select Genre,avg(Ratings) as Rating_genre  from scarb_imdb group by Genre"""
    if selected_option == "Ratings by genre":
        st.info("Fetching Ratings by genre...")
        result_data = execute_query(query_9)
        if not result_data.empty:
            st.table(result_data)
        else:
            st.warning("No data found.")


elif page == "FILTERS":
    st.title("Movie Filters")

    # Genre dropdown
    genre_query = "select distinct Genre from scarb_imdb"
    genres_df = execute_query(genre_query)
    genres = genres_df['Genre'].dropna().tolist()

    selected_genre = st.selectbox("Select Genre", genres)

    # Rating slider
    min_rating = st.slider("Minimum Rating", min_value=0.0, max_value=10.0, value=5.0, step=0.1)

    # Voting count slider
    min_votes = st.slider("Minimum Voting Count", min_value=0, max_value=100000, value=5000, step=500)

    # Filter button
    if st.button("Filter Movies"):
        filter_query = f"""
            select Titile, Genre, Ratings, Voting_count
            from scarb_imdb
            where Genre = '{selected_genre}'
              and Ratings >= {min_rating}
              and Voting_count >= {min_votes}
            order by Ratings desc, Voting_count desc
        """
        filtered_data = execute_query(filter_query)

        if not filtered_data.empty:
            st.subheader("Filtered Results")
            st.table(filtered_data)
        else:
            st.warning("No movies match the selected filters.")

