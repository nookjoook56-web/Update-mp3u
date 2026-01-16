import requests
import base64

# --- AYARLARINIZ ---
TOKEN = ""
REPO = "nookjoook56-web/Update-mp3u"
DOSYA_YOLU = "playlist.m3u"
IPTV_URL = "http://happytv.ooguy.com/get.php?username=erdem10&password=Cw1360cv&type=m3u_plus"
# --------------------

def iptv_islem():
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    print(">> Liste indiriliyor...")
    try:
        response = requests.get(IPTV_URL, headers=headers, timeout=30)
        lines = response.text.split('\n')
        
        print(">> Filtre uygulanıyor (Sadece Bein, S Sport ve Ulusal)...")
        temiz_icerik = "#EXTM3U\n"
        sayac = 0
        
        # Sadece bu kelimeleri içeren kanallar alınacak
        # Büyük/küçük harf duyarlılığı için hepsi büyük harf kontrol edilecek
        hedef_kanallar = [
            "BEIN SPORTS", "BEIN SPORT", "S SPORT", "TRT SPOR", "A SPOR", "TIVIBU SPOR", # SPOR
            "TRT 1", "ATV", "SHOW TV", "STAR TV", "KANAL D", "TV8", "NOW TV", "FOX", "KANAL 7", # ULUSAL
            "HABERTURK", "NTV", "CNN TURK", "A HABER", "ULKE TV" # HABER/DİĞER
        ]

        for i in range(len(lines)):
            if lines[i].startswith('#EXTINF:'):
                bilgi = lines[i].upper()
                link = lines[i+1].strip() if (i + 1) < len(lines) else ""
                
                if link.startswith('http'):
                    # Sadece hedef listesindeki kanalları ve sadece Türkiye gruplarını filtrele
                    eslesme_var_mi = any(x in bilgi for x in hedef_kanallar)
                    
                    # Yabancı Bein kanallarını elemek için 'FRANCE' veya 'ARAB' gibi kelimeleri dışla
                    yabanci_mi = any(y in bilgi for y in ["FRANCE", "ARAB", "USA", "UK", "ESPANA"])

                    if eslesme_var_mi and not yabanci_mi:
                        temiz_icerik += lines[i] + "\n" + link + "\n"
                        sayac += 1
        
        print(f"✅ Filtreleme bitti: {sayac} kanal seçildi.")
        
        if "ghp_" in TOKEN:
            github_url = f"https://api.github.com/repos/{REPO}/contents/{DOSYA_YOLU}"
            gh_headers = {"Authorization": f"token {TOKEN.strip()}", "Accept": "application/vnd.github.v3+json"}
            
            # SHA al
            res = requests.get(github_url, headers=gh_headers)
            sha = res.json().get('sha') if res.status_code == 200 else None
            
            # Yükle
            encoded = base64.b64encode(temiz_icerik.encode("utf-8")).decode("utf-8")
            payload = {"message": "Sadece Bein ve Ulusal Kanallar", "content": encoded}
            if sha: payload["sha"] = sha
            
            put_res = requests.put(github_url, json=payload, headers=gh_headers)
            if put_res.status_code in [200, 201]:
                print(f"🚀 BAŞARILI! {sayac} kanal GitHub'a gönderildi.")
            else:
                print("❌ GitHub Hatası:", put_res.json().get('message'))
        else:
            print("⚠️ Token girilmediği için GitHub'a yüklenmedi.")

    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    iptv_islem()
