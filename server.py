import cv2
import socket
import struct
import numpy as np

# 소켓 설정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 포트 재사용 설정
server_socket.bind(('0.0.0.0', 5000))  # 모든 IP에서의 5000번 포트 수신
server_socket.listen(1)

print("Waiting for a connection...")

# 클라이언트 연결 허용
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address} has been established!")

# 올바른 GStreamer 파이프라인 설정으로 카메라 연결
cap = cv2.VideoCapture("v4l2src device=/dev/video0 ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert ! appsink", cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

try:
    # 비디오 스트림 전송 루프
    while True:
        ret, frame = cap.read()  # 프레임 읽기
        if not ret:
            print("Failed to grab frame")
            break

        # 프레임을 JPEG로 인코딩
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]  # JPEG 품질 설정
        result, buffer = cv2.imencode('.jpg', frame, encode_param)
        if not result:
            print("Failed to encode frame")
            continue

        # 바이트 형식으로 변환하여 전송 준비
        data = np.array(buffer).tobytes()

        # 프레임의 크기를 먼저 전송
        message_size = struct.pack("L", len(data))
        client_socket.sendall(message_size + data)  # 크기와 데이터를 전송

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # 종료 시 정리
    cap.release()
    client_socket.close()
    server_socket.close()
    print("Resources released and sockets closed.")
