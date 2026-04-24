import time
import random
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 375, "height": 812},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1"
        )
        
        page = context.new_page()
        # Script untuk menyembunyikan status bot
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        try:
            print("--- Memulai Sesi ---")
            page.goto("https://zonagamearca.blogspot.com/2026/04/prism-match-3d.html?m=1", wait_until="networkidle")
            
            # Waktu tunggu agar iklan muncul
            time.sleep(random.uniform(15, 20))
            
            clicked = False
            # Mencari iframe/tombol
            for frame in page.frames:
                # Target selector tombol yang umum di iklan
                target = frame.locator("button.gpxLoader-button, ins.adsbygoogle, [aria-label*='Close'], button")
                
                if target.count() > 0:
                    try:
                        target.first.scroll_into_view_if_needed()
                        target.first.click(timeout=3000)
                        print(f"Berhasil klik di frame: {frame.name}")
                        clicked = True
                        break
                    except:
                        continue
            
            if not clicked:
                print("Tidak ada tombol iklan yang terdeteksi.")
            
            time.sleep(10)
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()
            print("--- Sesi Selesai ---")

if __name__ == "__main__":
    main()
