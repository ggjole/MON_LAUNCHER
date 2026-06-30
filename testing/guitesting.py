#!/usr/bin/env python3
"""Minecraft GUI Launcher dengan CustomTkinter"""
import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import threading
import subprocess
import json
from pathlib import Path

import minecraft_launcher_lib
from config import MINECRAFT_DIR, CLIENT_ID, REDIRECT_URL, AUTH_FILE

# Set theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MinecraftLauncherGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("Minecraft Launcher")
        self.geometry("800x600")
        self.minsize(700, 500)
        
        # Variables
        self.credentials = None
        self.current_version = None
        
        # Setup UI
        self.setup_ui()
        
        # Load data
        self.load_versions()
        self.load_credentials()
    
    def setup_ui(self):
        """Setup semua komponen UI"""
        
        # Main container dengan grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Header Frame
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="🎮 Minecraft Launcher",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Theme toggle
        self.theme_switch = ctk.CTkSwitch(
            self.header_frame,
            text="Dark Mode",
            command=self.toggle_theme,
            onvalue="dark",
            offvalue="light"
        )
        self.theme_switch.grid(row=0, column=2, padx=10, pady=10)
        self.theme_switch.select()
        
        # User info
        self.user_label = ctk.CTkLabel(
            self.header_frame,
            text="Belum login",
            font=ctk.CTkFont(size=12)
        )
        self.user_label.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        
        # Control Frame
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.control_frame.grid_columnconfigure(1, weight=1)
        
        # Version selection
        self.version_label = ctk.CTkLabel(self.control_frame, text="Versi:")
        self.version_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.version_combo = ctk.CTkComboBox(
            self.control_frame,
            values=[],
            state="readonly",
            width=200
        )
        self.version_combo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Filter type
        self.filter_label = ctk.CTkLabel(self.control_frame, text="Filter:")
        self.filter_label.grid(row=0, column=2, padx=5, pady=10, sticky="w")
        
        self.filter_combo = ctk.CTkComboBox(
            self.control_frame,
            values=["Semua", "Release", "Snapshot"],
            state="readonly",
            width=120,
            command=self.filter_versions
        )
        self.filter_combo.grid(row=0, column=3, padx=10, pady=10)
        self.filter_combo.set("Release")
        
        # Buttons Frame
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        # Action buttons
        self.install_button = ctk.CTkButton(
            self.button_frame,
            text="📥 Install",
            command=self.install_version,
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.install_button.pack(side="left", padx=5, pady=10)
        
        self.launch_button = ctk.CTkButton(
            self.button_frame,
            text="🚀 Launch",
            command=self.launch_version,
            fg_color="#007bff",
            hover_color="#0056b3"
        )
        self.launch_button.pack(side="left", padx=5, pady=10)
        
        self.login_button = ctk.CTkButton(
            self.button_frame,
            text="🔐 Login",
            command=self.login_microsoft,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        self.login_button.pack(side="left", padx=5, pady=10)
        
        self.logout_button = ctk.CTkButton(
            self.button_frame,
            text="🚪 Logout",
            command=self.logout,
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        self.logout_button.pack(side="left", padx=5, pady=10)
        
        # Refresh button
        self.refresh_button = ctk.CTkButton(
            self.button_frame,
            text="🔄 Refresh",
            command=self.load_versions,
            fg_color="#17a2b8",
            hover_color="#138496"
        )
        self.refresh_button.pack(side="right", padx=5, pady=10)
        
        # Log Frame
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        self.log_frame.grid_rowconfigure(1, weight=1)
        self.log_frame.grid_columnconfigure(0, weight=1)
        
        # Log title
        self.log_title = ctk.CTkLabel(
            self.log_frame,
            text="📋 Log",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.log_title.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        # Log text
        self.log_text = ctk.CTkTextbox(
            self.log_frame,
            wrap="word",
            state="disabled"
        )
        self.log_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.log_frame)
        self.progress_bar.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.progress_bar.set(0)
        
        # Status bar
        self.status_bar = ctk.CTkLabel(
            self,
            text="Siap",
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        self.status_bar.grid(row=4, column=0, sticky="ew", padx=10, pady=5)
    
    def toggle_theme(self):
        """Toggle antara dark dan light mode"""
        if self.theme_switch.get() == "dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
    
    def log(self, message):
        """Tambahkan message ke log"""
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
        self.update()
    
    def set_status(self, message):
        """Update status bar"""
        self.status_bar.configure(text=message)
        self.update()
    
    def load_credentials(self):
        """Load credentials dari file"""
        if AUTH_FILE.exists():
            try:
                with open(AUTH_FILE, 'r') as f:
                    self.credentials = json.load(f)
                self.user_label.configure(text=f"👤 {self.credentials['name']}")
                self.log(f"✓ Login sebagai: {self.credentials['name']}")
            except Exception as e:
                self.log(f"✗ Error loading credentials: {e}")
                self.credentials = None
        else:
            self.log("Belum login. Klik tombol Login untuk autentikasi.")
    
    def load_versions(self):
        """Load daftar versi Minecraft"""
        self.log("Memuat daftar versi...")
        self.set_status("Memuat versi...")
        
        def load_thread():
            try:
                versions = minecraft_launcher_lib.utils.get_available_versions(MINECRAFT_DIR)
                self.all_versions = versions
                self.filter_versions(None)
                self.log(f"✓ {len(versions)} versi tersedia")
                self.set_status("Siap")
            except Exception as e:
                self.log(f"✗ Error loading versions: {e}")
                self.set_status("Error")
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def filter_versions(self, choice):
        """Filter versi berdasarkan tipe"""
        if not hasattr(self, 'all_versions'):
            return
        
        filter_type = self.filter_combo.get()
        
        if filter_type == "Release":
            filtered = [v for v in self.all_versions if v["type"] == "release"]
        elif filter_type == "Snapshot":
            filtered = [v for v in self.all_versions if v["type"] == "snapshot"]
        else:
            filtered = self.all_versions
        
        # Update combo box
        version_list = [v["id"] for v in filtered[:50]]  # Batasi 50 versi
        self.version_combo.configure(values=version_list)
        
        if version_list:
            self.version_combo.set(version_list[0])
    
    def install_version(self):
        """Install versi yang dipilih"""
        version = self.version_combo.get()
        
        if not version:
            messagebox.showwarning("Peringatan", "Pilih versi terlebih dahulu")
            return
        
        # Konfirmasi
        if not messagebox.askyesno("Konfirmasi", f"Install Minecraft {version}?"):
            return
        
        self.log(f"\n📥 Menginstall Minecraft {version}...")
        self.set_status(f"Installing {version}...")
        self.install_button.configure(state="disabled")
        self.progress_bar.set(0)
        
        def install_thread():
            def callback(data):
                if "status" in data:
                    self.after(0, lambda: self.log(f"  {data['status']}"))
                
                if "progress" in data and "total" in data:
                    progress = data["progress"] / data["total"]
                    self.after(0, lambda: self.progress_bar.set(progress))
            
            try:
                minecraft_launcher_lib.install.install_minecraft_version(
                    version,
                    MINECRAFT_DIR,
                    callback=callback
                )
                self.after(0, lambda: self.log(f"✓ Install {version} selesai!"))
                self.after(0, lambda: self.set_status("Install selesai"))
                self.after(0, lambda: self.progress_bar.set(1))
            except Exception as e:
                self.after(0, lambda: self.log(f"✗ Install gagal: {e}"))
                self.after(0, lambda: self.set_status("Install gagal"))
            finally:
                self.after(0, lambda: self.install_button.configure(state="normal"))
        
        threading.Thread(target=install_thread, daemon=True).start()
    
    def launch_version(self):
        """Launch versi yang dipilih"""
        version = self.version_combo.get()
        
        if not version:
            messagebox.showwarning("Peringatan", "Pilih versi terlebih dahulu")
            return
        
        if not self.credentials:
            messagebox.showwarning("Peringatan", "Login terlebih dahulu")
            return
        
        self.log(f"\n🚀 Launching Minecraft {version}...")
        self.set_status(f"Launching {version}...")
        self.launch_button.configure(state="disabled")
        
        def launch_thread():
            try:
                options = {
                    "username": self.credentials["name"],
                    "uuid": self.credentials["id"],
                    "token": self.credentials["access_token"]
                }
                
                minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(
                    version,
                    MINECRAFT_DIR,
                    options
                )
                
                self.after(0, lambda: self.log("✓ Minecraft dimulai!"))
                self.after(0, lambda: self.set_status("Minecraft berjalan"))
                
                # Launch Minecraft
                subprocess.call(minecraft_command)
                
                self.after(0, lambda: self.log("Minecraft ditutup"))
                self.after(0, lambda: self.set_status("Siap"))
                
            except Exception as e:
                self.after(0, lambda: self.log(f"✗ Launch gagal: {e}"))
                self.after(0, lambda: self.set_status("Launch gagal"))
            finally:
                self.after(0, lambda: self.launch_button.configure(state="normal"))
        
        threading.Thread(target=launch_thread, daemon=True).start()
    
    def login_microsoft(self):
        """Login dengan Microsoft Account"""
        import webbrowser
        
        self.log("\n🔐 Memulai login Microsoft...")
        self.set_status("Login...")
        
        try:
            # Dapatkan URL login
            login_url = minecraft_launcher_lib.microsoft_account.get_login_url(
                CLIENT_ID,
                REDIRECT_URL
            )
            
            # Buka browser
            webbrowser.open(login_url)
            
            # Dialog untuk input URL
            dialog = ctk.CTkInputDialog(
                text="Setelah login, paste URL redirect di sini:",
                title="Microsoft Login"
            )
            url = dialog.get_input()
            
            if not url:
                self.log("Login dibatalkan")
                self.set_status("Login dibatalkan")
                return
            
            # Cek URL
            if not minecraft_launcher_lib.microsoft_account.url_contains_auth_code(url):
                self.log("✗ URL tidak valid")
                self.set_status("Login gagal")
                return
            
            # Extract auth code
            auth_code = minecraft_launcher_lib.microsoft_account.get_auth_code_from_url(url)
            
            # Complete login
            self.log("Memproses login...")
            credentials = minecraft_launcher_lib.microsoft_account.complete_login(
                CLIENT_ID,
                REDIRECT_URL,
                auth_code
            )
            
            # Simpan credentials
            with open(AUTH_FILE, 'w') as f:
                json.dump({
                    "name": credentials["name"],
                    "id": credentials["id"],
                    "access_token": credentials["access_token"]
                }, f)
            
            self.credentials = {
                "name": credentials["name"],
                "id": credentials["id"],
                "access_token": credentials["access_token"]
            }
            
            self.user_label.configure(text=f"👤 {credentials['name']}")
            self.log(f"✓ Login berhasil! Selamat datang, {credentials['name']}")
            self.set_status("Login berhasil")
            
        except Exception as e:
            self.log(f"✗ Login gagal: {e}")
            self.set_status("Login gagal")
    
    def logout(self):
        """Logout"""
        if not messagebox.askyesno("Konfirmasi", "Logout dari akun?"):
            return
        
        if AUTH_FILE.exists():
            AUTH_FILE.unlink()
        
        self.credentials = None
        self.user_label.configure(text="Belum login")
        self.log("✓ Logout berhasil")
        self.set_status("Logout berhasil")

def main():
    app = MinecraftLauncherGUI()
    app.mainloop()

if __name__ == "__main__":
    main()