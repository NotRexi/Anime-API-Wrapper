from animepahe import (
    set_browser_cookies, search_anime, get_episodes,
    getDownloadOptions, getDownloadLink
)

# === DEMO: Get All Episode Downloads ===
set_browser_cookies()
results = search_anime("bleach") # Searches for anime
if results:
    anime = results[0] # Gets first anime result
    episodes = get_episodes(anime.session) # Gets all episodes of anime

    print(f"Found {len(episodes)} episodes for {anime.title}")
    for ep in episodes:
        ep_info = {
            "episode": ep.number,
            "url": ep.url,
            "downloads": []
        }
        try:
            opts = getDownloadOptions(ep.url) # Gets all download options of episode
            for o in opts:
                try:
                    final_url = getDownloadLink(o.url) # Gets episode download link
                    ep_info["downloads"].append({
                        "res": o.res,
                        "size": o.fileSize,
                        "dubbed": o.is_dubbed,
                        "final_url": final_url
                    })
                    print(f"  - {o.res} | {o.fileSize} | {'Dub' if o.is_dubbed else 'Sub'}")
                    print(f"    Final URL: {final_url}")
                except Exception as e:
                    print(f"[!] Failed to resolve link for ep {ep.number}: {e}")
        except Exception as e:
            print(f"[!] Failed to get download options for ep {ep.number}: {e}")
