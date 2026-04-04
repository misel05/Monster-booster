import asyncio
from playwright.async_api import async_playwright
import random

async def eternal_revenue_engine():
    # URL TARGET LU
    url = "https://gamesfreeonlinehub.blogspot.com/2026/01/merge-royal-play-free-merge-game-online.html?m=1"
    
    async with async_playwright() as p:
        # Firefox lebih 'tahan banting' buat lari 24 jam
        browser = await p.firefox.launch(headless=True)
        counter = 1
        
        while True:
            # Rotasi User Agent biar trafik kelihatan alami dari berbagai HP
            ua = random.choice([
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
            ])
            
            context = await browser.new_context(viewport={'width': 400, 'height': 850}, user_agent=ua)
            page = await context.new_page()
            
            try:
                # 1. Buka Halaman
                await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                # Tunggu loading iklan (Ritme Sedang: 10-12 detik)
                await asyncio.sleep(random.randint(10, 12)) 

                # 2. SCAN & CLICK IKLAN (Cari Learn More / Simbol Iklan)
                ad_keywords = ["Learn More", "Open", "Visit", "Install", "Daftar", "Shop Now", "Selengkapnya"]
                ad_found = False
                
                for frame in page.frames:
                    if "gamepix.com" in frame.url: continue 
                    for text in ad_keywords:
                        try:
                            target = frame.get_by_text(text, exact=False)
                            if await target.count() > 0:
                                await target.first.click(timeout=3000)
                                print(f"💰 Sesi {counter} | Iklan '{text}' DIHAJAR!")
                                ad_found = True
                                break
                        except: continue
                    if ad_found: break

                # 3. BACKUP: KLIK AREA BANNER BAWAH (Berdasarkan foto lu)
                if not ad_found:
                    await page.mouse.click(200, 710) # Area Banner
                    await page.mouse.click(365, 640) # Area Tombol X/Close
                    print(f"🖱️ Sesi {counter} | Klik Banner & Simbol Iklan!")

                # 4. KLIK PLAY (Traffic Player)
                await page.mouse.click(200, 400)

                # 5. NGETEM VALIDASI (Ritme Pas: 30-40 detik)
                # Ini rahasia revenue gede tanpa dianggap bot cepat
                tunggu = random.randint(30, 40)
                print(f"⏳ Stay {tunggu} detik...")
                await asyncio.sleep(tunggu)
                
                print(f"✅ Sesi {counter} Selesai.")
                
            except:
                pass # Jika error (misal koneksi), langsung skip ke sesi berikutnya
            
            await context.close()
            counter += 1
            
            # Biar gak kena limit durasi GitHub (6 jam), kita batasi per run 400 sesi.
            # Pas run ini beres, cron di main.yml bakal otomatis jalanin lagi.
            if counter > 400: break 

        await browser.close()

if __name__ == "__main__":
    asyncio.run(eternal_revenue_engine())
