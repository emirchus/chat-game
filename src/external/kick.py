from os import system as sys
from time import sleep as wait

try:
    from undetected_chromedriver import Chrome, By
    import undetected_chromedriver as uc
    from selenium_stealth import stealth
    from selenium.common.exceptions import WebDriverException
except ImportError:
    sys("pip install setuptools")
    sys("pip install selenium==4.10.0")
    sys("pip install undetected_chromedriver")
    sys("pip install selenium-stealth")
    from undetected_chromedriver import Chrome, By
    import undetected_chromedriver as uc
    from selenium_stealth import stealth
    from selenium.common.exceptions import WebDriverException



def monitor_chatroom(thread, channel_name, ready_event, message_event, tick, interval=0):

    channel = channel_name
    url = "https://www.kick.com/" + channel + "/chatroom"

    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--enable-images")

    options.add_argument("--headless")

    try:
        with Chrome(use_subprocess=True, options=options) as browser:
            browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """     Object.defineProperty(navigator, 'webdriver', {       get: () => undefined     });     """
            })

            stealth(browser,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True)

            browser.set_window_size(1, 1, browser.window_handles[0])

            browser.get(url)

            sys('cls')

            readMessages = []
            history = []
            firstRun = True

            wait(2.5)

            bot_messages = [
                "Un momento…",
            ]

            if any(msg in browser.page_source for msg in bot_messages):
                print("Esperando a que termine el captcha...")
            while any(msg in browser.page_source for msg in bot_messages):
                wait(0.5)

            sys("cls")

            thread.submit(ready_event, channel, url)
            while True:
                wait(interval)

                page = browser.page_source

                if page.find("Oops, Something went wrong") != -1:
                    print("El navegador parece haber obtenido un error 404, asegúrate de que hayas ingresado tu nombre de canal en channel.txt correctamente. Es sensible a mayúsculas y minúsculas, asegúrate de ingresar solo el nombre de usuario, no la URL completa del canal.")

                messagesFormatted = []

                msgSplit = page.split('data-chat-entry="')
                del msgSplit[0]

                msgs = []
                usrs = []
                usrs_ids = []
                ids = []

                for v in msgSplit:
                    if (v.find("chatroom-history-breaker") != -1):
                        continue

                    ids.append(v.split('"')[0])

                    currentMsgList = v.split('class="chat-entry-content">')
                    del currentMsgList[0]
                    currentMsg = ""

                    for i in currentMsgList:
                        currentMsg += i.split("</span>")[0] + " "
                    currentMsg = currentMsg[0:len(currentMsg)-1]
                    msgs.append(currentMsg)

                    usrs_ids.append(v.split('data-chat-entry-user-id="')[1].split('"')[0])
                    colorCode = v.split('id="'+usrs_ids[len(usrs_ids)-1]+'" style="')[1].split(');">')[0]
                    usrs.append(v.split(colorCode + ');">')[1].split("</span>")[0])

                for i, v in enumerate(msgs):
                    messagesFormatted.append([usrs[i], msgs[i], ids[i], usrs_ids[i]])

                for i, v in enumerate(messagesFormatted):
                    if v[2] not in readMessages:
                        newMsg = v
                        if not firstRun:
                            thread.submit(message_event, newMsg)
                        else:
                            history.append(newMsg)
                        readMessages.append(v[2])
                firstRun = False

                thread.submit(tick)
    except WebDriverException as e:
        print(f"⭕ Error: {e}")

