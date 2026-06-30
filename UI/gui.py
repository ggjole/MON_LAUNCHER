import customtkinter as ctk
from src.installer import installer_mc as imc
from src.launcher import launcher as lc

ctk.set_appearance_mode("dark")



class Main_windows(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MON LAUNCHER")
        self.geometry("800x500")
        self.minsize(800,500)
        
        self.setup_ui()
        self.current_version = None
    
    def toggle_theme(self):
        if self.theme_switch.get() == 'Dark':
            ctk.set_appearance_mode("dark")
        elif self.theme_switch.get() =='light':
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("system")

    def setup_ui(self):        
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
            command=imc.All_minecraft_version
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
            command=imc.install_vanilla_mc,
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.install_button.pack(side="left", padx=5, pady=10)
        
        self.launch_button = ctk.CTkButton(
            self.button_frame,
            text="🚀 Launch",
            command=lc.launch,
            fg_color="#007bff",
            hover_color="#0056b3"
        )
        self.launch_button.pack(side="left", padx=5, pady=10)
        
        self.login_button = ctk.CTkButton(
            self.button_frame,
            text="🔐 Login",
            command=None,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        self.login_button.pack(side="left", padx=5, pady=10)
        
        self.logout_button = ctk.CTkButton(
            self.button_frame,
            text="🚪 Logout",
            command=None,
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        self.logout_button.pack(side="left", padx=5, pady=10)
        
        # Refresh button
        self.refresh_button = ctk.CTkButton(
            self.button_frame,
            text="🔄 Refresh",
            command=lc._get_all_installed_version,
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


            


if __name__ == "__main__":
    Main_windows()