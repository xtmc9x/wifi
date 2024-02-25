import binascii
import os

def cap_to_new_format(cap_file, new_file):
  """
  Chuyển đổi file *.cap sang định dạng mới phù hợp với mode 22000 của Hashcat

  Args:
    cap_file: Đường dẫn đến file *.cap
    new_file: Đường dẫn đến file mới
  """

  with open(cap_file, "rb") as f_cap:
    cap_data = f_cap.read()

  # Bỏ qua 8 byte đầu tiên

  cap_data = cap_data[8:]

  # Tạo header cho file mới

  header = b"$2y$12$" + binascii.unhexlify("0000000000000000")

  # Ghép header với dữ liệu

  new_data = header + cap_data

  # Ghi dữ liệu mới sang file

  with open(new_file, "wb") as f_new:
    f_new.write(new_data)

def main():
  """
  Chuyển đổi tất cả file *.cap trong thư mục ./handshakes sang định dạng mới và lưu vào thư mục ./handshakes-new
  """

  # Tạo thư mục ./handshakes-new nếu chưa tồn tại

  if not os.path.exists("./handshakes-new"):
    os.makedirs("./handshakes-new")

  # Duyệt qua tất cả file *.cap trong thư mục ./handshakes

  for filename in os.listdir("./handshakes"):
    if filename.endswith(".cap"):
      cap_file = os.path.join("./handshakes", filename)
      new_file = os.path.join("./handshakes-new", filename)

      # Chuyển đổi file

      cap_to_new_format(cap_file, new_file)

if __name__ == "__main__":
  main()

  print("Chuyển đổi file *.cap sang định dạng mới thành công!")
