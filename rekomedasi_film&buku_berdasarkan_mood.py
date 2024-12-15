import requests
import random
from transformers import pipeline

def analyze_sentiment(mood_input):
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    result = classifier(mood_input)
    return result[0]['label']

def get_movie_recommendations(mood):
    api_key = "b8ca0690ad75ba80a1d5694f644ebcea"  
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={mood}&language=en-US"
    response = requests.get(url)
    data = response.json()

    if data["results"]:
        sorted_movies = sorted(data["results"], key=lambda x: x.get("vote_average", 0), reverse=True)
        top_movies = random.sample(sorted_movies[:10], min(len(sorted_movies[:10]), 5))
        return top_movies
    else:
        return []

def get_book_recommendations(mood):
    api_key = "AIzaSyDhwTr-NDqHqDqIiPCsEKRMYqB9cQ0awks"  
    url = f"https://www.googleapis.com/books/v1/volumes?q={mood}&orderBy=relevance&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if "items" in data:
        top_books = random.sample(data["items"][:10], min(len(data["items"][:10]), 5))
        return top_books
    else:
        return []

def main():
    mood_input = input("Masukkan mood Anda (misalnya, senang, sedih, marah, excited): ").lower()

    sentiment = analyze_sentiment(mood_input)
    print(f"Sentimen mood Anda: {sentiment}")

    print("\nMencari rekomendasi film dan buku...\n")

    movies = get_movie_recommendations(mood_input)
    if movies:
        print("Rekomendasi Film:")
        for movie in movies:  
            title = movie["title"]
            release_date = movie.get("release_date", "Tanggal tidak tersedia")
            overview = movie.get("overview", "Deskripsi tidak tersedia")
            print(f"Judul: {title}\nRilis: {release_date}\nDeskripsi: {overview}\n")
    else:
        print("Tidak ada film yang ditemukan.")

    books = get_book_recommendations(mood_input)
    if books:
        print("\nRekomendasi Buku:")
        for book in books:  
            title = book["volumeInfo"]["title"]
            authors = book["volumeInfo"].get("authors", ["Tidak diketahui"])
            print(f"{title} oleh {', '.join(authors)}")
    else:
        print("Tidak ada buku yang ditemukan.")

if __name__ == "__main__":
    main()
