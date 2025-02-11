import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os


def download_video():
    url = url_entry.get()
    output_dir = output_entry.get()

    if not output_dir:  # 저장 경로가 선택되지 않았으면 파일 선택 창 열기
        output_dir = filedialog.askdirectory()
        if not output_dir:  # 사용자가 파일 선택을 취소한 경우
            return
   # URL 처리: "&" 이후 부분 제거
    url = url.split('&')[0]

    command = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "-o", f"{output_dir}/%(title)s.%(ext)s",
        url
    ]

    process = subprocess.Popen(command)  # yt-dlp 실행

    def check_download():
        if process.poll() is not None:  # 다운로드 완료
            messagebox.showinfo("다운로드 완료", "다운로드가 완료되었습니다.")
            url_entry.delete(0, tk.END)  # URL 창 비우기
            # output_entry.delete(0, tk.END)  # 저장 경로 창 비우기
        else:
            window.after(1000, check_download)  # 1초 뒤에 다시 확인

    window.after(1000, check_download)  # 1초 뒤에 다운로드 완료 확인 시작


window = tk.Tk()
window.title("유튜브 다운로더")

url_label = tk.Label(window, text="URL:")
url_label.grid(row=0, column=0)

url_entry = tk.Entry(window)
url_entry.grid(row=0, column=1)

output_label = tk.Label(window, text="저장 경로:")
output_label.grid(row=1, column=0)

output_entry = tk.Entry(window)
output_entry.grid(row=1, column=1)

output_button = tk.Button(window, text="파일 선택", command=lambda: show_last_path_part(filedialog.askdirectory()))  # 파일 선택 버튼
output_button.grid(row=1, column=2)

download_button = tk.Button(window, text="다운로드", command=download_video)
download_button.grid(row=2, column=1)

def show_last_path_part(path):
    if path:
        last_part = os.path.basename(path)  # 마지막 부분 추출
        output_entry.delete(0, tk.END)
        output_entry.insert(0, last_part)


window.mainloop()