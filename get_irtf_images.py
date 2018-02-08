from selenium import webdriver

import os
import time

irtf_url = "http://junoirtf.space.swri.edu"
browse_url = irtf_url + "/browse"
queue_url = irtf_url + "/queue"

home_dir = os.path.expanduser("~")
download_dir = os.path.join(home_dir, "irtf")
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.preferences.instantApply",True)
profile.set_preference("browser.download.panel.shown", False)
profile.set_preference("browser.helperApps.neverAsk.openFile", "image/fits,application/fits,application/octet-stream")
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/fits,application/fits,application/octet-stream")
profile.set_preference("browser.download.manager.showWhenStarting",False)
profile.set_preference("browser.download.dir", download_dir)
profile.set_preference("browser.download.folderList", 2)
driver = webdriver.Firefox(profile)

def select_images(url):
    driver.get(url)

    driver.get(url)

    num_pages = driver.find_element_by_css_selector("div.col-lg-12 center ul.pagination li.active").text.split()[2]

    for page in range(int(num_pages)):
        page_url = url + "?page=" + str(page+1) + "&amp;sort=IrtfArchive.DATE_OBS&amp;direction=desc"
        driver.get(page_url)

        buttons = driver.find_elements_by_class_name("addToqueue")

        for button in buttons:
            print("Adding " + button.get_attribute("data-name"))
            button.click()

    return

def download_images(url):
    driver.get(url)

    buttons = driver.find_elements_by_css_selector("td a.btn.btn-info.btn-sm")
    for button in buttons:
        if button.text != "Download":
            continue
        fname = os.path.basename(button.get_attribute("href"))
        print("Downloading " + fname)
        button.click()
        # TODO Add a timeout
        while not os.path.exists(os.path.join(download_dir, fname)):
            time.sleep(1)

if __name__ == "__main__":
    select_images(browse_url)
    download_images(queue_url)