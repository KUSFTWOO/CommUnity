#!/usr/bin/env python
import asyncio
from playwright.async_api import async_playwright

async def test_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            # 로그인 페이지 접속
            await page.goto("http://localhost:8000/accounts/login/", wait_until="networkidle")
            print("Login page loaded successfully")

            # 이메일 입력
            await page.fill('input[name="email"]', 'admin@example.com')

            # 비밀번호 입력
            await page.fill('input[name="password"]', 'admin123')

            # 로그인 버튼 클릭
            await page.click('button[type="submit"]')

            # 리다이렉트 대기
            await page.wait_for_load_state('networkidle')

            # 현재 URL 확인
            current_url = page.url
            print(f"Current URL after login: {current_url}")

            # 페이지 제목 확인
            title = await page.title()
            print(f"Page title: {title}")

            # 성공 메시지 확인
            page_content = await page.content()
            if 'Administrator' in page_content or 'home' in current_url:
                print("Login successful!")
            else:
                print("Login may have failed")

            await page.screenshot(path="login_result.png")
            print("Screenshot saved: login_result.png")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

asyncio.run(test_login())
