import tkinter as tk
from Word_manager import WordManager
from Timer import Timer

window = tk.Tk()
window.configure(background='#dbb9f0')
window.geometry("1400x750")
window.title("Typing Speed Test")

welcome_label = tk.Label(text="Welcome! Begin typing when you're ready.", font=("Serif", 15), background='#dbb9f0')
text = tk.Label(text="the text words", font=("Serif", 15), background='#dbb9f0')
typing_box = tk.Text(width=124, font=("Serif", 15), height=26)
timer_label = tk.Label(text="60", font=("Serif", 20), fg='blue', background='#dbb9f0')
start_button = tk.Button(text="Start", font=("Serif", 20), background="#dbb9f0")

manager = WordManager(entry=typing_box, first_label=welcome_label, word_label=text, window=window)
timer = Timer(window=window, label=timer_label, entry=typing_box, words=manager.words, button=start_button)
start_button.configure(command=timer.countdown)


welcome_label.grid(row=0, column=1, sticky="S")
text.grid(row=1, column=1, pady=15)
typing_box.grid(row=2, column=0, columnspan=3, padx=15)
timer_label.grid(row=1, column=2, sticky='N')
start_button.grid(row=1, column=0, pady=5)

typing_box.bind("<KeyRelease>", manager.new_words)

manager.start_up()


window.mainloop()
