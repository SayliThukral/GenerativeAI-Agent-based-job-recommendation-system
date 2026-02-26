import requests
import json

# 🔑 Replace with your actual Serper API key
SERPER_API_KEY = "788071f68c70c5fb8d24abd94cf0b6ea77ff5fa2"

def search_youtube(query):
    url = "https://google.serper.dev/search"

    payload = {
        "q": query,
        "type": "videos"   # This ensures YouTube/video results
    }

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        data = response.json()

        print("\n✅ API Working! Here are YouTube links:\n")

        for video in data.get("videos", []):
            print("Title:", video.get("title"))
            print("Link:", video.get("link"))
            print("-" * 50)

    else:
        print("❌ Error:", response.status_code)
        print(response.text)


# 🔍 Test Search
search_youtube("machine learning tutorial")

# # test_serper_api.py
# import asyncio
# from src.services.search_service import SearchService

# async def main():
#     service = SearchService()
#     skill = "Python"  # Example skill
#     videos = await service.get_youtube_tutorials(skill)
#     print("YouTube tutorials for", skill)
#     for v in videos:
#         print(v)

# if __name__ == "__main__":
#     asyncio.run(main())
