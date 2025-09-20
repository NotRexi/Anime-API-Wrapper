from animepahe import set_browser_cookies, search_anime

# Initialize session
set_browser_cookies()

# === DEMO: Search ===
query = "naruto"
results = search_anime(query) # Searches for anime

print(f"Search results for '{query}':")
for anime in results:
    print(f"- {anime.title} (id={anime.id}, session={anime.session})")
