import unittest
import sys
import requests
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

service = Service(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=service, options=options)

website_url = "http://localhost:8000/" # Standard url

class testPageTitle(unittest.TestCase):
    # Check if "Florist Blåklinten" is in the <title> of the page
    def test(self):
        pages = [
            "index.html",
            "index-ua.html",
            "norrkoping.html",
            "norrkoping-ua.html",
            "finspang.html",
            "finspang-ua.html",
        ]
        for page in pages:
            driver.get(website_url + page)
            title = driver.title
            self.assertIn(title, "Florist Blåklinten")

class testFavicon(unittest.TestCase):
    """
        Test if the page has a favicon
    """
    def test(self):
        pages = [
            "index.html",
            "index-ua.html",
            "norrkoping.html",
            "norrkoping-ua.html",
            "finspang.html",
            "finspang-ua.html",
        ]
        for page in pages:
            driver.get(website_url + page)

            logoElement = driver.find_element(By.XPATH, "//link[@type='image/x-icon']")
            self.assertIn('favicon.ico', logoElement.get_attribute("href"))

class testEmptyLinks(unittest.TestCase):
    """
        Test for empty links to prevent forgotten placeholders
    """
    pages = [
            "index.html",
            "index-ua.html",
            "norrkoping.html",
            "norrkoping-ua.html",
            "finspang.html",
            "finspang-ua.html",
        ]

    def test(self):
        
        for page in self.pages:
            driver.get(website_url + page)

            links = driver.find_elements(By.TAG_NAME, "a")

            for link in links:
                self.assertNotEqual(link.get_attribute("href").split("/")[-1], "#")
                self.assertIsNotNone(link.get_attribute("href"))

class testMenuLinks(unittest.TestCase):
    """
        Checks the navigation bar for the correct links
    """
    pages = [
        "finspang.html",
        "finspang-ua.html",
        "norrkoping.html",
        "norrkoping-ua.html",
    ]

    def testText(self):
        for page in self.pages:
            driver.get(website_url + page)
            
            navigation = driver.find_element(By.TAG_NAME, "nav")
            links = navigation.find_elements(By.TAG_NAME, "a")
            page_links = [link.get_attribute("href").split('/')[-1] for link in links]
            page_links = [link.split("html", 1)[1] for link in page_links]
            
            required_links = [
                "#home",
                "#products",
                "#services",
                "#team",
                "#find-us"
            ]

            for link in required_links:
                self.assertIn(link, page_links)
 
    def testFlag(self):
        pages = [
            "index.html",
            "index-ua.html",
            "norrkoping.html",
            "norrkoping-ua.html",
            "finspang.html",
            "finspang-ua.html",
        ]
        for page in pages:
            driver.get(website_url + page)

            navigation = driver.find_element(By.TAG_NAME, "nav")
            links = navigation.find_elements(By.TAG_NAME, "a")
            expected_flag_link = None
            if "ua" in page:
                expected_flag_link = page.replace("-ua", "")
            else:
                expected_flag_link = page.replace(".html", "-ua.html")

            self.assertIn(expected_flag_link, [link.get_attribute("href").split('/')[-1] for link in links])

class testIndex(unittest.TestCase):
    """
        Test check for content on index page
    """
    pages = {
        "index.html": [
            "VÅRA LOKALER",
            "Välj och tryck på en av bilderna nedan",
            "för att komma till en av våra två lokaler",
            "Finspång",
            "De Wijks väg 29",
            "612 30 Finspång",
            "Norrköping",
            "Färjledsvägen 38",
            "961 93 Norrköping",
            "Södra Sunderbyn"
        ],
        "index-ua.html": [
            "НАШІ ПРИМІЩЕННЯ",
            "Виберіть і торкніться одного із зображень нижче",
            "щоб прийти в одне з наших приміщень",
            "Finspång",
            "De Wijks väg 29",
            "612 30 Finspång",
            "Norrköping",
            "Färjledsvägen 38",
            "961 93 Norrköping",
            "Södra Sunderbyn"
        ]
    }
    
    def test(self):
        for page_url, content in self.pages.items():
            driver.get(website_url + page_url)
            page_text = driver.find_element(By.ID, "page-content").text.replace("\n", " ")
            
            for text in content:
                self.assertIn(text, driver.page_source)

