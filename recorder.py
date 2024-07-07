import cv2
import numpy as np
import pyautogui
import threading
import time
import collections

# Constants
SECOND = 15
TIME = SECOND/60 # 0.5 minutes
FRAME_RATE = 20.0
BUFFER_SIZE = TIME * 60 * FRAME_RATE  # 5 minutes buffer
SCREEN_SIZE = pyautogui.size()

# Circular buffer to store frames
buffer = collections.deque(maxlen=int(BUFFER_SIZE))

# Control flag
recording = True

def capture_screen():
    while recording:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        buffer.append(frame)
        time.sleep(1 / FRAME_RATE)
        print(f"Buffer size: {len(buffer)}")

def save_recording():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_filename = f"last_5_minutes_{timestamp}.mp4"
    
    out = cv2.VideoWriter(
        output_filename,
        cv2.VideoWriter_fourcc(*'mp4v'),
        FRAME_RATE,
        (SCREEN_SIZE.width, SCREEN_SIZE.height)
    )

    while buffer:
        frame = buffer.popleft()
        out.write(frame)
    
    out.release()
    print(f"Saved recording to {output_filename}")

def main():
    global recording
    # Start screen capture thread
    capture_thread = threading.Thread(target=capture_screen)
    capture_thread.start()
    
    # Wait for user input to stop recording
    input(f"Press Enter to stop recording and save the last {TIME} minutes...")
    recording = False
    capture_thread.join()
    
    # Save the recording
    save_recording()

if __name__ == "__main__":
    main()

