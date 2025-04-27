from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import traceback

def submit_donation_survey(num_submissions=1, randomize=False):
    """
    Submit the Donation Survey Google Form multiple times by directly interacting with form elements
    
    Args:
        num_submissions: Number of times to submit the form
        randomize: Whether to randomize the answers
    """
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Uncomment for headless mode
    # chrome_options.add_argument("--headless=new")
    
    # Initialize WebDriver
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return
    
    # Form URL
    FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSclLS6L0_UWKz4maZhKNeVa0HjUoZkg64JHVaHCzXhkYjHCpA/viewform"
    
    # Define options for each question
    options = {
        'awareness': [
            "never heard of it", 
            "somewhat familiar", 
            "very familiar"
        ],
        'motivation': [
            "Religious beliefs", 
            "Personal connection", 
            "Social responsibility", 
            "Tax benefits"
        ],
        'frequency': [
            "Never", 
            "Occasionally (no specific frequented)", 
            "Monthly", 
            "Quarterly", 
            "Annually"
        ],
        'donation_type': [
            "Clothing and shoes", 
            "Food items", 
            "Monetary donations", 
            "Personal care items", 
            "Educational supplies"
        ],
        'donation_method': [
            "Physical visiting", 
            "Online donation", 
            "Through intermediaries"
        ],
        'experience': [
            "Very positive", 
            "Positive", 
            "Neutral", 
            "Negative", 
            "Very negative"
        ],
        'organization_needs': [
            "Organization needs.", 
            "Staff competence", 
            "Donation usage transparency", 
            "Facility conditions", 
            "Number of children served"
        ],
        'challenges': [
            "Lack of information about orphanages", 
            "Inconvenient donation process", 
            "Limited donation options", 
            "Concerns about donation use", 
            "Time constraints"
        ],
        'future_donation': [
            "Yes, definitely", 
            "Probably", 
            "Not sure", 
            "Probably not", 
            "Definitely not"
        ],
        'payment_options': [
            "More payment options", 
            "Improved online platform", 
            "Regular updates on impact", 
            "Easier donation process", 
            "Tax deduction documentation"
        ]
    }
    
    # Default selections (indices in the options arrays)
    default_selections = {
        'awareness': 0,  # "never heard of it"
        'motivation': 0,  # "Religious beliefs"
        'frequency': 1,  # "Occasionally (no specific frequented)"
        'donation_type': 0,  # "Clothing and shoes"
        'donation_method': 0,  # "Physical visiting"
        'experience': 2,  # "Neutral"
        'organization_needs': 0,  # "Organization needs."
        'challenges': 0,  # "Lack of information about orphanages"
        'future_donation': 0,  # "Yes, definitely"
        'payment_options': 0   # "More payment options"
    }
    
    successful_submissions = 0
    
    for i in range(num_submissions):
        try:
            print(f"Starting submission {i+1}/{num_submissions}")
            
            # Navigate to the form
            driver.get(FORM_URL)
            
            # Wait for the form to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "form"))
            )
            
            # Get all questions (each question is in a separate div with role="listitem")
            questions = driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')
            print(f"Found {len(questions)} questions on the form")
            
            # Process each question
            # Process each question
            for question_index, question in enumerate(questions):
                try:
                    # Get the radio button options for this question
                    options_elements = question.find_elements(By.CSS_SELECTOR, 'div[role="radio"]')
                    
                    if options_elements:
                        # Determine which option to select
                        if question_index == 8:  # Check if it's the ninth question (index 8)
                            # Select "Yes, definitely" for the ninth question
                            option_to_select = options_elements[0]  # Assuming "Yes, definitely" is the first option
                        else:
                            if randomize:
                                # Select a random option
                                option_to_select = random.choice(options_elements)
                            else:
                                # Use the default selection based on question index
                                field_name = list(default_selections.keys())[question_index]
                                option_index = default_selections[field_name]
                                
                                # Make sure the option index is valid
                                if option_index >= len(options_elements):
                                    option_index = 0
                                
                                option_to_select = options_elements[option_index]
                        
                        # Scroll to the option
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option_to_select)
                        time.sleep(0.2)
                        
                        # Click the option
                        try:
                            option_to_select.click()
                            print(f"Selected option for question {question_index+1}")
                        except Exception as e:
                            print(f"Direct click failed: {e}")
                            driver.execute_script("arguments[0].click();", option_to_select)
                            print(f"JavaScript click for question {question_index+1}")
                    else:
                        print(f"No options found for question {question_index+1}")
                        
                except Exception as e:
                    print(f"Error processing question {question_index+1}: {e}")


            # Scroll to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            
            # Find and click submit button
            submit_button = None
            try:
                submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div[1]/div/span/span')
                
                if submit_button:
                    print("Found the Submit button")
                    
                    # Scroll to make sure it's visible
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                    time.sleep(0.5)
                    
                    # Click the button
                    try:
                        submit_button.click()
                    except:
                        driver.execute_script("arguments[0].click();", submit_button)
                    
                    print("Clicked submit button")
                    time.sleep(2)
                    
                    # Check if submission was successful
                    current_url = driver.current_url
                    if "formResponse" in current_url or "closedform" in current_url:
                        print(f"Submission {i+1} confirmed successful")
                        successful_submissions += 1
                    else:
                        print(f"Could not confirm submission {i+1}")
                else:
                    print("Could not find submit button")
            except Exception as e:
                print(f"Error with submit button: {e}")
            
            # Wait between submissions
            time.sleep(random.uniform(1, 2))
            
        except Exception as e:
            print(f"Error during submission {i+1}: {e}")
            traceback.print_exc()
    
    # Close the browser
    driver.quit()
    
    print(f"All submissions completed! Successful: {successful_submissions}/{num_submissions}")

if __name__ == "__main__":
    # Set number of submissions and whether to randomize
    submit_donation_survey(num_submissions=25, randomize=True)