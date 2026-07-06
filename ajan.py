name: Otonom Finans Robotu Gece Calismasi

on:
  schedule:
    # Her gece Türkiye saati ile 03:00'te otomatik uyan ve çalış (UTC 00:00)
    - cron: '0 0 * * *'
  workflow_dispatch: # Elle tetikleme butonu

jobs:
  run-analyst:
    runs-on: ubuntu-latest
    steps:
      - name: Kodu Buluta İndir
        uses: actions/checkout@v3

      - name: Python Kurulumu
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Gerekli Kütüphaneleri Yükle
        run: |
          pip install requests google-generativeai

      - name: Finans Ajanını Tetikle ve Analizi Başlat
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python ajan.py
