# Import các thư viện cần thiết
import random
import time

# Các biến lưu trữ trạng thái của các máy chủ tham gia
server1_state = None
server2_state = None

# Các hàm để mô phỏng việc thực hiện yêu cầu chuẩn bị và xác nhận giao dịch
def prepare(server_id):
    # Mô phỏng việc thực hiện chuẩn bị giao dịch
    print(f"Server {server_id} is preparing for the transaction...")
    time.sleep(random.uniform(0.5, 1.5))
    # Random trạng thái thành công hoặc lỗi
    return random.choice([True, False])

def commit(server_id):
    # Mô phỏng việc xác nhận giao dịch
    print(f"Server {server_id} is committing the transaction...")
    time.sleep(random.uniform(0.5, 1.5))
    # Random trạng thái thành công hoặc lỗi
    return random.choice([True, False])

# Hàm để thực hiện Two-phase commit protocol (2PC) payment
def two_phase_commit_payment():
    # Yêu cầu chuẩn bị giao dịch từ các máy chủ tham gia
    server1_state = prepare(1)
    server2_state = prepare(2)

    # Nếu tất cả các máy chủ đều chuẩn bị thành công, tiếp tục giao dịch
    if server1_state and server2_state:
        # Yêu cầu xác nhận giao dịch từ các máy chủ tham gia
        server1_commit = commit(1)
        server2_commit = commit(2)

        # Nếu tất cả các máy chủ đều xác nhận giao dịch, hoàn tất giao dịch
        if server1_commit and server2_commit:
            print("Transaction completed successfully.")
        # Nếu một trong các máy chủ không xác nhận giao dịch, hủy giao dịch
        else:
            print("Transaction failed. Rolling back...")
    # Nếu một trong các máy chủ không chuẩn bị thành công, hủy giao dịch
    else:
        print("Transaction failed. Rolling back...")

# Chạy hàm thực hiện Two-phase commit protocol (2PC) payment
two_phase_commit_payment()
