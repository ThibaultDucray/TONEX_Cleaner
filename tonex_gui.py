import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
# import tonex_actions as ta

# Tkinter GUI
class TonexApp(tk.Tk):
    def __init__(self, tonexActions):
        super().__init__()
        self.tonexActions = tonexActions
        self.title("TONEX Preset Manager")

        self.style = ttk.Style()
        self.style.theme_use("clam")  # Cross-platform theme

        # Custom theme
        self.dark_bg = "#202020"
        self.dark_bg2 = "#303030"
        self.dark_fg = "#c0c0c0"
        self.select_bg = "#604123"
        self.select_fg = "#fb9230"

        # Custom styles
        self.style.configure("Dark.TFrame", background=self.dark_bg)
        self.style.configure("Dark.TLabel", background=self.dark_bg, foreground=self.dark_fg)
        self.style.configure("Dark.TEntry", fieldbackground=self.dark_bg, foreground=self.dark_fg, relief="flat", borderwidth=0)
        self.style.configure("Dark.TButton", background=self.dark_bg2, foreground=self.dark_fg, relief="flat")
        self.style.map("Dark.TButton",
                background=[("active", self.select_bg)],
                foreground=[("active", self.select_fg)])

        self.configure(bg=self.dark_bg)
        self.create_widgets()
        self.load_filtered_names()

    def create_widgets(self):
        self.frame = ttk.Frame(self, padding=5, style="Dark.TFrame")
        self.frame.pack(fill="both", expand=True)

        # The list
        ttk.Label(self.frame, text="Presets:", style="Dark.TLabel").grid(row=0, column=0, pady=5)

        self.label_count = ttk.Label(self.frame, text="0 shown / 0 total", style="Dark.TLabel")
        self.label_count.grid(row=0, column=1, pady=0)

        self.listbox = tk.Listbox(self.frame, width=60, height=20, 
            bg=self.dark_bg2, fg=self.dark_fg,
            selectbackground=self.select_bg, selectforeground=self.select_fg,
            highlightbackground=self.dark_bg, highlightcolor=self.select_bg)
        self.listbox.grid(row=1, column=0, columnspan=2, rowspan=2, padx=5, pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.select_name)

        # Automatic cleanup feature
        self.btn_clean = ttk.Button(self.frame, text="Cleanup versions", command=self.clean_suffixes, style="Dark.TButton")
        self.btn_clean.grid(row=1, column=2, padx=5, pady=0)

        # Manual delete feature
        self.btn_delete = ttk.Button(self.frame, text="Delete", command=self.delete_from_name, style="Dark.TButton")
        self.btn_delete.grid(row=2, column=2, padx=5, pady=0)

        # Manual rename feature
        ttk.Label(self.frame, text="Manual rename:", style="Dark.TLabel").grid(row=3, column=0, padx=5, pady=5)
        ttk.Label(self.frame, text="Find:", style="Dark.TLabel").grid(row=4, column=0, padx=5, pady=0)
        self.entry_old = ttk.Entry(self.frame, width=30, style="Dark.TEntry")
        self.entry_old.grid(row=4, column=1, padx=5, pady=0)
        self.entry_old.bind("<KeyRelease>", self.load_filtered_names)
        
        ttk.Label(self.frame, text="New name:", style="Dark.TLabel").grid(row=5, column=0, padx=5, pady=0)
        self.entry_new = ttk.Entry(self.frame, width=30, style="Dark.TEntry")
        self.entry_new.grid(row=5, column=1, padx=5, pady=0)

        self.btn_replace = ttk.Button(self.frame, text="Rename", command=self.search_and_replace, style="Dark.TButton")
        self.btn_replace.grid(row=5, column=2, pady=0)

    # actions
    def load_filtered_names(self, event = None):
        filter = self.entry_old.get().strip()
        names = self.tonexActions.load_filtered_names(filter)
        self.listbox.delete(0, tk.END)
        for nom in names:
            self.listbox.insert(tk.END, nom)
        total = self.tonexActions.get_total_count()
        self.label_count.config(text=f"{len(names)} shown / {total} total")        

    def select_name(self, event):
        if self.listbox.curselection():
            select = self.listbox.get(self.listbox.curselection())
            self.entry_old.delete(0, tk.END)
            self.entry_old.insert(0, select)
            self.entry_new.delete(0, tk.END)
            self.entry_new.insert(0, select)
    
    def clean_suffixes(self):
        changes, groups, all_names = self.tonexActions.prepare_clean_suffixes()
        if not messagebox.askyesno(
            "Confirmation",
            "This will clean\n" + "\n".join(changes) + "\nand rename the latest to the base name. Proceed?"
        ):
            return
        changes = self.tonexActions.exec_clean_suffixes(groups, all_names)
        messagebox.showinfo("Success", f"Suffix cleanup complete. Cleanup:" + "\n".join(changes))
        self.load_filtered_names()

    def delete_from_name(self):
        tag_name = self.entry_old.get().strip()
        if not tag_name:
            return 0
        if not messagebox.askyesno("Confirmation", f"Confirm deletion of '{tag_name}'?"):
            return
        err = self.tonexActions.delete_from_name(tag_name)
        if err == 0:
            messagebox.showerror("Error", "Select a name to be deleted.")
        else:
            messagebox.showinfo("Success", f"Name '{tag_name}' has been deleted.")
            self.entry_old.delete(0, tk.END)
            self.load_filtered_names()

    def search_and_replace(self):
        tag_name = self.entry_old.get().strip()
        new_name = self.entry_new.get().strip()
        if not tag_name:
            messagebox.showerror("Error", "Enter a name to search.")
            return
        if not new_name:
            messagebox.showerror("Error", "Please enter new name.")
            return
        err = self.tonexActions.search_and_replace(tag_name, new_name)
        if err == 1:
            messagebox.showinfo("Info", f"Name '{tag_name}' doesn't exist.")
        elif err == 2:
            messagebox.showerror("Error", f"Name '{new_name}' already in use.")
        elif err == 0:
            messagebox.showinfo("Success", f"Name '{tag_name}' replaced with '{new_name}'.")
            self.entry_old.delete(0, tk.END)
            self.entry_old.insert(0, new_name)
        self.load_filtered_names()
