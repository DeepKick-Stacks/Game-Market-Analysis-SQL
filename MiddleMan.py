import requests
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

# 1. DATABASE CONNECTION
try:
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "password"),
        database=os.getenv("DB_NAME", "GameProject")
    )
    cursor = db.cursor()
    print("✓ Connected to MySQL")
except Error as e:
    print(f"✗ Database connection failed: {e}")
    exit(1)

# 2. API FETCH
api_url = "https://api.rawg.io/api/games?key={}&dates=2010-01-01,2020-12-31".format(
    os.getenv("RAWG_API_KEY", "REDACTED")
)

try:
    print("Connecting to RAWG API...")
    response = requests.get(api_url, timeout=10).json()
    print(f"✓ Fetched {len(response['results'])} games from API")
except Exception as e:
    print(f"✗ API fetch failed: {e}")
    exit(1)

# 3. DATA PROCESSING & INSERTION
insert_count = 0
for game in response['results']:
    try:
        release_year = int(game['released'][:4]) if game.get('released') else None
        
        # Insert game into master table
        sql_game = """
            INSERT IGNORE INTO `10yr_Video_Game_Sales`
            (GameID, Title, Releaseyear, Publisher)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql_game, (game['id'], game['name'], release_year, "Unknown"))
        
        # Insert platforms (normalized)
        if game.get('platforms'):
            for platform in game['platforms']:
                platform_name = platform['platform']['name']
                
                # Get or create platform
                cursor.execute("INSERT IGNORE INTO Platforms (PlatformName) VALUES (%s)", (platform_name,))
                cursor.execute("SELECT PlatformID FROM Platforms WHERE PlatformName = %s", (platform_name,))
                platform_id = cursor.fetchone()[0]
                
                # Link game to platform
                cursor.execute(
                    "INSERT IGNORE INTO Game_Platforms (GameID, PlatformID) VALUES (%s, %s)",
                    (game['id'], platform_id)
                )
        
        # Insert genres (normalized)
        if game.get('genres'):
            for genre in game['genres']:
                genre_name = genre['name']
                
                # Get or create genre
                cursor.execute("INSERT IGNORE INTO Genres (GenreName) VALUES (%s)", (genre_name,))
                cursor.execute("SELECT GenreID FROM Genres WHERE GenreName = %s", (genre_name,))
                genre_id = cursor.fetchone()[0]
                
                # Link game to genre
                cursor.execute(
                    "INSERT IGNORE INTO Game_Genres (GameID, GenreID) VALUES (%s, %s)",
                    (game['id'], genre_id)
                )
        
        # Insert transaction (using 'added' count as proxy for popularity)
        units_sold = game.get('added', 0)
        sql_trans = "INSERT INTO Transactions (GameID, UnitsSold, SaleDate) VALUES (%s, %s, %s)"
        cursor.execute(sql_trans, (game['id'], units_sold, game.get('released')))
        
        insert_count += 1
        
    except Error as e:
        print(f"  ⚠ Skipped game {game.get('name')}: {e}")
        continue

# 4. COMMIT & CLOSE
db.commit()
print(f"✓ Successfully synced {insert_count} games to database")
cursor.close()
db.close()
