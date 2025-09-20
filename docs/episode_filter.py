from animepahe import (
    set_browser_cookies, search_anime, get_episodes,
    getDownloadOptions, getDownloadLink, filter_downloads
)

set_browser_cookies()
results = search_anime("bleach")

if results:
    anime = results[0] # Gets first anime result
    episodes = get_episodes(anime.session) # Finds all episodes of the anime

    print(f"Found {len(episodes)} episodes for {anime.title}\n")

    for ep in episodes[:3]: # Only gets first 3 episodes, if you want to get all, then remove [:3]
        print(f"Episode {ep.number}: {ep.url}")
        opts = getDownloadOptions(ep.url) # Gets all download options

        # === CUSTOMIZABLE ===
        # only 720p (sub + dub)
        #filtered_episodes = filter_downloads(opts, quality="720p")

        # only subs (all qualities)
        #filtered_episodes = filter_downloads(opts, sub_only=True)

        # only dub at 1080p
        filtered_episodes = filter_downloads(opts, quality="1080p", dub_only=True)
        # ====================

        for filtered_episode in filtered_episodes:
            final_url = getDownloadLink(filtered_episode.url) # Gets download link of filtered episodes
            print(f"  {filtered_episode.res} | {filtered_episode.fileSize} | {filtered_episode.label} → {final_url}")
        print()
