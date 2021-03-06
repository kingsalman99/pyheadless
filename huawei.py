import argparse
import asyncio
import time

from pyppeteer import launch


async def main(username, password):
    browser = await launch(ignorehttpserrrors=True, headless=True,
                           args=['--disable-infobars', '--no-sandbox', '--start-maximized'])
    page = await browser.newPage()
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    try:
        for i in range(3):
            try:
                await page.setViewport({'width': 1200, 'height': 768})
                await page.goto('https://devcloud.huaweicloud.com/bonususer/mobile/home', {'waitUntil': 'load'})

                await page.waitForSelector('#personalAccountInputId .tiny-input-text', {'visible': True})

                await page.evaluate(
                    '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
                await page.type('#personalAccountInputId .tiny-input-text', username)
                await page.type('#personalPasswordInputId .tiny-input-text', password)
                await page.click('#btn_submit')
                await asyncio.sleep(5)

                page_url = page.url
                print(page_url)
                await page.waitForSelector('.mobile-loading-btn-body', {'visible': True})
                await asyncio.sleep(3)

                sign_txt = str(await page.Jeval('.mobile-loading-btn-body', 'el => el.textContent')).strip()
                credit = str(await page.Jeval('.count', 'el => el.textContent')).strip()
                print(sign_txt, credit)

                if sign_txt.find('今日已签到') == -1:
                    await page.click('.mobile-loading-btn-body')
                    await asyncio.sleep(3)
                    new_credit = str(await page.Jeval('.count', 'el => el.textContent')).strip()
                    print(new_credit)

                await asyncio.sleep(1)
                break
            except Exception as e:
                print(e)
                await page.close()
    finally:
        await page.close()
        await browser.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()
    params = vars(args)

    asyncio.get_event_loop().run_until_complete(main(params.get('username'), params.get('password')))
