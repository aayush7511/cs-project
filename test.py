import tkinter as tk
from tkinter import font

def show_fonts():
    root = tk.Tk()
    root.title("Fonts in Tkinter")

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    fonts_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=fonts_frame, anchor=tk.NW)

    all_fonts = list(font.families())

    for font_name in all_fonts:
        font_label = tk.Label(fonts_frame, text=font_name, font=(font_name, 12))
        font_label.pack()

    root.mainloop()

show_fonts()