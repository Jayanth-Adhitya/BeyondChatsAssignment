# Reddit User Persona Generator

## Overview

This project is a Python script that generates a detailed user persona based on a Reddit user's posts and comments. It scrapes the user's profile, analyzes the content using the Gemini API, and creates a comprehensive persona that includes basic information, personality traits, motivations, and more.

## Features

-   **Web Scraping:** Scrapes a Reddit user's profile for their latest posts and comments using `requests` and `BeautifulSoup`.
-   **AI-Powered Persona Generation:** Utilizes the Gemini API to analyze the scraped text and generate a detailed user persona.
-   **Cited Characteristics:** For each characteristic in the persona, the script provides a citation to the original post or comment.
-   **Organized Output:** Saves the scraped data and the generated persona in separate, organized folders.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/reddit-persona-generator.git
    cd reddit-persona-generator
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your Gemini API key:**
    Create a `.env` file in the root of the project directory and add your Gemini API key:
    ```
    GEMINI_API_KEY=YOUR_API_KEY
    ```

## Usage

Run the `Persona_Generator.py` script with the URL of the Reddit user's profile you want to analyze:

```bash
python Persona_Generator.py https://www.reddit.com/user/some_username/
```

## Output

The script will generate two files:

1.  **Scraped Data:** A JSON file containing the scraped posts and comments, saved in the `scraped_data` folder.
    -   `scraped_data/some_username_scraped_data.json`
2.  **User Persona:** A text file containing the generated user persona, saved in the `personas` folder.
    -   `personas/some_username_persona.txt`

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
