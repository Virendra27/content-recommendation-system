# 🎬 Movie Recommender System

A beautiful and intelligent movie recommendation web application built with Streamlit that helps you discover movies similar to your favorites based on genres and directors.

## 📋 Table of Contents
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Contributing](#contributing)

## ✨ Features

- **Intelligent Recommendations**: Get 10 personalized movie recommendations based on genre matching and director similarity
- **Beautiful UI**: Modern gradient design with smooth animations and hover effects
- **Dynamic Posters**: Fetches high-quality movie posters from TMDB API
- **Cloud-Based Data**: Loads movie data directly from Google Drive - no local files needed
- **Fast Search**: Quickly search through 5000+ movies
- **Detailed Movie Info**: View director, genres, and overview for each movie
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Debug Mode**: Optional debug panel for troubleshooting

## 🎯 How It Works

### Recommendation Algorithm

The app uses a simple but effective content-based filtering approach:

1. **Genre Matching**: Compares genres between your selected movie and all other movies
   - Each matching genre adds +2 points to the similarity score

2. **Director Matching**: Checks if movies share the same director
   - Same director adds +3 points to the similarity score

3. **Ranking**: Movies are ranked by their total score, and the top 10 are displayed

### Example:
If you search for **"The Dark Knight"** (Action, Crime, Drama - directed by Christopher Nolan):
- Movies with matching genres get 2-6 points
- Christopher Nolan movies get an additional 3 points
- "Inception" would score high (same director + similar genres)

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/movie-recommender.git
cd movie-recommender
```

### Step 2: Install Dependencies
```bash
pip install streamlit requests
```

Or create a `requirements.txt` file:
```txt
streamlit>=1.28.0
requests>=2.31.0
```

Then install:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. TMDB API Key (Required for Posters)

To display movie posters, you need a free TMDB API key:

1. Go to [The Movie Database](https://www.themoviedb.org/)
2. Create a free account
3. Go to Settings → API
4. Request an API key (choose "Developer" option)
5. Copy your API key

**Update in `app.py`:**
```python
TMDB_API_KEY = "your_api_key_here"
```

### 2. Google Drive CSV Files (Already Configured)

The app uses two CSV files hosted on Google Drive:
- `tmdb_5000_credits.csv` - Contains movie credits and crew information
- `tmdb_5000_movies.csv` - Contains movie details, genres, and overviews

**Current Configuration:**
```python
CREDITS_CSV_URL = "https://drive.google.com/file/d/1c5m3-p-ZTSMMwNtHCBYySWG4lijQlLkY/view?usp=sharing"
MOVIES_CSV_URL = "https://drive.google.com/file/d/18xo7HkKT24ZERhziF-XdwYXqBVPpvPE6/view?usp=sharing"
```

**Note:** These files must be set to "Anyone with the link can view" in Google Drive.

## 💻 Usage

### Running the App

```bash
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

### Using the App

1. **Search for a Movie**: Type a movie name in the search box
2. **View Details**: See the movie's poster, director, genres, and overview
3. **Get Recommendations**: Scroll down to see 10 similar movies
4. **Click on Recommendations**: Each recommended movie shows its poster, title, match score, and genres
5. **Try Sample Movies**: Use the quick-access buttons for popular movies

### Debug Mode

Enable the "Debug" checkbox to see:
- Movie IDs
- Poster URLs
- Error messages for troubleshooting

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web framework for building the UI |
| **Python** | Core programming language |
| **Requests** | HTTP library for API calls and file downloads |
| **CSV Module** | Reading and parsing CSV data |
| **JSON Module** | Parsing JSON fields in CSV data |
| **TMDB API** | Fetching movie posters and metadata |
| **Google Drive** | Cloud storage for CSV files |

## 📁 Project Structure

```
movie-recommender/
│
├── app.py                      # Main application file
├── README.md                   # This file
├── requirements.txt            # Python dependencies
│
└── data/ (on Google Drive)
    ├── tmdb_5000_credits.csv   # Movie credits data
    └── tmdb_5000_movies.csv    # Movie details data
```

## 🎨 UI Features

- **Gradient Background**: Purple gradient (from #667eea to #764ba2)
- **Glass-morphism Cards**: Semi-transparent white cards with blur effect
- **Hover Animations**: Cards lift and expand on hover
- **Genre Tags**: Colorful tags for easy genre identification
- **Match Scores**: Gradient badges showing similarity scores
- **Responsive Grid**: 5-column layout for recommendations
- **Loading Indicators**: Spinners during data loading
- **Error Messages**: User-friendly error notifications

## 📊 Data Schema

### Credits CSV
- `movie_id`: Unique identifier linking to movies
- `title`: Movie title
- `cast`: JSON array of cast members
- `crew`: JSON array of crew members (includes directors)

### Movies CSV
- `id`: Unique movie identifier
- `original_title`: Original movie title
- `genres`: JSON array of genre objects
- `overview`: Movie description
- `poster_path`: Path to poster image

## 🔧 Customization

### Change Number of Recommendations
In `find_similar_movies()` function:
```python
return target_movie, similar_movies[:10]  # Change 10 to desired number
```

### Adjust Scoring Algorithm
In `find_similar_movies()` function:
```python
score = (genre_matches * 2) + (director_match * 3)
# Adjust multipliers to change importance of genres vs directors
```

### Modify UI Colors
Update the CSS in the `st.markdown()` section:
```python
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# Change these hex colors to your preferred gradient
```

## 🐛 Troubleshooting

### Common Issues

**1. "Failed to load data from Google Drive"**
- Check if Google Drive files are set to "Anyone with the link"
- Verify the URLs are correct
- Check your internet connection

**2. "Poster unavailable"**
- Verify your TMDB API key is valid
- Check if the movie has a poster in TMDB database
- Enable Debug mode to see the actual error

**3. "Movie not found"**
- Check spelling of the movie name
- Try using the exact title from the dataset
- Use the sample movie buttons to verify the app is working

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

1. **Report Bugs**: Open an issue describing the bug
2. **Suggest Features**: Share ideas for new features
3. **Improve Algorithm**: Enhance the recommendation logic
4. **UI Improvements**: Make the interface more beautiful
5. **Documentation**: Help improve this README

### Steps to Contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created with ❤️ by [Your Name]

## 🙏 Acknowledgments

- Movie data from [The Movie Database (TMDB)](https://www.themoviedb.org/)
- Dataset from [Kaggle TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
- Built with [Streamlit](https://streamlit.io/)

## 📧 Contact

For questions or feedback, please reach out:
- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)

---

**Enjoy discovering new movies! 🍿🎬**
