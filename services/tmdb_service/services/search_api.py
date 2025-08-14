from clients.base_client import TMDBBaseClient


class SearchService(TMDBBaseClient):
    async def search_movie(self, query: str, year="2025", language="en-US", page=1, 
                    region="VN", include_adult=False):
        endpoint = "/search/movie"
        params = {
            "query": query,
            "year": year,
            "primary_release_year": year,
            "language": language,
            "page": page,
            "region": region,
            "include_adult": include_adult
        }
        
        return await self._get(endpoint, params)

    async def search_tv(self, query: str, first_air_date_year=2025, 
                  language="en-US", page=1, include_adult=False):
        endpoint = "/search/tv"
        params = {
            "query": query,
            "first_air_date_year": first_air_date_year,
            "language": language,
            "page": page,
            "include_adult": include_adult
        }
        
        return await self._get(endpoint, params)

    async def search_person(self, query: str, language="en-US", page=1, include_adult=False):
        endpoint = "/search/person"
        params = {
            "query": query,
            "language": language,
            "page": page,
            "include_adult": include_adult
        }
        
        return await self._get(endpoint, params)

    async def search_multi(self, query: str, language="en-US", page=1, include_adult=False):
        endpoint = "/search/multi"
        params = {
            "query": query,
            "language": language,
            "page": page,
            "include_adult": include_adult
        }
        
        return await self._get(endpoint, params)

    async def find_by_external_id(self, external_id: str, external_source: str):
        endpoint = f"/find/{external_id}"
        params = {"external_source": external_source}
        
        return await self._get(endpoint, params)
