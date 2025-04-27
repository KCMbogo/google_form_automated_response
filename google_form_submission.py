from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time, logging
import random, os, json

load_dotenv()

# Setup logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("form_automation.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Environment variables 
USER_AGENT = os.getenv("USER_AGENT")
BASE_URL = os.getenv("GOOGLE_FORM_BASE_PREFILL_URL")

def submit_form(num_submissions=1, randomize=False):
    """
    Submit the Google Form multiple times, handling multiple pages/sections
    
    Args:
        num_submissions: Number of times to submit the form
        randomize: Whether to randomize some of the answers
    """
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"--user-agent={USER_AGENT}")

    # Uncomment the line below to run in headless mode (no browser UI)
    chrome_options.add_argument("--headless")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    
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
            yes_no_options = ["Yes", "No", "May+be"]
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
        logger.info(f"======Processing submission {i+1}/{num_submissions}")
        
        # Step 1: Click on the first "Next" button - using the exact XPath you provided
        try:
            first_next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div[1]/div/span/span'))
            )
            print("Found the first Next button")
            first_next_button.click()
            time.sleep(2)  # Wait for page transition
        except Exception as e:
            # print(f"Error clicking first Next button: {e}")
            logger.error(f"Error clicking first next button: {e}")
            # driver.save_screenshot(f"first_page_error_{i+1}.png")
            continue  # Skip to next submission if we can't proceed
        
        # Fill in the second page if needed (if not using prefilled URL for those fields)
        # For now, we're assuming the form is prefilled or has default values
        
        # Step 2: Click on the second "Next" button - using the exact XPath you provided
        try:
            second_next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div[1]/div[2]/span/span'))
            )
            print("Found the second Next button")
            second_next_button.click()
            time.sleep(2)  # Wait for page transition
        except Exception as e:
            # print(f"Error clicking second Next button: {e}")
            logger.exception(f"Error clicking the next button: {e}")
            # driver.save_screenshot(f"second_page_error_{i+1}.png")
            continue  # Skip to next submission if we can't proceed
        
        # Step 3: Click on the final "Submit" button - using the exact XPath you provided
        try:
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div[1]/div[2]/span/span'))
            )
            # print("Found the Submit button")
            logger.info(f"Found the submit button")
            submit_button.click()
            time.sleep(2)  # Wait for submission
        except Exception as e:
            # print(f"Error clicking Submit button: {e}")
            logger.exception(f"Error clicking the submit button: {e}")
            # driver.save_screenshot(f"third_page_error_{i+1}.png")
            continue  # Skip to next submission if we can't proceed
        
        # Check for confirmation page
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Your response has been recorded') or contains(text(), 'Form submitted') or contains(text(), 'Thanks')]"))
            )
            # print(f"Submission {i+1}/{num_submissions} confirmed successful")
            logger.info(f"Submission {i+1}/{num_submissions} confirmed successful")
        except:
            # print(f"Could not confirm if submission {i+1}/{num_submissions} was successful")
            logger.warning(f"Could not confirm if submission {i+1}/{num_submissions} was successful")
            # driver.save_screenshot(f"confirmation_page_error_{i+1}.png")
        
        time.sleep(3)  # Pause between submissions
    
    # Close the browser once all submissions are complete
    driver.quit()
    # print("All submission attempts completed!")
    logger.info("All submission attempts completed!")

