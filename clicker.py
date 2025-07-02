import pyautogui
import time
import threading
from pynput import keyboard
import tkinter as tk
from tkinter import messagebox

print("Автокликер запущен! Наведите мышку на нужную точку и нажмите Enter.")

interval = 3  # Интервал между кликами в секундах

class ClickerApp:
    def __init__(self, master):
        self.master = master
        master.title("Автокликер")
        master.geometry("300x150")
        self.status = tk.StringVar()
        self.status.set("Остановлен")
        self.clicking = False
        self.selected_pos = None
        self.listener = None
        self.click_thread = None

        self.label = tk.Label(master, textvariable=self.status, font=("Arial", 14))
        self.label.pack(pady=10)

        self.start_button = tk.Button(master, text="Старт", command=self.start_clicker, width=10)
        self.start_button.pack(pady=5)
        self.stop_button = tk.Button(master, text="Стоп", command=self.stop_clicker, width=10, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

    def start_clicker(self):
        self.status.set("Выберите точку: наведите мышку и нажмите Enter")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.selected_pos = None
        self.clicking = False
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.master.after(100, self.check_point_selected)

    def check_point_selected(self):
        if self.selected_pos is not None:
            self.status.set(f"Кликаю по: {self.selected_pos}")
            self.clicking = True
            self.click_thread = threading.Thread(target=self.click_loop, daemon=True)
            self.click_thread.start()
        else:
            self.master.after(100, self.check_point_selected)

    def stop_clicker(self):
        self.clicking = False
        self.status.set("Остановлен")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def on_press(self, key):
        try:
            if key == keyboard.Key.enter and self.selected_pos is None:
                self.selected_pos = pyautogui.position()
                if self.listener:
                    self.listener.stop()
        except Exception:
            pass

    def click_loop(self):
        while self.clicking:
            if self.selected_pos:
                pyautogui.click(self.selected_pos[0], self.selected_pos[1])
            for _ in range(int(interval*10)):
                if not self.clicking:
                    break
                time.sleep(0.1)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickerApp(root)
    root.mainloop() 