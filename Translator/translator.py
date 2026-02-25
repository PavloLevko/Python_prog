from deep_translator import GoogleTranslator
import tkinter as tk

translatot = GoogleTranslator(source="auto", target="uk")


import tkinter as tk

window = tk.Tk()
window.title("Translator App")
window.geometry("400x300")
window.configure(bg="#f0f0f0")  # світлий фон

# Заголовок
title = tk.Label(window, text="Translator", font=("Arial", 16, "bold"), bg="#f0f0f0")
title.pack(pady=10)

# Підпис для поля вводу
input_label = tk.Label(window, text="Введіть текст: ", bg="#f0f0f0")
input_label.pack(anchor="w", padx=20)

# Поле вводу
entry = tk.Entry(window, borderwidth=2, relief="ridge", width=35, font=("Arial", 12))
entry.pack(padx=20, pady=5, ipady=5)

# Підпис для результату
output_label = tk.Label(window, text="Переклад: ", bg="#f0f0f0")
output_label.pack(anchor="w", padx=20)

# Поле виводу
result_label = tk.Label(
    window,
    text="",
    borderwidth=2,
    relief="ridge",
    width=35,
    height=5,
    bg="white",
    anchor="nw",
    justify="left",
    font=("Arial", 12)
)
result_label.pack(padx=20, pady=5)

# Функція кнопки
def show_text():
    text = entry.get()
    text_after_transl = translatot.translate(text=text)
    result_label.config(text=text_after_transl)

# Кнопка
button = tk.Button(
    window,
    text="Перекласти",
    command=show_text
)
button.pack(pady=15)

window.mainloop()
