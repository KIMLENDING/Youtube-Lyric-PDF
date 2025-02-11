import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image
from img2pdf import convert
import re

def open_folder():
    global image_folder
    image_folder = filedialog.askdirectory()
    if image_folder:
        folder_label.config(text=image_folder)

def create_pdf():
    if not image_folder:
        messagebox.showerror("오류", "사진 폴더를 선택하세요.")
        return

    try:
        image_files = [
            os.path.join(image_folder, f)
            for f in os.listdir(image_folder)
            if os.path.isfile(os.path.join(image_folder, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]

        # 파일 이름의 숫자 부분 추출하여 정렬
        def sort_key(file_path):
            match = re.search(r"\((\d+)\)", os.path.basename(file_path))
            if match:
                return int(match.group(1))
            return 0  # 숫자가 없는 파일은 0으로 취급

        image_files.sort(key=sort_key)

        # 첫 번째 사진 파일명에서 (1) 제거 후 PDF 파일명 생성
        first_file_name = os.path.basename(image_files[0])
        pdf_file_name = re.sub(r"\(1\)", "", first_file_name).split(".")[0] + ".pdf"

        # PDF 파일 저장 경로 설정 (사진 폴더와 동일)
        pdf_file_path = os.path.join(image_folder, pdf_file_name)

        with open(pdf_file_path, "wb") as f:
            f.write(convert(image_files))
        messagebox.showinfo("완료", f"PDF 파일 '{pdf_file_path}' 생성 완료")
    except Exception as e:
        messagebox.showerror("오류", f"PDF 생성 중 오류 발생: {e}")

# GUI 창 생성
window = tk.Tk()
window.title("사진 이름 순서대로 PDF 변환")

# 폴더 선택 버튼
open_button = tk.Button(window, text="사진 폴더 선택", command=open_folder)
open_button.pack(pady=10)

# 선택된 폴더 표시 레이블
folder_label = tk.Label(window, text="선택된 폴더 없음")
folder_label.pack()

# PDF 생성 버튼
create_button = tk.Button(window, text="PDF 생성", command=create_pdf)
create_button.pack(pady=10)

window.mainloop()