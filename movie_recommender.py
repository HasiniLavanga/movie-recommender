import pandas as pd
import random
import sys

class MovieRecommender:

    def __init__(self, file):
        try:
            self.movies = pd.read_csv(file)

            # Check required columns
            if "movie" not in self.movies.columns or "genre" not in self.movies.columns:
                print("Error: CSV must have 'movie' and 'genre' columns.")
                exit()

            # Convert genres to lowercase
            self.movies["genre"] = self.movies["genre"].str.lower()
            print("✅ Dataset Loaded Successfully\n")

        except FileNotFoundError:
            print(f"Error: File '{file}' not found.")
            exit()
        except pd.errors.ParserError:
            print(f"Error: Failed to parse '{file}'. Check CSV format.")
            exit()
        except Exception as e:
            print(f"Unexpected error: {e}")
            exit()

    def get_all_genres(self):
        """Return a sorted list of unique genres."""
        genres = set()
        for g in self.movies["genre"]:
            for item in g.split("|"):
                genres.add(item.strip())
        return sorted(list(genres))

    def recommend_by_genre(self, user_genre):
        """Return a list of movies matching the user's genre."""
        recommendations = []

        for _, row in self.movies.iterrows():
            genres = [g.strip() for g in row["genre"].split("|")]
            if user_genre in genres:
                recommendations.append(row["movie"])

        return recommendations

    def start(self):
        print("🎬 Movie Recommendation System")
        print("\nAvailable Genres:\n")

        genres = self.get_all_genres()
        for g in genres:
            print("-", g)

        while True:
            user_input = input("\nEnter Genre (or type 'exit'): ").lower().strip()

            if user_input == "exit":
                print("System Closed")
                break

            if user_input not in genres:
                print("❌ Invalid Genre. Try again.")
                continue

            movies = self.recommend_by_genre(user_input)

            if not movies:
                print("⚠️ No movies found for this genre.")
            else:
                print("\nRecommended Movies:\n")
                random.shuffle(movies)
                for m in movies[:10]:
                    print("-", m)


if __name__ == "__main__":
    # Use command-line argument if provided, else default to 'movies.csv'
    file = sys.argv[1] if len(sys.argv) > 1 else "movies.csv"
    recommender = MovieRecommender(file)
    recommender.start()
