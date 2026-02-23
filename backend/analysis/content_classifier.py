def categorize_url(url):
    url = url.lower()

    if "instagram" in url or "facebook" in url or "linkedin" in url:
        return "social"
    elif "youtube" in url or "netflix" in url:
        return "entertainment"
    elif "github" in url or "leetcode" in url or "stackoverflow" in url:
        return "study"
    elif "news" in url or "google.com/search" in url:
        return "news"
    else:
        return "other"


# quick test
if __name__ == "__main__":
    test_urls = [
        "https://www.instagram.com/",
        "https://github.com/Deekshith1064",
        "https://www.google.com/search?q=ulaa+extensions"
    ]

    for u in test_urls:
        print(u, "→", categorize_url(u))
