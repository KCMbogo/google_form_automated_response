from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time
import random
import os
import json

load_dotenv()

# Environment variables 
USER_AGENT = os.getenv("USER_AGENT")
BASE_URL = os.getenv("GOOGLE_FORM_BASE_PREFILL_URL")

def submit_form(num_submissions=1, randomize=False):
    """
    Submit the Google Form multiple times
    
    Args:
        num_submissions: Number of times to submit the form
        randomize: Whether to randomize some of the answers
    """
    # Setup Chrome options
    chrome_options = Options()
    
    # Add user agent to make it look more like a real user
    chrome_options.add_argument(f"--user-agent={USER_AGENT}")

    # Uncomment the line below to run in headless mode (no browser UI)
    # chrome_options.add_argument("--headless")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()  # Maximize window to ensure all elements are visible
    
    # Base URL with prefilled responses
    base_url = BASE_URL

    # load entries
    with open("entry_mapping.json", "r") as f:
        entry = json.load(f)
    
    for i in range(num_submissions):
        # Create the URL for this submission
        if randomize:
            # Options for randomization - you can modify these as needed
            market_options = ["Middlemen", "Local+market", "Cooperatives", "Direct+to+consumers"]
            payment_options = ["Cash", "Mobile+money", "Bank+transfer"]
            location_options = ["Urban", "Rural"]
            frequency_options = ["Daily", "Weekly", "Monthly", "Rarely"]
            purchase_options = ["Local+market", "Supermarkets", "Middlemen", "Farmers"]
            important_options = ["Price", "Quality", "Convenience"]
            yes_no_options = ["Yes", "No", "May+be", "I+will+try"]
            importance_options = ["Very+important", "Somewhat+important", "Not+important"]
            
            url = (f"{base_url}"
                  f"&{entry['market']}={random.choice(market_options)}"
                  f"&{entry['certified']}={random.choice(yes_no_options)}"
                  f"&{entry['quality_check']}={random.choice(yes_no_options)}"
                  f"&{entry['available']}={random.choice(yes_no_options)}"
                  f"&{entry['accessible']}={random.choice(yes_no_options)}"
                  f"&{entry['payment_method']}={random.choice(payment_options)}"
                  f"&{entry['interest_trying']}={random.choice(yes_no_options)}"
                  f"&{entry['location']}={random.choice(location_options)}"
                  f"&{entry['frequency']}={random.choice(frequency_options)}"
                  f"&{entry['purchase_place']}={random.choice(purchase_options)}"
                  f"&{entry['priority']}={random.choice(important_options)}"
                  f"&{entry['recommendation']}={random.choice(yes_no_options)}"
                  f"&{entry['already_used']}={random.choice(yes_no_options)}"
                  f"&{entry['openness']}={random.choice(yes_no_options)}"
                  f"&{entry['importance']}={random.choice(importance_options)}"
                  f"&{entry['feedback']}={random.choice(yes_no_options)}")
        else:
            # Use the provided prefilled URL
            url = (
                f"{base_url}"
                f"&{entry['market']}=Middlemen"
                f"&{entry['certified']}=No"
                f"&{entry['quality_check']}=No"
                f"&{entry['available']}=Yes"
                f"&{entry['accessible']}=Yes"
                f"&{entry['payment_method']}=Cash"
                f"&{entry['interest_trying']}=I+will+try"
                f"&{entry['location']}=Urban"
                f"&{entry['frequency']}=Rarely"
                f"&{entry['purchase_place']}=Local+market"
                f"&{entry['priority']}=Quality"
                f"&{entry['recommendation']}=No"
                f"&{entry['already_used']}=Yes"
                f"&{entry['openness']}=May+be"
                f"&{entry['importance']}=Very+important"
                f"&{entry['feedback']}=Yes"
            )
        
        # Navigate to the form
        driver.get(url)
        
        print(f"Processing submission {i+1}/{num_submissions}")
        
        # Wait for the page to load
        time.sleep(3)
        
        # Try multiple possible selectors for the submit button
        submit_button = None
        selectors = [
            "//div[@role='button' and contains(., 'Submit')]",
            "//span[contains(text(), 'Submit')]",
            "//div[contains(@class, 'freebirdFormviewerViewNavigationSubmitButton')]",
            "//div[contains(@class, 'freebirdFormviewerViewNavigationButtons')]/div[2]",
            "//div[contains(@class, 'freebirdFormviewerViewNavigation')]/div[contains(@class, 'freebirdFormviewerViewNavigationButtonsAndProgress')]/div[2]"
        ]
        
        for selector in selectors:
            try:
                submit_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"Found submit button with selector: {selector}")
                break
            except:
                print(f"Selector not found: {selector}")
                continue
        
        if submit_button is None:
            # If we cannot find the button with specific selectors, try JavaScript execution
            print("Trying to submit form using JavaScript...")
            try:
                # Take a screenshot for debugging
                driver.save_screenshot(f"form_before_submit_{i+1}.png")
                
                # Try to execute JavaScript to submit the form
                driver.execute_script("""
                    var buttons = document.querySelectorAll('div[role="button"]');
                    for (var i = 0; i < buttons.length; i++) {
                        if (buttons[i].textContent.includes('Submit')) {
                            buttons[i].click();
                            return;
                        }
                    }
                    
                    // If no button with text "Submit" is found, try to find the form and submit it
                    var forms = document.getElementsByTagName('form');
                    if (forms.length > 0) {
                        forms[0].submit();
                    }
                """)
                time.sleep(3)  # Wait for the submission to process
            except Exception as e:
                print(f"JavaScript execution failed: {e}")
                
                # Last resort: Try to find any clickable element at the bottom of the page
                try:
                    # Scroll to bottom of page
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
                    
                    # Take another screenshot after scrolling
                    # driver.save_screenshot(f"form_scrolled_bottom_{i+1}.png")
                    
                    # Try to find any button-like element at the bottom
                    elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'freebirdFormviewerViewNavigationButtons')]//div")
                    if elements and len(elements) > 0:
                        elements[-1].click()
                        print("Clicked on the last navigation element")
                except Exception as e:
                    print(f"Final fallback also failed: {e}")
        else:
            # If we found the submit button, click it
            submit_button.click()
        
        # Wait to see if we get to the confirmation page
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Your response has been recorded') or contains(text(), 'Form submitted') or contains(text(), 'Thanks')]"))
            )
            print(f"Submission {i+1}/{num_submissions} confirmed successful")
        except:
            print(f"Could not confirm if submission {i+1}/{num_submissions} was successful")
            # Take a screenshot of the current state
            driver.save_screenshot(f"form_after_submit_attempt_{i+1}.png")
        
        time.sleep(2)  # Pause between submissions
    
    # Close the browser once all submissions are complete
    driver.quit()
    print("All submission attempts completed!")

if __name__ == "__main__":
    # You can change these parameters as needed
    submit_form(num_submissions=25, randomize=True)