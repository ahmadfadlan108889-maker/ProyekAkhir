import cv2
import pytesseract
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import pygame

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def camera():
    cap=cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Kamera sedang tidak bisa digunakan")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal membaca frame")
            break
        
        frame_kw = frame.copy()

        cv2.putText(frame_kw, "Tekan 't' untuk Translate | 'q' untuk Keluar", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Test Kamera", frame)

        key =cv2.waitKey(1) & 0xFF
        if key == ord("t"):
            # rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            try:
                deteksi=pytesseract.image_to_string(gray,lang="eng")
                bersih =deteksi.strip()

                if bersih:
                    print(f"hasil = {bersih}")
                else:
                    print("teks tidak terbaca")
                    
            except Exception as e:
                print(f"error:{e}")
            


        elif key == ord("q"):
            print("menutup kamera")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera()