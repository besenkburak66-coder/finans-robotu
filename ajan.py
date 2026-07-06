import os
import json
import requests
import time

# Şifreyi GitHub kasasından güvenli bir şekilde çekiyoruz
API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

def seeking_alpha_toplu_veri_cek(hisse_listesi):
    toplu_piyasa_verisi = {}
    
    print(f"=== SİSTEM: İnternetten Toplu Veri Çekme İşlemi Başladı ===")
    for hisse in hisse_listesi:
        print(f"-> {hisse} verileri Seeking Alpha köprüsünden çekiliyor...")
        url = f"https://those-engineering.pro/api/v1/finance/seekingalpha/summary?ticker={hisse.upper()}"
        
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                veri = response.json()
                toplu_piyasa_verisi[hisse] = {
                    "Son Başlıklar": [art.get("title") for art in veri.get("articles", [])[:2]],
                    "Duyarlılık": veri.get("sentiment", "Nötr"),
                    "Gross Margin Tahmini": veri.get("estimated_gross_margin", "Veri Yok"),
                    "CapEx Durumu": veri.get("capex_trend", "Stabil Yatırım")
                }
            else:
                toplu_piyasa_verisi[hisse] = f"Ham bilanço simüle ediliyor (Alternatif Kaynak)."
        except Exception as e:
            toplu_piyasa_verisi[hisse] = f"Bağlantı hatası: {str(e)}"
        
        time.sleep(1)
        
    return toplu_piyasa_verisi

def otonom_piyasa_tarayici(hisse_listesi):
    canli_piyasa_havuzu = seeking_alpha_toplu_veri_cek(hisse_listesi)
    
    mesaj = (
        "Sen kıdemli bir küresel makro ve finans analiz ajanısın. Sana Seeking Alpha köprülerimiz üzerinden "
        "gelen şu toplu şirket verilerini incele. Her bir şirket için Gross Margin, CapEx yatırımları ve piyasa "
        "duyarlılığına bakarak çok kısa, vurucu ve profesyonel birer Türkçe özet çıkart. "
        "Raporun sonunda bu şirketleri finansal durumlarına göre en iyiden en risklisine doğru sırala.\n\n"
        f"Gelen Toplu Canlı Veri:\n{json.dumps(canli_piyasa_havuzu, ensure_ascii=False)}"
    )
    
    payload = {"contents": [{"parts": [{"text": mesaj}]}]}
    headers = {'Content-Type': 'application/json'}
    
    print(f"\n-> SİSTEM: Yapay Zeka tüm listeyi otonom olarak analiz ediyor...")
    res = requests.post(GEMINI_URL, headers=headers, data=json.dumps(payload))
    
    if res.status_code == 200:
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Gemini Hatası: {res.status_code} - {res.text}"

if __name__ == "__main__":
    izleme_listem = ["NVDA", "MU", "IREN", "DELL", "AAOI", "LITE", "GLW"]
    
    print(f"==================================================")
    print(f"   OTONOM TOPLU PİYASA TARAYICI BAŞLATILDI        ")
    print(f"==================================================")
    
    toplu_rapor = otonom_piyasa_tarayici(izleme_listem)
    
    print("\n==================================================")
    print("           PİYASA TAKİP VE ANALİZ RAPORU          ")
    print("==================================================")
    print(toplu_rapor)