class testHeader(unittest.TestCase):
    """
        Check if header content is correct on all pages
    """
    pages = {
        "finspang.html": [
            "Florist Blåklinten",
            "För bokning och beställning ring oss på 0630-555-555",
        ],
        "norrkoping.html": [
            "Florist Blåklinten",
            "För bokning och beställning ring oss på 0640-555-333",
        ],
        "finspang-ua.html": [
            "Florist Blåklinten",
            "Для бронювання та замовлення телефонуйте нам 0630-555-555",
        ],
        "norrkoping-ua.html": [
            "Florist Blåklinten",
            "Для бронювання та замовлення телефонуйте нам 0640-555-333",
        ],
    }
    
    def test(self):
        for page_url, content in self.pages.items():
            driver.get(website_url + page_url)
            headerText = driver.find_element(By.ID, "home").text.replace("\n", " ")
            for text in content:
                self.assertIn(text, headerText)

class testServices(unittest.TestCase):
    """
        test pages for correct services
    """
    services = [
        "Konsultation 30 minuter", "250 kr"
    ]

    services_ukraine = [
        "Консультація 30 хв", "250 kr"
    ]

    pages = {
        "finspang.html": services,
        "norrkoping.html": services,
        "finspang-ua.html": services_ukraine,
        "norrkoping-ua.html": services_ukraine,
    }

    def test(self):
        for page_url, content in self.pages.items():
            driver.get(website_url + page_url)
            serviceText = driver.find_element(By.CLASS_NAME, "serviceCards").text.replace("\n", " ")
            for text in content:
                self.assertIn(text, serviceText)


class testProducts(unittest.TestCase):
    """
        test for products on all pages
    """
    products = [
        "Bröllopsbukett", "1200 kr",
        "Begravningskrans", "800 kr",
        "Höstbukett", "400 kr",
        "Sommarbukett", "200 kr",
        "Rosor 10-pack", "150 kr", 
        "Tulpaner 10-pack", "100 kr", 
    ]
    products_ukraine = [
        "Весільний букет", "1200 kr",
        "Вінок", "800 kr",
        "Осінній букет", "400 kr",
        "Літній букет", "200 kr",
        "Троянди 10 шт", "150 kr", 
        "Тюльпани 10 шт", "100 kr", 
    ]

    pages = {
        "finspang.html": products,
        "norrkoping.html": products,
        "finspang-ua.html": products_ukraine,
        "norrkoping-ua.html": products_ukraine,
    }

    def test(self):

        for page_url, content in self.pages.items():
            driver.get(website_url + page_url)
            productText = driver.find_element(By.CLASS_NAME, "cards").text.replace("\n", " ")
            for text in content:
                self.assertIn(text, productText)

class testOpenHours(unittest.TestCase):
    """
        Test for the opening hours on all pages
    """
    pages = {
            "finspang.html": [
                "Vardagar", "10 - 16",
                "Lördag", "12 - 15",
                "Söndag", "Stängt"
            ],
            "finspang-ua.html": [
                "Пн-Пт", "10 - 16",
                "Субота", "12 - 15",
                "неділя", "Зачинено"
            ],
            "norrkoping.html": [
                "Måndag", "10 - 17",
                "Tisdag", "10 - 16",
                "Onsdag", "10 - 15",
                "Torsdag", "10 - 16",
                "Fredag", "10 - 16",
                "Lördag", "12 - 15",
                "Söndag", "Stängt"
            ],
            "norrkoping-ua.html": [
                "Понеділок", "10 - 17",
                "Вівторок", "10 - 16",
                "Середа", "10 - 15",
                "четвер", "10 - 16",
                "П'ятниця", "10 - 16",
                "Субота", "12 - 15",
                "Неділя", "Зачинено"
            ]
        }

    def test(self):
        for page_url, required_page_content in self.pages.items():
            driver.get(website_url + page_url)
            page_content = driver.find_element(By.CLASS_NAME, "openHours").text.replace("\n", " ")
            for text in required_page_content:
                self.assertIn(text, page_content)
            print("Open hours found") 

