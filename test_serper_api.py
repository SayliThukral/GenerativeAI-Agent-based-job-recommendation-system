import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def get_youtube_tutorials_for_gaps(domain):
    """
    Takes the extracted Domain and missing skills from the ATS logic
    and returns YouTube video recommendations.
    """
    
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),
        "Content-Type": "application/json"
    }
    
    # Construct a search query focused strictly on YouTube results
    query = f"{domain} resume formatting tutorial site:youtube.com"
    payload = json.dumps({
        "q": query,
        "num": 3  
    })
    
    recommendations = {}
    
    try:
        # Make the POST request to the Serper API
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status() # Catch any HTTP errors
        data = response.json()
        
        # Extract the relevant links from the 'organic' search results
        if "organic" in data:
            tutorials = []
            for item in data["organic"]:
                title = item.get("title")
                link = item.get("link")
                
                # Double-check that the link is actually a YouTube video
                if link and ("youtube.com" in link or "youtu.be" in link):
                    tutorials.append({
                        "title": title,
                        "url": link
                    })
            
            recommendations[f"{domain}_resume_tutorials"] = tutorials
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while calling the Serper API: {e}")
        recommendations["error"] = "Failed to fetch video recommendations."
                
    return recommendations