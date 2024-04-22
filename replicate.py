import time
from typing import Dict, List

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_docker_commands(url: str) -> Dict[str, List[str]]:
    docker_url = f"{url}?input=docker"

    # Set up Selenium
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Fetch the page
        driver.get(docker_url)

        # Wait for the page to load (adjust the time as needed)
        time.sleep(0.1)

        # Get the page source after JavaScript has loaded
        html = driver.page_source

        # Parse the HTML
        soup = BeautifulSoup(html, 'html.parser')

        pre_tags = soup.find_all('pre', class_='code')

        docker_run_command = ""
        is_docker_pre = False
        for pre_tag in pre_tags:
            code_tags = pre_tag.find_all('code', class_='language-shell')

            for code_tag in code_tags:
                command = code_tag.get_text(strip=True)

                if "docker run" in command:
                    docker_run_command = command
                    is_docker_pre = True
                elif is_docker_pre:
                    example_command = command
                    return {
                        'docker_run_command': docker_run_command,
                        'example_command': example_command
                    }
                else:
                    break

    finally:
        # Close the browser
        driver.quit()
        
    return False