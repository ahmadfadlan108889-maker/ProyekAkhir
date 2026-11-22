import requests
from deep_translator import GoogleTranslator


def terjemahkan_aman(teks: str, target_lang: str = "id", source_lang: str = "auto") -> str:
    """Menerjemahkan teks dengan deep_translator, lalu fallback ke API ringan jika kena limit."""
    if not teks or not teks.strip():
        return ""
    try:
        return GoogleTranslator(source=source_lang, target=target_lang).translate(teks)
    except Exception:
        # Jalur cadangan jika GoogleTranslator terkena TooManyRequests
        try:
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                "client": "gtx",
                "sl": source_lang,
                "tl": target_lang,
                "dt": "t",
                "q": teks,
            }
            res = requests.get(url, params=params, timeout=5)
            if res.status_code == 200:
                return "".join([item[0] for item in res.json()[0] if item[0]])
        except Exception:
            pass
    return teks


def lookup_word(word: str, target_lang: str = "id") -> dict:
    kata_bersih = word.strip()

    # 1. Terjemahkan 1 kata ke bahasa tujuan
    translated_word = terjemahkan_aman(kata_bersih, target_lang=target_lang)

    # 2. Cari kata bahasa Inggrisnya untuk mengambil detail kamus
    english_word = (
        kata_bersih.lower()
        if target_lang != "en" and kata_bersih.isascii()
        else terjemahkan_aman(kata_bersih, target_lang="en").lower()
    )

    phonetic = "-"
    part_of_speech = "istilah"
    definitions = []

    # 3. Ambil data fonetik, kelas kata, & definisi dari Free Dictionary API
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{english_word}"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()[0]

            if data.get("phonetic"):
                phonetic = data["phonetic"]
            elif data.get("phonetics"):
                for p in data["phonetics"]:
                    if p.get("text"):
                        phonetic = p["text"]
                        break

            if data.get("meanings"):
                meaning = data["meanings"][0]
                raw_pos = meaning.get("partOfSpeech", "istilah")
                raw_defs = [d["definition"] for d in meaning.get("definitions", [])[:3]]

                if target_lang != "en":
                    # Gabungkan kelas kata + semua definisi jadi 1 permintaan saja agar hemat kuota
                    gabungan = "\n".join([raw_pos] + raw_defs)
                    hasil_terjemahan = terjemahkan_aman(gabungan, target_lang=target_lang, source_lang="en")
                    baris = [b.strip() for b in hasil_terjemahan.split("\n") if b.strip()]
                    if baris:
                        part_of_speech = baris[0]
                        definitions = baris[1:] if len(baris) > 1 else raw_defs
                else:
                    part_of_speech = raw_pos
                    definitions = raw_defs
    except Exception:
        pass

    if not definitions:
        definitions = [f"Terjemahan langsung: {translated_word}"]

    return {
        "original_word": kata_bersih,
        "translated_word": translated_word,
        "target_lang": target_lang,
        "phonetic": phonetic,
        "part_of_speech": part_of_speech,
        "definitions": definitions,
    }


if __name__ == "__main__":
    hasil = lookup_word("comprehensive", target_lang="id")
    print("Kata Asli   :", hasil["original_word"])
    print("Terjemahan  :", hasil["translated_word"])
    print("Fonetik     :", hasil["phonetic"])
    print("Kelas Kata  :", hasil["part_of_speech"])
    print("Definisi    :")
    for i, d in enumerate(hasil["definitions"], start=1):
        print(f"  {i}. {d}")