class testTeamContent(unittest.TestCase):
    """
        test to check if the team section is correct
    """
    pages = {
        "finspang.html": [
            "Vår personal",
            "Välkommen till oss på Florist Blåklinten! Vi är ett sammansvetsat gäng med olika expertkompetenser som därmed kan hjälpa dig på bästa sätt utifrån dina behov.",
            "Örjan Johansson",
            "Florist",
            "Om du behöver en bukett, oavsett om det är till bröllop, födelsedagsfirande eller något helt annat kan jag hjälpa dig att komponera buketten utifrån dina önskemål.",
            "Anna Pettersson",
            "Hortonom",
            "Jag är utbildad hortonom och kan hjälpa dig eller ditt företag att göra det bästa valet utifrån dina behov och förutsättningar vad det gäller fruktträd, grönsaksodling och prydnadsväxter.",
            "Fredrik Örtqvist",
            "Ägare",
            "Min kärlek till blommor lade grunden till att Florist Blåklinten finns idag och jag hoppas att du som kund kan inspireras i vår butik."
        ],
        "finspang-ua.html": [
            "Наш персонал",
            "Вітаємо у Florist Blåklinten! Наша дружня команда з різними експертними навичками,які можуть допомогти вам найкращим чином.",
            "Örjan Johansson",
            "Флорист",
            "Якщо вам потрібен букет,чи то на весілля,день народження чи щось зовсім інше,я можу вам допомогти скласти букет за вашим бажанням.",
            "Anna Pettersson",
            "Експерт-садiвник",
            "Я кваліфікований садівник і можу допомогти вам або вашій компанії зробити найкращий вибір,фруктових дерев,декоративних рослин або овочевих культур,враховуючи ваші потреби,умови та вподобання.",
            "Fredrik Örtqvist",
            "Власник",
            "Моя любов до квітів заклала основу для існування Florist Blåklinten сьогодні, і я сподіваюся, що ви як клієнт можете надихнутися в нашому магазині."
        ],
        "norrkoping.html": [
            "Vår personal",
            "Välkommen till oss på Florist Blåklinten! Vi är ett sammansvetsat gäng med olika expertkompetenser som därmed kan hjälpa dig på bästa sätt utifrån dina behov.",
            "Johan Olsson",
            "Florist",
            "Jag finner lugnet och inspirationen i mina japanska trädgårdar. Min specialitet är kundsamtalet där vi tillsammans drömmer fram just ert skräddarsydda blomsterkoncept!",
            "Anna Andersson",
            "Florist",
            "När jag gör en bukett utgår jag ifrån en enda blomma. Till denna kärna lägger jag sedan till en blomma i taget tills buketten är lagom stor.",
            "Elin Nygård",
            "Hortonom",
            "Min kolonilott är min bästa lärare. Låt mig få dela med mig av de kunskaper jag förvärvat genom dussintalet säsonger av ömsom färgprakt, ömsom missväxt."
        ],
        "norrkoping-ua.html": [
            "Наш персонал",
            "Вітаємо у Florist Blåklinten! Наша дружня команда з різними експертними навичками,які можуть допомогти вам найкращим чином.",
            "Johan Olsson",
            "Флорист",
            "У своїх японських садах я знаходжу спокій і натхнення. Моя спеціалізація – спілкування з клієнтами, де ми разом створюємо індивідуальну квіткову концепцію!",
            "Anna Andersson",
            "Флорист",
            "Коли я складаю букет, то починаю з квітки. Я додаю по одній квітці в цю серцевину, поки букет не стане потрібного розміру.",
            "Elin Nygård",
            "Експерт-садiвник",
            "Мій сад – мій найкращий учитель. Дозвольте мені поділитися знаннями, які я отримав за десятки сезонів чергування пишних кольорів і уповільненого росту."
        ]
    }
        
    def test(self):
        
        for page_url, required_page_content in self.pages.items():
            driver.get(website_url + page_url)
            page_content = driver.find_element(By.ID, "team").text.replace("\n", " ")
            for content in required_page_content:
                self.assertIn(content, page_content)

