import re
import requests
import http.cookiejar as cookiejar
from bs4 import BeautifulSoup
from .models import Anime, Episode, Download
from .decrypter import decrypt

BASE_URL = "https://animepahe.ru" # You can change this to animepahe.com if .ru stops working
_session = None

def set_cookie_file(path):
    global _session
    cookie_jar = cookiejar.MozillaCookieJar()
    cookie_jar.load(path, ignore_discard=True, ignore_expires=True)

    _session = requests.session()
    _session.cookies = cookie_jar
    _session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
    })


def fetch_image_bytes(image_url):
    headers = {
        "Referer": BASE_URL,
        "User-Agent": _session.headers.get("User-Agent", "Mozilla/5.0"),
        "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    }
    resp = _session.get(image_url, headers=headers)
    resp.raise_for_status()
    return resp.content


def get_related_anime_ids(soup, relation_type):
    rel_div = soup.find("div", class_="tab-content anime-relation row")
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
        match = re.match(r"^/anime/([a-z0-9\-]+)", a['href'])
        if match:
            ids.append(match.group(1))
    return ids


def fetch_seasons_chain(start_anime_id):
    visited_prequels = set()
    visited_sequels = set()

    def fetch_prequels(anime_id):
        if anime_id in visited_prequels:
            return []
        visited_prequels.add(anime_id)
        res = _session.get(f"{BASE_URL}/anime/{anime_id}")
        if not res.ok:
            return []
        soup = BeautifulSoup(res.text, "html.parser")
        prequels = get_related_anime_ids(soup, "Prequel")
        return fetch_prequels(prequels[0]) + [anime_id] if prequels else [anime_id]

    def fetch_sequels(anime_id):
        if anime_id in visited_sequels:
            return []
        visited_sequels.add(anime_id)
        res = _session.get(f"{BASE_URL}/anime/{anime_id}")
        if not res.ok:
            return []
        soup = BeautifulSoup(res.text, "html.parser")
        sequels = get_related_anime_ids(soup, "Sequel")
        return [anime_id] + fetch_sequels(sequels[0]) if sequels else [anime_id]

    prequels = fetch_prequels(start_anime_id)
    sequels = fetch_sequels(start_anime_id)

    if prequels and prequels[-1] == start_anime_id:
        prequels.pop()

    all_ids = prequels + sequels
    full_info = []
    for aid in all_ids:
        try:
            full_info.append(get_anime_info(aid))
        except:
            full_info.append({"id": aid, "title": "Unknown"})
    return full_info


def search_anime(query):
    url = f"{BASE_URL}/api?m=search&q={query}"
    res = _session.get(url)
    if res.status_code != 200:
        return []

    anime_list = []
    for anime in res.json().get("data", []):
        anime_list.append(Anime(
            id_=anime["id"],
            title=anime["title"],
            type_=anime["type"],
            status=anime["status"],
            poster=anime["poster"],
            session=anime["session"]
        ))
    return anime_list


def get_first_episode(session_id):
    page = 1
    while True:
        url = f"{BASE_URL}/api?m=release&id={session_id}&sort=episode_asc&page={page}"
        res = _session.get(url)
        if res.status_code != 200:
            return None

        matches = re.findall(
            r'"id":(\d+),"anime_id":(\d+),"episode":(\d+),"episode2":0,"edition":"","title":"","snapshot":"(.*?)","disc":"(.*?)","audio":"(.*?)","duration":"(.*?)","session":"(.*?)"',
            res.text
        )
        if matches:
            ep = matches[0]
            return Episode(ep[0], ep[1], ep[2], ep[3], ep[5], ep[6], f'{BASE_URL}/play/{session_id}/{ep[7]}')
        page += 1


def get_episodes(session_id):
    page = 1
    all_episodes = []
    while True:
        url = f"{BASE_URL}/api?m=release&id={session_id}&sort=episode_asc&page={page}"
        res = _session.get(url)
        if res.status_code != 200:
            break
        matches = re.findall(
            r'"id":(\d+),"anime_id":(\d+),"episode":(\d+),"episode2":0,"edition":"","title":"","snapshot":"(.*?)","disc":"(.*?)","audio":"(.*?)","duration":"(.*?)","session":"(.*?)"',
            res.text
        )
        if not matches:
            break
        for ep in matches:
            all_episodes.append({
                "id": ep[0],
                "anime_id": ep[1],
                "number": ep[2],
                "snapshot": ep[3],
                "audio": ep[5],
                "duration": ep[6],
                "url": ep[7],
                "is_dubbed": ep[5].lower() == "eng"
            })
        page += 1
    return all_episodes


def getDownloadOptions(url):
    res = _session.get(url)
    if res.status_code != 200:
        return []

    matches = re.findall(
        r'<a href="(?P<url>.+?)" .+? class="dropdown-item">.+? (?P<resolution>\d+)p (.+?)MB(.+?)</a>',
        res.text
    )
    downloads = []
    for m in matches:
        is_dubbed = "eng" in m[3].lower()
        downloads.append(Download(m[0], m[1]+"p", m[2].strip('(')+"MB", is_dubbed, is_dubbed))
    return downloads


def getDownloadLink(intermediary_url):
    page = _session.get(intermediary_url).text
    m = re.search(r'\.attr\("href","(https://[^"]+)"\)', page)
    if not m:
        raise Exception("Couldn't find redirect URL")
    redirect_url = m.group(1)

    download_page = _session.get(redirect_url).text
    keys = re.search(r'\("(\w+)",\d+,"(\w+)",(\d+),(\d+),\d+\)', download_page)
    if not keys:
        raise Exception("Missing decryption keys")
    decrypted = decrypt(*keys.groups())

    post_url = re.search(r'action="(.+?)"', decrypted).group(1)
    token = re.search(r'value="(.+?)"', decrypted).group(1)

    resp = _session.post(post_url, allow_redirects=False, data={"_token": token}, headers={"Referer": "https://kwik.cx/"})
    if "Location" not in resp.headers:
        raise Exception("Final redirect link missing.")
    return resp.headers["Location"]


def get_airing(page=1):
    url = f"{BASE_URL}/api?m=airing&page={page}"
    res = _session.get(url)
    if res.status_code != 200:
        return []
    return [
        {
            'id': item['anime_session'],
            'title': item['anime_title'],
            'image': item['snapshot']
        }
        for item in res.json().get("data", [])
    ]


def get_anime_info(session_id):
    url = f"{BASE_URL}/anime/{session_id}"
    res = _session.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    title = soup.select_one("h1.user-select-none > span")
    desc = soup.select_one("div.anime-synopsis")
    image = soup.select_one(".youtube-preview")

    img_url = image["href"] if image else ""
    if img_url.startswith("https://i.animepahe.ru/"):
        img_url = "/image-proxy/" + img_url.split("/")[-1]

    return {
        "id": session_id,
        "title": title.text.strip() if title else "Unknown",
        "description": desc.text.strip() if desc else "",
        "image": img_url
    }
