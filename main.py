import time
import random
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        # Browser setup dengan parameter lebih stabil
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1"
        )
        
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        try:
            print("--- Membuka situs... ---")
            # timeout dinaikkan jadi 90 detik agar tidak mudah crash
            page.goto("https://zonagamearca.blogspot.com/2026/04/prism-match-3d.html?m=1", timeout=90000)
            
            # Tunggu lebih lama agar iklan benar-benar selesai dimuat
            print("--- Menunggu iklan muncul... ---")
            time.sleep(random.uniform(30, 40))
            
            clicked = False
            # Mencari tombol iklan dengan selector yang lebih luas
            for frame in page.frames:
                # Mencari tombol yang kemungkinan besar adalah iklan
                target = frame.locator("button, [aria-label*='Ad'], .adsbygoogle, [id*='ad']")
                
                count = target.count()
                if count > 0:
                    for i in range(count):
                        try:
                            tombol = target.nth(i)
                            if tombol.is_visible():
                                tombol.click(timeout=5000)
                                print(f"✅ Berhasil klik iklan di frame: {frame.name}")
                                clicked = True
                                break
                        except:
                            continue
                if clicked: break
            
            if not clicked:
                print("⚠️ Tidak ada iklan yang terdeteksi.")
            
            time.sleep(10)
            
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            browser.close()
            print("--- Sesi Selesai ---")

if __name__ == "__main__":
    main()
