
# AnimePahe Python API Wrapper

  

A powerful Python library for searching, retrieving, and downloading anime episodes directly from [AnimePahe](https://animepahe.si), including support for episode metadata, sub/dub audio, multiple resolutions, and bypassing download protection.

  

## 🔥 Features

  

- 🔍 Search for anime by name  
- 📺 Fetch all episodes and metadata  
- 🧭 Detect and traverse prequels/sequels (season chaining)  
- 🎧 Support for subbed & dubbed audio  
- 📥 Get direct download links (1080p, 720p, etc.)  
- 🖼️ Download poster/snapshot images  
- 🍪 Cookie injection via browser automation  
- ✅ Requests-based with retry handling  
- 📦 Lightweight, no external API dependencies  

  

---

  

## 🛠 Requirements

  

- Python 3.8+  
- Google Chrome + ChromeDriver (for Selenium cookies)  
- `requests`, `beautifulsoup4`, `selenium`, `lxml`  

- [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg) (or any browser cookie export tool)

  

---

  

## ⚙️ Installation

1.  **Clone or extract** this project.
    
2.  **Install required dependencies** (see above): 
```bash
pip install requests beautifulsoup4 selenium lxml
```
3. Run ```docs/``` examples to test



  

---

  

## 🧠 Cookie Setup (IMPORTANT)


This wrapper uses Selenium to grab fresh cookies from AnimePahe.
Run once at the start of your script:
  

```python
from animepahe import set_browser_cookies

set_browser_cookies()
```

  

---

  


## 📘 Full API Docs

  

### `set_browser_cookies()`

Launches a headless browser, waits for JS cookies, and applies them to the requests session.\
**Returns:** `None`
  

### `search_anime(query: str) → List[Anime]`

Search AnimePahe by name.\
**Returns:** List of `Anime` objects with `id`, `title`, `type`, `status`, `poster`, `session`.
  

### `get_first_episode(session_id: str) → Episode`

Fetch metadata for the first episode of a series.\
**Returns:** `Episode` object
  

### `get_episodes(session_id: str) → List[Episode]`

Fetch all episodes for a series.\
**Returns:** List of `Episode` objects (`id`, `number`, `snapshot`, `duration`, `url`).

  

### `getDownloadOptions(episode_url: str) → List[Download]`

Parse all available download entries.\
**Returns:** List of `Download` objects with:

- `url` → intermediary link

- `res` → resolution (`1080p`, `720p`, etc.)

- `fileSize` → file size (MB)

- `is_dubbed` → `True` (dub) / `False` (sub)

  

### `getDownloadLink(intermediary_url: str) → str`

Bypass protection to fetch the final direct MP4 link.\
**Returns:** Direct download URL (string).

  

### `get_anime_info(session_id: str) → dict`

Get metadata for a series.\
**Returns:** Dict `{id, title, description, image}`.

  

### `fetch_seasons_chain(session_id: str) → List[dict]`

Traverse prequel/sequel chain and return all connected anime.\
**Returns:** List of dicts with anime metadata.
  

### `get_airing(page: int = 1) → List[dict]`

Lists currently airing anime series. (not the best)\
**Returns:** List of dicts `{id, title, image}`.
  

### `fetch_image_bytes(url: str) → bytes`

Download raw image bytes from AnimePahe.\
**Returns:** `bytes`

### `filter_downloads(downloads, quality=None, sub_only=False, dub_only=False, qualities=None) → List[Download]`

Filter downloads by resolution and/or sub/dub.

- `quality:`  `"720p"` (single)

- `qualities:` `["720p","1080p"]` (multiple)

- `sub_only:` `keep only subbed`

- `dub_only:` `keep only dubbed`\
**Returns:** Filtered list of `Download`.

---
## ❓ FAQ

  

### **Q: Will this work forever?**

A: This depends on AnimePahe's site structure. If they make major changes, small fixes might be needed — but it's built to be stable. If the animepahe.ru website goes down, you can use their alternate website animepahe.com. 


### **Q: Do I need cookies every time?**

A: Yes, but the Selenium session makes it easy—just call `set_browser_cookies()`.

### **Q: Does this break TOS?**

A: You are responsible for how you use this. This wrapper is intended for educational and research purposes only.

  

### **Q: Can I embed this in my anime site?**

A: Absolutely. This can be used as a backend library or CLI tool.

  

---

  

## 💸 License & Selling Terms

  

This project is **paid**, and distributed under a license that prohibits free redistribution. You may:

  

- ✅ Personal + commercial use allowed

- 🔒 Redistribution of source not allowed

- ⚠️ You are responsible for usage

  

---

  

## 💬 Support

  

For help or other inquiries:

💬 Discord: `rex.i`\
💬 Github: `NotRexi`

  

---

  

## 🧾 Changelog

  

**v1.0.0** – Initial release

- Full episode metadata support

- Sub/dub resolution filtering

- Season traversal

- Raw image downloading

- Cookie injection

**v1.0.1** - QOL Update + fixes

- Automatic Cookie injection
- Episode Filtering
- Docs folder added
- Removed redundant functions

---

## 📜 Legal Disclaimer

> This project is intended for **educational use only**.
> 
> I am **not affiliated with AnimePahe** or any of its owners, developers, or partners. All trademarks and copyrights belong to their respective owners.
> 
> By using this software, you agree that you are **responsible for your own actions**. The author is **not liable for any misuse**, including but not limited to unauthorized redistribution, commercial use of copyrighted content, or violations of any third-party terms of service.
