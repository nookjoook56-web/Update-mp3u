import requests

# Güncellenmesini istediğiniz linkleri buraya ekleyin
def create_m3u():
    channels = [
        {"name": "Kanal 1", "url": "http://ornek.com/yayin1.m3u8"},
        {"name": "Kanal 2", "url": "http://ornek.com/yayin2.m3u8"}
    ]
    
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for channel in channels:
            f.write(f"#EXTINF:-1,{channel['name']}\n")
            f.write(f"{channel['url']}\n")
    print("Playlist.m3u başarıyla oluşturuldu!")

if __name__ == "__main__":
    create_m3u()
