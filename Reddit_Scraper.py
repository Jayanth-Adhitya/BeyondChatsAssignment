import argparse
import requests
from bs4 import BeautifulSoup
import sys
import os
import json

def get_user_profile(url):
    """
    Fetches and parses a Reddit user's profile page using old.reddit.com.

    Args:
        url (str): The URL of the Reddit user's profile.

    Returns:
        BeautifulSoup: A BeautifulSoup object representing the parsed HTML of the profile page.
    """
    try:
        old_url = url.replace("www.reddit.com", "old.reddit.com")
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(old_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        sys.exit(1)


def get_posts_and_comments(soup):
    """
    Extracts posts and comments from a parsed Reddit user profile page.

    Args:
        soup (BeautifulSoup): The parsed HTML of the profile page.

    Returns:
        list: A list of dictionaries, where each dictionary represents a post or comment.
    """
    items = []
    for item in soup.select('.thing'):
        item_type = 'post' if 'link' in item['class'] else 'comment'
        
        if item_type == 'post':
            title_tag = item.select_one('p.title a')
            content = title_tag.text.strip() if title_tag else ''
            link_tag = item.select_one('p.title a')
            link = link_tag['href'] if link_tag else ''
            
            # Check for self post body
            if 'self' in item['class']:
                selftext_div = item.select_one('.usertext-body .md')
                if selftext_div:
                    content += '\n' + selftext_div.text.strip()
        else:  # comment
            content_div = item.select_one('.md')
            content = content_div.text.strip() if content_div else ''
            link_tag = item.select_one('a.bylink')
            link = link_tag['href'] if link_tag else ''

        if content:
            items.append({'type': item_type, 'content': content, 'link': link})
            if len(items) >= 100:
                break
    return items


def main():
    """
    Main function to run the Reddit scraper.
    """
    parser = argparse.ArgumentParser(description="Scrape a Reddit user's posts and comments.")
    parser.add_argument('url', help="The URL of the Reddit user's profile.")
    args = parser.parse_args()

    username = args.url.split('/user/')[1].split('/')[0]
    print(f"Scraping user profile: {args.url}")
    soup = get_user_profile(args.url)
    
    if soup:
        items = get_posts_and_comments(soup)

        if not os.path.exists('scraped_data'):
            os.makedirs('scraped_data')

        output_path = os.path.join('scraped_data', f'{username}_scraped_data.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)

        print(f"Found {len(items)} items and saved them to {output_path}")

if __name__ == '__main__':
    main()
