import tkinter as tk
from tkinter import filedialog, messagebox
import os
import tempfile
import shutil

from main_logic import main  

class PDFSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dekont Sırala")
        self.pdf_files = []

        # Upload Button
        self.upload_btn = tk.Button(root, text="PDF Yükle", command=self.upload_pdfs)
        self.upload_btn.pack(pady=10)

        # Listbox to show files
        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=60)
        self.listbox.pack(pady=10)

        # Sort & Save Button
        self.sort_btn = tk.Button(root, text="Sırala & Kaydet", command=self.sort_and_save)
        self.sort_btn.pack(pady=10)
        
        self.info_label = tk.Label(root, text="Ali Arda Fincan 2025", fg="grey")
        self.info_label.pack(pady=5)

    def upload_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)
                self.listbox.insert(tk.END, os.path.basename(file))
            
            # This part needs fixing - we'll create temporary files only when needed
            # No need to create temp files here as we're just storing the paths

    def create_temp_files(self):
        """Create temporary copies of all uploaded PDF files and return their paths."""
        temp_files = []
        for file in self.pdf_files:
            # Create a temporary file with the same name as the original
            basename = os.path.basename(file)
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{basename}") as temp_file:
                temp_path = temp_file.name
                
                # Copy the content from the original to the temp file
                with open(file, 'rb') as src_file:
                    shutil.copyfileobj(src_file, temp_file)
                    
                temp_files.append(temp_path)
                
        return temp_files

    def sort_and_save(self):
        if not self.pdf_files:
            messagebox.showwarning("Uyarı", "Dosya Yok, Lütfen PDF Yükleyin")
            return
        try:
            output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if not output_path:
                return
            
            # Create temporary copies of the files for processing
            temp_files = self.create_temp_files()
            
            # Use the temporary files for processing
            main(temp_files, output_path)
            
            # Clean up temporary files
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file)
                except Exception as e:
                    print(f"Could not delete temporary file {temp_file}: {e}")
            
            messagebox.showinfo("Başarılı", f"Düzenlenen PDF dosyası şurada kaydedildi:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Hata", f"Bir şeyler ters gitti, hata:\n{e}")
            print(e)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFSorterApp(root)
    root.mainloop()