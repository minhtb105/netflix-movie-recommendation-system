import 
from collections import defaultdict
from pathlib import Path

RAW_DIR = Path("data/raw")

def extract_features(meta_list, out_path: str, review_out_path: str, is_tv: bool=False):
    features = []
    all_cast = defaultdict(list)
    for item in meta_list:
        details = item.get("details", item)
        
        # Id
        id = item.get("id")
        
        # Title
        title = details.get("title") or details.get("name")
        
        # Genres
        genre_ids = details.get("genres", []) or details.get("genre_ids", [])
        genres = [g["name"] for g in genre_ids]

        # Keywords
        keywords = [kw.get("name") for kw in details.get("keywords", {}).get("results" if is_tv else "keywords", [])]
        keywords = " ".join(keywords)

        # Credits
        credits = details.get("credits") or details.get("aggregate_credits")
        cast = []
        crew = []
        if credits:
            cast = []
            for c in credits.get("cast", []):
                character = (c.get("character") or c.get("roles", [{}])[0].get("character") or "").lower()
                if "uncredited" not in character and "voice" not in character:
                    cast.append({
                        "id": c.get("id"),
                        "name": c.get("name"),
                        "character": character,
                        "popularity": c.get("popularity", 0),
                    })

            crew = " ".join([c.get("name") for c in credits.get("crew", [])])
        sorted_cast_list = sorted(cast, key=lambda x: x["popularity"], reverse=True)[:3]
        all_cast[id] = sorted_cast_list
        cast = [c["name"] for c in sorted_cast_list]
        
        # Poster & Backdrop
        poster_path = details.get("poster_path")
        backdrop_path = details.get("backdrop_path")

        # Vote & popularity
        vote_average = details.get("vote_average")
        vote_count = details.get("vote_count")
        popularity = details.get("popularity")

        # Videos
        videos = item.get("videos", {}).get("results", [])

        # Reviews
        reviews = item.get("reviews", {}).get("results", [])
        movie_reviews = []
        for review in reviews:
            movie_reviews.append({
                "id": id,
                "username": review['author_details'].get('username', ''),
                "content": review.get('content', ''),
                "rating": review['author_details'].get('rating', 0)
            })


        # Budget
        budget = details.get("budget", 0)

        # Revenue
        revenue = details.get("revenue", 0)

        # Runtime
        runtime = details.get("runtime", 0)
        
        # Origin, Production countries
        origin_country = details.get("origin_country", [])
        origin_country = " ".join(origin_country)
        
        production_countries = details.get("production_countries", [])
        
        countries_name = []
        for production_country in production_countries:
            countries_name.append(production_country['name']) 
            
        countries_name = " ".join(countries_name)

        # Original language
        original_language = details.get("original_language", "")

        record = {
            "id": details.get("id"),
            "title": title,
            "overview": str(details.get("overview")),
            "vote_average": vote_average,
            "vote_count": vote_count,
            "popularity": popularity,
            "budget": budget,
            "revenue": revenue,
            "runtime": runtime,
            "origin_country": origin_country,
            "original_language": original_language,
            "production_countries": countries_name,
            "genres": genres,
            "keywords": keywords,
            "cast": cast,
            "crew": crew,
            "poster_path": poster_path,
            "backdrop_path": backdrop_path,
            "videos": videos,
        }
        features.append(record)

    # Save feature
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(features, f, ensure_ascii=False, indent=2)

    # Save review
    with open(review_out_path, "w", encoding="utf-8") as f:
        json.dump(movie_reviews, f, ensure_ascii=False, indent=2)
        
    # Save cast metadata
    if is_tv:
        cast_out_path = f"{RAW_DIR}/tv_cast_metadata.json"
    else:
        cast_out_path = f"{RAW_DIR}/movie_cast_metadata.json"
        
    with open(cast_out_path, "w", encoding="utf-8") as f:
        json.dump(all_cast, f, ensure_ascii=False, indent=2)


def main():
    # Load raw metadata
    with open(RAW_DIR / "movies_metadata.json", encoding="utf-8") as f:
        movies_meta = json.load(f)
    with open(RAW_DIR / "tv_metadata.json", encoding="utf-8") as f:
        tv_meta = json.load(f)

    # Extract and save
    extract_features(movies_meta, RAW_DIR / "movies_features.json", RAW_DIR / "movies_reviews.json")
    extract_features(tv_meta, RAW_DIR / "tv_features.json", RAW_DIR / "tv_reviews.json")

if __name__ == "__main__":
    main()