def submit_form_with_manual_fill(num_submissions=1, randomize=False):
    """
    Alternative approach that goes to the form and fills in each field manually
    rather than using prefilled URLs
    """
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"--user-agent={USER_AGENT}")
    # chrome_options.add_argument("--headless")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    
    # Base URL without prefills
    base_url = BASE_URL
    
    for i in range(num_submissions):
        # Navigate to the form
        driver.get(base_url)
        # print(f"======Processing submission {i+1}/{num_submissions}")
        logger.info(f"======Processing submission {i+1}/{num_submissions}")
        
        # Wait for the form to load
        time.sleep(3)
        
        # === PAGE 1: Farmers Section ===
        # We need to select options on this page
        try:
            # Find and click radio buttons for each question on the first page
            # For simplicity, we'll randomly select from the available options
            
            # For each question, find all the radio buttons and click one randomly
            questions = driver.find_elements(By.XPATH, "//div[contains(@role, 'radiogroup')]")
            
            for q_idx, question in enumerate(questions):
                options = question.find_elements(By.XPATH, ".//div[@role='radio']")
                if options:
                    # Select a random option or specific one based on preference
                    option_to_select = random.choice(options) if randomize else options[0]
                    driver.execute_script("arguments[0].scrollIntoView();", option_to_select)
                    option_to_select.click()
                    # print(f"Selected an option for question {q_idx+1}")
                    logger.info(f"Selected an option for question {q_idx+1}")
            
            # Click the next button
            first_next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div[1]/div/span/span'))
            )
            first_next_button.click()
            # print("Moved to page 2")
            logger.info("Moved to page 2")
            time.sleep(2)
        except Exception as e:
            print(f"Error on page 1: {e}")
            logger.exception(f"Error on page 1: {e}")
            # driver.save_screenshot(f"page1_error_{i+1}.png")
            continue
        
        # === PAGE 2: Technology Usage & Payments ===
        try:
            # Find and click radio buttons for each question on the second page
            questions = driver.find_elements(By.XPATH, "//div[contains(@role, 'radiogroup')]")
            
            for q_idx, question in enumerate(questions):
                options = question.find_elements(By.XPATH, ".//div[@role='radio']")
                if options:
                    option_to_select = random.choice(options) if randomize else options[0]
                    driver.execute_script("arguments[0].scrollIntoView();", option_to_select)
                    option_to_select.click()
                    print(f"Selected an option for question {q_idx+1} on page 2")
                    logger.info(f"Selected an option for question {q_idx+1} on page 2")

            # Click the next button
            second_next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div[1]/div[2]/span/span'))
            )
            second_next_button.click()
            print("Moved to page 3")
            logger.info("Moved to page 3")
            time.sleep(2)
        except Exception as e:
            # print(f"Error on page 2: {e}")
            logger.exception(f"Error on page 2: {e}")
            # driver.save_screenshot(f"page2_error_{i+1}.png")
            continue
        
        # === PAGE 3: Final Section ===
        try:
            # Find and click radio buttons for each question on the third page
            questions = driver.find_elements(By.XPATH, "//div[contains(@role, 'radiogroup')]")
            
            for q_idx, question in enumerate(questions):
                options = question.find_elements(By.XPATH, ".//div[@role='radio']")
                if options:
                    option_to_select = random.choice(options) if randomize else options[0]
                    driver.execute_script("arguments[0].scrollIntoView();", option_to_select)
                    option_to_select.click()
                    # print(f"Selected an option for question {q_idx+1} on page 3")
                    logger.info(f"Selected an option for question {q_idx+1} on page 3")
            
            # Click the submit button
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div[1]/div[2]/span/span'))
            )
            submit_button.click()
            # print("Submitted the form")
            logger.info("Submitted the form")
            time.sleep(2)
        except Exception as e:
            # print(f"Error on page 3: {e}")
            logger.exception(f"Error on page 3: {e}")
            # driver.save_screenshot(f"page3_error_{i+1}.png")
            continue
        
        # Check for confirmation page
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Your response has been recorded') or contains(text(), 'Form submitted') or contains(text(), 'Thanks')]"))
            )
            # print(f"Submission {i+1}/{num_submissions} confirmed successful")
            logger.info(f"Submission {i+1}/{num_submissions} confirmed successful")
        except:
            # print(f"Could not confirm if submission {i+1}/{num_submissions} was successful")
            logger.exception(f"Could not confirm if submission {i+1}/{num_submissions} was successful")
            # driver.save_screenshot(f"confirmation_error_{i+1}.png")
        
        time.sleep(3)  # Pause between submissions
    
    # Close the browser once all submissions are complete
    driver.quit()
    # print("All submission attempts completed!")
    logger.info("All submission attempts completed!")

if __name__ == "__main__":
    # Choose which function to use

    submit_form(num_submissions=2, randomize=True)  # Uses prefilled URLs
    # submit_form_with_manual_fill(num_submissions=1, randomize=True)  # Fills in the form manually