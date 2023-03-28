import requests

def fetch_reddit(query, subreddit):
    url = "https://api.pushshift.io/reddit/search/submission/"
    params = {
        "q": query,
        "size": 100,
        # "sort": "desc",
        # "sort_type": "created_utc",
        # "subreddit": subreddit,
    }
    r = requests.get(url, params=params)
    data = r.json()
    return data["data"]


if __name__ == "__main__":
    data = fetch_reddit("bc1qwukmzzjqn5hwsp4uaswc4c53gc0xz5asrv0prx", "bitcoin")
    print(data)
    print(len(data))