import json
from pathlib import Path

RAW_DIR = Path("data/raw")

def extract_features(meta_list, out_path, is_tv=False):
    features = []
    for item in meta_list:
        details = item.get("details", item)
        
        # Genres
        genres = [g["id"] for g in details.get("genres", [])]

        # Keywords
        if is_tv:
            keywords = [kw["name"] for kw in details.get("keywords", {}).get("results", [])]
        else:
            keywords = [kw["name"] for kw in details.get("keywords", {}).get("keywords", [])]

        # Credits
        credits = details.get("credits") or details.get("aggregate_credits")
        cast = []
        crew = []
        if credits:
            cast = [
                {
                    "name": c.get("name"),
                    "character": c.get("character") or c.get("roles", [{}])[0].get("character"),
                }
                for c in credits.get("cast", [])
            ]
            crew = [
                c.get("name") for c in credits.get("crew", [])
            ]
            
        # Content ratings (TV)
        content_ratings = []
        if is_tv:
            content_ratings = details.get("content_ratings", {}).get("results", [])

        # External IDs
        external_ids = details.get("external_ids", {})

        # Poster & Backdrop
        poster_path = details.get("poster_path")
        backdrop_path = details.get("backdrop_path")

        # Vote & popularity
        vote_average = details.get("vote_average")
        popularity = details.get("popularity")

        # Videos
        videos = item.get("videos", {}).get("results", [])
        video_key = -1
        for vid in videos:
            if vid['site'] == "Youtube" and vid['type'] == 'Trailer':
                video_key = vid['key']
                break

        # Reviews
        reviews = item.get("reviews", {}).get("results", [])
        reviews_content = []
        if len(reviews) > 0:
            for review in reviews:
                reviews_content.append(review['content'])

        record = {
            "id": details.get("id"),
            "title": details.get("title") or details.get("name"),
            "overview": details.get("overview"),
            "vote_average": vote_average,
            "popularity": popularity,
            "genres": genres,
            "keywords": keywords,
            "cast": cast,
            "crew": crew,
            "content_ratings": content_ratings,
            "external_ids": external_ids,
            "poster_path": poster_path,
            "backdrop_path": backdrop_path,
            "video_key": video_key,
            "review": reviews_content
        }
        features.append(record)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(features, f, ensure_ascii=False, indent=2)

def main():
    # Load raw metadata
    with open(RAW_DIR / "movies_metadata.json", encoding="utf-8") as f:
        movies_meta = json.load(f)
    with open(RAW_DIR / "tv_metadata.json", encoding="utf-8") as f:
        tv_meta = json.load(f)

    # Extract and save
    extract_features(movies_meta, RAW_DIR / "movies_features.json")
    extract_features(tv_meta, RAW_DIR / "tv_features.json")

if __name__ == "__main__":
    main()
