import requests
import base64
import re

# --- AYARLARINIZ ---
# Buraya yeni aldığın ghp_ ile başlayan tokeni yapıştır
GITHUB_TOKEN = "" 
REPO = "nookjoook56-web/Update-mp3u"
DOSYA_YOLU = "playlist.m3u"

# --- IPTV KAYNAĞI ---
# Bu linki kimseyle paylaşmaman güvenliğin için önemlidir.
IPTV_URL = "BURAYA_IPTV_LINKINI_YAPIŞTIR"

def kanal_temizle(ad):
    """Kanal isimlerini VIVO X tarzında sadeleştirir."""
    ad = ad.replace("TR:", "").replace("HD", "").replace("HQ", "").replace("tr:", "").strip()
    return ad

def iptv_to_github():
    headers = {'User-Agent': 'Mozilla/5.0'}
    print(">> İşlem başlatıldı...")
    
    try:
        # Listeyi çek
        res = requests.get(IPTV_URL, headers=headers, timeout=20)
        res.raise_for_status()
        lines = res.text.split('\n')
        
        m3u_output = "#EXTM3U\n"
        sayac = 0
        
        # Filtreleme Listeleri
        sporlar = ["BEIN", "S SPORT", "TIVIBU SPOR", "TRT SPOR", "A SPOR"]
        ulusallar = ["TRT 1", "ATV", "SHOW", "STAR", "KANAL D", "TV8", "NOW", "FOX", "KANAL 7"]

        for i in range(len(lines)):
            if lines[i].startswith('#EXTINF:'):
                bilgi = lines[i].upper()
                url = lines[i+1].strip() if (i+1) < len(lines) else ""
                
                if url.startswith('http'):
                    is_spor = any(s in bilgi for s in sporlar)
                    is_ulusal = any(u in bilgi for u in ulusallar)
                    
                    if is_spor or is_ulusal:
                        original_name = lines[i].split(',')[-1]
                        clean_name = kanal_temizle(original_name)
                        grup = "Spor Kanalları" if is_spor else "Ulusal Kanallar"
                        
                        logo_match = re.search('tvg-logo="(.*?)"', lines[i])
                        logo = logo_match.group(1) if logo_match else ""
                        
                        m3u_output += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{grup}",{clean_name}\n{url}\n'
                        sayac += 1

        print(f">> {sayac} adet profesyonel kanal hazırlandı. GitHub'a yükleniyor...")
        
        # GitHub API
        api_url = f"https://api.github.com/repos/{REPO}/contents/{DOSYA_YOLU}"
        gh_headers = {
            "Authorization": f"token {GITHUB_TOKEN.strip()}", 
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Eski dosyanın SHA bilgisini al
        sha_res = requests.get(api_url, headers=gh_headers)
        sha = sha_res.json().get('sha') if sha_res.status_code == 200 else None
        
        # Base64 dönüşümü ve yükleme
        content_b64 = base64.b64encode(m3u_output.encode("utf-8")).decode("utf-8")
        payload = {"message": "VIVOX Liste Güncelleme", "content": content_b64}
        if sha: payload["sha"] = sha
        
        put_res = requests.put(api_url, json=payload, headers=gh_headers)
        if put_res.status_code in [200, 201]:
            print("🚀 BAŞARILI: Listeniz GitHub üzerinde güncellendi!")
        else:
            print(f"❌ HATA: GitHub yüklemesi başarısız. (Kod: {put_res.status_code})")

    except Exception as e:
        print(f"❌ HATA: {str(e)}")

if __name__ == "__main__":
    iptv_to_github()
