import tkinter as tk
from tkinter import ttk, messagebox
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

# ====== GIAO DIỆN SINH VIÊN ======
def mo_giao_dien_sinhvien(maSV):
    window = tk.Tk()
    window.title("🎓 Thông tin Sinh viên")
    window.geometry("700x500")
    window.resizable(False, False)

    lbl_title = tk.Label(window, text="🎓 HỆ THỐNG SINH VIÊN", font=("Times New Roman", 18, "bold"), fg="green")
    lbl_title.pack(pady=15)

    # Thông tin cá nhân
    frame_info = tk.LabelFrame(window, text="📋 Thông tin cá nhân", font=("Times New Roman", 11, "bold"), padx=10, pady=10)
    frame_info.pack(fill="x", padx=15, pady=5)

    tk.Label(frame_info, text="Mã SV:", width=15, anchor="e").grid(row=0, column=0, padx=5, pady=5)
    entry_maSV = tk.Entry(frame_info, width=35)
    entry_maSV.grid(row=0, column=1, padx=5, pady=5)
    entry_maSV.insert(0, maSV)
    entry_maSV.config(state="readonly")

    tk.Label(frame_info, text="Họ tên:", width=15, anchor="e").grid(row=1, column=0, padx=5, pady=5)
    entry_hoTen = tk.Entry(frame_info, width=35)
    entry_hoTen.grid(row=1, column=1, padx=5, pady=5)
    entry_hoTen.config(state="readonly")

    tk.Label(frame_info, text="Ngày sinh:", width=15, anchor="e").grid(row=2, column=0, padx=5, pady=5)
    entry_ngaySinh = tk.Entry(frame_info, width=35)
    entry_ngaySinh.grid(row=2, column=1, padx=5, pady=5)
    entry_ngaySinh.config(state="readonly")

    tk.Label(frame_info, text="Giới tính:", width=15, anchor="e").grid(row=3, column=0, padx=5, pady=5)
    entry_gioiTinh = tk.Entry(frame_info, width=35)
    entry_gioiTinh.grid(row=3, column=1, padx=5, pady=5)
    entry_gioiTinh.config(state="readonly")

    tk.Label(frame_info, text="Địa chỉ:", width=15, anchor="e").grid(row=4, column=0, padx=5, pady=5)
    entry_diaChi = tk.Entry(frame_info, width=35)
    entry_diaChi.grid(row=4, column=1, padx=5, pady=5)
    entry_diaChi.config(state="readonly")

    # Bảng điểm
    lbl_diem = tk.Label(window, text="📚 Điểm các môn học", font=("Times New Roman", 13, "bold"))
    lbl_diem.pack(pady=5)

    frame_table = tk.Frame(window)
    frame_table.pack(fill="both", expand=True, padx=15, pady=5)

    cols = ("Mã MH", "Tên môn học", "Điểm")
    tree = ttk.Treeview(frame_table, columns=cols, show="headings", height=10)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=200, anchor="center")
    tree.pack(fill="both", expand=True)

    # Load dữ liệu
    def tai_du_lieu():
        conn = ket_noi_mysql()
        if conn:
            cursor = conn.cursor()
            # Thông tin cá nhân
            cursor.execute("SELECT hoTen, ngaySinh, gioiTinh, diaChi FROM sinhvien WHERE maSV=%s", (maSV,))
            info = cursor.fetchone()
            if info:
                entry_hoTen.config(state="normal")
                entry_hoTen.delete(0, tk.END)
                entry_hoTen.insert(0, info[0])
                entry_hoTen.config(state="readonly")

                entry_ngaySinh.config(state="normal")
                entry_ngaySinh.delete(0, tk.END)
                entry_ngaySinh.insert(0, info[1])
                entry_ngaySinh.config(state="readonly")

                entry_gioiTinh.config(state="normal")
                entry_gioiTinh.delete(0, tk.END)
                entry_gioiTinh.insert(0, info[2])
                entry_gioiTinh.config(state="readonly")

                entry_diaChi.config(state="normal")
                entry_diaChi.delete(0, tk.END)
                entry_diaChi.insert(0, info[3])
                entry_diaChi.config(state="readonly")

            # Điểm các môn học
            for i in tree.get_children():
                tree.delete(i)
            cursor.execute("""
                SELECT m.maMH, m.tenMH, k.diem
                FROM ketqua k
                JOIN monhoc m ON k.maMH = m.maMH
                WHERE k.maSV=%s
            """, (maSV,))
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
            conn.close()

    tai_du_lieu()
    window.mainloop()

# ====== CHẠY GIAO DIỆN SINH VIÊN ======
if __name__ == "__main__":
    mo_giao_dien_sinhvien("SV001")  # 👈 thay mã SV để thử
