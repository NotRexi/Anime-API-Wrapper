from animepahe import (
    set_browser_cookies, search_anime, get_episodes
)

set_browser_cookies()

# === DEMO: Get all episodes ===
results = search_anime("bleach")
if results:
    anime = results[0] # Gets first anime result
    episodes = get_episodes(anime.session) # Gets all episodes of anime

    print(f"Found {len(episodes)} episodes for {anime.title}")
    for ep in episodes[:5]:  # Only gets first 5 episodes, if you want to get all, then remove [:5]
        print(f"Episode {ep.number} → {ep.url}")
