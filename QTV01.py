import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
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

# ====== GIAO DIỆN ADMIN ======
def mo_giao_dien_admin():
    window = tk.Tk()
    window.title("🛠️ Giao diện Quản trị viên")
    window.geometry("1100x650")
    window.resizable(False, False)

    lbl_title = tk.Label(window, text="🛠️ HỆ THỐNG QUẢN TRỊ VIÊN", font=("Times New Roman", 18, "bold"), fg="darkred")
    lbl_title.pack(pady=10)

    tab_control = ttk.Notebook(window)
    tab_sinhvien = ttk.Frame(tab_control)
    tab_monhoc = ttk.Frame(tab_control)
    tab_ketqua = ttk.Frame(tab_control)

    tab_control.add(tab_sinhvien, text="👤 Quản lý Sinh viên")
    tab_control.add(tab_monhoc, text="📘 Quản lý Môn học")
    tab_control.add(tab_ketqua, text="📊 Quản lý Kết quả / Đăng ký môn học")
    tab_control.pack(expand=1, fill="both")

    # ====== TAB SINH VIÊN ======
    frame_sv = tk.Frame(tab_sinhvien)
    frame_sv.pack(fill="both", expand=True, padx=10, pady=10)

    cols_sv = ("Mã SV", "Họ tên", "Ngày sinh", "Giới tính", "Địa chỉ", "Mã Lớp")
    tree_sv = ttk.Treeview(frame_sv, columns=cols_sv, show="headings", height=15)
    for col in cols_sv:
        tree_sv.heading(col, text=col)
        tree_sv.column(col, width=140, anchor="center")
    tree_sv.pack(side="left", fill="both", expand=True)

    scrollbar_sv = ttk.Scrollbar(frame_sv, orient="vertical", command=tree_sv.yview)
    scrollbar_sv.pack(side="left", fill="y")
    tree_sv.configure(yscrollcommand=scrollbar_sv.set)

    frame_edit_sv = tk.LabelFrame(tab_sinhvien, text="✏️ Thêm/Sửa Sinh viên", font=("Times New Roman", 11, "bold"), padx=10, pady=10)
    frame_edit_sv.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_edit_sv, text="Mã SV:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_maSV = tk.Entry(frame_edit_sv, width=15)
    entry_maSV.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_edit_sv, text="Họ tên:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    entry_hoTen = tk.Entry(frame_edit_sv, width=25)
    entry_hoTen.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(frame_edit_sv, text="Ngày sinh:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
    entry_ngaySinh = DateEntry(frame_edit_sv, width=15, date_pattern="yyyy-MM-dd")
    entry_ngaySinh.grid(row=0, column=5, padx=5, pady=5)

    tk.Label(frame_edit_sv, text="Giới tính:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    gioiTinhVar = tk.StringVar(value="Nam")
    tk.Radiobutton(frame_edit_sv, text="Nam", variable=gioiTinhVar, value="Nam").grid(row=1, column=1)
    tk.Radiobutton(frame_edit_sv, text="Nữ", variable=gioiTinhVar, value="Nữ").grid(row=1, column=2)

    tk.Label(frame_edit_sv, text="Địa chỉ:").grid(row=1, column=3, padx=5, pady=5, sticky="e")
    entry_diaChi = tk.Entry(frame_edit_sv, width=25)
    entry_diaChi.grid(row=1, column=4, padx=5, pady=5)

    tk.Label(frame_edit_sv, text="Mã Lớp:").grid(row=1, column=5, padx=5, pady=5, sticky="e")
    entry_maLop = tk.Entry(frame_edit_sv, width=15)
    entry_maLop.grid(row=1, column=6, padx=5, pady=5)

    # ====== Chọn dòng trong treeview ======
    def chon_sv(event):
        selected = tree_sv.selection()
        if selected:
            data = tree_sv.item(selected[0], "values")
            entry_maSV.delete(0, tk.END); entry_maSV.insert(0, data[0])
            entry_hoTen.delete(0, tk.END); entry_hoTen.insert(0, data[1])
            entry_ngaySinh.set_date(data[2])
            gioiTinhVar.set(data[3])
            entry_diaChi.delete(0, tk.END); entry_diaChi.insert(0, data[4])
            entry_maLop.delete(0, tk.END); entry_maLop.insert(0, data[5])

    tree_sv.bind("<<TreeviewSelect>>", chon_sv)

    # ====== Load danh sách sinh viên ======
    def tai_ds_sv():
        for i in tree_sv.get_children():
            tree_sv.delete(i)
        conn = ket_noi_mysql()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT maSV, hoTen, ngaySinh, gioiTinh, diaChi, maLop FROM sinhvien")
            for row in cursor.fetchall():
                tree_sv.insert("", "end", values=row)
            conn.close()

    tai_ds_sv()

    # ====== Thêm/Sửa/Xóa sinh viên ======
    def them_sv():
        maSV = entry_maSV.get().strip()
        hoTen = entry_hoTen.get().strip()
        ngaySinh = entry_ngaySinh.get_date().strftime("%Y-%m-%d")
        gioiTinh = gioiTinhVar.get()
        diaChi = entry_diaChi.get().strip()
        maLop = entry_maLop.get().strip()
        if not maSV or not hoTen:
            messagebox.showerror("Lỗi", "Mã SV và Họ tên không được để trống.")
            return
        conn = ket_noi_mysql()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO sinhvien(maSV, hoTen, ngaySinh, gioiTinh, diaChi, maLop) VALUES (%s,%s,%s,%s,%s,%s)",
                    (maSV, hoTen, ngaySinh, gioiTinh, diaChi, maLop)
                )
                conn.commit()
                messagebox.showinfo("✅ Thành công", "Đã thêm sinh viên.")
                tai_ds_sv()
            except mysql.connector.Error as err:
                messagebox.showerror("❌ Lỗi MySQL", f"{err}")
            finally:
                conn.close()

    def sua_sv():
        maSV = entry_maSV.get().strip()
        hoTen = entry_hoTen.get().strip()
        ngaySinh = entry_ngaySinh.get_date().strftime("%Y-%m-%d")
        gioiTinh = gioiTinhVar.get()
        diaChi = entry_diaChi.get().strip()
        maLop = entry_maLop.get().strip()
        if not maSV:
            messagebox.showerror("Lỗi", "Chọn sinh viên để sửa.")
            return
        conn = ket_noi_mysql()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE sinhvien SET hoTen=%s, ngaySinh=%s, gioiTinh=%s, diaChi=%s, maLop=%s WHERE maSV=%s",
                    (hoTen, ngaySinh, gioiTinh, diaChi, maLop, maSV)
                )
                conn.commit()
                messagebox.showinfo("✅ Thành công", "Đã cập nhật sinh viên.")
                tai_ds_sv()
            except mysql.connector.Error as err:
                messagebox.showerror("❌ Lỗi MySQL", f"{err}")
            finally:
                conn.close()

    def xoa_sv():
        maSV = entry_maSV.get().strip()
        if not maSV:
            messagebox.showerror("Lỗi", "Chọn sinh viên để xóa.")
            return
        conn = ket_noi_mysql()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM sinhvien WHERE maSV=%s", (maSV,))
                conn.commit()
                messagebox.showinfo("✅ Thành công", "Đã xóa sinh viên.")
                tai_ds_sv()
            except mysql.connector.Error as err:
                messagebox.showerror("❌ Lỗi MySQL", f"{err}")
            finally:
                conn.close()

    tk.Button(frame_edit_sv, text="➕ Thêm", bg="#27ae60", fg="white", width=10, command=them_sv).grid(row=2, column=1, pady=5)
    tk.Button(frame_edit_sv, text="✏️ Sửa", bg="#2980b9", fg="white", width=10, command=sua_sv).grid(row=2, column=3, pady=5)
    tk.Button(frame_edit_sv, text="❌ Xóa", bg="#c0392b", fg="white", width=10, command=xoa_sv).grid(row=2, column=5, pady=5)

    # ====== TAB MÔN HỌC ======
    frame_mh = tk.Frame(tab_monhoc)
    frame_mh.pack(fill="both", expand=True, padx=10, pady=10)

    cols_mh = ("Mã MH", "Tên môn học", "Số tín chỉ", "Mã GV")
    tree_mh = ttk.Treeview(frame_mh, columns=cols_mh, show="headings", height=15)
    for col in cols_mh:
        tree_mh.heading(col, text=col)
        tree_mh.column(col, width=180, anchor="center")
    tree_mh.pack(side="left", fill="both", expand=True)

    scrollbar_mh = ttk.Scrollbar(frame_mh, orient="vertical", command=tree_mh.yview)
    scrollbar_mh.pack(side="left", fill="y")
    tree_mh.configure(yscrollcommand=scrollbar_mh.set)

    frame_edit_mh = tk.LabelFrame(tab_monhoc, text="✏️ Thêm/Sửa Môn học", font=("Times New Roman", 11, "bold"), padx=10, pady=10)
    frame_edit_mh.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_edit_mh, text="Mã MH:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_maMH = tk.Entry(frame_edit_mh, width=20)
    entry_maMH.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_edit_mh, text="Tên môn học:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    entry_tenMH = tk.Entry(frame_edit_mh, width=25)
    entry_tenMH.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(frame_edit_mh, text="Số tín chỉ:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
    entry_soTinChi = tk.Entry(frame_edit_mh, width=10)
    entry_soTinChi.grid(row=0, column=5, padx=5, pady=5)

    tk.Label(frame_edit_mh, text="Mã GV:").grid(row=0, column=6, padx=5, pady=5, sticky="e")
    entry_maGV = tk.Entry(frame_edit_mh, width=20)
    entry_maGV.grid(row=0, column=7, padx=5, pady=5)

    # ====== Load danh sách môn học ======
    def tai_ds_mh():
        for i in tree_mh.get_children():
            tree_mh.delete(i)
        conn = ket_noi_mysql()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT maMH, tenMH, soTinChi, maGV FROM monhoc")
            for row in cursor.fetchall():
                tree_mh.insert("", "end", values=row)
            conn.close()

    tai_ds_mh()

    def chon_mh(event):
        selected = tree_mh.selection()
        if selected:
            data = tree_mh.item(selected[0], "values")
            entry_maMH.delete(0, tk.END); entry_maMH.insert(0, data[0])
            entry_tenMH.delete(0, tk.END); entry_tenMH.insert(0, data[1])
            entry_soTinChi.delete(0, tk.END); entry_soTinChi.insert(0, data[2])
            entry_maGV.delete(0, tk.END); entry_maGV.insert(0, data[3])

    tree_mh.bind("<<TreeviewSelect>>", chon_mh)

    def them_mh():
        maMH = entry_maMH.get().strip()
        tenMH = entry_tenMH.get().strip()
        soTinChi = entry_soTinChi.get().strip()
        maGV = entry_maGV.get().strip()
        if not maMH or not tenMH:
            messagebox.showerror("Lỗi", "Mã MH và Tên môn học không được để trống.")
            return
        conn = ket_noi_mysql()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO monhoc(maMH, tenMH, soTinChi, maGV) VALUES (%s,%s,%s,%s)",
                    (maMH, tenMH, soTinChi, maGV)
                )
                conn.commit()
                messagebox.showinfo("✅ Thành công", "Đã thêm môn học.")
                tai_ds_mh()
            except mysql.connector.Error as err:
                messagebox.showerror("❌ Lỗi MySQL", f"{err}")
            finally:
                conn.close()

    def sua_mh():
        maMH = entry_maMH.get().strip()
        tenMH = entry_tenMH.get().strip()
        soTinChi = entry_soTinChi.get().strip()
        maGV = entry_maGV.get().strip()
        if not maMH:
            messagebox.showerror("Lỗi", "Chọn môn học để sửa.")
            return
        conn = ket_noi_mysql()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE monhoc SET tenMH=%s, soTinChi=%s, maGV=%s WHERE maMH=%s",
                    (tenMH, soTinChi, maGV, maMH)
                )
                conn.commit()
                messagebox.showinfo("✅ Thành công", "Đã cập nhật môn học.")
                tai_ds_mh()
            except mysql.connector.Error as err:
                messagebox.showerror("❌ Lỗi MySQL", f"{err}")
            finally:
                conn.close()

    def xoa_mh():
        maMH = entry_maMH.get().strip()
        if not maMH:
            messagebox.showerror("Lỗi", "Chọn môn học để xóa.")
            return
        conn = ket_noi_mysql()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM monhoc WHERE maMH=%s", (maMH,))
                conn.commit()
                messagebox.showinfo("✅ Thành công", "Đã xóa môn học.")
                tai_ds_mh()
            except mysql.connector.Error as err:
                messagebox.showerror("❌ Lỗi MySQL", f"{err}")
            finally:
                conn.close()

    tk.Button(frame_edit_mh, text="➕ Thêm", bg="#27ae60", fg="white", width=10, command=them_mh).grid(row=1, column=1, pady=5)
    tk.Button(frame_edit_mh, text="✏️ Sửa", bg="#2980b9", fg="white", width=10, command=sua_mh).grid(row=1, column=3, pady=5)
    tk.Button(frame_edit_mh, text="❌ Xóa", bg="#c0392b", fg="white", width=10, command=xoa_mh).grid(row=1, column=5, pady=5)

    # ====== TAB KẾT QUẢ / ĐĂNG KÝ MÔN HỌC ======
    frame_kq = tk.Frame(tab_ketqua)
    frame_kq.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Label(frame_kq, text="📘 Chọn môn học:", font=("Times New Roman", 11, "bold")).pack(anchor="w")
    combo_mh_kq = ttk.Combobox(frame_kq, width=40, state="readonly")
    combo_mh_kq.pack(anchor="w", pady=5)

    tree_kq = ttk.Treeview(frame_kq, columns=("Mã SV", "Họ tên", "Điểm"), show="headings", height=15)
    for col in ("Mã SV", "Họ tên", "Điểm"):
        tree_kq.heading(col, text=col)
        tree_kq.column(col, width=200, anchor="center")
    tree_kq.pack(fill="both", expand=True)

    def tai_ds_mh_kq():
        conn = ket_noi_mysql()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tenMH FROM monhoc")
            ds = [r[0] for r in cursor.fetchall()]
            combo_mh_kq["values"] = ds
            if ds:
                combo_mh_kq.current(0)
                tai_ds_sv_kq()
            conn.close()

    def tai_ds_sv_kq():
        for i in tree_kq.get_children():
            tree_kq.delete(i)
        tenMH = combo_mh_kq.get()
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
                tree_kq.insert("", "end", values=row)
            conn.close()

    combo_mh_kq.bind("<<ComboboxSelected>>", lambda e: tai_ds_sv_kq())
    tai_ds_mh_kq()

    frame_edit_kq = tk.LabelFrame(frame_kq, text="✏️ Đăng ký sinh viên / Cập nhật điểm", font=("Times New Roman", 11, "bold"), padx=10, pady=10)
    frame_edit_kq.pack(fill="x", pady=5)

    tk.Label(frame_edit_kq, text="Mã SV:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_kq_masv = tk.Entry(frame_edit_kq, width=20)
    entry_kq_masv.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_edit_kq, text="Điểm:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    entry_kq_diem = tk.Entry(frame_edit_kq, width=10)
    entry_kq_diem.grid(row=0, column=3, padx=5, pady=5)

    def dang_ky_sv():
        maSV = entry_kq_masv.get().strip()
        tenMH = combo_mh_kq.get()
        if not maSV:
            messagebox.showerror("Lỗi", "Nhập mã sinh viên để đăng ký.")
            return
        conn = ket_noi_mysql()
        if conn:
            try:
                cursor = conn.cursor()
                # Lấy maMH từ tên môn
                cursor.execute("SELECT maMH FROM monhoc WHERE tenMH=%s", (tenMH,))
                res = cursor.fetchone()
                if not res:
                    messagebox.showerror("Lỗi", "Môn học không tồn tại.")
                    return
                maMH = res[0]
                cursor.execute("INSERT INTO ketqua(maSV, maMH, diem) VALUES (%s,%s,%s)", (maSV, maMH, None))
                conn.commit()
                messagebox.showinfo("✅ Thành công", "Đã đăng ký sinh viên vào môn học.")
                tai_ds_sv_kq()
            except mysql.connector.Error as err:
                messagebox.showerror("❌ Lỗi MySQL", f"{err}")
            finally:
                conn.close()

    def cap_nhat_diem():
        maSV = entry_kq_masv.get().strip()
        diem = entry_kq_diem.get().strip()
        tenMH = combo_mh_kq.get()
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
                messagebox.showinfo("✅ Thành công", "Đã cập nhật điểm.")
                tai_ds_sv_kq()
            except mysql.connector.Error as err:
                messagebox.showerror("❌ Lỗi MySQL", f"{err}")
            finally:
                conn.close()

    tk.Button(frame_edit_kq, text="➕ Đăng ký", bg="#27ae60", fg="white", width=12, command=dang_ky_sv).grid(row=1, column=1, pady=5)
    tk.Button(frame_edit_kq, text="✏️ Cập nhật điểm", bg="#2980b9", fg="white", width=15, command=cap_nhat_diem).grid(row=1, column=3, pady=5)

    # ====== Tìm kiếm sinh viên theo Mã SV ======
    tk.Label(frame_edit_sv, text="🔍 Tìm Mã SV:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    entry_timSV = tk.Entry(frame_edit_sv, width=20)
    entry_timSV.grid(row=3, column=1, padx=5, pady=5)

    def tim_sv():
        maSV = entry_timSV.get().strip()
        for i in tree_sv.get_children():
            tree_sv.delete(i)
        if not maSV:
            tai_ds_sv()
            return
        conn = ket_noi_mysql()
        if conn:
            cursor = conn.cursor()
        # Sử dụng LIKE để tránh vấn đề khoảng trắng và phân biệt chữ hoa
            cursor.execute("SELECT maSV, hoTen, ngaySinh, gioiTinh, diaChi, maLop "
                           "FROM sinhvien WHERE maSV LIKE %s", (maSV,))
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    tree_sv.insert("", "end", values=row)
            else:
            # thử tìm không phân biệt hoa thường
                cursor.execute("SELECT maSV, hoTen, ngaySinh, gioiTinh, diaChi, maLop "
                           "FROM sinhvien WHERE LOWER(maSV)=LOWER(%s)", (maSV,))
                rows = cursor.fetchall()
                if rows:
                    for row in rows:
                        tree_sv.insert("", "end", values=row)
                else:
                    messagebox.showinfo("Thông báo", "Không tìm thấy sinh viên với Mã SV này.")
            conn.close()

    tk.Button(frame_edit_sv, text="🔎 Tìm", bg="#f39c12", fg="white", width=10, command=tim_sv).grid(row=3, column=3, pady=5)

# ====== Nút Thoát ======
    def thoat_app():
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát?"):
            window.destroy()

    tk.Button(frame_edit_sv, text="🚪 Thoát", bg="#7f8c8d", fg="white", width=10, command=thoat_app).grid(row=3, column=5, pady=5)

    window.mainloop()


# ====== CHẠY APP ======
if __name__ == "__main__":
    mo_giao_dien_admin()
