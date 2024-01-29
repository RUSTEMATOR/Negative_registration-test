from playwright.sync_api import Playwright, sync_playwright, Page
import pytest
import allure
from negative_mapping import link_mapping, translations_mapping

class TestData():
    from playwright.sync_api import Page
# Define the list of test data
    test_data = [
        "example#kbc.pp.ua",
        "example@kbc.pp-ua",
        "example@kbc.pp_ua",
        "example@kbc.pp..ua",
        "",  # Empty value
        "exämple@kbc.pp.ua",
        "example@softs_wis..com",
        "example.softswis.com",
        "example@@softswis.com",
        "example@soft swis.com",
        "example@softswis..com",
        "example@"
    ]

    links = [
    "https://lp.kingbillycasino.com/50-free-spins-ch/"
]

@allure.title("Negative emails_check")
# Define the test function
@pytest.mark.parametrize("email, link", [(e, l) for e in TestData.test_data 
                                         for l in TestData.links])
def test_negative_registration(playwright: Playwright, email: str, link: str) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
     # Determine locale based on the provided link
    current_locale = link_mapping.get(link, "default_locale")

    # Determine translations based on the locale
    current_translations = translations_mapping.get(current_locale, {}).get("translations", {})
    
    #--------------------------------------------------------------
    page.goto(link)
    allure.attach(page.screenshot(), name="Step 1: Page is reached", attachment_type=allure.attachment_type.PNG)
    
    print(current_translations)
    
    page.get_by_role("button", name="JETZT BEKOMMEN").click()
    allure.attach(page.screenshot(), name="Step 2: Form is opened", attachment_type=allure.attachment_type.PNG)
    
    page.get_by_placeholder(current_translations["email_placeholder"]).click()
    page.get_by_placeholder(current_translations["email_placeholder"]).fill(email)
    allure.attach(page.screenshot(), name="Step 3: Email is filled", attachment_type=allure.attachment_type.PNG)

    page.get_by_placeholder(current_translations["password_placeholder"]).click()
    page.get_by_placeholder(current_translations["password_placeholder"]).fill("193786Az()")
    allure.attach(page.screenshot(), name="Step 4: Password is filled", attachment_type=allure.attachment_type.PNG)
    
    terms_and_conditions_text = current_translations["terms_and_conditions"]
    page.get_by_role("main").locator("div").filter(has_text=terms_and_conditions_text).locator("label").nth(2).click()
    
    create_account_button = page.get_by_role("button", name=current_translations["create_account_button"])
    if create_account_button.is_enabled():
        create_account_button.click()
        allure.attach(page.screenshot(), name="Final result", attachment_type=allure.attachment_type.PNG)
    else:
        # Handle the situation when the button is not enabled
        allure.attach(page.screenshot(), name="Button Not Enabled", attachment_type=allure.attachment_type.PNG)
        print("Button is not enabled, skipping click action.")

        print("Test is concluding...")
        
    
    
    if page.get_by_role("link", name="Logo").is_visible():
        pass
     
    else:
        # Registration succeeded, test failed for this input
        assert False, f"Registration succeeded for email: {email}"

    # -----------------------------------------------------------
    context.tracing.stop(path="trace.zip")
    context.close()
    browser.close()
    print("Test concluded successfully.")

