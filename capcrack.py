import binascii
import hashlib
import os
import sys
import threading
from time import sleep

# Hàm hiển thị hiệu ứng hệ thống đang chạy
def loading_animation():
  while True:
    for i in range(4):
      sys.stdout.write("\b-")
      sys.stdout.flush()
      sleep(0.1)
    for i in range(4):
      sys.stdout.write("\b\\")
      sys.stdout.flush()
      sleep(0.1)
    for i in range(4):
      sys.stdout.write("\b|")
      sys.stdout.flush()
      sleep(0.1)
    for i in range(4):
      sys.stdout.write("\b/")
      sys.stdout.flush()
      sleep(0.1)

# Hàm kiểm tra tính tương thích của file cap
def check_cap_format(cap_file):
  with open(cap_file, "rb") as f:
    data = f.read()
  if data[:8] == b"\x00\x00\x00\x00\x00\x00\x00\x00":
    return "old"
  else:
    return "new"

# Hàm dò mật khẩu theo chuẩn cũ
def crack_cap_old(cap_file, dict_file):
  found = False
  total_words = 0
  with open(dict_file, "r") as f_dict:
    for word in f_dict:
      total_words += 1
  with open(cap_file, "rb") as f_cap:
    cap_data = f_cap.read()
  with open(dict_file, "r") as f_dict:
    for word in f_dict:
      word = word.strip()
      hash_word = hashlib.sha1(word.encode()).digest()
      if hash_word == cap_data[:20]:
        print(f"Mật khẩu được tìm thấy: {word}")
        # Ghi mật khẩu vào file
        try:
          with open(f"./pass/{os.path.basename(cap_file)}.txt", "w") as f:
            f.write(word)
        except Exception as e:
          print(f"Lỗi khi ghi file: {e}")
        found = True
        break
  if not found:
    print("Mật khẩu không được tìm thấy!")

# Hàm dò mật khẩu theo chuẩn mới
def crack_cap_new(cap_file, dict_file):
  found = False
  total_words = 0
  with open(dict_file, "r") as f_dict:
    for word in f_dict:
      total_words += 1
  with open(cap_file, "rb") as f_cap:
    cap_data = f_cap.read()
  with open(dict_file, "r") as f_dict:
    for word in f_dict:
      word = word.strip()
      hash_word = hashlib.pbkdf2_hmac("sha512", word.encode(), b"\x00" * 12, 100000, 64)
      if hash_word == cap_data[12:]:
        print(f"Mật khẩu được tìm thấy: {word}")
        # Ghi mật khẩu vào file
        try:
          with open(f"./pass/{os.path.basename(cap_file)}.txt", "w") as f:
            f.write(word)
        except Exception as e:
          print(f"Lỗi khi ghi file: {e}")
        found = True
        break
  if not found:
    print("Mật khẩu không được tìm thấy!")

# Hàm chính
def main():
  # Kiểm tra số lượng tham số
  if len(sys.argv) != 3:
    print("Cách sử dụng: capcrack.py <dict> <cap>")
    print("  <dict>: File từ điển để dò mật khẩu")
    print("  <cap>: File cap chứa mật khẩu")
    return

  # Lấy thông tin từ tham số
  dict_file = sys.argv[1]
  cap_file = sys.argv[2]

  # Kiểm tra tính tương thích của file cap
  cap_format = check_cap_format(cap_file)

  # Bắt đầu dò mật khẩu
  if cap_format == "old":
    print("Đang dò mật khẩu theo chuẩn cũ...")
    crack_cap_old(cap_file, dict_file)
  elif cap_format == "new":
    print("Đang dò mật khẩu theo chuẩn mới...")
    crack_cap_new(cap_file, dict_file)
  else:
    print("File cap không hợp lệ!")
    return

# Khởi chạy chương trình
if __name__ == "__main__":
  # Hiển thị hiệu ứng hệ thống đang chạy
  loading_thread = threading.Thread(target=loading_animation)
  loading_thread.start()

  # Chạy hàm chính
  main()

  # Dừng hiệu ứng hệ thống đang chạy
  loading_thread.join()

