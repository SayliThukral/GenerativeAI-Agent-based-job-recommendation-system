# import os
# import aiohttp  # for async HTTP requests
# import asyncio

# class SearchService:
#     def __init__(self):
#         self.api_key = os.getenv('SERPER_API_KEY')
#         self.url = "https://google.serper.dev/videos"

#     async def get_youtube_tutorials(self, skill):
#         headers = {
#             "X-API-KEY": self.api_key,
#             "Content-Type": "application/json"
#         }
#         payload = {"q": f"{skill} tutorial"}

#         async with aiohttp.ClientSession() as session:
#             async with session.post(self.url, json=payload, headers=headers) as response:
#                 if response.status == 200:
#                     data = await response.json()
#                     # Extract YouTube video links from API response
#                     video_links = []
#                     for item in data.get("videos", []):
#                         video_links.append(item.get("link"))
#                     return video_links
#                 else:
#                     print(f"Error fetching videos: {response.status}")
#                     return []  