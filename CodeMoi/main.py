from tkinter import (ttk, Tk, PhotoImage, Canvas, filedialog, colorchooser, RIDGE,
                     GROOVE, ROUND, Scale, HORIZONTAL)
from tkinter import messagebox
import cv2
from PIL import ImageTk, Image
import numpy as np
class FrontEnd:
    def __init__(self, master):
        self.master = master
        self.menu()
        self.image_loaded = False  # Thêm biến cờ để kiểm tra ảnh đã được tải lên hay chưa
    def menu(self):
        self.master.geometry('750x630+250+10')
        self.master.title('Photo Editing')

        self.frame_menu = ttk.Frame(self.master)
        self.frame_menu.pack()
        self.frame_menu.config(relief=RIDGE, padding=(50, 15))

        ttk.Button(
            self.frame_menu, text="Chọn ảnh", command=self.anh).grid(
            row=0, column=0, columnspan=2, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.frame_menu, text="Thêm văn bản", command=self.van_ban).grid(
            row=3, column=0, columnspan=2, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.frame_menu, text="Lưu", command=self.luu).grid(
            row=4, column=0, columnspan=2, padx=5, pady=5, sticky='sw')
        self.canvas = Canvas(self.frame_menu, bg="gray", width=300, height=400)
        self.canvas.grid(row=0, column=3, rowspan=10)
        self.side_frame = ttk.Frame(self.frame_menu)
        self.side_frame.grid(row=0, column=4, rowspan=10)
        self.side_frame.config(relief=GROOVE, padding=(50, 15))
        self.apply_and_cancel = ttk.Frame(self.master)
        self.apply_and_cancel.pack()
        self.apply = ttk.Button(self.apply_and_cancel, text="Áp dụng", command=self.ap_dung).grid(
            row=0, column=0, columnspan=1, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.apply_and_cancel, text="Quay lại", command=self.quay_lai).grid(
            row=0, column=1, columnspan=1, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.apply_and_cancel, text="Ảnh gốc", command=self.anh_goc).grid(
            row=0, column=2, columnspan=1, padx=5, pady=5, sticky='sw')

    def anh(self):
        self.canvas.delete("all")
        self.filename = filedialog.askopenfilename()
        # Kiểm tra định dạng tệp tin
        if self.filename:
            valid_image_formats = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
            if self.filename.lower().endswith(valid_image_formats):
                self.original_image = cv2.imread(self.filename)
                self.edited_image = cv2.imread(self.filename)
                self.filtered_image = cv2.imread(self.filename)
                self.display_image(self.edited_image)
                self.image_loaded = True
            else:
                # Hiển thị thông báo nếu tệp tin không đúng định dạng
                messagebox.showwarning("Lỗi", "Vui lòng chọn đúng định dạng")

    def van_ban(self):
        if not self.image_loaded:
            messagebox.showwarning("Lỗi", "Vui lòng chọn ảnh")
            return
        self.lam_moi_khung()
        ttk.Label(
            self.side_frame, text="Nhập:").grid(
            row=0, column=2, padx=5, pady=5, sticky='sw')

        self.text_entry = ttk.Entry(self.side_frame, font=("Arial", 12))
        self.text_entry.grid(row=1, column=2, padx=5, pady=5, sticky='sw')

        add_text_button = ttk.Button(
            self.side_frame, text="Thêm", command=self.them_van_ban)
        add_text_button.grid(row=2, column=2, padx=5, pady=5, sticky='sw')

    def them_van_ban(self):
        text = self.text_entry.get()
        if text:
            start_font = (10, 100)  # Thay đổi vị trí bắt đầu văn bản trên ảnh
            r, g, b = 255, 255, 255  # Thay đổi màu sắc theo nhu cầu của bạn
            # Chuyển đổi ảnh sang định dạng mà OpenCV có thể hiểu
            image_for_cv2 = cv2.cvtColor(self.edited_image, cv2.COLOR_BGR2RGB)
            # Thêm văn bản vào ảnh
            image_with_text = cv2.putText(
                image_for_cv2, text, start_font, cv2.FONT_HERSHEY_TRIPLEX, 3, (b, g, r), 3)
            # Chuyển đổi ảnh trở lại định dạng ban đầu để hiển thị trên giao diện
            self.filtered_image = cv2.cvtColor(image_with_text, cv2.COLOR_RGB2BGR)
            self.display_image(self.filtered_image)
    def lam_moi_khung(self):
        try:
            self.side_frame.grid_forget()
        except:
            pass
        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease>")
        self.display_image(self.edited_image)
        self.side_frame = ttk.Frame(self.frame_menu)
        self.side_frame.grid(row=0, column=4, rowspan=10)
        self.side_frame.config(relief=GROOVE, padding=(50, 15))

    def luu(self):
        if not self.image_loaded:
            messagebox.showwarning("Lỗi", "Vui lòng chọn ảnh")
            return
        original_file_type = self.filename.split('.')[-1]
        filename = filedialog.asksaveasfilename()
        filename = filename + "." + original_file_type

        save_as_image = self.edited_image
        cv2.imwrite(filename, save_as_image)
        self.filename = filename

    def ap_dung(self):
            # Áp dụng bộ lọc hoặc thay đổi hình ảnh nếu có
            self.edited_image = self.filtered_image
            self.display_image(self.edited_image)

    def quay_lai(self):
            self.display_image(self.edited_image)

    def anh_goc(self):
            self.edited_image = self.original_image.copy()
            self.display_image(self.original_image)

    def display_image(self, image=None):
        self.canvas.delete("all")
        if image is None:
                image = self.edited_image.copy()
        else:
            image = image

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = image.shape
        ratio = height / width

        new_width = width
        new_height = height

        if height > 400 or width > 300:
            if ratio < 1:
                new_width = 300
                new_height = int(new_width * ratio)
            else:
                new_height = 400
                new_width = int(new_height * (width / height))

        self.ratio = height / new_height
        self.new_image = cv2.resize(image, (new_width, new_height))

        self.new_image = ImageTk.PhotoImage(
            Image.fromarray(self.new_image))

        self.canvas.config(width=new_width, height=new_height)
        self.canvas.create_image(
                new_width / 2, new_height / 2, image=self.new_image)

mainWindow = Tk()
FrontEnd(mainWindow)
mainWindow.mainloop()