class testClosedDays(unittest.TestCase):
    """
        Test that the closed days are correct on all pages
    """
    page_content = [
            "Nyårsdagen",
            "1 Januari",
            "Trettondedag jul",
            "6 Januari",
            "Första maj",
            "1 Maj",
            "Sveriges nationaldag",
            "6 Juni",
            "Julafton",
            "24 December",
            "Juldagen",
            "25 December",
            "Annandag jul",
            "26 December",
            "Nyårsafton",
            "31 December",
        ]
    page_content_ukraine = [
            "Вихідні дні",
            "Новий рік",
            "1 січня",
            "Тринадцятий день Різдва",
            "6 січня",
            "1 травня",
            "1 травня",
            "Національний день Швеції",
            "6 червня",
            "Святвечір",
            "24 грудня",
            "Різдво",
            "25 грудня",
            "День подарунків Різдва",
            "26 грудня",
            "Переддень Нового року",
            "31 грудня",
    ]
    pages = {
        "finspang.html": page_content,
        "finspang-ua.html": page_content_ukraine,
        "norrkoping.html": page_content,
        "norrkoping-ua.html": page_content_ukraine,
    }
    
    def test(self):
      
        for page_url, required_page_content in self.pages.items():
            driver.get(website_url + page_url)
            page_content = driver.find_element(By.ID, "holidays").text.replace("\n", " ")
            for content in required_page_content:
                self.assertIn(content, page_content)


class testCopyright(unittest.TestCase):
    """
        Checks to see of the correct copyright text is displayed on
        all the pages
    """
    pages = [
        "index.html",
        "index-ua.html",
        "finspang.html",
        "finspang-ua.html",
        "norrkoping.html",
        "norrkoping-ua.html",
    ]

    def test(self):
        for url in self.pages:
            driver.get(website_url + url)
            self.assertIn("© 2022 NTI-Gymnasiet", driver.find_element(By.TAG_NAME, "footer").text.replace("\n", " "))
            print("Copyright text found on " + url)
        
class testSocials(unittest.TestCase):
    """
        Checks the href of the social links and checks if the url is correct
    """
    pages = [
        "finspang.html",
        "finspang-ua.html",
        "norrkoping.html",
        "norrkoping-ua.html",
    ]

    def test(self):
        for page in self.pages:

            driver.get(website_url + page)

            # List of social medias
            socials = ["facebook", "instagram", "twitter"]

            # Loop over list
            for social in socials:
                # Check if link and icon is on page
                socialElement =  driver.find_element(By.CLASS_NAME, f"fa-{social}")
                ActionChains(socialElement).move_to_element(socialElement).click()
                socialHref = socialElement.get_attribute("href")

                self.assertEqual(socialHref, f"https://{social}.com/ntiuppsala")

