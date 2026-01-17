import streamlit as st
import csv
import json
import requests
import io

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(page_title="Movie Recommender", layout="wide", page_icon="🎬")

# -------------------------------
# Google Drive CSV URLs Configuration
# -------------------------------
# Your actual Google Drive sharing URLs
CREDITS_CSV_URL = "https://drive.google.com/file/d/1c5m3-p-ZTSMMwNtHCBYySWG4lijQlLkY/view?usp=sharing"
MOVIES_CSV_URL = "https://drive.google.com/file/d/18xo7HkKT24ZERhziF-XdwYXqBVPpvPE6/view?usp=sharing"

# -------------------------------
# Enhanced Custom CSS
# -------------------------------
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* Header styling */
    h1 {
        color: #000000 !important;
        text-align: center;
        font-weight: 800;
        font-size: 3.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Suboriginal_title styling */
    .suboriginal_title {
        text-align: center;
        color: #000000;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        font-weight: 600;
    }
    
    /* Search box styling */
    .stTextInput > div > div > input {
        font-size: 18px;
        padding: 15px;
        border-radius: 50px;
        border: 3px solid #ffffff;
        background: rgba(255, 255, 255, 0.95);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Movie card container */
    .movie-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        margin-bottom: 30px;
        border: 2px solid rgba(255,255,255,0.3);
    }
    
    /* Section headers */
    .section-header {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
        text-align: center;
        margin: 30px 0 20px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Poster card styling */
    .poster-card {
        background: white;
        padding: 10px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 15px;
    }
    
    .poster-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    /* Info box styling */
    .info-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        border-left: 5px solid #667eea;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 10px;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    /* Movie original_title in recommendations */
    .movie-original_title-rec {
        text-align: center;
        font-weight: 700;
        color: #333;
        margin-top: 10px;
        font-size: 0.95rem;
    }
    
    /* Match score badge */
    .match-score {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        margin: 5px 0;
    }
    
    /* Genre tags */
    .genre-tag {
        background: #e0e7ff;
        color: #4c51bf;
        padding: 5px 15px;
        border-radius: 20px;
        display: inline-block;
        margin: 5px 5px 5px 0;
        font-size: 0.9rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# TMDB API Configuration
# -------------------------------
TMDB_API_KEY = "ac191eb4fb931fc0aa67f7dfc283e0e7"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# -------------------------------
# Google Drive Helper Functions
# -------------------------------
def convert_gdrive_url(share_url):
    """Convert Google Drive sharing URL to direct download URL"""
    try:
        # Extract file ID from the sharing URL
        file_id = share_url.split('/d/')[1].split('/')[0]
        # Return direct download URL
        return f'https://drive.google.com/uc?id={file_id}&export=download'
    except Exception as e:
        st.error(f"Error converting URL: {e}")
        return share_url

def read_csv_from_gdrive(url):
    """Read CSV file from Google Drive URL"""
    try:
        # Convert to direct download URL
        download_url = convert_gdrive_url(url)
        
        # Download the file
        response = requests.get(download_url, timeout=30)
        response.raise_for_status()
        
        # Decode content and create CSV reader
        content = response.content.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(content))
        
        # Convert to list
        data = list(csv_reader)
        return data
    except Exception as e:
        st.error(f"Error reading CSV from Google Drive: {e}")
        return []

# -------------------------------
# Load Movies from CSV Files
# -------------------------------
@st.cache_data
def load_movies():
    """Load and merge movie data from two CSV files on Google Drive"""
    # Read credits CSV from Google Drive
    credits = read_csv_from_gdrive(CREDITS_CSV_URL)
    
    # Read movies CSV from Google Drive
    movies = read_csv_from_gdrive(MOVIES_CSV_URL)
    
    # Check if data was loaded successfully
    if not credits or not movies:
        st.error("❌ Failed to load data from Google Drive. Please check your URLs and file permissions.")
        return []

    # Create a dictionary of movies by ID for faster lookup
    movies_dict = {m["id"]: m for m in movies}

    # Merge credits and movies data
    merged_data = []
    for credit in credits:
        movie_id = credit.get("movie_id")
        if movie_id in movies_dict:
            merged_data.append({**movies_dict[movie_id], **credit})

    return merged_data

# -------------------------------
# Helper Functions
# -------------------------------
def parse_json_field(text):
    """Safely parse JSON fields from CSV"""
    try:
        return json.loads(text) if text else []
    except:
        return []

def get_genres(movie):
    """Extract genre names from movie data"""
    genres = parse_json_field(movie.get("genres", ""))
    return [g["name"] for g in genres]

def get_director(movie):
    """Find the director from crew data"""
    crew = parse_json_field(movie.get("crew", ""))
    for person in crew:
        if person.get("job") == "Director":
            return person.get("name")
    return "Unknown"

@st.cache_data(ttl=3600)
def fetch_poster_from_tmdb(movie_id):
    """Fetch poster URL from TMDB API using movie ID"""
    if not TMDB_API_KEY or TMDB_API_KEY == "YOUR_API_KEY_HERE":
        return None
    
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "en-US"
        }
        
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get("poster_path")
            
            if poster_path:
                return f"{TMDB_IMAGE_BASE_URL}{poster_path}"
        
        return None
    except Exception as e:
        print(f"Error fetching poster for movie {movie_id}: {e}")
        return None

def get_poster_url(movie):
    """Get poster URL - first try TMDB API, then fallback to CSV data"""
    movie_id = movie.get("id")
    
    if movie_id:
        api_poster = fetch_poster_from_tmdb(movie_id)
        if api_poster:
            return api_poster
    
    poster_path = movie.get("poster_path", "")
    
    if not poster_path or str(poster_path).strip() in ["", "nan", "None", "null", "NaN"]:
        return None
    
    poster_path = str(poster_path).strip()
    
    if poster_path.startswith("http"):
        return poster_path
    
    if not poster_path.startswith("/"):
        poster_path = "/" + poster_path
    
    return f"{TMDB_IMAGE_BASE_URL}{poster_path}"

def find_similar_movies(movie_name, all_movies):
    """Find movies similar to the given movie"""
    target_movie = None
    for movie in all_movies:
        if movie["original_title"].lower() == movie_name.lower():
            target_movie = movie
            break

    if not target_movie:
        return None, []

    target_genres = set(get_genres(target_movie))
    target_director = get_director(target_movie)

    similar_movies = []
    for movie in all_movies:
        if movie["id"] == target_movie["id"]:
            continue

        movie_genres = set(get_genres(movie))
        genre_matches = len(target_genres & movie_genres)
        director_match = 1 if get_director(movie) == target_director else 0

        score = (genre_matches * 2) + (director_match * 3)

        if score > 0:
            similar_movies.append((score, movie))

    similar_movies.sort(reverse=True, key=lambda x: x[0])
    return target_movie, similar_movies[:10]

# -------------------------------
# Main App
# -------------------------------

# Check if URLs are configured
if "YOUR_CREDITS_FILE_ID" in CREDITS_CSV_URL or "YOUR_MOVIES_FILE_ID" in MOVIES_CSV_URL:
    st.error("⚠️ Please configure your Google Drive CSV URLs in the code!")
    st.markdown("""
    <div class='info-box'>
    <h3>📋 Setup Instructions:</h3>
    <ol>
        <li><strong>Upload CSV files to Google Drive:</strong>
            <ul>
                <li>tmdb_5000_credits.csv</li>
                <li>tmdb_5000_movies.csv</li>
            </ul>
        </li>
        <li><strong>Make files publicly accessible:</strong>
            <ul>
                <li>Right-click on each file → "Share"</li>
                <li>Click "Change to anyone with the link"</li>
                <li>Set permission to "Viewer"</li>
            </ul>
        </li>
        <li><strong>Get the sharing URL:</strong>
            <ul>
                <li>Click "Copy link"</li>
                <li>URL format: https://drive.google.com/file/d/<strong>FILE_ID</strong>/view?usp=sharing</li>
            </ul>
        </li>
        <li><strong>Update the code:</strong>
            <ul>
                <li>Replace CREDITS_CSV_URL with your credits file URL</li>
                <li>Replace MOVIES_CSV_URL with your movies file URL</li>
            </ul>
        </li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Check API key
if TMDB_API_KEY == "YOUR_API_KEY_HERE":
    st.warning("⚠️ Please add your TMDB API key to enable dynamic poster fetching!")
    st.info("Get your free API key from: https://www.themoviedb.org/settings/api")

# Load data with loading spinner
with st.spinner("📥 Loading movie data from Google Drive..."):
    movies_data = load_movies()

# Check if data loaded successfully
if not movies_data:
    st.error("❌ No movie data loaded. Please check your Google Drive URLs and file permissions.")
    st.stop()

st.success(f"✅ Successfully loaded {len(movies_data)} movies from Google Drive!")

# Header
st.markdown("<h1>🎬 Movie Recommender</h1>", unsafe_allow_html=True)
st.markdown("<p class='suboriginal_title'>✨ Discover movies similar to your favorites ✨</p>", unsafe_allow_html=True)

# Search input with debug option
col1, col2 = st.columns([5, 1])
with col1:
    movie_input = st.text_input("Search", placeholder="🔍 Search for a movie... (e.g., Avatar, Inception, Titanic)", label_visibility="collapsed")
with col2:
    show_debug = st.checkbox("Debug", value=False)

# Main content area
if movie_input:
    searched_movie, recommendations = find_similar_movies(movie_input, movies_data)

    if not searched_movie:
        st.error("❌ Movie not found. Please check the spelling or try another movie.")
        st.info("💡 Tip: Try popular movies like 'Avatar', 'The Dark Knight', or 'Inception'")
    else:
        st.success(f"✅ Found: **{searched_movie['original_title']}**")
        
        # Display the searched movie
        st.markdown("<h2 class='section-header'>🎯 Your Selected Movie</h2>", unsafe_allow_html=True)
        
        st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])

        with col1:
            poster = get_poster_url(searched_movie)
            
            if show_debug:
                st.info(f"Movie ID: {searched_movie.get('id')}")
                st.info(f"Poster URL: {poster}")
            
            if poster:
                try:
                    st.markdown("<div class='poster-card'>", unsafe_allow_html=True)
                    st.image(poster, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                except Exception as e:
                    if show_debug:
                        st.error(f"Error: {e}")
                    st.markdown("<div style='text-align:center; font-size:80px;'>🎭</div>", unsafe_allow_html=True)
                    st.caption("Poster unavailable")
            else:
                st.markdown("<div style='text-align:center; font-size:80px;'>🎭</div>", unsafe_allow_html=True)
                st.caption("Poster unavailable")

        with col2:
            st.markdown(f"### {searched_movie['original_title']}")
            
            st.markdown(f"**🎬 Director:** {get_director(searched_movie)}")
            
            st.markdown("**🎭 Genres:**")
            genres = get_genres(searched_movie)
            if genres:
                genre_html = "".join([f"<span class='genre-tag'>{g}</span>" for g in genres])
                st.markdown(genre_html, unsafe_allow_html=True)
            else:
                st.write("N/A")
            
            if searched_movie.get('overview'):
                st.markdown("**📖 Overview:**")
                overview = searched_movie.get('overview', '')
                st.write(overview[:300] + "..." if len(overview) > 300 else overview)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Display recommendations
        st.markdown("<h2 class='section-header'>🍿 Similar Movies You Might Like</h2>", unsafe_allow_html=True)
        
        if recommendations:
            for row in range(0, len(recommendations), 5):
                cols = st.columns(5)
                for i, col in enumerate(cols):
                    if row + i < len(recommendations):
                        score, movie = recommendations[row + i]
                        with col:
                            poster = get_poster_url(movie)
                            st.markdown("<div class='poster-card'>", unsafe_allow_html=True)
                            if poster:
                                try:
                                    st.image(poster, use_container_width=True)
                                except:
                                    st.markdown("<div style='text-align:center; font-size:60px;'>🎭</div>", unsafe_allow_html=True)
                            else:
                                st.markdown("<div style='text-align:center; font-size:60px;'>🎭</div>", unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            st.markdown(f"<div class='movie-original_title-rec'>{movie['original_title']}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div style='text-align:center'><span class='match-score'>⭐ {score}</span></div>", unsafe_allow_html=True)
                            genres_list = get_genres(movie)[:2]
                            if genres_list:
                                st.markdown(f"<div style='text-align:center; font-size:12px; color:#666; margin-top:5px;'>{' • '.join(genres_list)}</div>", unsafe_allow_html=True)
        else:
            st.info("😕 No similar movies found. Try searching for another movie!")

else:
    # Welcome screen with instructions
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("### 🎥 How it works:")
    st.markdown("""
    - **Step 1:** Enter a movie name you love in the search box above
    - **Step 2:** Get 10 personalized movie recommendations
    - **Step 3:** Discover new movies based on matching genres and directors
    - **Step 4:** Enjoy posters fetched dynamically from TMDB API
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align:center; color:white; margin-top:30px;'>🌟 Try searching for:</h3>", unsafe_allow_html=True)
    sample_movies = ["Avatar", "The Dark Knight", "Inception", "Titanic", "Interstellar", "The Matrix"]
    cols = st.columns(3)
    for i, movie in enumerate(sample_movies):
        with cols[i % 3]:
            if st.button(f"🎬 {movie}", key=movie):
                st.rerun()