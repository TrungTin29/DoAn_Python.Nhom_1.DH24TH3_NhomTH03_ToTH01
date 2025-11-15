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

# ====== GIAO DIỆN GIẢNG VIÊN ======
def mo_giao_dien_giangvien():
    window = tk.Tk()
    window.title("👩‍🏫 Giao diện Giảng viên")
    window.geometry("800x600")
    window.resizable(False, False)

    lbl_title = tk.Label(window, text="👩‍🏫 HỆ THỐNG GIẢNG VIÊN", font=("Times New Roman", 18, "bold"), fg="darkblue")
    lbl_title.pack(pady=10)

    frame = tk.Frame(window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Chọn môn học
    tk.Label(frame, text="📘 Chọn môn học:", font=("Times New Roman", 11, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    combo_mh = ttk.Combobox(frame, width=40, state="readonly")
    combo_mh.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Treeview danh sách sinh viên môn học
    cols = ("Mã SV", "Họ tên", "Điểm")
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=15)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=250, anchor="center")
    tree.grid(row=1, column=0, columnspan=2, pady=10)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=1, column=2, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    # Load danh sách môn học
    def tai_ds_monhoc():
        conn = ket_noi_mysql()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tenMH FROM monhoc")
            ds = [r[0] for r in cursor.fetchall()]
            combo_mh["values"] = ds
            if ds:
                combo_mh.current(0)
                tai_ds_sv()
            conn.close()

    # Load danh sách sinh viên theo môn học
    def tai_ds_sv(event=None):
        for i in tree.get_children():
            tree.delete(i)
        tenMH = combo_mh.get()
        if not tenMH:
            return
        conn = ket_noi_mysql()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT sv.maSV, sv.hoTen, kq.diem
                FROM ketqua kq
                JOIN sinhvien sv ON kq.maSV = sv.maSV
                JOIN monhoc mh ON kq.maMH = mh.maMH
                WHERE mh.tenMH=%s
            """, (tenMH,))
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
            conn.close()

    combo_mh.bind("<<ComboboxSelected>>", tai_ds_sv)
    tai_ds_monhoc()

    # Khung cập nhật điểm
    frame_edit = tk.LabelFrame(frame, text="✏️ Cập nhật điểm", font=("Times New Roman", 11, "bold"), padx=10, pady=10)
    frame_edit.grid(row=2, column=0, columnspan=3, pady=10, sticky="w")

    tk.Label(frame_edit, text="Mã SV:").grid(row=0, column=0, padx=5, pady=5)
    entry_masv = tk.Entry(frame_edit, width=20)
    entry_masv.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_edit, text="Điểm:").grid(row=0, column=2, padx=5, pady=5)
    entry_diem = tk.Entry(frame_edit, width=10)
    entry_diem.grid(row=0, column=3, padx=5, pady=5)

    # Chọn dòng trong treeview
    def chon_sv(event):
        selected = tree.selection()
        if selected:
            data = tree.item(selected[0], "values")
            entry_masv.delete(0, tk.END)
            entry_masv.insert(0, data[0])
            entry_diem.delete(0, tk.END)
            entry_diem.insert(0, data[2] if data[2] is not None else "")

    tree.bind("<<TreeviewSelect>>", chon_sv)

    # Cập nhật điểm
    def cap_nhat_diem():
        maSV = entry_masv.get().strip()
        diem = entry_diem.get().strip()
        tenMH = combo_mh.get()
        if not maSV or diem == "":
            messagebox.showerror("Lỗi", "Nhập mã sinh viên và điểm.")
            return
        conn = ket_noi_mysql()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT maMH FROM monhoc WHERE tenMH=%s", (tenMH,))
                maMH = cursor.fetchone()[0]
                cursor.execute("UPDATE ketqua SET diem=%s WHERE maSV=%s AND maMH=%s", (diem, maSV, maMH))
                conn.commit()
                messagebox.showinfo("✅ Thành công", f"Đã cập nhật điểm {diem} cho {maSV}.")
                tai_ds_sv()
            except mysql.connector.Error as err:
                messagebox.showerror("❌ Lỗi MySQL", f"{err}")
            finally:
                conn.close()

    tk.Button(frame_edit, text="✏️ Cập nhật điểm", bg="#2980b9", fg="white", width=15, command=cap_nhat_diem).grid(row=1, column=1, pady=5)

    window.mainloop()

# ====== CHẠY GIAO DIỆN GIẢNG VIÊN ======
if __name__ == "__main__":
    mo_giao_dien_giangvien()
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

# ====== GIAO DIỆN GIẢNG VIÊN ======
def mo_giao_dien_giangvien():
    window = tk.Tk()
    window.title("👩‍🏫 Giao diện Giảng viên")
    window.geometry("850x650")
    window.resizable(False, False)

    lbl_title = tk.Label(window, text="👩‍🏫 HỆ THỐNG GIẢNG VIÊN", font=("Times New Roman", 18, "bold"), fg="darkblue")
    lbl_title.pack(pady=10)

    frame = tk.Frame(window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # ===== Chọn môn học =====
    tk.Label(frame, text="📘 Chọn môn học:", font=("Times New Roman", 11, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    combo_mh = ttk.Combobox(frame, width=40, state="readonly")
    combo_mh.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # ===== Tìm kiếm sinh viên =====
    tk.Label(frame, text="🔍 Tìm theo Mã SV:", font=("Times New Roman", 11, "bold")).grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_timSV = tk.Entry(frame, width=20)
    entry_timSV.grid(row=0, column=3, padx=5, pady=5)

    def tim_sv():
        tai_ds_sv(tim=True)

    tk.Button(frame, text="Tìm", bg="#27ae60", fg="white", width=10, command=tim_sv).grid(row=0, column=4, padx=5, pady=5)

    # ===== Treeview danh sách sinh viên =====
    cols = ("Mã SV", "Họ tên", "Điểm")
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=20)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=250, anchor="center")
    tree.grid(row=1, column=0, columnspan=5, pady=10)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=1, column=5, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    # ===== Load danh sách môn học =====
    def tai_ds_monhoc():
        conn = ket_noi_mysql()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tenMH FROM monhoc")
            ds = [r[0] for r in cursor.fetchall()]
            combo_mh["values"] = ds
            if ds:
                combo_mh.current(0)
                tai_ds_sv()
            conn.close()

    # ===== Load danh sách sinh viên =====
    def tai_ds_sv(event=None, tim=False):
        for i in tree.get_children():
            tree.delete(i)
        tenMH = combo_mh.get()
        masv = entry_timSV.get().strip()
        if not tenMH:
            return
        conn = ket_noi_mysql()
        if conn:
            cursor = conn.cursor()
            if tim and masv:
                # Tìm theo Mã SV
                cursor.execute("""
                    SELECT sv.maSV, sv.hoTen, kq.diem
                    FROM ketqua kq
                    JOIN sinhvien sv ON TRIM(kq.maSV) = TRIM(sv.maSV)
                    JOIN monhoc mh ON kq.maMH = mh.maMH
                    WHERE LOWER(TRIM(sv.maSV)) = LOWER(%s) AND LOWER(TRIM(mh.tenMH)) = LOWER(%s)
                """, (masv, tenMH))
            else:
                # Hiển thị tất cả sinh viên môn học
                cursor.execute("""
                    SELECT sv.maSV, sv.hoTen, kq.diem
                    FROM ketqua kq
                    JOIN sinhvien sv ON kq.maSV = sv.maSV
                    JOIN monhoc mh ON kq.maMH = mh.maMH
                    WHERE mh.tenMH = %s
                """, (tenMH,))
            rows = cursor.fetchall()
            if not rows and tim and masv:
                messagebox.showinfo("❌ Không tìm thấy", f"Không tìm thấy sinh viên {masv} trong môn {tenMH}.")
            for row in rows:
                tree.insert("", "end", values=row)
            conn.close()

    combo_mh.bind("<<ComboboxSelected>>", tai_ds_sv)
    tai_ds_monhoc()

    # ===== Khung cập nhật điểm =====
    frame_edit = tk.LabelFrame(frame, text="✏️ Cập nhật điểm", font=("Times New Roman", 11, "bold"), padx=10, pady=10)
    frame_edit.grid(row=2, column=0, columnspan=5, pady=10, sticky="w")

    tk.Label(frame_edit, text="Mã SV:").grid(row=0, column=0, padx=5, pady=5)
    entry_masv = tk.Entry(frame_edit, width=20)
    entry_masv.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_edit, text="Điểm:").grid(row=0, column=2, padx=5, pady=5)
    entry_diem = tk.Entry(frame_edit, width=10)
    entry_diem.grid(row=0, column=3, padx=5, pady=5)

    # Chọn dòng trong treeview
    def chon_sv(event):
        selected = tree.selection()
        if selected:
            data = tree.item(selected[0], "values")
            entry_masv.delete(0, tk.END)
            entry_masv.insert(0, data[0])
            entry_diem.delete(0, tk.END)
            entry_diem.insert(0, data[2] if data[2] is not None else "")

    tree.bind("<<TreeviewSelect>>", chon_sv)

    # Cập nhật điểm
    def cap_nhat_diem():
        maSV = entry_masv.get().strip()
        diem = entry_diem.get().strip()
        tenMH = combo_mh.get()
        if not maSV or diem == "":
            messagebox.showerror("Lỗi", "Nhập mã sinh viên và điểm.")
            return
        conn = ket_noi_mysql()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT maMH FROM monhoc WHERE tenMH=%s", (tenMH,))
                result = cursor.fetchone()
                if not result:
                    messagebox.showerror("❌ Lỗi", f"Không tìm thấy môn học {tenMH}.")
                    return
                maMH = result[0]
                cursor.execute("""
                    UPDATE ketqua
                    SET diem=%s
                    WHERE TRIM(maSV) = %s AND maMH=%s
                """, (diem, maSV, maMH))
                conn.commit()
                messagebox.showinfo("✅ Thành công", f"Đã cập nhật điểm {diem} cho {maSV}.")
                tai_ds_sv()
            except mysql.connector.Error as err:
                messagebox.showerror("❌ Lỗi MySQL", f"{err}")
            finally:
                conn.close()

    tk.Button(frame_edit, text="✏️ Cập nhật điểm", bg="#2980b9", fg="white", width=15, command=cap_nhat_diem).grid(row=1, column=1, pady=5)

    window.mainloop()

# ====== CHẠY GIAO DIỆN GIẢNG VIÊN ======
if __name__ == "__main__":
    mo_giao_dien_giangvien()