class testMap(unittest.TestCase):
    """
        Checks if the map is on the page with the correct link
    """
    pages = {
        "finspang.html": "google.com/maps/embed?pb=!1m18!1m12!1m3!1d2072.472099087858!2d15.768257516460107!3d58.70529006794066!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46594feedcca3b1d%3A0x6c778af446b70e00!2sDe%20Wijks%20v%C3%A4g%2029%2C%20612%2030%20Finsp%C3%A5ng!5e0!3m2!1sen!2sse!4v1664435816938!5m2!1sen!2sse",
        "finspang-ua.html": "google.com/maps/embed?pb=!1m18!1m12!1m3!1d2072.472099087858!2d15.768257516460107!3d58.70529006794066!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46594feedcca3b1d%3A0x6c778af446b70e00!2sDe%20Wijks%20v%C3%A4g%2029%2C%20612%2030%20Finsp%C3%A5ng!5e0!3m2!1sen!2sse!4v1664435816938!5m2!1sen!2sse",
        "norrkoping.html": "google.com/maps/embed?pb=!1m18!1m12!1m3!1d1682519.779459749!2d19.60985580541526!3d65.6808040934861!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x467f677c34b6b1af%3A0x493f441e2dee92f!2sF%C3%A4rjledsv%C3%A4gen%2038%2C%20961%2093%20S%C3%B6dra%20Sunderbyn!5e0!3m2!1sen!2sse!4v1664893740273!5m2!1sen!2sse",
        "norrkoping-ua.html": "google.com/maps/embed?pb=!1m18!1m12!1m3!1d1682519.779459749!2d19.60985580541526!3d65.6808040934861!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x467f677c34b6b1af%3A0x493f441e2dee92f!2sF%C3%A4rjledsv%C3%A4gen%2038%2C%20961%2093%20S%C3%B6dra%20Sunderbyn!5e0!3m2!1sen!2sse!4v1664893740273!5m2!1sen!2sse"
    }

    def test(self):
        for page_url, map_url in self.pages.items():
            driver.get(website_url + page_url)
            map_element = driver.find_element(By.ID, "mapiframe")

            self.assertTrue(map_element.is_displayed())
            self.assertIn(map_url, map_element.get_attribute("src"))

class testBackground(unittest.TestCase):
    """
        checks background image on all pages
    """
    pages = {
        "norrkoping.html": ["bg-r.jpg", "bgimg2"],
        "norrkoping-ua.html": ["bg-r.jpg", "bgimg2"],
        "finspang.html": ["bg-b.jpg", "bgimg"],
        "finspang-ua.html": ["bg-b.jpg" , "bgimg"],
    }

    def test(self):
        for page_url, page_background_value in self.pages.items():
            driver.get(website_url + page_url)

            background_image_value = driver.find_element(By.CLASS_NAME, page_background_value[1]).value_of_css_property("background-image")
            self.assertIn(page_background_value[0], background_image_value)

class testExistingImages(unittest.TestCase):
    """
        For all the images (img elements) on the page check if its source is not empty
        then try to fetch the image to see if the image exists
    """
    pages = [
        "index.html",
        "index-ua.html",
        "finspang.html",
        "finspang-ua.html",
        "norrkoping.html",
        "norrkoping-ua.html",
    ]

    def test(self):
        for page in self.pages:
            print("Currently testing on {}".format(page))
            driver.get(website_url + page)
            # get all elements with img tag
            image_elements = driver.find_elements(By.TAG_NAME, 'img')

            for image in image_elements:
                image_source = image.get_attribute('src')

                # if the img has a src attribute with a image
                if image.get_attribute('src') is not None:
                    # Assert that the image source is fetchable from the server ( < 400 )
                    print("Checking {}".format(image_source))
                    self.assertLess(requests.get(image_source).status_code, 400)
                else:  # assert False (Just a fail)
                    self.assertTrue(False)
                    continue

class testImageSize(unittest.TestCase):
    """
        Check if the images are not bigger than 500kb
    """

    def test(self):
        images = Path(__file__).resolve().parents[1] / Path('florist-blaklint/assets/images/')
        # Assert check for images larger than 1Mb
        for image in images.glob('**/*.*'):
            # Get the file size property
            image_size = Path(image).stat().st_size
            print("Image path: {} \t image size: {}".format(image, image_size))
            # Assert if the file is greater than 500kb
            self.assertGreater(500_000, image_size)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        website_url = sys.argv.pop()

    unittest.main(verbosity=2)
    
