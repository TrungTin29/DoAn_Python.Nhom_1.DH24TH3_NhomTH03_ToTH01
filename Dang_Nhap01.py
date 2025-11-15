import tkinter as tk
from tkinter import messagebox
import mysql.connector

# ====== KẾT NỐI MYSQL ======
def ket_noi_mysql():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",       
            password="Tinh060705@",  
            database="qlsinhvien"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("❌ Lỗi MySQL", f"Không thể kết nối: {err}")
        return None

# ====== IMPORT CÁC GIAO DIỆN ĐÃ VIẾT ======


from SV01 import mo_giao_dien_sinhvien
from GV01 import  mo_giao_dien_giangvien
from QTV01 import mo_giao_dien_admin

# ====== GIAO DIỆN ĐĂNG NHẬP ======
def dang_nhap():
    role = combo_role.get()
    ma = entry_ma.get().strip()

    if not role or not ma:
        messagebox.showwarning("⚠️ Thiếu thông tin", "Vui lòng chọn vai trò và nhập mã!")
        return

    conn = ket_noi_mysql()
    if conn:
        cursor = conn.cursor()
        if role == "Sinh viên":
            cursor.execute("SELECT maSV FROM sinhvien WHERE maSV=%s", (ma,))
            if cursor.fetchone():
                login.destroy()
                mo_giao_dien_sinhvien(ma)
            else:
                messagebox.showerror("❌ Lỗi", "Mã sinh viên không tồn tại!")
        elif role == "Giảng viên":
            cursor.execute("SELECT maGV FROM giangvien WHERE maGV=%s", (ma,))
            if cursor.fetchone():
                login.destroy()
                mo_giao_dien_giangvien()
            else:
                messagebox.showerror("❌ Lỗi", "Mã giảng viên không tồn tại!")
        elif role == "Admin":
            # Chỉ cần kiểm tra mã admin, ví dụ "admin1"
            cursor.execute("SELECT maAdmin FROM admin WHERE maAdmin=%s", (ma,))
            if cursor.fetchone():
                login.destroy()
                mo_giao_dien_admin()
            else:
                messagebox.showerror("❌ Lỗi", "Mã quản trị viên không tồn tại!")
        conn.close()

# ====== MAIN LOGIN ======
login = tk.Tk()
login.title("🔑 HỆ THỐNG QUẢN LÝ")
login.geometry("400x250")
login.resizable(False, False)

tk.Label(login, text="🔑 Đăng nhập hệ thống", font=("Times New Roman", 16, "bold")).pack(pady=15)

tk.Label(login, text="Chọn vai trò:").pack(pady=5)
combo_role = tk.ttk.Combobox(login, values=["Sinh viên", "Giảng viên", "Admin"], state="readonly")
combo_role.pack()

tk.Label(login, text="Nhập mã:").pack(pady=5)
entry_ma = tk.Entry(login, width=30)
entry_ma.pack()

btn_login = tk.Button(login, text="Đăng nhập", bg="#2980b9", fg="white", width=20, command=dang_nhap)
btn_login.pack(pady=20)

login.mainloop()
