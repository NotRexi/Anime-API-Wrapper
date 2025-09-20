
# AnimePahe Python API Wrapper

  

A powerful Python library for searching, retrieving, and downloading anime episodes directly from [AnimePahe](https://animepahe.ru), including support for episode metadata, sub/dub audio, multiple resolutions, and bypassing download protection.

  

## 🔥 Features

  

- 🔍 Search for anime by name

- 📺 Fetch all episodes and metadata

- 🧭 Detect and traverse prequels/sequels (season chaining)

- 🎧 Support for subbed & dubbed audio

- 📥 Get direct download links (1080p, 720p, etc.)

- 🖼️ Download poster/snapshot images

- 🍪 Cookie support to bypass bot protection

- ✅ Fully asynchronous-safe and requests-based

- 📦 Lightweight, zero external API dependencies

  

---

  

## 🛠 Requirements

  

- Python 3.8+

- Browser (for cookies export)

- [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg) (or any browser cookie export tool)

  

---

  

## ⚙️ Installation

1.  **Download the ZIP package** you received and extract it anywhere on your computer.
    
2.  **Install required dependencies** (only `requests`, `beautifulsoup4` and optionally `lxml` for faster parsing): 
```bash
pip install requests beautifulsoup4 lxml` 
```
    

4.  **Export your cookies from AnimePahe**:
    
    -   Visit [https://animepahe.ru](https://animepahe.ru) in your browser.
        
    -   Use a browser extension like EditThisCookie or similar.
        
    -   Export your cookies as a **Netscape format `.txt` file**.
        
    -   Save it somewhere on your computer (e.g., `C:/Users/YourName/Project/cookies.txt`).
        
5.  **Edit the demo file** (e.g., `demo.py`) and set your cookie path:
```python
cookie_path = "C:/Users/YourName/cookies.txt"
```

6.  **Run the script**:
    
```bash
python client.py
```


  

---

  

## 🧠 Cookie Setup (IMPORTANT)

  

This library **requires your own cookies** from visiting AnimePahe in your browser, to bypass cloudflare or ddos protection.

  

1. Go to [https://animepahe.ru](https://animepahe.ru) in your browser.

2. Use  a extension like [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg) to export the cookies

3. Export as **Netscape HTTP Cookie File** (`cookies.txt`)

4. Place the file anywhere, and **set the path manually** in your code:

  

```python

from animepahe import set_cookie_file

set_cookie_file("C:/Users/youruser/Downloads/cookies.txt")

```

  

---

  

## 🚀 Usage Example

  

```python

from animepahe import  (

search_anime, get_first_episode,

getDownloadOptions, getDownloadLink,

set_cookie_file

)

  

# Set cookie file path

set_cookie_file("C:/Users/youruser/Downloads/cookies.txt")

  

# Search

results =  search_anime("bleach")

anime = results[0]

  

# Get first episode info

ep1 =  get_first_episode(anime.session)

  

# Show download options

options =  getDownloadOptions(ep1.url)

for opt in options:

print(f"{opt.res} - {opt.fileSize} - {'Dub'  if opt.is_dubbed else  'Sub'}")

print("Final URL:",  getDownloadLink(opt.url))

```

  

---

  

## 📘 Full API Docs

  

### `set_cookie_file(path)`

Sets the cookies from a `.txt` Netscape format file.

  

### `search_anime(query) → List[Anime]`

Searches AnimePahe and returns matching anime.

  

### `get_first_episode(session_id) → Episode`

Fetches metadata for the very first episode of the anime.

  

### `get_episodes(session_id) → List[dict]`

Returns all available episodes with info: number, audio, snapshot, duration.

  

### `getDownloadOptions(episode_url) → List[Download]`

Returns all available download links (resolution, size, dub/sub, etc).

  

### `getDownloadLink(intermediary_url) → str`

Returns final direct download link (MP4) from the episode's available download links

  

### `get_anime_info(session_id) → dict`

Gets title, description, and cover image of an anime series.

  

### `fetch_seasons_chain(session_id) → List[dict]`

Traverses prequels/sequels and returns full anime season chain.

  

### `get_airing(page=1) → List[dict]`

Lists currently airing anime series.

  

### `fetch_image_bytes(url) → bytes`

Downloads raw image bytes from AnimePahe.

---
## ❓ FAQ

  

**Q: Will this work forever?**

A: This depends on AnimePahe's site structure. If they make major changes, small fixes might be needed — but it's built to be stable. If the animepahe.ru website goes down, you can use their alternate website animepahe.com. 

  

**Q: Does this break TOS?**

A: You are responsible for how you use this. This tool mimics a real browser visit using your own cookies.

  

**Q: Can I embed this in my anime site?**

A: Absolutely. This can be used as a backend library or CLI tool.

  

---

  

## 💸 License & Selling Terms

  

This project is **paid**, and distributed under a license that prohibits free redistribution. You may:

  

- Use it in your commercial or private projects

- Modify it for personal use

- NOT resell or share the source without permission

  

---

  

## 💬 Support

  

For help or other inquiries:

💬 Discord: `rex.i`

  

---

  

## 🧾 Changelog

  

**v1.0.0** – Initial release

- Full episode metadata support

- Sub/dub resolution filtering

- Season traversal

- Raw image downloading

- Cookie injection

  

---

## 📜 Legal Disclaimer

> This project is intended for **educational use only**.
> 
> I am **not affiliated with AnimePahe** or any of its owners, developers, or partners. All trademarks and copyrights belong to their respective owners.
> 
> By using this software, you agree that you are **responsible for your own actions**. The author is **not liable for any misuse**, including but not limited to unauthorized redistribution, commercial use of copyrighted content, or violations of any third-party terms of service.
