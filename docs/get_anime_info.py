from animepahe import set_browser_cookies, search_anime, get_anime_info

set_browser_cookies()

# === DEMO: Get anime info page ===
results = search_anime("attack on titan")
if results:
    anime = results[0] # Gets first anime result
    info = get_anime_info(anime.session) # Retrieves info of anime

    print("Title:", info["title"])
    print("Description:", info["description"][:200], "...")
    print("Image:", info["image"])
