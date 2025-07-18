import time
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import threading
try:
    from tkcalendar import Calendar
    CALENDAR_AVAILABLE = True
except ImportError:
    CALENDAR_AVAILABLE = False

# Modern color scheme - brighter for better readability
PRIMARY_BG = '#121417'
SECONDARY_BG = '#1c1f26'
ACCENT_COLOR = '#f25a70'
PROGRESS_COLOR = '#42b883'
TEXT_COLOR = '#e1e1e1'

class DeathClockGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Death Clock - Time Remaining Calculator")
        self.root.geometry("1920x1080")
        self.root.configure(bg=PRIMARY_BG)
        
        # Variables
        self.death_date = None
        self.birth_date = None
        self.lifespan_years = None
        self.is_running = False
        self.update_thread = None
        self.display_format = tk.StringVar(value="detailed")
        
        # Animation variables for smooth transitions
        self.last_heartbeats = 0
        self.last_breaths = 0
        self.heartbeat_animation_offset = 0
        self.breath_animation_offset = 0
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        # Bigger fonts and clearer colors
        style.configure('Title.TLabel', font=('Helvetica', 26, 'bold'),
                        background=PRIMARY_BG, foreground=ACCENT_COLOR)
        style.configure('Input.TLabel', font=('Helvetica', 14),
                        background=SECONDARY_BG, foreground=TEXT_COLOR)
        style.configure('Clock.TLabel', font=('Courier', 28, 'bold'),
                        background='#000000', foreground='#00ff41')
        style.configure('Time.TLabel', font=('Helvetica', 22, 'bold'),
                        background=SECONDARY_BG, foreground=ACCENT_COLOR)
        style.configure('Stats.TLabel', font=('Helvetica', 14),
                        background=SECONDARY_BG, foreground=TEXT_COLOR)
        style.configure('Vital.TLabel', font=('Helvetica', 14),
                        background=SECONDARY_BG, foreground=ACCENT_COLOR)
        style.configure('Analysis.TLabel', font=('Helvetica', 14),
                        background=SECONDARY_BG, foreground=TEXT_COLOR)
        style.configure('Watermark.TLabel', font=('Helvetica', 12),
                        background=PRIMARY_BG, foreground='#95a5a6')
        style.configure('Custom.TButton', font=('Helvetica', 12, 'bold'))
        style.map('Custom.TButton', background=[('active', '#5aa9ff')])
        style.configure('Life.Horizontal.TProgressbar', troughcolor=SECONDARY_BG,
                        background=PROGRESS_COLOR)

        self.create_widgets()
        
    def get_country_list(self):
        """Return list of countries with life expectancy data"""
        return [
            "Global Average",
            "Japan",
            "Switzerland", 
            "South Korea",
            "Singapore",
            "Spain",
            "Italy",
            "Australia",
            "Iceland",
            "Israel",
            "Sweden",
            "France",
            "Norway",
            "Malta",
            "Netherlands",
            "Austria",
            "Finland",
            "New Zealand",
            "Ireland",
            "United Kingdom",
            "Belgium",
            "Germany",
            "Canada",
            "Luxembourg",
            "Greece",
            "Portugal",
            "Slovenia",
            "Denmark",
            "Cyprus",
            "United States",
            "Czech Republic",
            "Chile",
            "Costa Rica",
            "Poland",
            "Estonia",
            "Panama",
            "Turkey",
            "Albania",
            "Croatia",
            "Uruguay",
            "Cuba",
            "Argentina",
            "Lebanon",
            "China",
            "Brazil",
            "Thailand",
            "Iran",
            "Mexico",
            "Colombia",
            "Algeria",
            "Tunisia",
            "Ecuador",
            "Sri Lanka",
            "Morocco",
            "Peru",
            "Jordan",
            "Armenia",
            "Vietnam",
            "Venezuela",
            "Egypt",
            "Libya",
            "Paraguay",
            "Ukraine",
            "Philippines",
            "El Salvador",
            "Honduras",
            "Guatemala",
            "Bolivia",
            "Nepal",
            "Nicaragua",
            "Bangladesh",
            "Cambodia",
            "India",
            "Pakistan",
            "Myanmar",
            "Kenya",
            "Ghana",
            "Tanzania",
            "Uganda",
            "Rwanda",
            "Ethiopia",
            "Madagascar",
            "Senegal",
            "Mali",
            "Burkina Faso",
            "Niger",
            "Chad",
            "Nigeria",
            "South Africa",
            "Zimbabwe",
            "Botswana",
            "Zambia",
            "Mozambique",
            "Angola",
            "Sierra Leone",
            "Central African Republic"
        ]
    
    def get_life_expectancy(self, country, gender):
        """Get life expectancy based on country and gender"""
        # Life expectancy data (2023 estimates) - [Male, Female]
        life_expectancy_data = {
            "Global Average": [70.8, 75.9],
            "Japan": [81.5, 87.6],
            "Switzerland": [81.8, 85.5],
            "South Korea": [79.3, 85.4],
            "Singapore": [81.0, 85.7],
            "Spain": [80.7, 86.2],
            "Italy": [81.2, 85.6],
            "Australia": [81.2, 85.3],
            "Iceland": [80.5, 84.8],
            "Israel": [79.9, 84.1],
            "Sweden": [80.8, 84.7],
            "France": [79.8, 85.8],
            "Norway": [80.5, 84.4],
            "Malta": [79.8, 84.5],
            "Netherlands": [80.1, 83.8],
            "Austria": [79.0, 84.1],
            "Finland": [78.8, 84.5],
            "New Zealand": [80.2, 83.5],
            "Ireland": [79.9, 83.5],
            "United Kingdom": [79.2, 82.9],
            "Belgium": [79.2, 84.1],
            "Germany": [78.7, 83.4],
            "Canada": [80.0, 84.0],
            "Luxembourg": [79.8, 84.6],
            "Greece": [78.4, 83.8],
            "Portugal": [78.9, 84.9],
            "Slovenia": [78.3, 84.3],
            "Denmark": [78.9, 82.9],
            "Cyprus": [79.2, 83.1],
            "United States": [76.4, 81.2],
            "Czech Republic": [76.1, 82.1],
            "Chile": [77.2, 82.4],
            "Costa Rica": [77.8, 82.2],
            "Poland": [74.0, 81.6],
            "Estonia": [74.4, 82.4],
            "Panama": [76.2, 81.8],
            "Turkey": [76.2, 81.3],
            "Albania": [76.9, 80.9],
            "Croatia": [75.4, 81.2],
            "Uruguay": [74.5, 81.2],
            "Cuba": [77.2, 81.9],
            "Argentina": [73.0, 79.8],
            "Lebanon": [77.4, 81.3],
            "China": [75.1, 80.5],
            "Brazil": [72.2, 79.4],
            "Thailand": [72.6, 80.0],
            "Iran": [74.2, 77.6],
            "Mexico": [72.1, 77.7],
            "Colombia": [73.0, 79.0],
            "Algeria": [75.9, 78.3],
            "Tunisia": [74.2, 78.7],
            "Ecuador": [74.1, 79.5],
            "Sri Lanka": [73.1, 79.2],
            "Morocco": [74.0, 77.3],
            "Peru": [73.7, 79.1],
            "Jordan": [72.7, 76.1],
            "Armenia": [71.6, 78.9],
            "Vietnam": [71.7, 80.9],
            "Venezuela": [69.2, 77.2],
            "Egypt": [70.2, 74.1],
            "Libya": [70.2, 75.9],
            "Paraguay": [71.7, 77.2],
            "Ukraine": [67.0, 76.9],
            "Philippines": [67.5, 75.0],
            "El Salvador": [70.4, 78.1],
            "Honduras": [72.3, 76.9],
            "Guatemala": [71.2, 76.8],
            "Bolivia": [67.5, 72.4],
            "Nepal": [69.0, 71.9],
            "Nicaragua": [72.4, 78.1],
            "Bangladesh": [71.2, 74.2],
            "Cambodia": [67.1, 71.1],
            "India": [68.4, 70.7],
            "Pakistan": [66.1, 68.4],
            "Myanmar": [64.8, 69.8],
            "Kenya": [61.4, 66.2],
            "Ghana": [62.4, 64.7],
            "Tanzania": [63.1, 67.3],
            "Uganda": [61.7, 65.4],
            "Rwanda": [67.3, 71.7],
            "Ethiopia": [64.9, 68.9],
            "Madagascar": [64.5, 67.8],
            "Senegal": [66.3, 70.1],
            "Mali": [57.3, 59.8],
            "Burkina Faso": [59.3, 61.4],
            "Niger": [60.4, 62.1],
            "Chad": [52.5, 55.4],
            "Nigeria": [53.4, 55.7],
            "South Africa": [62.3, 68.5],
            "Zimbabwe": [59.3, 63.4],
            "Botswana": [66.1, 72.4],
            "Zambia": [61.2, 65.1],
            "Mozambique": [58.8, 64.2],
            "Angola": [59.3, 64.4],
            "Sierra Leone": [52.2, 55.7],
            "Central African Republic": [51.0, 55.7]
        }
        
        data = life_expectancy_data.get(country, life_expectancy_data["Global Average"])
        return data[0] if gender == "Male" else data[1]
    
    def open_calendar(self):
        """Open calendar widget for date selection"""
        if not CALENDAR_AVAILABLE:
            messagebox.showwarning("Calendar Not Available", "Please install tkcalendar package")
            return
            
        # Create calendar popup window
        cal_window = tk.Toplevel(self.root)
        cal_window.title("Select Birth Date")
        cal_window.geometry("300x250")
        cal_window.configure(bg=SECONDARY_BG)
        cal_window.transient(self.root)
        cal_window.grab_set()
        
        # Center the window
        cal_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Calendar widget
        cal = Calendar(
            cal_window,
            selectmode='day',
            background=SECONDARY_BG,
            foreground='white',
            bordercolor=PRIMARY_BG,
            headersbackground=PRIMARY_BG,
            headersforeground='white',
            selectbackground=ACCENT_COLOR,
            selectforeground='white'
        )
        cal.pack(pady=20, padx=20)
        
        def select_date():
            selected_date = cal.get_date()
            # Convert from MM/DD/YY to DD/MM/YYYY format
            try:
                date_obj = datetime.strptime(selected_date, "%m/%d/%y")
                formatted_date = date_obj.strftime("%d/%m/%Y")
                self.birth_date_entry.delete(0, tk.END)
                self.birth_date_entry.insert(0, formatted_date)
                cal_window.destroy()
            except:
                messagebox.showerror("Error", "Invalid date selected")
        
        # Buttons
        btn_frame = tk.Frame(cal_window, bg=SECONDARY_BG)
        btn_frame.pack(pady=10)
        
        select_btn = ttk.Button(btn_frame, text="Select", command=select_date)
        select_btn.pack(side='left', padx=5)
        
        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=cal_window.destroy)
        cancel_btn.pack(side='left', padx=5)
        
    def create_widgets(self):
        # Menu bar for basic actions
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        # Title
        title_label = ttk.Label(self.root, text="💀 DEATH CLOCK CALCULATOR 💀", style='Title.TLabel')
        title_label.pack(pady=25)
        
        # Input frame with better styling
        input_frame = tk.Frame(self.root, bg=SECONDARY_BG, relief='groove', bd=2)
        input_frame.pack(pady=20, padx=30, fill='x')
        
        input_title = ttk.Label(
            input_frame,
            text="📝 PERSONAL INFORMATION",
            font=('Helvetica', 14, 'bold'),
            background=SECONDARY_BG,
            foreground=TEXT_COLOR,
        )
        input_title.grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(input_frame, text="Date of Birth:", style='Input.TLabel').grid(row=1, column=0, padx=15, pady=8, sticky='w')
        
        # Date input with calendar option
        date_input_frame = tk.Frame(input_frame, bg=SECONDARY_BG)
        date_input_frame.grid(row=1, column=1, padx=15, pady=8, sticky='w')
        
        self.birth_date_entry = ttk.Entry(date_input_frame, font=('Arial', 13), width=15)
        self.birth_date_entry.pack(side='left', padx=(0, 5))
        
        # Calendar button
        if CALENDAR_AVAILABLE:
            calendar_btn = ttk.Button(date_input_frame, text="📅", width=3, command=self.open_calendar)
            calendar_btn.pack(side='left')
            
        # Format hint
        format_hint = ttk.Label(
            input_frame,
            text="(DD/MM/YYYY)",
            font=('Helvetica', 12, 'italic'),
            background=SECONDARY_BG,
            foreground='#95a5a6',
        )
        format_hint.grid(row=1, column=2, padx=5, pady=8, sticky='w')
        
        ttk.Label(input_frame, text="Gender:", style='Input.TLabel').grid(row=2, column=0, padx=15, pady=8, sticky='w')
        self.gender_var = tk.StringVar(value="Male")
        gender_frame = tk.Frame(input_frame, bg=SECONDARY_BG)
        gender_frame.grid(row=2, column=1, padx=15, pady=8, sticky='w')
        ttk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="Male").pack(side='left', padx=5)
        ttk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="Female").pack(side='left', padx=5)
        
        ttk.Label(input_frame, text="Country/Region:", style='Input.TLabel').grid(row=3, column=0, padx=15, pady=8, sticky='w')
        self.country_var = tk.StringVar(value="Global Average")
        self.country_combo = ttk.Combobox(input_frame, textvariable=self.country_var, font=('Arial', 12), width=16, state="readonly")
        self.country_combo['values'] = self.get_country_list()
        self.country_combo.grid(row=3, column=1, padx=15, pady=8)
        
        ttk.Label(input_frame, text="Custom Lifespan (optional):", style='Input.TLabel').grid(row=4, column=0, padx=15, pady=8, sticky='w')
        self.lifespan_var = tk.StringVar(value="")
        self.lifespan_entry = ttk.Entry(input_frame, textvariable=self.lifespan_var, font=('Arial', 13), width=18)
        self.lifespan_entry.grid(row=4, column=1, padx=15, pady=8)
        
        # Calculate button
        calculate_btn = ttk.Button(input_frame, text="⚡ CALCULATE & START", command=self.calculate_death_date, style='Custom.TButton')
        calculate_btn.grid(row=5, column=0, columnspan=2, pady=15)
        
        # Display format selection - more compact
        format_frame = tk.Frame(self.root, bg=PRIMARY_BG)
        format_frame.pack(pady=15)
        
        ttk.Label(
            format_frame,
            text="🎯 Display Format:",
            font=('Helvetica', 13, 'bold'),
            background=PRIMARY_BG,
            foreground=TEXT_COLOR,
        ).pack()
        
        # Create a more compact radio button layout
        radio_frame = tk.Frame(format_frame, bg=PRIMARY_BG)
        radio_frame.pack(pady=5)

        format_options = [
            ("Detailed", "detailed"),
            ("Years & Days", "years_days"),
            ("Weeks & Days", "weeks_days"),
            ("Days & Hours", "days_hours"),
            ("Total Weeks", "total_weeks"),
            ("Total Days", "total_days"),
            ("Total Hours", "total_hours"),
            ("Total Minutes", "total_minutes"),
            ("Total Seconds", "total_seconds")
        ]
        
        for i, (text, value) in enumerate(format_options):
            ttk.Radiobutton(radio_frame, text=text, variable=self.display_format, value=value,
                           command=self.update_display_format).grid(row=i//3, column=i%3, padx=10, pady=2, sticky='w')
        
        # Death date display
        self.death_date_label = ttk.Label(self.root, text="", style='Input.TLabel')
        self.death_date_label.pack(pady=8)
        
        # Main time information frame - enhanced styling
        time_info_frame = tk.Frame(self.root, bg=SECONDARY_BG, relief='sunken', bd=3)
        time_info_frame.pack(pady=15, padx=20, fill='x')
        

        # Add a subtle border effect around the clock
        clock_border = tk.Frame(countdown_frame, bg='#00ff41', height=2)
        clock_border.pack(fill='x', padx=50, pady=(0, 15))
        
        # Life progress display
        progress_frame = tk.Frame(time_info_frame, bg=SECONDARY_BG)
        progress_frame.pack(pady=10, fill='x')
        
        self.life_progress_label = ttk.Label(progress_frame, text="", style='Input.TLabel')
        self.life_progress_label.pack()
        self.life_progress_bar = ttk.Progressbar(
            progress_frame,
            style='Life.Horizontal.TProgressbar',
            length=400,
            maximum=100,
        )
        self.life_progress_bar.pack(pady=5)

        # Insights displayed directly under the countdown
        self.insights_label = ttk.Label(countdown_frame, text="", style='Analysis.TLabel')
        self.insights_label.pack(pady=(0, 15))
        
        # Statistics and Analysis Section - Enhanced with larger size
        stats_frame = tk.Frame(time_info_frame, bg=SECONDARY_BG, relief='raised', bd=4)
        stats_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        stats_title = ttk.Label(
            stats_frame,
            text="📊 COMPREHENSIVE STATISTICAL ANALYSIS",
            font=('Helvetica', 20, 'bold'),
            background=SECONDARY_BG,
            foreground='#f39c12',
        )
        stats_title.pack(pady=15)
        
        # Create multiple rows for better organization with increased spacing
        stats_row1 = tk.Frame(stats_frame, bg=SECONDARY_BG)
        stats_row1.pack(pady=12, fill='x', padx=20)
        
        self.time_stats_label = ttk.Label(stats_row1, text="", style='Stats.TLabel')
        self.time_stats_label.pack(pady=8)
        
        stats_row2 = tk.Frame(stats_frame, bg=SECONDARY_BG)
        stats_row2.pack(pady=12, fill='x', padx=20)
        
        # Vital signs with larger, more prominent display
        self.vital_stats_label = ttk.Label(stats_row2, text="", style='Vital.TLabel')
        self.vital_stats_label.pack(pady=10)
        
        stats_row3 = tk.Frame(stats_frame, bg=SECONDARY_BG)
        stats_row3.pack(pady=12, fill='x', padx=20)
        
        self.analysis_label = ttk.Label(stats_row3, text="", style='Analysis.TLabel')
        self.analysis_label.pack(pady=8)
        
        stats_row4 = tk.Frame(stats_frame, bg=SECONDARY_BG)
        stats_row4.pack(pady=12, fill='x', padx=20)
        
        self.demographic_label = ttk.Label(stats_row4, text="", style='Analysis.TLabel')
        self.demographic_label.pack(pady=8)
        
        stats_row5 = tk.Frame(stats_frame, bg=SECONDARY_BG)
        stats_row5.pack(pady=12, fill='x', padx=20)
        
        self.milestones_label = ttk.Label(stats_row5, text="", style='Analysis.TLabel')
        self.milestones_label.pack(pady=8)
        
        # New enhanced analysis sections
        stats_row6 = tk.Frame(stats_frame, bg=SECONDARY_BG)
        stats_row6.pack(pady=12, fill='x', padx=20)
        
        self.life_quality_label = ttk.Label(stats_row6, text="", style='Analysis.TLabel')
        self.life_quality_label.pack(pady=8)
        
        stats_row7 = tk.Frame(stats_frame, bg=SECONDARY_BG)
        stats_row7.pack(pady=12, fill='x', padx=20)
        
        self.perspective_label = ttk.Label(stats_row7, text="", style='Analysis.TLabel')
        self.perspective_label.pack(pady=8)
        
        # Additional fun facts section
        stats_row8 = tk.Frame(stats_frame, bg=SECONDARY_BG)
        stats_row8.pack(pady=12, fill='x', padx=20)
        
        self.fun_facts_label = ttk.Label(stats_row8, text="", style='Analysis.TLabel')
        self.fun_facts_label.pack(pady=(8, 25))
        
        # Control buttons - simplified
        button_frame = tk.Frame(self.root, bg=PRIMARY_BG)
        button_frame.pack(pady=20)
        
        self.stop_btn = ttk.Button(button_frame, text="⏸️ PAUSE COUNTDOWN", command=self.stop_countdown, style='Custom.TButton')
        self.stop_btn.pack(side='left', padx=15)
        
        self.restart_btn = ttk.Button(button_frame, text="🔄 RESTART", command=self.restart_countdown, style='Custom.TButton')
        self.restart_btn.pack(side='left', padx=15)

        self.copy_btn = ttk.Button(button_frame, text="📋 COPY STATS", command=self.copy_stats, style='Custom.TButton')
        self.copy_btn.pack(side='left', padx=15)

        self.reset_btn = ttk.Button(button_frame, text="🗑️ RESET", command=self.reset_fields, style='Custom.TButton')
        self.reset_btn.pack(side='left', padx=15)
        
        # Status label
        self.status_label = ttk.Label(
            self.root,
            text="Ready - Enter your details above",
            font=('Helvetica', 10, 'italic'),
            background=PRIMARY_BG,
            foreground='#95a5a6',
        )
        self.status_label.pack(pady=8)
        
        # Watermark at the bottom
        watermark_frame = tk.Frame(self.root, bg=PRIMARY_BG)
        watermark_frame.pack(side='bottom', fill='x')
        
        watermark_label = ttk.Label(watermark_frame, text="Created by Eran", style='Watermark.TLabel')
        watermark_label.pack(side='bottom', padx=20, pady=5)

    def show_about(self):
        """Display application information"""
        messagebox.showinfo(
            "About",
            "Death Clock\nEstimate your remaining time.\nCreated by Eran",
        )

    def calculate_death_date(self):
        try:
            birth_date_str = self.birth_date_entry.get().strip()
            custom_lifespan_str = self.lifespan_var.get().strip()
            gender = self.gender_var.get()
            country = self.country_var.get()
            
            if not birth_date_str:
                messagebox.showerror("Error", "Please enter your date of birth")
                return
            
            birth_date = datetime.strptime(birth_date_str, "%d/%m/%Y")
            
            # Use custom lifespan if provided, otherwise use demographic data
            if custom_lifespan_str:
                lifespan_years = float(custom_lifespan_str)
                if lifespan_years <= 0:
                    messagebox.showerror("Error", "Lifespan must be positive")
                    return
            else:
                lifespan_years = self.get_life_expectancy(country, gender)
                
            self.birth_date = birth_date
            self.lifespan_years = lifespan_years
            self.gender = gender
            self.country = country
            self.death_date = birth_date + timedelta(days=lifespan_years * 365.25)
            
            # Show demographic info
            demo_info = f"📍 {country} | {gender} | Life expectancy: {lifespan_years:.1f} years"
            if custom_lifespan_str:
                demo_info += " (Custom)"
            
            self.death_date_label.config(text=f"⚰️ Estimated death date: {self.death_date.strftime('%d/%m/%Y %H:%M:%S')}")
            self.status_label.config(text=f"✅ {demo_info}")

            # Update life progress info
            self.update_life_progress()
            
            # Show initial countdown and start timer automatically
            self.update_static_countdown()
            self.start_countdown_automatically()
            
        except ValueError as e:
            if "time data" in str(e):
                messagebox.showerror("Error", "Invalid date format. Please use DD/MM/YYYY")
            else:
                messagebox.showerror("Error", "Invalid lifespan value. Please enter a number")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def update_life_progress(self):
        if not hasattr(self, 'birth_date') or not hasattr(self, 'lifespan_years'):
            return
            
        now = datetime.now()
        total_life_seconds = self.lifespan_years * 365.25 * 24 * 3600
        lived_seconds = (now - self.birth_date).total_seconds()
        
        if lived_seconds < 0:
            self.life_progress_label.config(text="⚠️ Birth date is in the future!")
            return
            
        progress_percentage = (lived_seconds / total_life_seconds) * 100
        age_years = lived_seconds / (365.25 * 24 * 3600)
        
        self.life_progress_bar['value'] = progress_percentage
        self.life_progress_label.config(
            text=f"Life Progress: {progress_percentage:.1f}% | Age: {age_years:.1f} years"
        )
    
    def update_static_countdown(self):
        """Update the countdown display once without starting the timer"""
        if not self.death_date:
            return
            
        now = datetime.now()
        time_left = self.death_date - now
        
        if time_left.total_seconds() <= 0:
            self.countdown_label.config(text="⚰️ YOUR TIME HAS EXPIRED! LIVE EVERY MOMENT! ⚰️")
            self.time_stats_label.config(text="")
            self.analysis_label.config(text="")
            self.demographic_label.config(text="")
            self.milestones_label.config(text="")
            return
        
        # Update main countdown
        formatted_time = self.format_time_display(time_left)
        self.countdown_label.config(text=formatted_time)
        
        # Add color effects to countdown based on urgency (same as clock)
        total_seconds = int(time_left.total_seconds())
        days = total_seconds // (24 * 3600)
        
        if days <= 7:  # Less than a week - bright red alert
            self.countdown_label.config(foreground='#ff0000')
        elif days <= 30:  # Less than a month - orange warning
            self.countdown_label.config(foreground='#ff8800')
        elif days <= 365:  # Less than a year - yellow caution
            self.countdown_label.config(foreground='#f1c40f')
        else:  # Normal blue instead of red
            self.countdown_label.config(foreground='#3498db')
        
        # Update statistics and analysis
        self.update_statistics_and_analysis(time_left)
    
    
    def update_statistics_and_analysis(self, time_left):
        """Update comprehensive statistics and analysis with smooth animations"""
        total_seconds = int(time_left.total_seconds())
        
        # Basic time statistics
        total_minutes = total_seconds // 60
        total_hours = total_seconds // 3600
        total_days = total_seconds // (24 * 3600)
        total_weeks = total_days // 7
        total_months = total_days // 30.44
        total_years = total_days // 365.25
        
        # Life percentage calculations
        if hasattr(self, 'lifespan_years'):
            total_life_seconds = self.lifespan_years * 365.25 * 24 * 3600
            remaining_percentage = (total_seconds / total_life_seconds) * 100
            lived_percentage = 100 - remaining_percentage
            
            # Current age
            now = datetime.now()
            lived_seconds = (now - self.birth_date).total_seconds()
            current_age = lived_seconds / (365.25 * 24 * 3600)
            
            # Basic stats
            stats_text = (f"⏰ {total_years:.1f} years | {total_months:.0f} months | {total_weeks:.0f} weeks | "
                         f"{total_days:,} days | {remaining_percentage:.1f}% remaining")
            self.time_stats_label.config(text=stats_text)
            
            # Enhanced vital signs with smooth animation
            heartbeats_remaining = total_seconds * 70  # Average 70 bpm
            breaths_remaining = total_seconds * 15     # Average 15 breaths per minute
            
            # Smooth transition for vital signs
            if self.last_heartbeats == 0:
                self.last_heartbeats = heartbeats_remaining
                self.last_breaths = breaths_remaining
            
            # Animate the transition
            heartbeat_diff = abs(heartbeats_remaining - self.last_heartbeats)
            breath_diff = abs(breaths_remaining - self.last_breaths)
            
            if heartbeat_diff > 100:  # Smooth large changes
                self.heartbeat_animation_offset = heartbeat_diff * 0.1
            if breath_diff > 20:
                self.breath_animation_offset = breath_diff * 0.1
            
            # Apply animation offset for smooth counting
            display_heartbeats = int(heartbeats_remaining + self.heartbeat_animation_offset)
            display_breaths = int(breaths_remaining + self.breath_animation_offset)
            
            # Gradually reduce animation offset
            self.heartbeat_animation_offset *= 0.95
            self.breath_animation_offset *= 0.95
            
            # Update last values
            self.last_heartbeats = heartbeats_remaining
            self.last_breaths = breaths_remaining
            
            # Add heartbeat and breath rhythm indicators
            import math
            rhythm_indicator = "💓" if int(total_seconds) % 2 == 0 else "🖤"
            breath_indicator = "🫁" if int(total_seconds) % 4 < 2 else "💨"
            
            vital_text = (f"{rhythm_indicator} ~{display_heartbeats:,} heartbeats left | "
                         f"{breath_indicator} ~{display_breaths:,} breaths left | "
                         f"🎂 Current age: {current_age:.1f} years")
            self.vital_stats_label.config(text=vital_text)
            
            # Enhanced analysis with more insights
            sleep_hours_remaining = total_hours // 3  # Assuming 8 hours sleep per day
            awake_hours_remaining = total_hours - sleep_hours_remaining
            meals_remaining = total_days * 3  # 3 meals per day
            weekends_remaining = total_weeks * 2  # 2 weekend days per week
            
            work_hours_remaining = total_days * 8
            vacation_days_remaining = int(total_years * 20)
            tv_episodes_remaining = total_hours  # Assuming 1h episodes
            workout_sessions = total_days // 2  # Workout every other day

            analysis_text = (
                f"😴 ~{sleep_hours_remaining:,} hours of sleep | "
                f"☀️ ~{awake_hours_remaining:,} awake hours | "
                f"🍽️ ~{meals_remaining:,} meals | "
                f"🎉 ~{weekends_remaining:,} weekend days | "
                f"💼 ~{work_hours_remaining:,} work hours | "
                f"✈️ ~{vacation_days_remaining:,} vacation days | "
                f"📺 ~{tv_episodes_remaining:,} TV episodes | "
                f"🏋️ ~{workout_sessions:,} workouts"
            )
            self.analysis_label.config(text=analysis_text)
            
            # Demographic comparisons
            if hasattr(self, 'gender') and hasattr(self, 'country'):
                global_male = self.get_life_expectancy("Global Average", "Male")
                global_female = self.get_life_expectancy("Global Average", "Female")
                global_avg = (global_male + global_female) / 2
                
                # Compare to global average
                vs_global = self.lifespan_years - global_avg
                vs_global_text = f"+{vs_global:.1f}" if vs_global > 0 else f"{vs_global:.1f}"
                
                # Compare to opposite gender in same country
                opposite_gender = "Female" if self.gender == "Male" else "Male"
                opposite_expectancy = self.get_life_expectancy(self.country, opposite_gender)
                vs_opposite = self.lifespan_years - opposite_expectancy
                vs_opposite_text = f"+{vs_opposite:.1f}" if vs_opposite > 0 else f"{vs_opposite:.1f}"
                
                demographic_text = (f"🌍 vs Global avg: {vs_global_text} years | "
                                  f"⚥ vs {opposite_gender} in {self.country}: {vs_opposite_text} years | "
                                  f"🏆 Rank: {'Above' if vs_global > 0 else 'Below'} average")
                self.demographic_label.config(text=demographic_text)
            
            # Milestones and insights
            years_left = total_years
            milestones = []
            
            if years_left >= 10:
                milestones.append(f"🎯 {int(years_left//10)} more decades")
            if years_left >= 5:
                milestones.append(f"🌟 {int(years_left//5)} five-year periods")
            if years_left >= 1:
                milestones.append(f"📅 {int(years_left)} more years")
            
            # Add perspective comparisons
            if total_days > 365:
                milestones.append(f"⭐ {total_days//365} more birthdays")
            if total_weeks > 52:
                milestones.append(f"📆 {total_weeks//52} more years of weekends")
                
            milestone_text = " | ".join(milestones[:3]) if milestones else "⚡ Less than a year remaining"
            self.milestones_label.config(text=milestone_text)
            
            # New life quality metrics
            books_readable = total_days // 7  # 1 book per week
            movies_watchable = total_hours // 2  # 2-hour movies
            conversations = total_days * 5  # 5 meaningful conversations per day
            steps_remaining = total_days * 8000  # Average 8000 steps per day
            
            quality_text = (f"📚 ~{books_readable:,} books to read | "
                           f"🎬 ~{movies_watchable:,} movies to watch | "
                           f"💬 ~{conversations:,} conversations | "
                           f"👟 ~{steps_remaining:,} steps to take")
            self.life_quality_label.config(text=quality_text)
            
            # Enhanced perspective and fascinating facts - optimized for long lifetimes
            coffee_cups = total_days * 2  # 2 cups per day
            sunrises = total_days  # One per day
            hugs_possible = total_days * 3  # 3 hugs per day
            laughs_remaining = total_days * 15  # 15 laughs per day
            photos_to_take = total_days * 10  # 10 photos per day
            songs_to_hear = total_hours * 15  # 15 songs per hour awake
            
            # Scale perspective messages for different time ranges
            if total_years > 50:
                perspective = (f"🌟 Over {total_years:.0f} years ahead! Epic lifetime for: ☕ {coffee_cups:,} coffee moments, "
                             f"🌅 {sunrises:,} sunrises, 🤗 {hugs_possible:,} warm hugs, 😂 {laughs_remaining:,} joyful laughs")
            elif total_years > 25:
                perspective = (f"🚀 {total_years:.0f} years ahead! Enough time for: 🎵 {songs_to_hear:,} songs, "
                             f"📸 {photos_to_take:,} precious photos, ☕ {coffee_cups:,} shared coffee moments")
            elif total_days > 1000:
                perspective = (f"🌱 Over 1,000 days ahead! Time for: ☕ {coffee_cups:,} coffees, "
                             f"🌅 {sunrises:,} sunrises, 🤗 {hugs_possible:,} hugs, 😂 {laughs_remaining:,} laughs")
            elif total_days > 365:
                perspective = (f"🌱 Multiple seasons ahead! Time for: 🎵 {songs_to_hear:,} songs, "
                             f"📸 {photos_to_take:,} photos, ☕ {coffee_cups:,} coffee moments")
            elif total_days > 100:
                perspective = (f"⚡ Focused time ahead! Potential for: 🤗 {hugs_possible:,} hugs, "
                             f"😂 {laughs_remaining:,} moments of laughter, 🌅 {sunrises:,} beautiful sunrises")
            elif total_days > 30:
                perspective = (f"🔥 Precious weeks ahead! Cherish: ☕ {coffee_cups:,} warm drinks, "
                             f"🎵 {songs_to_hear:,} amazing songs, 📸 {photos_to_take:,} memories to capture")
            else:
                perspective = (f"💎 Every moment is precious! Savor: 🤗 {hugs_possible:,} hugs, "
                             f"😂 {laughs_remaining:,} laughs, 🌅 {sunrises:,} sunrises - make them count!")
                
            self.perspective_label.config(text=perspective)
            
            # Additional fun facts and comparisons - enhanced for all lifespans
            blinks_remaining = total_seconds * 0.33  # About 20 blinks per minute
            words_to_speak = total_days * 16000  # Average 16,000 words per day
            dreams_remaining = total_days * 4  # Average 4 dreams per night
            years_in_space = total_years  # If you were on the International Space Station
            distance_walked_km = steps_remaining * 0.0008

            # Scale the display based on magnitude
            if total_years > 20:
                fun_facts = (f"👁️ ~{blinks_remaining/1000000:.1f}M blinks ahead | "
                            f"🗣️ ~{words_to_speak/1000000:.1f}M words to speak | "
                            f"💭 ~{dreams_remaining:,} dreams to have | "
                            f"🚀 {years_in_space:.1f} years in orbit | "
                            f"🎧 ~{songs_to_hear:,} songs | "
                            f"🚶 ~{distance_walked_km:,.0f} km to walk")
            else:
                fun_facts = (f"👁️ ~{blinks_remaining:,.0f} blinks ahead | "
                            f"🗣️ ~{words_to_speak:,} words to speak | "
                            f"💭 ~{dreams_remaining:,} dreams to have | "
                            f"🚀 {years_in_space:.1f} years in orbit | "
                            f"🎧 ~{songs_to_hear:,} songs | "
                            f"🚶 ~{distance_walked_km:,.0f} km to walk")
            self.fun_facts_label.config(text=fun_facts)

            # Show combined insights under the countdown
            self.insights_label.config(text=f"{analysis_text} | {fun_facts}")
        
    def start_countdown_automatically(self):
        """Start countdown automatically after calculation"""
        if not self.death_date:
            return
            
        if self.is_running:
            return
            
        self.is_running = True
        self.status_label.config(text="🔥 Countdown running... Time is ticking!")
        self.update_thread = threading.Thread(target=self.update_countdown, daemon=True)
        self.update_thread.start()
    
    def restart_countdown(self):
        """Restart the countdown"""
        if self.death_date:
            self.stop_countdown()
            self.start_countdown_automatically()
        else:
            messagebox.showwarning("Warning", "Please calculate death date first")
    
    def start_countdown(self):
        if not self.death_date:
            messagebox.showwarning("Warning", "Please calculate death date first")
            return
            
        if self.is_running:
            messagebox.showinfo("Info", "Countdown is already running")
            return
            
        self.is_running = True
        self.status_label.config(text="Countdown running...")
        self.update_thread = threading.Thread(target=self.update_countdown, daemon=True)
        self.update_thread.start()
    
    def stop_countdown(self):
        self.is_running = False
        self.status_label.config(text="⏸️ Countdown paused")

    def copy_stats(self):
        """Copy current statistics to clipboard"""
        if not self.death_date:
            messagebox.showinfo("Info", "No data to copy. Calculate first.")
            return
        stats = "\n".join([
            self.time_stats_label.cget("text"),
            self.vital_stats_label.cget("text"),
            self.analysis_label.cget("text"),
            self.demographic_label.cget("text"),
            self.milestones_label.cget("text"),
            self.life_quality_label.cget("text"),
            self.perspective_label.cget("text"),
            self.fun_facts_label.cget("text"),
            self.insights_label.cget("text"),
        ])
        self.root.clipboard_clear()
        self.root.clipboard_append(stats)
        messagebox.showinfo("Copied", "Statistics copied to clipboard")

    def reset_fields(self):
        """Reset input fields and clear data"""
        self.stop_countdown()
        self.birth_date_entry.delete(0, tk.END)
        self.lifespan_entry.delete(0, tk.END)
        self.gender_var.set("Male")
        self.country_var.set("Global Average")
        self.death_date_label.config(text="")
        for lbl in [
            self.countdown_label,
            self.time_stats_label,
            self.analysis_label,
            self.demographic_label,
            self.milestones_label,
            self.life_quality_label,
            self.perspective_label,
            self.fun_facts_label,
            self.insights_label,
        ]:
            lbl.config(text="")
        self.status_label.config(text="Ready - Enter your details above")
        self.life_progress_label.config(text="")
        self.life_progress_bar["value"] = 0
    
    def update_countdown(self):
        while self.is_running:
            try:
                now = datetime.now()
                time_left = self.death_date - now
                
                if time_left.total_seconds() <= 0:
                    self.root.after(0, lambda: self.countdown_label.config(text="⚰️ YOUR TIME HAS EXPIRED! LIVE EVERY MOMENT! ⚰️"))
                    self.root.after(0, lambda: self.time_stats_label.config(text=""))
                    self.root.after(0, lambda: self.analysis_label.config(text=""))
                    self.root.after(0, lambda: self.demographic_label.config(text=""))
                    self.root.after(0, lambda: self.milestones_label.config(text=""))
                    self.root.after(0, lambda: self.insights_label.config(text=""))
                    self.is_running = False
                    self.root.after(0, lambda: self.status_label.config(text="💀 Time expired"))
                    break
                
                # Update main countdown
                formatted_time = self.format_time_display(time_left)
                self.root.after(0, lambda ft=formatted_time: self.countdown_label.config(text=ft))
                
                # Update countdown color based on urgency
                total_seconds_live = int(time_left.total_seconds())
                days_live = total_seconds_live // (24 * 3600)
                
                if days_live <= 7:  # Less than a week - red alert
                    self.root.after(0, lambda: self.countdown_label.config(foreground='#ff0000'))
                elif days_live <= 30:  # Less than a month - orange warning
                    self.root.after(0, lambda: self.countdown_label.config(foreground='#ff8800'))
                elif days_live <= 365:  # Less than a year - yellow caution
                    self.root.after(0, lambda: self.countdown_label.config(foreground='#f1c40f'))
                else:  # Normal blue instead of red
                    self.root.after(0, lambda: self.countdown_label.config(foreground='#3498db'))
                
                # Update statistics and analysis
                self.root.after(0, lambda tl=time_left: self.update_statistics_and_analysis(tl))
                
                # Update life progress
                self.root.after(0, self.update_life_progress)
                
                time.sleep(1)
            except Exception as e:
                self.root.after(0, lambda: self.status_label.config(text=f"❌ Error: {str(e)}"))
                break
    
    def format_time_display(self, time_left):
        total_seconds = int(time_left.total_seconds())
        
        if self.display_format.get() == "detailed":
            years = total_seconds // (365.25 * 24 * 3600)
            remaining = total_seconds % (365.25 * 24 * 3600)
            months = int(remaining // (30.44 * 24 * 3600))  # Average month length
            remaining = remaining % (30.44 * 24 * 3600)
            days = int(remaining // (24 * 3600))
            remaining = remaining % (24 * 3600)
            hours = remaining // 3600
            remaining = remaining % 3600
            minutes = remaining // 60
            seconds = remaining % 60
            return f"⏳ {int(years)}y {months}m {days}d {hours}h {minutes}min {seconds}s"
            
        elif self.display_format.get() == "years_days":
            years = total_seconds // (365.25 * 24 * 3600)
            days = int((total_seconds % (365.25 * 24 * 3600)) // (24 * 3600))
            return f"⏳ {int(years)} years, {days} days"

        elif self.display_format.get() == "weeks_days":
            weeks = total_seconds // (7 * 24 * 3600)
            days = (total_seconds % (7 * 24 * 3600)) // (24 * 3600)
            return f"⏳ {weeks} weeks, {days} days"

        elif self.display_format.get() == "days_hours":
            days = total_seconds // (24 * 3600)
            hours = (total_seconds % (24 * 3600)) // 3600
            return f"⏳ {days} days, {hours} hours"
            
        elif self.display_format.get() == "hours_minutes":
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"⏳ {hours} hours, {minutes} minutes"
            
        elif self.display_format.get() == "total_weeks":
            weeks = total_seconds // (7 * 24 * 3600)
            return f"⏳ {weeks} total weeks"

        elif self.display_format.get() == "total_days":
            days = total_seconds // (24 * 3600)
            return f"⏳ {days} total days"
            
        elif self.display_format.get() == "total_hours":
            hours = total_seconds // 3600
            return f"⏳ {hours} total hours"
            
        elif self.display_format.get() == "total_minutes":
            minutes = total_seconds // 60
            return f"⏳ {minutes} total minutes"
            
        elif self.display_format.get() == "total_seconds":
            return f"⏳ {total_seconds} total seconds"
    
    def update_display_format(self):
        """Refresh countdown when display format changes"""
        if self.death_date:
            self.update_static_countdown()

def main():
    root = tk.Tk()
    app = DeathClockGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
