import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

ACCENT_COLOR = "#7FDBFF"
BG_COLOR = "#23272F"
TOPBAR_COLOR = "#181A20"
BTN_COLOR = "#2ECCFA"
BTN_HOVER = "#51C4D3"

class WebcamGUI:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title("GesturePanda")
        icon_path = os.path.join(os.path.dirname(__file__), "favicon.ico")
        self.window.iconbitmap(icon_path)
        self.window.geometry("900x650")
        self.window.configure(bg=BG_COLOR)
        self.video_source = 0

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=BG_COLOR)
        style.configure("TLabel", background=BG_COLOR, foreground="#F5F6FA", font=("Segoe UI", 18, "bold"))
        style.configure("Status.TLabel", background=TOPBAR_COLOR, foreground=ACCENT_COLOR, font=("Segoe UI", 12))
        style.configure("TButton", font=("Segoe UI", 12), padding=6)

        self.topbar = tk.Frame(window, bg=TOPBAR_COLOR, height=60)
        self.topbar.pack(fill=tk.X, side=tk.TOP)
        self.topbar.grid_columnconfigure(0, weight=1)
        self.topbar.grid_columnconfigure(1, weight=0)
        self.topbar.grid_columnconfigure(2, weight=1)

        # Load and display logo image beside the app name
        logo_path = os.path.join(os.path.dirname(__file__), "Logo_Name.png")
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((40, 40), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_img)
        self.icon_label = tk.Label(
            self.topbar, image=self.logo_photo, bg=TOPBAR_COLOR
        )
        self.icon_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="e")

        self.title_label = tk.Label(
            self.topbar,
            text="GesturePanda",
            bg=TOPBAR_COLOR,
            fg="#F5F6FA",
            font=("Segoe UI", 22, "bold")
        )
        self.title_label.grid(row=0, column=1, pady=10, sticky="nsew")

        self.accent_line = tk.Canvas(window, height=4, bg=BG_COLOR, highlightthickness=0)
        self.accent_line.pack(fill=tk.X)
        self.accent_line.create_rectangle(0, 0, 900, 4, fill=ACCENT_COLOR, outline="")

        self.center_frame = tk.Frame(window, bg=BG_COLOR)
        self.center_frame.pack(expand=True)

        self.card_frame = tk.Frame(self.center_frame, bg=BG_COLOR)
        self.card_frame.pack(pady=(30, 10))
        self.shadow = tk.Canvas(self.card_frame, width=660, height=500, bg=BG_COLOR, highlightthickness=0)
        self.shadow.place(x=8, y=8)
        self.shadow.create_oval(20, 480, 640, 500, fill="#181A20", outline="")
        self.video_frame = tk.Frame(self.card_frame, bg=TOPBAR_COLOR, bd=0, relief=tk.FLAT)
        self.video_frame.place(x=0, y=0)
        self.canvas = tk.Canvas(self.video_frame, width=640, height=480, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(padx=0, pady=0)
        self.card_frame.config(width=660, height=500)
        self.card_frame.pack_propagate(0)

        self.status_var = tk.StringVar(value="Webcam running...")
        self.status_bar = tk.Label(window, textvariable=self.status_var, bg=ACCENT_COLOR, fg=TOPBAR_COLOR, font=("Segoe UI", 12, "bold"), bd=0, relief=tk.FLAT)
        self.status_bar.pack(fill=tk.X, pady=(10, 0), padx=0, ipady=6)
        self.status_bar.config(highlightbackground=ACCENT_COLOR, highlightthickness=0)

        self.button_frame = tk.Frame(self.center_frame, bg=BG_COLOR)
        self.button_frame.pack(pady=(20, 0))

        self.exit_button = tk.Button(
            self.button_frame, text="Exit", bg=BTN_COLOR, fg="#23272F", font=("Segoe UI", 12, "bold"),
            activebackground=BTN_HOVER, activeforeground="#23272F", bd=0, relief=tk.FLAT, width=12, height=1,
            command=self.on_closing, cursor="hand2", highlightthickness=0
        )
        self.exit_button.pack(ipady=4, ipadx=4)
        self.exit_button.config(borderwidth=0, highlightbackground=BTN_COLOR, highlightcolor=BTN_COLOR)
        self.exit_button.bind("<Enter>", lambda e: self.exit_button.config(bg=BTN_HOVER))
        self.exit_button.bind("<Leave>", lambda e: self.exit_button.config(bg=BTN_COLOR))

        self.vid = cv2.VideoCapture(self.video_source)
        if not self.vid.isOpened():
            self.status_var.set("Unable to open webcam.")
            raise RuntimeError("Unable to open webcam.")

        self.delay = 15
        self.update()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (7, 7), 0)
            img = Image.fromarray(blurred)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.imgtk = imgtk
            self.status_var.set("Webcam running...")
        else:
            self.status_var.set("Failed to capture frame.")
        self.window.after(self.delay, self.update)

    def on_closing(self):
        if self.vid.isOpened():
            self.vid.release()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    WebcamGUI(root, "Hand Gesture Recognition - Webcam Feed")
    root.mainloop()