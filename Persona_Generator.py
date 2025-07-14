import argparse
import os
import json
import google.generativeai as genai
from Reddit_Scraper import get_user_profile, get_posts_and_comments

def generate_persona(api_key, username, scraped_data):
    """
    Generates a user persona using the Gemini API.

    Args:
        api_key (str): The Gemini API key.
        username (str): The Reddit username.
        scraped_data (list): A list of the user's posts and comments.

    Returns:
        str: The generated user persona.
    """
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    You are a psychological analyst. Based on the following Reddit posts and comments from the user '{username}', create a detailed user persona.
    The persona should include the following sections:
    - Basic info (age, occupation, location, etc.)
    - Personality traits
    - Motivations
    - Behavior & habits
    - Frustrations
    - Goals & needs

    For each characteristic in the user persona, you must cite the specific post or comment that provided the information. For example:
    "**Characteristic:** [The characteristic] (Source: [link to post/comment])"

    Here is the scraped data:
    {json.dumps(scraped_data, indent=2)}
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating persona: {e}"

def main():
    """
    Main function to run the persona generator.
    """
    parser = argparse.ArgumentParser(description="Generate a user persona from a Reddit profile URL.")
    parser.add_argument('url', help="The URL of the Reddit user's profile.")
    args = parser.parse_args()

    api_key = None
    with open('.env', 'r') as f:
        for line in f:
            if line.startswith('GEMINI_API_KEY'):
                api_key = line.split('=')[1].strip()
                break
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file.")
        return

    username = args.url.split('/user/')[1].split('/')[0]
    print(f"Scraping user profile: {args.url}")
    soup = get_user_profile(args.url)
    
    if soup:
        items = get_posts_and_comments(soup)
        
        if not os.path.exists('scraped_data'):
            os.makedirs('scraped_data')
            
        # Save scraped data for caching/review
        scraped_data_path = os.path.join('scraped_data', f'{username}_scraped_data.json')
        with open(scraped_data_path, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)

        if not os.path.exists('personas'):
            os.makedirs('personas')

        print(f"Found {len(items)} items. Generating persona...")
        persona = generate_persona(api_key, username, items)

        output_path = os.path.join('personas', f'{username}_persona.txt')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(persona)

        print(f"Persona for '{username}' saved to {output_path}")

if __name__ == '__main__':
    main()
