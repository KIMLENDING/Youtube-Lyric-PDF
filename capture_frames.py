import cv2

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def detect_scene_changes(video_path, threshold=10):
    """
    이전 프레임과 현재 프레임의 모양이 다르면 캡쳐합니다.

    Args:
        video_path (str): 동영상 파일 경로
        threshold (float): 변화 감지 임계값 (0.0 ~ 1.0)

    Returns:
        list: 캡쳐된 프레임 이미지 목록
    """

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("동영상 파일을 열 수 없습니다.")

    # 동영상 파일 경로에서 폴더 경로 추출
    folder_path = os.path.dirname(video_path)

    # 동영상 파일 이름 (확장자 제외)
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # 캡쳐된 이미지를 저장할 폴더 경로 생성
    output_dir = r"C:\temp\test_save"

    # 폴더가 없으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    prev_frame = None
    captured_frames = []
    frame_count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 총 프레임 수

    no_capture_count = 0  # 캡쳐되지 않은 프레임 수를 세는 변수

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 프레임을 회색조로 변환

        if prev_frame is not None:
            diff = cv2.absdiff(prev_frame, gray)  # 이전 프레임과 현재 프레임의 차이 계산
        
            _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)  # 임계값 설정
            count = cv2.countNonZero(thresh)  # 변화가 있는 픽셀 수
            print(count, frame_count)

            if count > threshold:  # 임계값보다 크고 2프레임 연속 캡쳐되지 않았을 때
                if captured_frames and frame_count - captured_frames[-1][1] == 1:
                    # 이전 캡쳐된 프레임과 차이가 1인 경우 이전 프레임 제거
                    os.remove(os.path.join(output_dir, f"video_name_{captured_frames[-1][1]}.jpg"))
                    captured_frames.pop()
                captured_frames.append((frame, frame_count))
                cv2.imwrite(os.path.join(output_dir, f"video_name_{frame_count}.jpg"), frame)
                no_capture_count = 0  # 캡쳐 후 초기화
            else:
                no_capture_count += 1  # 캡쳐되지 않은 프레임 수 증가

        prev_frame = gray  # 현재 프레임을 이전 프레임으로 저장

        # 진행률 업데이트
        progress_bar["value"] = (frame_count / total_frames) * 100
        window.update()  # GUI 업데이트

    cap.release()
    return [frame for frame, _ in captured_frames]

def open_video_file():
    global video_path  # 전역 변수 video_path 사용
    video_path = filedialog.askopenfilename(title="동영상 파일 선택", filetypes=[("동영상 파일", "*.mp4;*.avi;*.mov")])  # 동영상 파일 선택 창 열기
    if video_path:  # 파일 선택 시
        video_path_label.config(text=video_path)  # 선택한 파일 경로 표시

def start_detection():
    if video_path:  # 동영상 파일이 선택되었을 때
        try:
            captured_frames = detect_scene_changes(video_path)
            messagebox.showinfo("완료", f"총 {len(captured_frames)}개의 프레임이 캡쳐되었습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"오류가 발생했습니다: {e}")
    else:
        messagebox.showwarning("경고", "동영상 파일을 선택해주세요.")

# GUI 생성
window = tk.Tk()
window.title("장면 변화 감지 프로그램")

# 동영상 파일 선택 버튼
open_button = tk.Button(window, text="동영상 파일 선택", command=open_video_file)
open_button.pack(pady=10)

# 동영상 파일 경로 표시 레이블
video_path_label = tk.Label(window, text="선택된 동영상 파일: 없음")
video_path_label.pack()

# 진행률 표시줄
progress_bar = ttk.Progressbar(window, mode="determinate")  # ttk 프로그레스바 사용
progress_bar.pack(pady=10)

# 시작 버튼
start_button = tk.Button(window, text="시작", command=start_detection)
start_button.pack(pady=10)

window.mainloop()