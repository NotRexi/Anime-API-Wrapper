from animepahe import (
    search_anime, get_first_episode, getDownloadOptions,
    getDownloadLink, set_cookie_file
)
import os

# === CONFIGURABLE COOKIE PATH ===
# IMPORTANT: Visit https://animepahe.ru in your browser
# Use a browser extension like EditThisCookie to export your cookies.txt as a Netscape HTTP Cookie File
# Save that file in the project (edit path as needed)

cookie_path = "path/to/your/cookie/file"  # replace this with cookie file path

if not os.path.exists(cookie_path):
    raise FileNotFoundError(f"Cookie file not found: {cookie_path}")

# Load the cookies.txt
set_cookie_file(cookie_path)

# === DEMO USAGE ===
results = search_anime("bleach")
if results:
    anime = results[0]
    print("Title:", anime.title)

    ep1 = get_first_episode(anime.session)
    if ep1:
        print("Episode URL:", ep1.url)
        opts = getDownloadOptions(ep1.url)
        for o in opts:
            print(f"{o.res} - {o.fileSize} - {o.type}")
            try:
                final_url = getDownloadLink(o.url)
                print("Final download link:", final_url)
                #break <-- this would make it only return the first episode out of however many there are (lowest quality)
            except Exception as e:
                print("Error getting final link:", e)
