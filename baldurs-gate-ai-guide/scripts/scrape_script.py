import asyncio
import pprint

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

TAG_TO_MARKDOWN = {
    "h1": "# ",
    "h2": "## ",
    "h3": "### ",
    "h4": "#### ",
    "h5": "##### ",
    "h6": "###### ",
    "p": "",
    "ol": "1. ",
    "li": "- ",
    "em": "*",
    "strong": "**",
    "a": "",
}

def remove_unwanted_tags(html_content, unwanted_tags=["script", "style"]):
    soup = BeautifulSoup(html_content, 'html.parser')

    for tag in unwanted_tags:
        for element in soup.find_all(tag):
            element.decompose()

    return str(soup)


def extract_tags(html_content, tags: list[str]):
    soup = BeautifulSoup(html_content, 'html.parser')
    text_parts = []

    # Track if we're inside an ordered list and its item count
    ordered_list_count = 0

    for idx, element in enumerate(soup.find_all(tags)):  # loop through all tags in order
        prefix = TAG_TO_MARKDOWN.get(element.name, "")

        if element.name == "ol":
            ordered_list_count = 0  # Reset count when a new ordered list starts
            continue  # Don't append the ol tag itself

        # If the tag is an 'li' and is a child of 'ol'
        if element.name == "li" and element.find_parent("ol"):
            ordered_list_count += 1
            prefix = f"{ordered_list_count}. "
        # If the tag is an 'li' and is a child of 'ul'
        elif element.name == "li" and element.find_parent("ul"):
            prefix = "* "

        # If the tag is a link (a tag), only get its text
        if element.name == "a":
            text = element.get_text()
            text_parts.append(text)
        else:
            text_parts.append(f"{prefix}{element.get_text()}")

         # Add a newline before and after certain tags for better formatting
        if element.name in ["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "br"]:
            if idx != 0 and not text_parts[-1] == "\n":  # Don't insert a newline before the first element or if the previous character is already a newline
                text_parts.append("\n")
            text_parts.append("\n")

    return ''.join(text_parts)


def save_to_txt(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


def remove_unessesary_lines(content):
    # Split content into lines
    lines = content.split("\n")

    # Strip whitespace for each line
    stripped_lines = [line.strip() for line in lines]

    # Filter out empty lines
    non_empty_lines = [line for line in stripped_lines if line]

    # Join the cleaned lines with newline separators
    cleaned_content = "\n".join(non_empty_lines)

    return cleaned_content


async def ascrape_playwright(url, tags: list[str] = ["h1", "h2", "h3", "p", "li", "em", "br", "div"]) -> str:
    print("Started scraping...")
    results = ""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            await page.goto(url)

            page_source = await page.content()
            print(page_source[:1000])

            results = extract_tags(remove_unwanted_tags(
                page_source), tags)
            print("Content scraped")
        except Exception as e:
            results = f"Error: {e}"
        await browser.close()
    return results


# TESTING
if __name__ == "__main__":
    urls = [
        "https://baldursgate3.wiki.fextralife.com/Astarion",
        "https://baldursgate3.wiki.fextralife.com/Lae'zel",
        "https://baldursgate3.wiki.fextralife.com/Gale",
        "https://baldursgate3.wiki.fextralife.com/Shadowheart",
        "https://baldursgate3.wiki.fextralife.com/Wyll",
        "https://baldursgate3.wiki.fextralife.com/Karlach",
        "https://baldursgate3.wiki.fextralife.com/The+Dark+Urge"
    ]
    
    names = [
        "astarion",
        "laezel",
        "gale",
        "shadowheart",
        "wyll",
        "karlach",
        "dark_urge"
    ]

    async def scrape_playwright():
        for name, url in zip(names, urls):
            print(f"Scraping {url} for {name}")
            content = await ascrape_playwright(url)
            save_to_txt(content, f"./documents/original_texts/{name}.txt")

    asyncio.run(scrape_playwright())
    
    