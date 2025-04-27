# 🧠 Google Form Response Submitter

> A Python-based Google Form automation script that collects fake responses (for good reasons 😉) — using Selenium and some clever randomization.

---

## 📖 About

This project automates the process of submitting responses to a **Google Form** using Selenium. It can submit multiple entries — randomized or fixed — which is especially useful when:

- You’re building a data analysis app.
- You want to demo data visualization.
- You have a presentation and need to simulate user input.
- You're just too lazy to manually share your form with people (like me 😅).

I built this tool for my **final year college project** where I had to:
1. Collect form responses from many users.
2. Visualize the data using Google Form charts.
But instead of begging people to fill it out... I let Python do the hard work. 🎯

---

## 🔐 Using .env and JSON

To keep things secure and clean, this project uses a `.env` file and a separate JSON file to store sensitive or repetitive data:

### `.env`

Create a `.env` file in the root folder with:

```env
USER_AGENT=YourUserAgentHere
GOOGLE_FORM_BASE_PREFILL_URL=https://docs.google.com/forms/d/e/XXXXXXXXXXXXXXXXXXXXXXXXXX/viewform?usp=pp_url

#### NOTE: 
The USER_AGENT is just any random value you choose for it. 
The GOOGLE_FORM_BASE_PREFILL_URL is the url that you get when you go to the prefill section of your Google form(you only have to take the base part and use, the variable or query parameter seen in the url are added in the json file)
