import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from ultralytics import YOLO
import os

class YOLOApp:
    def __init__(self, root):
        self.root = root
        self.root.title('YOLO Image Predictor')
        self.model = YOLO('best.tflite')
        self.image_path = None
        self.img_label = tk.Label(root)
        self.img_label.pack(pady=10)
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=10)
        self.load_btn = tk.Button(self.btn_frame, text='Load Image', command=self.load_image)
        self.load_btn.grid(row=0, column=0, padx=5)
        self.predict_btn = tk.Button(self.btn_frame, text='Predict', command=self.predict, state=tk.DISABLED)
        self.predict_btn.grid(row=0, column=1, padx=5)
        self.reset_btn = tk.Button(self.btn_frame, text='Reset', command=self.reset, state=tk.DISABLED)
        self.reset_btn.grid(row=0, column=2, padx=5)
        self.result_img = None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp *.ppm *.pgm *.pbm *.pnm *.tif *.ico *.jfif *.bmp')])
        if file_path:
            self.image_path = file_path
            img = Image.open(file_path)
            img.thumbnail((400, 400))
            self.result_img = ImageTk.PhotoImage(img)
            self.img_label.config(image=self.result_img)
            self.predict_btn.config(state=tk.NORMAL)
            self.reset_btn.config(state=tk.NORMAL)

    def predict(self):
        if not self.image_path:
            messagebox.showwarning('No Image', 'Please load an image first!')
            return
        results = self.model(self.image_path)
        results[0].save(filename='predicted.jpg')
        pred_img = Image.open('predicted.jpg')
        pred_img.thumbnail((400, 400))
        self.result_img = ImageTk.PhotoImage(pred_img)
        self.img_label.config(image=self.result_img)
        os.remove('predicted.jpg')

    def reset(self):
        self.img_label.config(image='')
        self.image_path = None
        self.result_img = None
        self.predict_btn.config(state=tk.DISABLED)
        self.reset_btn.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = YOLOApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
