import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfMerger

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.file_list = []

        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=50)
        self.listbox.pack(pady=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Add PDFs", command=self.add_files).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Move Up", command=self.move_up).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Move Down", command=self.move_down).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Merge and Save", command=self.merge_pdfs).grid(row=0, column=3, padx=5)

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for file in files:
            if file not in self.file_list:
                self.file_list.append(file)
                self.listbox.insert(tk.END, file.split("/")[-1])

    def move_up(self):
        idx = self.listbox.curselection()
        if idx and idx[0] > 0:
            i = idx[0]
            self.file_list[i-1], self.file_list[i] = self.file_list[i], self.file_list[i-1]
            self.update_listbox()

    def move_down(self):
        idx = self.listbox.curselection()
        if idx and idx[0] < len(self.file_list) - 1:
            i = idx[0]
            self.file_list[i+1], self.file_list[i] = self.file_list[i], self.file_list[i+1]
            self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for f in self.file_list:
            self.listbox.insert(tk.END, f.split("/")[-1])

    def merge_pdfs(self):
        if not self.file_list:
            messagebox.showwarning("No PDFs", "Please add PDF files first.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not output_path:
            return

        merger = PdfMerger()
        for f in self.file_list:
            merger.append(f)
        merger.write(output_path)
        merger.close()

        messagebox.showinfo("Success", f"Merged PDF saved to:\n{output_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()