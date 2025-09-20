import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry

from .decrypter import decrypt
from .models import Anime, Episode, Download

BASE_URL = "https://animepahe.si"
IMAGE_PROXY = "/image-proxy/"

_session = None

# --- Precompiled regex patterns ---
EPISODE_PATTERN = re.compile(
    r'"id":(\d+),"anime_id":(\d+),"episode":(\d+),"episode2":0,"edition":"","title":"","snapshot":"(.*?)","disc":"(.*?)","audio":"(.*?)","duration":"(.*?)","session":"(.*?)"'
)
DOWNLOAD_PATTERN = re.compile(
    r'<a href="(?P<url>.+?)" .+? class="dropdown-item">.+? (?P<resolution>\d+)p (.+?)MB(.+?)</a>'
)
REDIRECT_PATTERN = re.compile(r'\.attr\("href","(https://[^"]+)"\)')
KEYS_PATTERN = re.compile(r'\("(\w+)",\d+,"(\w+)",(\d+),(\d+),\d+\)')
POST_URL_PATTERN = re.compile(r'action="(.+?)"')
TOKEN_PATTERN = re.compile(r'value="(.+?)"')

# ---------------- Core Functions ----------------
def set_browser_cookies():
    """Launch Selenium, wait for JS cookies, then transfer them to requests session."""
    global _session
    _session = requests.Session()

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(BASE_URL)

    def cookie_ready(d):
        cookies = d.get_cookies()
        return any(c['name'] == "laravel_session" for c in cookies)

    try:
        WebDriverWait(driver, 15).until(cookie_ready)
    except:
        print("Warning: Key cookie not found, using whatever is available.")

    selenium_cookies = driver.get_cookies()
    print(f"Collected {len(selenium_cookies)} cookies.")

    for c in selenium_cookies:
        _session.cookies.set(c['name'], c['value'], domain=c.get('domain'), path=c.get('path'))

    _session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Accept": "application/json",
    })

    retries = Retry(total=5, backoff_factor=0.2, status_forcelist=[502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries, pool_connections=20, pool_maxsize=20)
    _session.mount("http://", adapter)
    _session.mount("https://", adapter)

    driver.quit()
    print("Requests session ready with browser cookies!")


def proxy_image_url(url: str) -> str:
    if url and url.startswith("https://i.animepahe"):
        return IMAGE_PROXY + url.split("/")[-1]
    return url


def fetch_image_bytes(image_url: str) -> bytes:
    headers = {
        "Referer": BASE_URL,
        "User-Agent": _session.headers.get("User-Agent"),
        "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    }
    resp = _session.get(image_url, headers=headers, stream=True, timeout=10)
    resp.raise_for_status()
    return resp.content


def get_related_anime_ids(soup: BeautifulSoup, relation_type: str):
    rel_div = soup.select_one("div.tab-content.anime-relation.row")
    if not rel_div:
        return []

    section = rel_div.find("h4", string=lambda x: x and relation_type.lower() in x.lower())
    if not section:
        return []

    container = section.find_parent("div", class_="col-12 col-sm-6")
    if not container:
        return []

    ids = []
    for a in container.find_all("a", href=True):
        m = re.match(r"^/anime/([a-z0-9\-]+)", a["href"])
        if m:
            ids.append(m.group(1))
    return ids


def fetch_seasons_chain(start_anime_id: str):
    """Traverse prequel + sequel chain and return full info list."""
    visited = {"prequel": set(), "sequel": set()}

    def fetch_chain(anime_id, rel_type):
        if anime_id in visited[rel_type]:
            return []
        visited[rel_type].add(anime_id)
        res = _session.get(f"{BASE_URL}/anime/{anime_id}")
        if not res.ok:
            return []
        soup = BeautifulSoup(res.text, "html.parser")
        related = get_related_anime_ids(soup, rel_type.capitalize())
        if rel_type == "prequel":
            return fetch_chain(related[0], rel_type) + [anime_id] if related else [anime_id]
        return [anime_id] + fetch_chain(related[0], rel_type) if related else [anime_id]

    prequels = fetch_chain(start_anime_id, "prequel")
    sequels = fetch_chain(start_anime_id, "sequel")

    if prequels and prequels[-1] == start_anime_id:
        prequels.pop()

    all_ids = prequels + sequels
    info = []
    for aid in all_ids:
        try:
            info.append(get_anime_info(aid))
        except Exception:
            info.append({"id": aid, "title": "Unknown"})
    return info


def search_anime(query: str):
    url = f"{BASE_URL}/api?m=search&q={query}"
    res = _session.get(url)
    res.raise_for_status()
    return [
        Anime(
            id_=a["id"],
            title=a["title"],
            type_=a["type"],
            status=a["status"],
            poster=a["poster"],
            session=a["session"]
        )
        for a in res.json().get("data", [])
    ]


def _fetch_episode_page(session_id: str, page: int):
    url = f"{BASE_URL}/api?m=release&id={session_id}&sort=episode_asc&page={page}"
    res = _session.get(url)
    res.raise_for_status()
    return EPISODE_PATTERN.findall(res.text)


def get_first_episode(session_id: str):
    matches = _fetch_episode_page(session_id, 1)
    if not matches:
        return None
    ep = matches[0]
    return Episode(ep[0], ep[1], ep[2], ep[3], ep[6], f"{BASE_URL}/play/{session_id}/{ep[7]}")


def get_episodes(session_id: str):
    page, episodes = 1, []
    while True:
        matches = _fetch_episode_page(session_id, page)
        if not matches:
            break
        for ep in matches:
            episodes.append(Episode(
                id_=ep[0],
                anime_id=ep[1],
                number=ep[2],
                snapshot=ep[3],
                duration=ep[6],
                url=f"{BASE_URL}/play/{session_id}/{ep[7]}"
            ))
        page += 1
    return episodes


def getDownloadOptions(url: str):
    res = _session.get(url)
    res.raise_for_status()

    downloads = []
    for m in DOWNLOAD_PATTERN.finditer(res.text):
        label_text = m.group(4).strip().lower()
        if "eng" in label_text:
            is_dubbed = True
        elif "sub" in label_text:
            is_dubbed = False
        else:
            # fallback: assume sub if unclear
            is_dubbed = False

        downloads.append(Download(
            url=m.group("url"),
            res=f"{m.group('resolution')}p",
            fileSize=m.group(3).strip("(") + "MB",
            is_dubbed=is_dubbed
        ))
    return downloads






def getDownloadLink(intermediary_url: str):
    page = _session.get(intermediary_url).text
    m = REDIRECT_PATTERN.search(page)
    if not m:
        raise Exception("Couldn't find redirect URL")

    download_page = _session.get(m.group(1)).text
    keys = KEYS_PATTERN.search(download_page)
    if not keys:
        raise Exception("Missing decryption keys")

    decrypted = decrypt(*keys.groups())
    post_url = POST_URL_PATTERN.search(decrypted).group(1)
    token = TOKEN_PATTERN.search(decrypted).group(1)

    resp = _session.post(post_url, allow_redirects=False, data={"_token": token}, headers={"Referer": "https://kwik.cx/"})
    if "Location" not in resp.headers:
        raise Exception("Final redirect link missing.")
    return resp.headers["Location"]


def get_airing(page: int = 1):
    url = f"{BASE_URL}/api?m=airing&page={page}"
    res = _session.get(url)
    res.raise_for_status()
    return [
        {
            "id": item["anime_session"],
            "title": item["anime_title"],
            "image": item["snapshot"],
        }
        for item in res.json().get("data", [])
    ]


def get_anime_info(session_id: str):
    url = f"{BASE_URL}/anime/{session_id}"
    res = _session.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    title = soup.select_one("h1.user-select-none > span")
    desc = soup.select_one("div.anime-synopsis")
    image = soup.select_one(".youtube-preview")

    return {
        "id": session_id,
        "title": title.text.strip() if title else "Unknown",
        "description": desc.text.strip() if desc else "",
        "image": image["href"] if image else "",
    }

def filter_downloads(downloads, quality=None, sub_only=False, dub_only=False, qualities=None):
    """
    Filter a list of Download objects based on preferences.

    :param downloads: list of Download
    :param quality: str (e.g. "720p") for a single resolution
    :param sub_only: bool, keep only sub
    :param dub_only: bool, keep only dub
    :param qualities: list of str (e.g. ["720p", "1080p"]) if you want multiple resolutions
    :return: list of Download
    """
    result = []

    for d in downloads:
        # quality filtering
        if quality and d.res != quality:
            continue
        if qualities and d.res not in qualities:
            continue

        # sub/dub filtering
        if sub_only and d.is_dubbed:
            continue
        if dub_only and not d.is_dubbed:
            continue

        result.append(d)

    return result

