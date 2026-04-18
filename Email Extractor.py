import re
from tkinter import *
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        entry_input.delete(0, END)
        entry_input.insert(0, file_path)

def extract_emails():
    input_file = entry_input.get()
    output_file = entry_output.get()

    if input_file == "" or output_file == "":
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        with open(input_file, "r", encoding="utf-8") as file:
            content = file.read()

        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+'
        emails = list(set(re.findall(pattern, content)))

        with open(output_file, "w", encoding="utf-8") as file:
            for email in sorted(emails):
                file.write(email + "\n")

        messagebox.showinfo("Success", f"{len(emails)} emails extracted!")

    except FileNotFoundError:
        messagebox.showerror("Error", "Input file not found")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def drop_file(event):
    file_path = event.data.strip("{}")
    entry_input.delete(0, END)
    entry_input.insert(0, file_path)

window = TkinterDnD.Tk()
window.title("Email Extractor")
window.geometry("500x350")
window.configure(bg="#1e1e1e")

bg_color = "#1e1e1e"
fg_color = "#ffffff"
entry_bg = "#2d2d2d"
btn_color = "#4CAF50"

Label(window, text="Email Extractor", font=("Arial", 16, "bold"),
      bg=bg_color, fg=fg_color).pack(pady=10)

drop_area = Label(window, text="Drag & Drop .txt File Here",
                  bg="#333333", fg="white", width=40, height=5)
drop_area.pack(pady=10)

drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind('<<Drop>>', drop_file)

Label(window, text="Input File Name to Process:", bg=bg_color, fg=fg_color).pack()
frame_input = Frame(window, bg=bg_color)
frame_input.pack(pady=5)

entry_input = Entry(frame_input, width=40, bg=entry_bg, fg=fg_color, insertbackground="white")
entry_input.pack(side=LEFT, padx=5)

Button(frame_input, text="Browse", command=browse_file,
       bg=btn_color, fg="white").pack(side=LEFT)

Label(window, text="Name of Output File:", bg=bg_color, fg=fg_color).pack()
entry_output = Entry(window, width=45, bg=entry_bg, fg=fg_color, insertbackground="white")
entry_output.pack(pady=5)

Button(window, text="Extract Emails", command=extract_emails,
       bg=btn_color, fg="white", width=20, height=2).pack(pady=15)

window.mainloop()
