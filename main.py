import time
import random
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

def main():
    with sync_playwright() as p:
        # Browser setup
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 375, "height": 812},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1"
        )
        
        page = context.new_page()
        stealth_sync(page)
        
        try:
            print("--- Memulai Sesi ---")
            page.goto("https://zonagamearca.blogspot.com/2026/04/prism-match-3d.html?m=1", wait_until="domcontentloaded")
            
            # Beri waktu loading organik
            time.sleep(random.uniform(10, 15))
            
            # Mencari iframe dan tombol secara rekursif
            clicked = False
            for frame in page.frames:
                try:
                    # Mencari berbagai variasi tombol iklan
                    selector = "button, a[role='button'], .adsbygoogle, [id*='ad']"
                    tombol = frame.locator(selector).first
                    
                    if tombol.is_visible():
                        tombol.scroll_into_view_if_needed()
                        tombol.click(timeout=2000)
                        print(f"Berhasil klik di frame: {frame.name}")
                        clicked = True
                        break
                except:
                    continue
            
            if not clicked:
                print("Tidak menemukan tombol untuk diklik.")
            
            time.sleep(10)
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()
            print("--- Sesi Selesai ---")

if __name__ == "__main__":
    main()
