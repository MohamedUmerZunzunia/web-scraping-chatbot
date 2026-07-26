import requests
from bs4 import BeautifulSoup


class WebScraper:

    def scrape(self, url: str):

        try:
            response = requests.get(
                url,
                timeout=15,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/138.0 Safari/537.36"
                    )
                }
            )

            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove unwanted elements
            for tag in soup([
                "script",
                "style",
                "noscript",
                "header",
                "footer",
                "nav",
                "aside",
                "svg"
            ]):
                tag.decompose()

            title = (
                soup.title.get_text(strip=True)
                if soup.title
                else "No Title"
            )

            # Try to extract only the main content
            content = (
                soup.find("main")
                or soup.find("article")
                or soup.find("section")
                or soup.find("body")
            )

            if content is None:
                return {
                    "success": False,
                    "error": "No readable content found."
                }

            text = content.get_text(
                separator="\n",
                strip=True
            )

            # Remove empty lines
            lines = [
                line.strip()
                for line in text.splitlines()
                if line.strip()
            ]

            cleaned_text = "\n".join(lines)

            return {
                "success": True,
                "title": title,
                "content": cleaned_text
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }