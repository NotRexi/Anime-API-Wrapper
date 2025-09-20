from animepahe import (
    search_anime, get_first_episode, getDownloadOptions,
    getDownloadLink, set_browser_cookies
)

# Initialize session
set_browser_cookies()

# === DEMO: Get first episode of Bleach ===
results = search_anime("bleach")
if results:
    anime = results[0] # Gets first anime result
    print("Title:", anime.title)

    ep1 = get_first_episode(anime.session) # Gets only the first anime episode
    if ep1:
        print("Episode URL:", ep1.url)
        opts = getDownloadOptions(ep1.url) # Gets episodes download options
        for o in opts:
            print(f"{o.res} - {o.fileSize} - Dubbed: {o.is_dubbed}")
            try:
                final_url = getDownloadLink(o.url) # Gets the episodes download link
                print("Final download link:", final_url)
            except Exception as e:
                print("Error getting final link:", e)
