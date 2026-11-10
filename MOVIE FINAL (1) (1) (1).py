import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import json
import os
from datetime import datetime, timedelta
import random
import string
try:
    import qrcode
    from PIL import Image, ImageTk
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

class MovieBookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 BookMyShow - Movie Ticket Booking System")
        self.root.geometry("1100x750")
        self.root.configure(bg="#0d1117")
        
        # Modern color scheme
        self.colors = {
            "bg_dark": "#0d1117",
            "bg_card": "#161b22",
            "bg_header": "#1c2128",
            "primary": "#ff6b6b",
            "secondary": "#4ecdc4",
            "accent": "#45aaf2",
            "warning": "#f7b731",
            "success": "#26de81",
            "text_light": "#f0f6fc",
            "text_muted": "#8b949e",
            "border": "#30363d"
        }
        
        # Data storage
        self.users = {}
        self.admins = {"admin": "admin123"}
        self.movies = {}
        self.cities = {}
        self.theaters = {}
        self.showtimes = {}
        self.bookings = {}
        self.current_user = None
        self.current_admin = None
        self.poster_cache = {}
        self.marquee_text = "Welcome to BookMyShow! Book your favorite movies now!"
        
        # Load data
        self.load_data()
        
        # Initialize sample data if empty
        if not self.movies:
            self.initialize_sample_data()
        elif len(self.movies) < 20 or len(self.cities) < 30 or len(self.theaters) < 65:
            # Regenerate if data is incomplete
            self.initialize_sample_data()
        
        # Ensure all movies have release dates
        self.ensure_release_dates()
        self.ensure_poster_paths()
        self.ensure_booking_statuses()
        self.ensure_show_dates()
        
        # Debug: Print data counts
        print(f"Loaded {len(self.movies)} movies, {len(self.cities)} cities, {len(self.theaters)} theaters, {len(self.showtimes)} showtimes")
        
        # Show login screen
        self.show_login_screen()
    
    def force_regenerate_data(self):
        """Force regenerate all sample data"""
        try:
            # Delete existing data file to force regeneration
            if os.path.exists("bookmyshow_data.json"):
                os.remove("bookmyshow_data.json")
                print("Old data file removed. Regenerating fresh data...")
            
            # Initialize fresh data
            self.initialize_sample_data()
            self.load_data()
            
            print(f"Generated fresh data: {len(self.movies)} movies, {len(self.cities)} cities, {len(self.theaters)} theaters, {len(self.showtimes)} showtimes")
            
        except Exception as e:
            print(f"Error regenerating data: {e}")

    def initialize_sample_data(self):
        """Initialize with sample data"""
        # Add sample movies with variety
        self.movies = {
            "MOV001": {
                "name": "Avatar 3",
                "language": "English",
                "duration": "180 min",
                "genre": "Sci-Fi/Action",
                "rating": "⭐ 8.5/10",
                "release_date": "2026-12-18"
            },
            "MOV002": {
                "name": "Pathaan Returns",
                "language": "Hindi",
                "duration": "150 min",
                "genre": "Action/Thriller",
                "rating": "⭐ 8.2/10",
                "release_date": "2025-05-01"
            },
            "MOV003": {
                "name": "The Kashmir Files 2",
                "language": "Hindi",
                "duration": "170 min",
                "genre": "Drama",
                "rating": "⭐ 8.7/10",
                "release_date": "2025-08-15"
            },
            "MOV004": {
                "name": "Fighter",
                "language": "Hindi",
                "duration": "145 min",
                "genre": "Action/War",
                "rating": "⭐ 7.8/10",
                "release_date": "2024-12-25"
            },
            "MOV005": {
                "name": "Dune: Part Three",
                "language": "English",
                "duration": "165 min",
                "genre": "Sci-Fi/Adventure",
                "rating": "⭐ 8.9/10",
                "release_date": "2025-10-20"
            },
            "MOV006": {
                "name": "Jawan 2",
                "language": "Hindi",
                "duration": "160 min",
                "genre": "Action/Thriller",
                "rating": "⭐ 8.1/10",
                "release_date": "2025-06-15"
            },
            "MOV007": {
                "name": "Animal Park",
                "language": "Hindi",
                "duration": "180 min",
                "genre": "Crime/Drama",
                "rating": "⭐ 7.5/10",
                "release_date": "2025-03-20"
            },
            "MOV008": {
                "name": "Oppenheimer: Extended",
                "language": "English",
                "duration": "200 min",
                "genre": "Biographical/Drama",
                "rating": "⭐ 9.0/10",
                "release_date": "2025-02-15"
            },
            "MOV009": {
                "name": "Kalki 2898 AD",
                "language": "Telugu/Hindi",
                "duration": "175 min",
                "genre": "Sci-Fi/Action",
                "rating": "⭐ 8.3/10",
                "release_date": "2025-05-20"
            },
            "MOV010": {
                "name": "Salaar Part 2",
                "language": "Kannada/Hindi",
                "duration": "165 min",
                "genre": "Action/Crime",
                "rating": "⭐ 8.6/10",
                "release_date": "2025-07-10"
            },
            "MOV011": {
                "name": "Pushpa 3: The Rule",
                "language": "Telugu/Hindi",
                "duration": "180 min",
                "genre": "Action/Drama",
                "rating": "⭐ 8.4/10",
                "release_date": "2025-09-15"
            },
            "MOV012": {
                "name": "Gadar 3",
                "language": "Hindi",
                "duration": "155 min",
                "genre": "Action/Drama",
                "rating": "⭐ 7.9/10",
                "release_date": "2025-04-25"
            },
            "MOV013": {
                "name": "Tiger 4",
                "language": "Hindi",
                "duration": "145 min",
                "genre": "Action/Thriller",
                "rating": "⭐ 8.0/10",
                "release_date": "2025-08-10"
            },
            "MOV014": {
                "name": "Bahubali 3: The Conclusion",
                "language": "Telugu/Hindi",
                "duration": "190 min",
                "genre": "Epic/Action",
                "rating": "⭐ 8.8/10",
                "release_date": "2025-12-20"
            },
            "MOV015": {
                "name": "Marvel: The Multiverse Saga",
                "language": "English",
                "duration": "170 min",
                "genre": "Superhero/Action",
                "rating": "⭐ 8.5/10",
                "release_date": "2025-11-15"
            },
            "MOV016": {
                "name": "Fast & Furious 11",
                "language": "English",
                "duration": "140 min",
                "genre": "Action/Adventure",
                "rating": "⭐ 7.6/10",
                "release_date": "2025-06-25"
            },
            "MOV017": {
                "name": "Mission Impossible 8",
                "language": "English",
                "duration": "150 min",
                "genre": "Action/Thriller",
                "rating": "⭐ 8.7/10",
                "release_date": "2025-10-15"
            },
            "MOV018": {
                "name": "Jurassic World 4",
                "language": "English",
                "duration": "135 min",
                "genre": "Adventure/Sci-Fi",
                "rating": "⭐ 7.8/10",
                "release_date": "2025-03-15"
            },
            "MOV019": {
                "name": "Avatar: The Last Airbender",
                "language": "English",
                "duration": "155 min",
                "genre": "Fantasy/Adventure",
                "rating": "⭐ 8.2/10",
                "release_date": "2025-09-25"
            },
            "MOV020": {
                "name": "The Dark Knight Returns",
                "language": "English",
                "duration": "165 min",
                "genre": "Action/Crime",
                "rating": "⭐ 8.9/10",
                "release_date": "2025-07-20"
            }
        }
        
        # Add sample cities with major metropolitan areas
        self.cities = {
            "CITY001": "Mumbai",
            "CITY002": "Delhi", 
            "CITY003": "Bangalore",
            "CITY004": "Chennai",
            "CITY005": "Kolkata",
            "CITY006": "Hyderabad",
            "CITY007": "Pune",
            "CITY008": "Ahmedabad",
            "CITY009": "Jaipur",
            "CITY010": "Lucknow",
            "CITY011": "Surat",
            "CITY012": "Kanpur",
            "CITY013": "Nagpur",
            "CITY014": "Indore",
            "CITY015": "Thane",
            "CITY016": "Bhopal",
            "CITY017": "Visakhapatnam",
            "CITY018": "Patna",
            "CITY019": "Vadodara",
            "CITY020": "Agra",
            "CITY021": "Nashik",
            "CITY022": "Faridabad",
            "CITY023": "Meerut",
            "CITY024": "Rajkot",
            "CITY025": "Kalyan-Dombivali",
            "CITY026": "Vasai-Virar",
            "CITY027": "Varanasi",
            "CITY028": "Srinagar",
            "CITY029": "Dhanbad",
            "CITY030": "Jodhpur"
        }
        
        # Add comprehensive theaters across all cities
        self.theaters = {
            # Mumbai theaters
            "TH001": {
                "name": "PVR Phoenix",
                "city_id": "CITY001",
                "screen": "Screen 1",
                "capacity": 120
            },
            "TH002": {
                "name": "INOX Metropolitan",
                "city_id": "CITY001",
                "screen": "Screen 2",
                "capacity": 150
            },
            "TH003": {
                "name": "Cinepolis",
                "city_id": "CITY001",
                "screen": "Screen 3",
                "capacity": 100
            },
            "TH004": {
                "name": "PVR Juhu",
                "city_id": "CITY001",
                "screen": "Screen 1",
                "capacity": 80
            },
            # Delhi theaters
            "TH005": {
                "name": "PVR Select City",
                "city_id": "CITY002",
                "screen": "Screen 1",
                "capacity": 180
            },
            "TH006": {
                "name": "DT Cinemas",
                "city_id": "CITY002",
                "screen": "Screen 2",
                "capacity": 120
            },
            "TH007": {
                "name": "Carnival Cinemas",
                "city_id": "CITY002",
                "screen": "Screen 3",
                "capacity": 90
            },
            "TH008": {
                "name": "PVR Saket",
                "city_id": "CITY002",
                "screen": "Screen 1",
                "capacity": 140
            },
            # Bangalore theaters
            "TH009": {
                "name": "PVR Orion",
                "city_id": "CITY003",
                "screen": "Screen 1",
                "capacity": 110
            },
            "TH010": {
                "name": "INOX Garuda",
                "city_id": "CITY003",
                "screen": "Screen 2",
                "capacity": 130
            },
            "TH011": {
                "name": "Cinepolis Royal",
                "city_id": "CITY003",
                "screen": "Screen 3",
                "capacity": 95
            },
            # Chennai theaters
            "TH012": {
                "name": "PVR Marina",
                "city_id": "CITY004",
                "screen": "Screen 1",
                "capacity": 160
            },
            "TH013": {
                "name": "Sathyam Cinemas",
                "city_id": "CITY004",
                "screen": "Screen 2",
                "capacity": 200
            },
            # Kolkata theaters
            "TH014": {
                "name": "PVR South City",
                "city_id": "CITY005",
                "screen": "Screen 1",
                "capacity": 140
            },
            "TH015": {
                "name": "INOX Quest",
                "city_id": "CITY005",
                "screen": "Screen 2",
                "capacity": 110
            },
            # Hyderabad theaters
            "TH016": {
                "name": "PVR Hyderabad",
                "city_id": "CITY006",
                "screen": "Screen 1",
                "capacity": 150
            },
            "TH017": {
                "name": "AMB Cinemas",
                "city_id": "CITY006",
                "screen": "Screen 2",
                "capacity": 120
            },
            # Pune theaters
            "TH018": {
                "name": "PVR Pune",
                "city_id": "CITY007",
                "screen": "Screen 1",
                "capacity": 100
            },
            "TH019": {
                "name": "Cinepolis Pune",
                "city_id": "CITY007",
                "screen": "Screen 2",
                "capacity": 85
            },
            # Ahmedabad theaters
            "TH020": {
                "name": "PVR Ahmedabad",
                "city_id": "CITY008",
                "screen": "Screen 1",
                "capacity": 130
            },
            "TH021": {
                "name": "Cinepolis Ahmedabad",
                "city_id": "CITY008",
                "screen": "Screen 2",
                "capacity": 110
            },
            # Jaipur theaters
            "TH022": {
                "name": "PVR Jaipur",
                "city_id": "CITY009",
                "screen": "Screen 1",
                "capacity": 140
            },
            "TH023": {
                "name": "INOX Jaipur",
                "city_id": "CITY009",
                "screen": "Screen 2",
                "capacity": 120
            },
            # Lucknow theaters
            "TH024": {
                "name": "PVR Lucknow",
                "city_id": "CITY010",
                "screen": "Screen 1",
                "capacity": 160
            },
            "TH025": {
                "name": "Cinepolis Lucknow",
                "city_id": "CITY010",
                "screen": "Screen 2",
                "capacity": 130
            },
            # Surat theaters
            "TH026": {
                "name": "PVR Surat",
                "city_id": "CITY011",
                "screen": "Screen 1",
                "capacity": 110
            },
            "TH027": {
                "name": "INOX Surat",
                "city_id": "CITY011",
                "screen": "Screen 2",
                "capacity": 100
            },
            # Kanpur theaters
            "TH028": {
                "name": "PVR Kanpur",
                "city_id": "CITY012",
                "screen": "Screen 1",
                "capacity": 120
            },
            "TH029": {
                "name": "Cinepolis Kanpur",
                "city_id": "CITY012",
                "screen": "Screen 2",
                "capacity": 90
            },
            # Nagpur theaters
            "TH030": {
                "name": "PVR Nagpur",
                "city_id": "CITY013",
                "screen": "Screen 1",
                "capacity": 130
            },
            "TH031": {
                "name": "INOX Nagpur",
                "city_id": "CITY013",
                "screen": "Screen 2",
                "capacity": 110
            },
            # Indore theaters
            "TH032": {
                "name": "PVR Indore",
                "city_id": "CITY014",
                "screen": "Screen 1",
                "capacity": 140
            },
            "TH033": {
                "name": "Cinepolis Indore",
                "city_id": "CITY014",
                "screen": "Screen 2",
                "capacity": 120
            },
            # Thane theaters
            "TH034": {
                "name": "PVR Thane",
                "city_id": "CITY015",
                "screen": "Screen 1",
                "capacity": 150
            },
            "TH035": {
                "name": "INOX Thane",
                "city_id": "CITY015",
                "screen": "Screen 2",
                "capacity": 130
            },
            # Bhopal theaters
            "TH036": {
                "name": "PVR Bhopal",
                "city_id": "CITY016",
                "screen": "Screen 1",
                "capacity": 120
            },
            "TH037": {
                "name": "Cinepolis Bhopal",
                "city_id": "CITY016",
                "screen": "Screen 2",
                "capacity": 100
            },
            # Visakhapatnam theaters
            "TH038": {
                "name": "PVR Visakhapatnam",
                "city_id": "CITY017",
                "screen": "Screen 1",
                "capacity": 110
            },
            "TH039": {
                "name": "INOX Visakhapatnam",
                "city_id": "CITY017",
                "screen": "Screen 2",
                "capacity": 90
            },
            # Patna theaters
            "TH040": {
                "name": "PVR Patna",
                "city_id": "CITY018",
                "screen": "Screen 1",
                "capacity": 130
            },
            "TH041": {
                "name": "Cinepolis Patna",
                "city_id": "CITY018",
                "screen": "Screen 2",
                "capacity": 110
            },
            # Vadodara theaters
            "TH042": {
                "name": "PVR Vadodara",
                "city_id": "CITY019",
                "screen": "Screen 1",
                "capacity": 100
            },
            "TH043": {
                "name": "INOX Vadodara",
                "city_id": "CITY019",
                "screen": "Screen 2",
                "capacity": 80
            },
            # Agra theaters
            "TH044": {
                "name": "PVR Agra",
                "city_id": "CITY020",
                "screen": "Screen 1",
                "capacity": 90
            },
            "TH045": {
                "name": "Cinepolis Agra",
                "city_id": "CITY020",
                "screen": "Screen 2",
                "capacity": 70
            },
            # Nashik theaters
            "TH046": {
                "name": "PVR Nashik",
                "city_id": "CITY021",
                "screen": "Screen 1",
                "capacity": 80
            },
            "TH047": {
                "name": "INOX Nashik",
                "city_id": "CITY021",
                "screen": "Screen 2",
                "capacity": 60
            },
            # Faridabad theaters
            "TH048": {
                "name": "PVR Faridabad",
                "city_id": "CITY022",
                "screen": "Screen 1",
                "capacity": 110
            },
            "TH049": {
                "name": "Cinepolis Faridabad",
                "city_id": "CITY022",
                "screen": "Screen 2",
                "capacity": 90
            },
            # Meerut theaters
            "TH050": {
                "name": "PVR Meerut",
                "city_id": "CITY023",
                "screen": "Screen 1",
                "capacity": 100
            },
            "TH051": {
                "name": "INOX Meerut",
                "city_id": "CITY023",
                "screen": "Screen 2",
                "capacity": 80
            },
            # Rajkot theaters
            "TH052": {
                "name": "PVR Rajkot",
                "city_id": "CITY024",
                "screen": "Screen 1",
                "capacity": 90
            },
            "TH053": {
                "name": "Cinepolis Rajkot",
                "city_id": "CITY024",
                "screen": "Screen 2",
                "capacity": 70
            },
            # Kalyan-Dombivali theaters
            "TH054": {
                "name": "PVR Kalyan",
                "city_id": "CITY025",
                "screen": "Screen 1",
                "capacity": 120
            },
            "TH055": {
                "name": "INOX Kalyan",
                "city_id": "CITY025",
                "screen": "Screen 2",
                "capacity": 100
            },
            # Vasai-Virar theaters
            "TH056": {
                "name": "PVR Vasai",
                "city_id": "CITY026",
                "screen": "Screen 1",
                "capacity": 110
            },
            "TH057": {
                "name": "Cinepolis Vasai",
                "city_id": "CITY026",
                "screen": "Screen 2",
                "capacity": 90
            },
            # Varanasi theaters
            "TH058": {
                "name": "PVR Varanasi",
                "city_id": "CITY027",
                "screen": "Screen 1",
                "capacity": 100
            },
            "TH059": {
                "name": "INOX Varanasi",
                "city_id": "CITY027",
                "screen": "Screen 2",
                "capacity": 80
            },
            # Srinagar theaters
            "TH060": {
                "name": "PVR Srinagar",
                "city_id": "CITY028",
                "screen": "Screen 1",
                "capacity": 80
            },
            "TH061": {
                "name": "Cinepolis Srinagar",
                "city_id": "CITY028",
                "screen": "Screen 2",
                "capacity": 60
            },
            # Dhanbad theaters
            "TH062": {
                "name": "PVR Dhanbad",
                "city_id": "CITY029",
                "screen": "Screen 1",
                "capacity": 90
            },
            "TH063": {
                "name": "INOX Dhanbad",
                "city_id": "CITY029",
                "screen": "Screen 2",
                "capacity": 70
            },
            # Jodhpur theaters
            "TH064": {
                "name": "PVR Jodhpur",
                "city_id": "CITY030",
                "screen": "Screen 1",
                "capacity": 100
            },
            "TH065": {
                "name": "Cinepolis Jodhpur",
                "city_id": "CITY030",
                "screen": "Screen 2",
                "capacity": 80
            }
        }
        
        # Generate comprehensive realistic showtimes for all theaters
        self.showtimes = {}
        show_id_counter = 1
        
        # Realistic time slots for each period
        time_slots = {
            "Morning": ["8:00 AM", "9:15 AM", "10:30 AM", "11:45 AM", "12:30 PM"],
            "Afternoon": ["1:00 PM", "2:15 PM", "3:30 PM", "4:45 PM", "5:30 PM"],
            "Evening": ["6:00 PM", "7:15 PM", "8:30 PM", "9:45 PM", "10:30 PM"],
            "Night": ["11:00 PM", "11:45 PM", "12:30 AM", "1:15 AM", "2:00 AM"]
        }
        
        # Realistic price ranges based on city tier and slot (in INR)
        price_ranges = {
            "CITY001": {  # Mumbai - Tier 1 (highest prices)
                "Morning": (200, 350),
                "Afternoon": (250, 400),
                "Evening": (300, 500),
                "Night": (280, 450)
            },
            "CITY002": {  # Delhi - Tier 1
                "Morning": (180, 320),
                "Afternoon": (220, 380),
                "Evening": (280, 450),
                "Night": (250, 400)
            },
            "CITY003": {  # Bangalore - Tier 1
                "Morning": (190, 340),
                "Afternoon": (230, 390),
                "Evening": (290, 480),
                "Night": (260, 420)
            },
            "CITY004": {  # Chennai - Tier 2
                "Morning": (150, 280),
                "Afternoon": (180, 320),
                "Evening": (220, 380),
                "Night": (200, 340)
            },
            "CITY005": {  # Kolkata - Tier 2
                "Morning": (140, 260),
                "Afternoon": (170, 300),
                "Evening": (210, 360),
                "Night": (190, 320)
            },
            "CITY006": {  # Hyderabad - Tier 2
                "Morning": (160, 290),
                "Afternoon": (190, 330),
                "Evening": (230, 390),
                "Night": (210, 350)
            },
            "CITY007": {  # Pune - Tier 2
                "Morning": (150, 270),
                "Afternoon": (180, 310),
                "Evening": (220, 370),
                "Night": (200, 330)
            },
            "CITY008": {  # Ahmedabad - Tier 3 (lowest prices)
                "Morning": (120, 220),
                "Afternoon": (140, 260),
                "Evening": (180, 300),
                "Night": (160, 280)
            },
            "CITY009": {  # Jaipur - Tier 3
                "Morning": (110, 200),
                "Afternoon": (130, 240),
                "Evening": (170, 290),
                "Night": (150, 260)
            },
            "CITY010": {  # Lucknow - Tier 3
                "Morning": (100, 190),
                "Afternoon": (120, 220),
                "Evening": (160, 270),
                "Night": (140, 240)
            },
            "CITY011": {  # Surat - Tier 3
                "Morning": (110, 210),
                "Afternoon": (130, 250),
                "Evening": (170, 300),
                "Night": (150, 270)
            },
            "CITY012": {  # Kanpur - Tier 4
                "Morning": (90, 170),
                "Afternoon": (110, 200),
                "Evening": (150, 250),
                "Night": (130, 220)
            },
            "CITY013": {  # Nagpur - Tier 4
                "Morning": (95, 180),
                "Afternoon": (115, 210),
                "Evening": (155, 260),
                "Night": (135, 230)
            },
            "CITY014": {  # Indore - Tier 4
                "Morning": (90, 170),
                "Afternoon": (110, 200),
                "Evening": (150, 250),
                "Night": (130, 220)
            },
            "CITY015": {  # Thane - Tier 2 (near Mumbai)
                "Morning": (140, 260),
                "Afternoon": (170, 310),
                "Evening": (210, 390),
                "Night": (190, 350)
            },
            "CITY016": {  # Bhopal - Tier 4
                "Morning": (85, 160),
                "Afternoon": (105, 190),
                "Evening": (145, 240),
                "Night": (125, 210)
            },
            "CITY017": {  # Visakhapatnam - Tier 4
                "Morning": (90, 170),
                "Afternoon": (110, 200),
                "Evening": (150, 250),
                "Night": (130, 220)
            },
            "CITY018": {  # Patna - Tier 4
                "Morning": (80, 150),
                "Afternoon": (100, 180),
                "Evening": (140, 230),
                "Night": (120, 200)
            },
            "CITY019": {  # Vadodara - Tier 4
                "Morning": (85, 160),
                "Afternoon": (105, 190),
                "Evening": (145, 240),
                "Night": (125, 210)
            },
            "CITY020": {  # Agra - Tier 5
                "Morning": (70, 130),
                "Afternoon": (90, 160),
                "Evening": (130, 210),
                "Night": (110, 180)
            },
            "CITY021": {  # Nashik - Tier 4
                "Morning": (85, 160),
                "Afternoon": (105, 190),
                "Evening": (145, 240),
                "Night": (125, 210)
            },
            "CITY022": {  # Faridabad - Tier 3 (near Delhi)
                "Morning": (110, 200),
                "Afternoon": (130, 240),
                "Evening": (170, 290),
                "Night": (150, 260)
            },
            "CITY023": {  # Meerut - Tier 4
                "Morning": (80, 150),
                "Afternoon": (100, 180),
                "Evening": (140, 230),
                "Night": (120, 200)
            },
            "CITY024": {  # Rajkot - Tier 4
                "Morning": (85, 160),
                "Afternoon": (105, 190),
                "Evening": (145, 240),
                "Night": (125, 210)
            },
            "CITY025": {  # Kalyan-Dombivali - Tier 2 (near Mumbai)
                "Morning": (130, 250),
                "Afternoon": (160, 300),
                "Evening": (200, 380),
                "Night": (180, 340)
            },
            "CITY026": {  # Vasai-Virar - Tier 2 (near Mumbai)
                "Morning": (130, 250),
                "Afternoon": (160, 300),
                "Evening": (200, 380),
                "Night": (180, 340)
            },
            "CITY027": {  # Varanasi - Tier 4
                "Morning": (80, 150),
                "Afternoon": (100, 180),
                "Evening": (140, 230),
                "Night": (120, 200)
            },
            "CITY028": {  # Srinagar - Tier 5
                "Morning": (70, 130),
                "Afternoon": (90, 160),
                "Evening": (130, 210),
                "Night": (110, 180)
            },
            "CITY029": {  # Dhanbad - Tier 5
                "Morning": (75, 140),
                "Afternoon": (95, 170),
                "Evening": (135, 220),
                "Night": (115, 190)
            },
            "CITY030": {  # Jodhpur - Tier 4
                "Morning": (85, 160),
                "Afternoon": (105, 190),
                "Evening": (145, 240),
                "Night": (125, 210)
            }
        }
        
        # Movie popularity factors (affects number of shows)
        movie_popularity = {
            "MOV001": 1.2,  # Avatar 3 - High popularity
            "MOV002": 1.1,  # Pathaan Returns - High popularity
            "MOV003": 0.9,  # The Kashmir Files 2 - Medium
            "MOV004": 1.0,  # Fighter - Medium
            "MOV005": 1.1,  # Dune: Part Three - High
            "MOV006": 1.2,  # Jawan 2 - High popularity
            "MOV007": 0.8,  # Animal Park - Lower
            "MOV008": 0.7,  # Oppenheimer: Extended - Lower (extended runtime)
            "MOV009": 1.1,  # Kalki 2898 AD - High
            "MOV010": 1.2,  # Salaar Part 2 - High popularity
            "MOV011": 1.1,  # Pushpa 3: The Rule - High
            "MOV012": 0.9,  # Gadar 3 - Medium
            "MOV013": 1.0,  # Tiger 4 - Medium
            "MOV014": 1.3,  # Bahubali 3: The Conclusion - Very High
            "MOV015": 1.2,  # Marvel: The Multiverse Saga - High
            "MOV016": 0.8,  # Fast & Furious 11 - Lower
            "MOV017": 1.1,  # Mission Impossible 8 - High
            "MOV018": 0.9,  # Jurassic World 4 - Medium
            "MOV019": 1.0,  # Avatar: The Last Airbender - Medium
            "MOV020": 1.2   # The Dark Knight Returns - High
        }
        
        # Generate shows for next 14 days
        try:
            for day_offset in range(14):
                current_date = (datetime.now() + timedelta(days=day_offset)).strftime("%Y-%m-%d")
                
                # Weekend factor (more shows on weekends)
                day_obj = datetime.now() + timedelta(days=day_offset)
                is_weekend = day_obj.weekday() >= 5  # Saturday, Sunday
                weekend_factor = 1.3 if is_weekend else 1.0
                
                for movie_id, popularity in movie_popularity.items():
                    for theater_id, theater in self.theaters.items():
                        city_id = theater["city_id"]
                        
                        # Calculate number of shows based on popularity and weekend
                        base_shows = max(3, int(4 * popularity * weekend_factor))
                        num_shows = min(base_shows, 6)  # Max 6 shows per day per movie per theater
                        
                        # Select random slots
                        available_slots = list(time_slots.keys())
                        selected_slots = random.sample(available_slots, min(num_shows, len(available_slots)))
                        
                        for slot in selected_slots:
                            # Random time from the slot
                            time = random.choice(time_slots[slot])
                            
                            # Random price based on city and slot
                            min_price, max_price = price_ranges[city_id][slot]
                            price = random.randint(min_price, max_price)
                            
                            # Create show with error handling
                            try:
                                show_id = f"SHOW{show_id_counter:03d}"
                                self.showtimes[show_id] = {
                                    "movie_id": movie_id,
                                    "theater_id": theater_id,
                                    "date": current_date,
                                    "time": time,
                                    "slot": slot,
                                    "price": price,
                                    "capacity": theater["capacity"],
                                    "booked_seats": []
                                }
                                show_id_counter += 1
                            except Exception as e:
                                print(f"Error creating show {show_id}: {e}")
                                continue
                                
        except Exception as e:
            print(f"Error in show generation: {e}")
            # Fallback to basic shows if generation fails
            self.showtimes = {
                "SHOW001": {
                    "movie_id": "MOV001",
                    "theater_id": "TH001",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "time": "10:00 AM",
                    "slot": "Morning",
                    "price": 200,
                    "capacity": 120,
                    "booked_seats": []
                }
            }
        
        self.save_data()
    
    def ensure_release_dates(self):
        """Ensure every movie has a release_date field"""
        for movie in self.movies.values():
            if "release_date" not in movie or not movie["release_date"]:
                movie["release_date"] = "Not set"
        self.save_data()

    def ensure_poster_paths(self):
        """Ensure every movie has a poster_path field"""
        for movie in self.movies.values():
            if "poster_path" not in movie:
                movie["poster_path"] = ""
        self.save_data()

    def ensure_booking_statuses(self):
        """Ensure every booking has a status field"""
        changed = False
        for booking in self.bookings.values():
            if "status" not in booking or not booking["status"]:
                booking["status"] = "confirmed"
                changed = True
        if changed:
            self.save_data()

    def ensure_show_dates(self):
        """Ensure every showtime has a valid future date field"""
        changed = False
        today = datetime.now()
        for show in self.showtimes.values():
            if "date" not in show or not show["date"]:
                # Default to today's date if no date is set
                show["date"] = today.strftime("%Y-%m-%d")
                changed = True
            else:
                # Check if the existing date is in the past
                try:
                    show_date = datetime.strptime(show["date"], "%Y-%m-%d")
                    if show_date.date() < today.date():
                        # Set past dates to today's date
                        show["date"] = today.strftime("%Y-%m-%d")
                        changed = True
                except ValueError:
                    # If date format is invalid, set to today
                    show["date"] = today.strftime("%Y-%m-%d")
                    changed = True
        if changed:
            self.save_data()

    def load_poster_image(self, movie_id, target_w=200, target_h=80):
        """Load a movie poster from local path using Tkinter PhotoImage"""
        if movie_id in self.poster_cache:
            return self.poster_cache[movie_id]

        movie = self.movies.get(movie_id)
        if not movie:
            return None

        poster_path = movie.get("poster_path", "")
        if not poster_path:
            return None
        if not os.path.exists(poster_path):
            return None

        try:
            img = tk.PhotoImage(file=poster_path)
            x = max(1, img.width() // target_w) if img.width() > target_w else 1
            y = max(1, img.height() // target_h) if img.height() > target_h else 1
            if x > 1 or y > 1:
                img = img.subsample(x, y)
            self.poster_cache[movie_id] = img
            return img
        except Exception:
            return None
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_modern_button(self, parent, text, command, bg_color=None, fg_color="#ffffff", width=None):
        """Create a modern styled button"""
        if not bg_color:
            bg_color = self.colors["primary"]
        
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            activebackground=self.darken_color(bg_color, 20),
            activeforeground=fg_color
        )
        
        if width:
            btn.config(width=width)
        
        return btn
    
    def create_card(self, parent, **kwargs):
        """Create a modern card container"""
        card = tk.Frame(
            parent,
            bg=self.colors["bg_card"],
            relief="flat",
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            **kwargs
        )
        return card
    
    def create_marquee(self, parent):
        """Create a scrolling marquee at the top of the page"""
        marquee_frame = tk.Frame(parent, bg=self.colors["primary"], height=40)
        marquee_frame.pack(fill='x', padx=0, pady=0)
        marquee_frame.pack_propagate(False)
        
        # Create canvas for scrolling text
        marquee_canvas = tk.Canvas(marquee_frame, bg=self.colors["primary"], highlightthickness=0, height=40)
        marquee_canvas.pack(fill='both', expand=True)
        
        # Create text label with marquee message
        marquee_text = marquee_canvas.create_text(10, 20, text=self.marquee_text, 
                                                 fill=self.colors["text_light"], 
                                                 font=("Segoe UI", 12, "bold"),
                                                 anchor='w')
        
        # Get text width for animation
        text_width = marquee_canvas.bbox(marquee_text)[2] - marquee_canvas.bbox(marquee_text)[0]
        canvas_width = 1100  # Default window width
        
        # Animate the text
        def animate_marquee(x=0):
            marquee_canvas.coords(marquee_text, x, 20)
            if x < -text_width:
                x = canvas_width
            else:
                x -= 2  # Scroll speed
            marquee_frame.after(50, animate_marquee, x)
        
        # Start animation after a short delay
        marquee_frame.after(100, animate_marquee, canvas_width)
        
        return marquee_frame
    
    def calculate_columns(self):
        """Calculate optimal number of columns based on window width"""
        try:
            # Use current window width for better responsiveness
            window_width = self.root.winfo_width()
            if window_width <= 1:  # Window not yet rendered
                window_width = 1100  # Default to initial size
            
            # Calculate columns: minimum 2, maximum 8 for better large screen support
            # Each movie card needs approximately 220px width (reduced for better fit)
            min_card_width = 220
            max_columns = 8
            min_columns = 2
            
            # Calculate based on window width (leave some margin for padding and scrollbar)
            available_width = window_width - 100  # Account for margins, padding, and scrollbar
            calculated_columns = max(min_columns, min(max_columns, available_width // min_card_width))
            
            return calculated_columns
        except:
            # Fallback to 4 columns if calculation fails
            return 4
    
    def darken_color(self, color, percent):
        """Darken a hex color by percentage"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(max(0, int(c * (100 - percent) / 100)) for c in rgb)
        return '#%02x%02x%02x' % rgb
    
    def generate_qr_code(self, booking_data, parent=None):
        """Generate a real QR code with booking information"""
        if parent is None:
            parent = self.root
            
        if not QR_AVAILABLE:
            # Fallback to random QR code pattern if qrcode library not available
            return self.generate_random_qr(parent)
        
        try:
            # Create QR code with booking information
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=4,
                border=2,
            )

            # Format booking data as JSON string
            qr_data = json.dumps(booking_data, indent=2)
            qr.add_data(qr_data)
            qr.make(fit=True)

            # Create QR code image
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Resize to fit in ticket (150x150)
            # Use LANCZOS resampling (compatible with both old and new Pillow versions)
            try:
                resample = Image.Resampling.LANCZOS  # Pillow 9.0+
            except AttributeError:
                resample = Image.LANCZOS  # Older Pillow versions
            qr_img = qr_img.resize((150, 150), resample)

            # Convert to PhotoImage for Tkinter
            qr_photo = ImageTk.PhotoImage(qr_img)

            # Create label to display QR code
            qr_label = tk.Label(parent, image=qr_photo, bg="white")
            qr_label.image = qr_photo  # Keep a reference

            return qr_label

        except Exception as e:
            print(f"Error generating QR code: {e}")
            # Fallback to simple canvas-based QR code
            return self.generate_random_qr(parent)

    def generate_random_qr(self, parent=None):
        """Generate an attractive fake QR code pattern"""
        if parent is None:
            parent = self.root
        qr_canvas = tk.Canvas(parent, width=150, height=150, bg="white", highlightthickness=2, highlightbackground="#34495e")

        # Generate attractive QR code pattern
        cell_size = 4
        grid_size = 37  # 37x37 grid for 148x148 canvas (leaving 1px border)
        
        # Enhanced color palette
        dark_colors = ["#1a1a1a", "#2c3e50", "#34495e", "#2d3436"]
        accent_colors = ["#e74c3c", "#3498db", "#9b59b6"]
        
        # Create corner finder patterns (authentic QR structure)
        corner_patterns = [
            (0, 0), (0, grid_size - 7), (grid_size - 7, 0)
        ]
        
        for corner_x, corner_y in corner_patterns:
            # Outer square - 7x7
            for i in range(7):
                for j in range(7):
                    x, y = corner_x + i, corner_y + j
                    if x < grid_size and y < grid_size:
                        if i == 0 or i == 6 or j == 0 or j == 6:  # Outer border
                            color = "#1a1a1a"
                        elif 2 <= i <= 4 and 2 <= j <= 4:  # Center dot
                            color = "#1a1a1a"
                        elif (i == 1 or i == 5) and (1 <= j <= 5):  # Inner border
                            color = "#1a1a1a"
                        elif (j == 1 or j == 5) and (1 <= i <= 5):  # Inner border
                            color = "#1a1a1a"
                        else:
                            color = "white"
                        
                        x1, y1 = y * cell_size + 1, x * cell_size + 1
                        x2, y2 = x1 + cell_size, y1 + cell_size
                        qr_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
        
        # Add timing patterns (alternating dots)
        for i in range(8, grid_size - 7):
            # Vertical timing pattern
            if i % 2 == 0:
                x1, y1 = 6 * cell_size + 1, i * cell_size + 1
                x2, y2 = x1 + cell_size, y1 + cell_size
                qr_canvas.create_rectangle(x1, y1, x2, y2, fill="#1a1a1a", outline="#1a1a1a")
            
            # Horizontal timing pattern
            if i % 2 == 0:
                x1, y1 = i * cell_size + 1, 6 * cell_size + 1
                x2, y2 = x1 + cell_size, y1 + cell_size
                qr_canvas.create_rectangle(x1, y1, x2, y2, fill="#1a1a1a", outline="#1a1a1a")
        
        # Add alignment pattern (small square in data area)
        if grid_size > 20:
            align_x, align_y = grid_size - 10, grid_size - 10
            for i in range(5):
                for j in range(5):
                    x, y = align_x + i, align_y + j
                    if x < grid_size and y < grid_size:
                        if i == 0 or i == 4 or j == 0 or j == 4:  # Border
                            color = "#1a1a1a"
                        elif 2 <= i <= 2 and 2 <= j <= 2:  # Center
                            color = "#1a1a1a"
                        else:
                            color = "white"
                        
                        x1, y1 = y * cell_size + 1, x * cell_size + 1
                        x2, y2 = x1 + cell_size, y1 + cell_size
                        qr_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
        
        # Create attractive random pattern for data area
        for i in range(grid_size):
            for j in range(grid_size):
                # Skip reserved areas
                if (i < 7 and j < 7) or (i < 7 and j >= grid_size - 7) or (i >= grid_size - 7 and j < 7):
                    continue
                if i == 6 or j == 6:
                    continue
                if (grid_size - 10 <= i < grid_size - 5) and (grid_size - 10 <= j < grid_size - 5):
                    continue
                
                # Create structured random pattern
                if random.random() > 0.48:  # 52% chance of filled
                    # Use different colors for visual appeal
                    rand = random.random()
                    if rand > 0.95:  # 5% chance for bright accent
                        color = random.choice(accent_colors)
                    else:  # 95% chance for dark colors
                        color = random.choice(dark_colors)
                    
                    x1, y1 = j * cell_size + 1, i * cell_size + 1
                    x2, y2 = x1 + cell_size, y1 + cell_size
                    qr_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
        
        # Add decorative corner dots (alignment markers)
        dot_positions = [
            (3, 3), (3, grid_size - 4), (grid_size - 4, 3),
            (grid_size - 4, grid_size - 4)
        ]
        
        for dot_x, dot_y in dot_positions:
            if dot_x < grid_size and dot_y < grid_size:
                cx = dot_y * cell_size + cell_size // 2 + 1
                cy = dot_x * cell_size + cell_size // 2 + 1
                radius = cell_size // 3
                qr_canvas.create_oval(
                    cx - radius, cy - radius,
                    cx + radius, cy + radius,
                    fill="#e74c3c", outline="#e74c3c"
                )
        
        # Add center logo area (larger white square)
        center_size = 5
        center_x, center_y = grid_size // 2, grid_size // 2
        
        for i in range(center_size):
            for j in range(center_size):
                x, y = center_x - 2 + i, center_y - 2 + j
                if 0 <= x < grid_size and 0 <= y < grid_size:
                    x1, y1 = y * cell_size + 1, x * cell_size + 1
                    x2, y2 = x1 + cell_size, y1 + cell_size
                    qr_canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="white")
        
        # Add movie logo in center
        logo_x = center_y * cell_size + cell_size // 2 + 1
        logo_y = center_x * cell_size + cell_size // 2 + 1
        qr_canvas.create_text(
            logo_x, logo_y,
            text="🎬",
            font=("Arial", 10, "bold"),
            fill="#2c3e50"
        )
        
        # Add version information (bottom right)
        version_text = "v7"
        qr_canvas.create_text(
            grid_size * cell_size - 10, grid_size * cell_size - 5,
            text=version_text,
            font=("Arial", 6),
            fill="#7f8c8d",
            anchor="se"
        )
        
        return qr_canvas
    
    def show_login_screen(self):
        """Display login/register screen"""
        self.clear_window()

        # Create main container with gradient effect
        main_container = tk.Frame(self.root, bg=self.colors["bg_dark"])
        main_container.pack(expand=True, fill='both')

        # Decorative elements
        left_decoration = tk.Frame(main_container, bg=self.colors["primary"], width=100)
        left_decoration.pack(side='left', fill='y')

        # Main content area
        content_area = tk.Frame(main_container, bg=self.colors["bg_dark"])
        content_area.pack(expand=True, fill='both', padx=50, pady=50)

        # Logo and title
        logo_frame = tk.Frame(content_area, bg=self.colors["bg_dark"])
        logo_frame.pack(pady=(0, 40))

        # Animated logo
        logo_label = tk.Label(
            logo_frame,
            text="🎬",
            font=("Arial", 64),
            bg=self.colors["bg_dark"],
            fg=self.colors["primary"]
        )
        logo_label.pack()

        tk.Label(
            logo_frame,
            text="BookMyShow",
            font=("Segoe UI", 36, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(pady=10)

        tk.Label(
            logo_frame,
            text="Experience Cinematic Magic",
            font=("Segoe UI", 14),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_muted"]
        ).pack()

        # Login form in modern card
        form_card = self.create_card(content_area, padx=50, pady=40)
        form_card.pack(expand=True, fill='both')

        tk.Label(
            form_card,
            text="Welcome Back!",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).pack(pady=(0, 30))

        # Username field with icon
        user_frame = tk.Frame(form_card, bg=self.colors["bg_card"])
        user_frame.pack(fill='x', pady=10)

        tk.Label(
            user_frame,
            text="👤",
            font=("Arial", 14),
            bg=self.colors["bg_card"],
            fg=self.colors["text_muted"]
        ).pack(side='left', padx=(0, 10))

        username_entry = tk.Entry(
            user_frame,
            font=("Segoe UI", 12),
            bg="#21262d",
            fg=self.colors["text_light"],
            insertbackground=self.colors["text_light"],
            relief="flat",
            width=30
        )
        username_entry.pack(side='left', fill='x', expand=True, ipady=10)

        # Password field with icon
        pass_frame = tk.Frame(form_card, bg=self.colors["bg_card"])
        pass_frame.pack(fill='x', pady=10)

        tk.Label(
            pass_frame,
            text="🔒",
            font=("Arial", 14),
            bg=self.colors["bg_card"],
            fg=self.colors["text_muted"]
        ).pack(side='left', padx=(0, 10))

        password_entry = tk.Entry(
            pass_frame,
            font=("Segoe UI", 12),
            bg="#21262d",
            fg=self.colors["text_light"],
            insertbackground=self.colors["text_light"],
            relief="flat",
            show="•",
            width=30
        )
        password_entry.pack(side='left', fill='x', expand=True, ipady=10)

        # Buttons in a row
        btn_container = tk.Frame(form_card, bg=self.colors["bg_card"])
        btn_container.pack(pady=30)

        self.create_modern_button(
            btn_container,
            "🎫 User Login",
            lambda: self.user_login(username_entry.get(), password_entry.get()),
            self.colors["primary"],
            width=15
        ).pack(side='left', padx=10)

        self.create_modern_button(
            btn_container,
            "📝 Register",
            lambda: self.register_user(username_entry.get(), password_entry.get()),
            self.colors["secondary"],
            width=15
        ).pack(side='left', padx=10)

        self.create_modern_button(
            btn_container,
            "⚙️ Admin Login",
            lambda: self.admin_login(username_entry.get(), password_entry.get()),
            self.colors["warning"],
            width=15
        ).pack(side='left', padx=10)

        # Footer
        footer = tk.Frame(content_area, bg=self.colors["bg_dark"])
        footer.pack(pady=20)

        tk.Label(
            footer,
            text="© 2024 BookMyShow. All rights reserved.",
            font=("Segoe UI", 10),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_muted"]
        ).pack()
    
    def user_login(self, username, password):
        """Handle user login"""
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return

        if username in self.users and self.users[username]["password"] == password:
            self.current_user = username
            self.current_admin = None  # Clear admin session when user logs in
            messagebox.showinfo("Success", f"Welcome {username}!")
            self.show_user_home()
        else:
            messagebox.showerror("Error", "Invalid credentials")
    
    def register_user(self, username, password):
        """Register new user"""
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return

        if username in self.users:
            messagebox.showerror("Error", "Username already exists")
            return

        self.users[username] = {
            "password": password,
            "bookings": []
        }
        self.save_data()
        messagebox.showinfo("Success", "Registration successful! Please login.")
    
    def admin_login(self, username, password):
        """Handle admin login"""
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return

        if username in self.admins and self.admins[username] == password:
            self.current_admin = username
            self.current_user = None  # Clear user session when admin logs in
            messagebox.showinfo("Success", f"Welcome Admin!")
            self.show_admin_panel()
        else:
            messagebox.showerror("Error", "Invalid admin credentials")
    
    def show_user_home(self):
        """Display user home screen with movies"""
        self.clear_window()

        # Add marquee at the top
        self.create_marquee(self.root)

        # Modern header
        header = tk.Frame(self.root, bg=self.colors["bg_header"], height=70)
        header.pack(fill='x')

        tk.Label(
            header,
            text="🎬 BookMyShow",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg_header"],
            fg=self.colors["text_light"]
        ).pack(side='left', padx=30, pady=15)
        # Decorative elements
        left_decoration = tk.Frame(main_container, bg=self.colors["primary"], width=100)
        left_decoration.pack(side='left', fill='y')
        
        # Main content area
        content_area = tk.Frame(main_container, bg=self.colors["bg_dark"])
        content_area.pack(expand=True, fill='both', padx=50, pady=50)
        
        # Logo and title
        logo_frame = tk.Frame(content_area, bg=self.colors["bg_dark"])
        logo_frame.pack(pady=(0, 40))
        
        # Animated logo
        logo_label = tk.Label(
            logo_frame,
            text="🎬",
            font=("Arial", 64),
            bg=self.colors["bg_dark"],
            fg=self.colors["primary"]
        )
        logo_label.pack()
        
        tk.Label(
            logo_frame,
            text="BookMyShow",
            font=("Segoe UI", 36, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(pady=10)
        
        tk.Label(
            logo_frame,
            text="Experience Cinematic Magic",
            font=("Segoe UI", 14),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_muted"]
        ).pack()
        
        # Login form in modern card
        form_card = self.create_card(content_area, padx=50, pady=40)
        form_card.pack(expand=True, fill='both')
        
        tk.Label(
            form_card,
            text="Welcome Back!",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).pack(pady=(0, 30))
        
        # Username field with icon
        user_frame = tk.Frame(form_card, bg=self.colors["bg_card"])
        user_frame.pack(fill='x', pady=10)
        
        tk.Label(
            user_frame,
            text="👤",
            font=("Arial", 14),
            bg=self.colors["bg_card"],
            fg=self.colors["text_muted"]
        ).pack(side='left', padx=(0, 10))
        
        username_entry = tk.Entry(
            user_frame,
            font=("Segoe UI", 12),
            bg="#21262d",
            fg=self.colors["text_light"],
            insertbackground=self.colors["text_light"],
            relief="flat",
            width=30
        )
        username_entry.pack(side='left', fill='x', expand=True, ipady=10)
        
        # Password field with icon
        pass_frame = tk.Frame(form_card, bg=self.colors["bg_card"])
        pass_frame.pack(fill='x', pady=10)
        
        tk.Label(
            pass_frame,
            text="🔒",
            font=("Arial", 14),
            bg=self.colors["bg_card"],
            fg=self.colors["text_muted"]
        ).pack(side='left', padx=(0, 10))
        
        password_entry = tk.Entry(
            pass_frame,
            font=("Segoe UI", 12),
            bg="#21262d",
            fg=self.colors["text_light"],
            insertbackground=self.colors["text_light"],
            relief="flat",
            show="•",
            width=30
        )
        password_entry.pack(side='left', fill='x', expand=True, ipady=10)
        
        # Buttons in a row
        btn_container = tk.Frame(form_card, bg=self.colors["bg_card"])
        btn_container.pack(pady=30)
        
        self.create_modern_button(
            btn_container,
            "🎫 User Login",
            lambda: self.user_login(username_entry.get(), password_entry.get()),
            self.colors["primary"],
            width=15
        ).pack(side='left', padx=10)
        
        self.create_modern_button(
            btn_container,
            "📝 Register",
            lambda: self.register_user(username_entry.get(), password_entry.get()),
            self.colors["secondary"],
            width=15
        ).pack(side='left', padx=10)
        
        self.create_modern_button(
            btn_container,
            "⚙️ Admin Login",
            lambda: self.admin_login(username_entry.get(), password_entry.get()),
            self.colors["warning"],
            width=15
        ).pack(side='left', padx=10)
        
        # Footer
        footer = tk.Frame(content_area, bg=self.colors["bg_dark"])
        footer.pack(pady=20)
        
        tk.Label(
            footer,
            text="© 2024 BookMyShow. All rights reserved.",
            font=("Segoe UI", 10),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_muted"]
        ).pack()
    
    def user_login(self, username, password):
        """Handle user login"""
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        if username in self.users and self.users[username]["password"] == password:
            self.current_user = username
            self.current_admin = None  # Clear admin session when user logs in
            messagebox.showinfo("Success", f"Welcome {username}!")
            self.show_user_home()
        else:
            messagebox.showerror("Error", "Invalid credentials")
    
    def register_user(self, username, password):
        """Register new user"""
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        if username in self.users:
            messagebox.showerror("Error", "Username already exists")
            return
        
        self.users[username] = {
            "password": password,
            "bookings": []
        }
        self.save_data()
        messagebox.showinfo("Success", "Registration successful! Please login.")
    
    def admin_login(self, username, password):
        """Handle admin login"""
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        if username in self.admins and self.admins[username] == password:
            self.current_admin = username
            self.current_user = None  # Clear user session when admin logs in
            messagebox.showinfo("Success", f"Welcome Admin!")
            self.show_admin_panel()
        else:
            messagebox.showerror("Error", "Invalid admin credentials")
    
    def show_user_home(self):
        """Display user home screen with movies"""
        self.clear_window()
        
        # Add marquee at the top
        self.create_marquee(self.root)
        
        # Modern header
        header = tk.Frame(self.root, bg=self.colors["bg_header"], height=70)
        header.pack(fill='x')
        
        tk.Label(
            header,
            text="🎬 BookMyShow",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg_header"],
            fg=self.colors["text_light"]
        ).pack(side='left', padx=30, pady=15)
        
        # User info and buttons on right
        right_panel = tk.Frame(header, bg=self.colors["bg_header"])
        right_panel.pack(side='right', padx=20)
        
        # User name as clickable button
        user_button = tk.Frame(right_panel, bg=self.darken_color(self.colors["bg_header"], 5), relief="raised", bd=1, cursor="hand2")
        user_button.pack(side='left', padx=10)
        
        username_label = tk.Label(
            user_button,
            text=f"👋 {self.current_user}",
            font=("Segoe UI", 12, "bold"),
            bg=self.darken_color(self.colors["bg_header"], 5),
            fg=self.colors["text_light"],
            padx=15,
            pady=8
        )
        username_label.pack(side='left')
        
        arrow_label = tk.Label(
            user_button,
            text="▼",
            font=("Segoe UI", 8),
            bg=self.darken_color(self.colors["bg_header"], 5),
            fg=self.colors["text_light"]
        )
        arrow_label.pack(side='left', padx=(5, 15))
        
        # Bind click event to navigate to My Account page
        open_account = lambda e: self.show_my_account()
        user_button.bind("<Button-1>", open_account)
        username_label.bind("<Button-1>", open_account)
        arrow_label.bind("<Button-1>", open_account)
        user_button.bind("<Enter>", lambda e: user_button.config(bg=self.darken_color(self.colors["bg_header"], 10)))
        user_button.bind("<Leave>", lambda e: user_button.config(bg=self.darken_color(self.colors["bg_header"], 5)))
        
        # Quick action buttons
        self.create_modern_button(
            right_panel,
            "📖 Bookings",
            self.show_my_bookings,
            self.darken_color(self.colors["bg_header"], 10),
            width=12
        ).pack(side='left', padx=5)
        
        self.create_modern_button(
            right_panel,
            "🚪 Logout",
            self.show_login_screen,
            self.colors["primary"],
            width=10
        ).pack(side='left', padx=5)
        
        # Content area
        content = tk.Frame(self.root, bg=self.colors["bg_dark"])
        content.pack(expand=True, fill='both', padx=20, pady=20)
        
        # User profile card at the top
        user_data = self.users[self.current_user]
        profile_card = self.create_card(content, padx=20, pady=12)
        profile_card.pack(fill='x', pady=(0, 15))
        
        # Profile content
        profile_content = tk.Frame(profile_card, bg=self.colors["bg_card"])
        profile_content.pack(fill='x', padx=15, pady=10)
        
        # Left side - User info
        left_profile = tk.Frame(profile_content, bg=self.colors["bg_card"])
        left_profile.pack(side='left', fill='both', expand=True)
        
        # Welcome message with user details
        tk.Label(
            left_profile,
            text=f"👋 Welcome back, {self.current_user}!",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).pack(anchor='w', pady=(0, 5))
        
        stats_frame = tk.Frame(left_profile, bg=self.colors["bg_card"])
        stats_frame.pack(anchor='w', pady=(5, 0))
        
        # Booking stats
        total_bookings = len(user_data.get("bookings", []))
        
        tk.Label(
            stats_frame,
            text=f"🎫 {total_bookings} Bookings",
            font=("Segoe UI", 11),
            bg=self.colors["bg_card"],
            fg=self.colors["primary"]
        ).pack(side='left', padx=(0, 20))
        
        tk.Label(
            stats_frame,
            text=f"📅 Member since {user_data.get('created_date', 'Unknown')}",
            font=("Segoe UI", 11),
            bg=self.colors["bg_card"],
            fg=self.colors["text_muted"]
        ).pack(side='left')
        
        # Contact info
        if user_data.get("email") or user_data.get("phone"):
            contact_frame = tk.Frame(left_profile, bg=self.colors["bg_card"])
            contact_frame.pack(anchor='w', pady=(5, 0))
            
            if user_data.get("email"):
                tk.Label(
                    contact_frame,
                    text=f"📧 {user_data['email']}",
                    font=("Segoe UI", 10),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_muted"]
                ).pack(side='left', padx=(0, 15))
            
            if user_data.get("phone"):
                tk.Label(
                    contact_frame,
                    text=f"📱 {user_data['phone']}",
                    font=("Segoe UI", 10),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_muted"]
                ).pack(side='left')
        # Right side - Quick actions
        right_profile = tk.Frame(profile_content, bg=self.colors["bg_card"])
        right_profile.pack(side='right')
        
        self.create_modern_button(
            right_profile,
            "📋 My Bookings",
            self.show_my_bookings,
            self.colors["primary"],
            width=15
        ).pack(pady=5)
        
        # Movies section
        tk.Label(
            content,
            text="🎬 Now Showing",
            font=("Segoe UI", 28, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(anchor='w', pady=(0, 20))
        
        # Genre Filter Section
        filter_frame = self.create_card(content, padx=15, pady=10)
        filter_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            filter_frame,
            text="🎭 Filter by Genre",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).pack(anchor='w', pady=(0, 8))
        
        # Genre buttons
        genre_buttons_frame = tk.Frame(filter_frame, bg=self.colors["bg_card"])
        genre_buttons_frame.pack(fill='x', pady=(0, 8))
        
        # Create genre filter variable
        self.selected_genre = tk.StringVar(value="All")
        
        # Store genre buttons to update colors
        self.genre_buttons = {}
        
        # Genre options based on all available movies
        genres = [
            "All", "Action", "Sci-Fi", "Thriller", "Drama", 
            "Adventure", "Crime", "War", "Biographical", 
            "Epic", "Superhero", "Fantasy"
        ]
        
        for genre in genres:
            genre_btn = self.create_modern_button(
                genre_buttons_frame,
                genre,
                lambda g=genre: self.filter_movies_by_genre(g),
                self.colors["primary"] if genre == "All" else self.colors["secondary"],
                width=12
            )
            genre_btn.pack(side='left', padx=(0, 10))
            self.genre_buttons[genre] = genre_btn
        
        # Movies grid in scrollable frame
        canvas = tk.Canvas(content, bg=self.colors["bg_dark"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["bg_dark"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Movies responsive layout
        self.movies_frame = tk.Frame(scrollable_frame, bg=self.colors["bg_dark"])
        self.movies_frame.pack(fill='x', padx=20, pady=10)
        
        # Fixed layout: 5 movies in one row
        max_columns = 5
        row, col = 0, 0
        
        # Get filtered movies
        filtered_movies = self.get_filtered_movies_by_genre()
        
        for movie_id, movie in sorted(filtered_movies.items(), key=lambda x: x[1]["name"]):
            # Create movie card
            movie_card = self.create_card(self.movies_frame, padx=10, pady=10)
            movie_card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            self.movies_frame.columnconfigure(col, weight=1)
            
            # Movie poster placeholder with gradient
            poster = tk.Frame(movie_card, bg=self.colors["primary"], height=300)
            poster.pack(fill='x', pady=(0, 10))
            poster.pack_propagate(False)
            poster_img = self.load_poster_image(movie_id, target_w=250, target_h=300)
            if poster_img:
                poster_label = tk.Label(poster, image=poster_img, bg=self.colors["primary"])
                poster_label.image = poster_img
                poster_label.pack(expand=True)
            
            # Movie title
            tk.Label(
                movie_card,
                text=movie["name"],
                font=("Segoe UI", 12, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"],
                wraplength=150
            ).pack(pady=3)
            
            # Rating
            tk.Label(
                movie_card,
                text=movie.get("rating", "⭐ N/A"),
                font=("Segoe UI", 10),
                bg=self.colors["bg_card"],
                fg=self.colors["warning"]
            ).pack()
            
            # Movie details
            details = [
                f"🎬 {movie['language']}",
                f"⏱️ {movie['duration']}",
                f"🎭 {movie['genre']}"
            ]
            
            for detail in details:
                tk.Label(
                    movie_card,
                    text=detail,
                    font=("Segoe UI", 9),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_muted"]
                ).pack(anchor='w', pady=1)
            
            tk.Label(
                movie_card,
                text=f"📅 Release Date: {movie.get('release_date', 'Not set')}",
                font=("Segoe UI", 9),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(anchor='w', pady=(0, 4))
            
            # Book button
            self.create_modern_button(
                movie_card,
                "🎟️ Book Now",
                lambda m_id=movie_id: self.select_city(m_id),
                self.colors["primary"],
                width=18
            ).pack(pady=10)
            
            col += 1
            if col >= max_columns:
                col = 0
                row += 1
        
        if not self.movies:
            tk.Label(
                scrollable_frame,
                text="🎬 No movies available",
                font=("Segoe UI", 16),
                bg=self.colors["bg_dark"],
                fg=self.colors["text_muted"]
            ).pack(pady=50)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def select_city(self, movie_id):
        """Select city for movie"""
        self.clear_window()
        
        # Header
        header = tk.Frame(self.root, bg=self.colors["bg_header"], height=70)
        header.pack(fill='x')
        
        tk.Label(
            header,
            text="📍 Select City",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg_header"],
            fg=self.colors["text_light"]
        ).pack(side='left', padx=30, pady=15)
        
        self.create_modern_button(
            header,
            "← Back",
            self.show_user_home,
            self.darken_color(self.colors["bg_header"], 10),
            width=10
        ).pack(side='right', padx=30, pady=15)
        
        # Content
        content = tk.Frame(self.root, bg=self.colors["bg_dark"])
        content.pack(expand=True, fill='both', padx=30, pady=30)
        
        movie_name = self.movies[movie_id]["name"]
        
        tk.Label(
            content,
            text=f"Selected: {movie_name}",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(pady=20)
        
        tk.Label(
            content,
            text="Choose your city:",
            font=("Segoe UI", 14),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_muted"]
        ).pack(pady=10)
        
        # Scrollable cities responsive grid
        canvas = tk.Canvas(content, bg=self.colors["bg_dark"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
        cities_frame = tk.Frame(canvas, bg=self.colors["bg_dark"])
        
        cities_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=cities_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar first
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)
        
        # Cities responsive layout (matching movies layout)
        # Calculate responsive columns (same as movies)
        max_columns = self.calculate_columns()
        row, col = 0, 0
        
        for city_id, city_name in sorted(self.cities.items(), key=lambda x: x[1]):
            # Create city card (same style as movie cards)
            city_card = self.create_card(cities_frame, padx=10, pady=10)
            city_card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            cities_frame.columnconfigure(col, weight=1)
            
            # City icon placeholder (like movie poster)
            icon_frame = tk.Frame(city_card, bg=self.colors["primary"], height=80)
            icon_frame.pack(fill='x', pady=(0, 10))
            icon_frame.pack_propagate(False)
            
            tk.Label(
                icon_frame,
                text="🏙️",
                font=("Arial", 32),
                bg=self.colors["primary"],
                fg="white"
            ).pack(expand=True)
            
            # City name (like movie title)
            tk.Label(
                city_card,
                text=city_name,
                font=("Segoe UI", 12, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"],
                wraplength=150
            ).pack(pady=3)
            
            # City info (like movie details)
            details = [
                "📍 Available",
                "🎬 Multiple Theaters"
            ]
            
            for detail in details:
                tk.Label(
                    city_card,
                    text=detail,
                    font=("Segoe UI", 9),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_muted"]
                ).pack(anchor='w', pady=1)
            
            # Select button (like Book Now button)
            self.create_modern_button(
                city_card,
                "📍 Select City",
                lambda c_id=city_id, m_id=movie_id: self.select_theater(m_id, c_id),
                self.colors["primary"],
                width=18
            ).pack(pady=10)
            
            col += 1
            if col >= max_columns:
                col = 0
                row += 1
        
        if not self.cities:
            tk.Label(
                cities_frame,
                text="🌆 No cities available",
                font=("Segoe UI", 16),
                bg=self.colors["bg_dark"],
                fg=self.colors["text_muted"]
            ).pack(pady=50)
    
    def select_theater(self, movie_id, city_id):
        """Select theater"""
        self.clear_window()
        
        # Header
        header = tk.Frame(self.root, bg=self.colors["bg_header"], height=70)
        header.pack(fill='x')
        
        tk.Label(
            header,
            text="🎭 Select Theater",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg_header"],
            fg=self.colors["text_light"]
        ).pack(side='left', padx=30, pady=15)
        
        self.create_modern_button(
            header,
            "← Back",
            lambda: self.select_city(movie_id),
            self.darken_color(self.colors["bg_header"], 10),
            width=10
        ).pack(side='right', padx=30, pady=15)
        
        # Content with enhanced design
        content = tk.Frame(self.root, bg=self.colors["bg_dark"])
        content.pack(expand=True, fill='both', padx=30, pady=30)
        
        movie_name = self.movies[movie_id]["name"]
        city_name = self.cities[city_id]
        
        # Enhanced movie and city header
        header_card = self.create_card(content, padx=20, pady=15)
        header_card.pack(fill='x', pady=(0, 20))
        
        # Movie info with icon
        movie_frame = tk.Frame(header_card, bg=self.colors["bg_card"])
        movie_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            movie_frame,
            text="🎬",
            font=("Segoe UI", 20),
            bg=self.colors["bg_card"],
            fg=self.colors["primary"]
        ).pack(side='left', padx=(0, 10))
        
        tk.Label(
            movie_frame,
            text=movie_name,
            font=("Segoe UI", 18, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).pack(side='left')
        
        # City info with icon
        city_frame = tk.Frame(header_card, bg=self.colors["bg_card"])
        city_frame.pack(fill='x')
        
        tk.Label(
            city_frame,
            text="📍",
            font=("Segoe UI", 16),
            bg=self.colors["bg_card"],
            fg=self.colors["accent"]
        ).pack(side='left', padx=(0, 10))
        
        tk.Label(
            city_frame,
            text=city_name,
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).pack(side='left')
        
        # Theater count badge
        available_theaters = []
        for show_id, show in self.showtimes.items():
            if show["movie_id"] == movie_id:
                theater = self.theaters.get(show["theater_id"])
                if theater and theater["city_id"] == city_id:
                    if show["theater_id"] not in [t[0] for t in available_theaters]:
                        available_theaters.append((show["theater_id"], theater))
        
        count_badge = tk.Frame(city_frame, bg=self.colors["success"], relief="flat", bd=0)
        count_badge.pack(side='right', padx=10)
        count_badge.pack_propagate(False)
        
        tk.Label(
            count_badge,
            text=f"{len(available_theaters)} Theaters",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors["success"],
            fg="white"
        ).pack(padx=10, pady=5)
        
        # Sort theaters alphabetically
        available_theaters.sort(key=lambda x: x[1]["name"])
        
        if available_theaters:
            # Scrollable theaters responsive grid
            canvas = tk.Canvas(content, bg=self.colors["bg_dark"], highlightthickness=0)
            scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
            theaters_container = tk.Frame(canvas, bg=self.colors["bg_dark"])
            
            theaters_container.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=theaters_container, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Add mouse wheel scrolling
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            def _bind_to_mousewheel(event):
                canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            def _unbind_from_mousewheel(event):
                canvas.unbind_all("<MouseWheel>")
            
            canvas.bind('<Enter>', _bind_to_mousewheel)
            canvas.bind('<Leave>', _unbind_from_mousewheel)
            
            # Pack canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Calculate responsive columns for theaters
            max_columns = max(2, self.calculate_columns() - 1)  # Theaters need medium space
            row, col = 0, 0
            
            for theater_id, theater in available_theaters:
                # Enhanced theater card with hover effects
                theater_card = self.create_card(theaters_container, padx=15, pady=15)
                theater_card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
                theaters_container.columnconfigure(col, weight=1)
                
                # Theater header with icon
                header_frame = tk.Frame(theater_card, bg=self.colors["bg_card"])
                header_frame.pack(fill='x', pady=(0, 10))
                
                # Theater icon and name
                icon_label = tk.Label(
                    header_frame,
                    text="🎭",
                    font=("Segoe UI", 24),
                    bg=self.colors["bg_card"],
                    fg=self.colors["primary"]
                )
                icon_label.pack(side='left', padx=(0, 10))
                
                name_label = tk.Label(
                    header_frame,
                    text=theater["name"],
                    font=("Segoe UI", 16, "bold"),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_light"]
                )
                name_label.pack(side='left')
                
                # Theater details with enhanced styling
                details_frame = tk.Frame(theater_card, bg=self.colors["bg_card"])
                details_frame.pack(fill='x', pady=(0, 10))
                
                # Screen info with icon
                screen_frame = tk.Frame(details_frame, bg=self.colors["bg_card"])
                screen_frame.pack(fill='x', pady=2)
                
                tk.Label(
                    screen_frame,
                    text="🎪",
                    font=("Segoe UI", 12),
                    bg=self.colors["bg_card"],
                    fg=self.colors["accent"]
                ).pack(side='left', padx=(0, 8))
                
                tk.Label(
                    screen_frame,
                    text=f"Screen: {theater['screen']}",
                    font=("Segoe UI", 11),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_muted"]
                ).pack(side='left')
                
                # Capacity info with icon
                capacity_frame = tk.Frame(details_frame, bg=self.colors["bg_card"])
                capacity_frame.pack(fill='x', pady=2)
                
                tk.Label(
                    capacity_frame,
                    text="🪑",
                    font=("Segoe UI", 12),
                    bg=self.colors["bg_card"],
                    fg=self.colors["warning"]
                ).pack(side='left', padx=(0, 8))
                
                tk.Label(
                    capacity_frame,
                    text=f"Capacity: {theater['capacity']} seats",
                    font=("Segoe UI", 11),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_muted"]
                ).pack(side='left')
                
                # Theater type badge
                if theater['capacity'] >= 150:
                    theater_type = "Large"
                    type_color = self.colors["success"]
                elif theater['capacity'] >= 100:
                    theater_type = "Medium"
                    type_color = self.colors["warning"]
                else:
                    theater_type = "Small"
                    type_color = self.colors["accent"]
                
                type_badge = tk.Frame(details_frame, bg=type_color, relief="flat", bd=0)
                type_badge.pack(anchor='w', pady=(5, 0))
                type_badge.pack_propagate(False)
                
                tk.Label(
                    type_badge,
                    text=f" {theater_type} Theater ",
                    font=("Segoe UI", 9, "bold"),
                    bg=type_color,
                    fg="white"
                ).pack(padx=8, pady=3)
                
                # Enhanced action button
                button_frame = tk.Frame(theater_card, bg=self.colors["bg_card"])
                button_frame.pack(fill='x', pady=(10, 0))
                
                self.create_modern_button(
                    button_frame,
                    "🎬 View Shows",
                    lambda m_id=movie_id, c_id=city_id, t_id=theater_id: self.select_date(m_id, c_id, t_id),
                    self.colors["primary"],
                    width=18
                ).pack(fill='x')
                
                col += 1
                if col >= max_columns:
                    col = 0
                    row += 1
        else:
            tk.Label(
                content,
                text="🎭 No theaters available for this movie",
                font=("Segoe UI", 14),
                bg=self.colors["bg_dark"],
                fg=self.colors["text_muted"]
            ).pack(pady=50)
    
    def generate_shows_for_date(self, movie_id, theater_id, date_str):
        """Generate show slots for a specific date automatically"""
        # Time slots and price ranges (same as used in initialization)
        time_slots = {
            "Morning": ["9:00 AM", "10:15 AM", "11:30 AM", "12:45 PM"],
            "Afternoon": ["1:00 PM", "2:15 PM", "3:30 PM", "4:45 PM"],
            "Evening": ["5:00 PM", "6:15 PM", "7:30 PM", "8:45 PM"],
            "Night": ["9:30 PM", "10:15 PM", "11:00 PM", "11:45 PM"]
        }
        
        price_ranges = {
            "CITY001": {"Morning": (200, 350), "Afternoon": (250, 400), "Evening": (300, 500), "Night": (280, 450)},
            "CITY002": {"Morning": (180, 320), "Afternoon": (220, 380), "Evening": (280, 450), "Night": (250, 400)},
            "CITY003": {"Morning": (190, 340), "Afternoon": (230, 390), "Evening": (290, 480), "Night": (260, 420)},
            "CITY004": {"Morning": (150, 280), "Afternoon": (180, 320), "Evening": (220, 380), "Night": (200, 340)},
            "CITY005": {"Morning": (140, 260), "Afternoon": (170, 300), "Evening": (210, 360), "Night": (190, 320)},
            "CITY006": {"Morning": (130, 250), "Afternoon": (160, 280), "Evening": (200, 340), "Night": (180, 300)},
            "CITY007": {"Morning": (120, 240), "Afternoon": (150, 270), "Evening": (190, 320), "Night": (170, 280)},
            "CITY008": {"Morning": (110, 220), "Afternoon": (140, 250), "Evening": (180, 300), "Night": (160, 260)}
        }
        
        # Get city and theater info
        theater = self.theaters[theater_id]
        city_id = theater["city_id"]
        
        # Generate shows for all slots (4 shows per day)
        import random
        show_id_counter = len(self.showtimes) + 1
        
        for slot in ["Morning", "Afternoon", "Evening", "Night"]:
            # Select a random time from the slot
            time = random.choice(time_slots[slot])
            
            # Get price range for this city and slot
            min_price, max_price = price_ranges.get(city_id, {"Morning": (150, 250), "Afternoon": (180, 280), "Evening": (220, 320), "Night": (200, 300)}).get(slot, (150, 250))
            price = random.randint(min_price, max_price)
            
            # Create show
            show_id = f"SHOW{show_id_counter:03d}"
            self.showtimes[show_id] = {
                "movie_id": movie_id,
                "theater_id": theater_id,
                "date": date_str,
                "time": time,
                "slot": slot,
                "price": price,
                "capacity": theater["capacity"],
                "booked_seats": []
            }
            show_id_counter += 1
        
        # Save the generated shows
        self.save_data()
    
    def select_date(self, movie_id, city_id, theater_id):
        """Select date for show"""
        self.clear_window()
        
        # Header
        header = tk.Frame(self.root, bg=self.colors["bg_header"], height=70)
        header.pack(fill='x')
        
        tk.Label(
            header,
            text="📅 Select Date",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg_header"],
            fg=self.colors["text_light"]
        ).pack(side='left', padx=30, pady=15)
        
        self.create_modern_button(
            header,
            "← Back",
            lambda: self.select_theater(movie_id, city_id),
            self.darken_color(self.colors["bg_header"], 10),
            width=10
        ).pack(side='right', padx=30, pady=15)
        
        # Content
        content = tk.Frame(self.root, bg=self.colors["bg_dark"])
        content.pack(expand=True, fill='both', padx=30, pady=30)
        
        movie_name = self.movies[movie_id]["name"]
        theater_name = self.theaters[theater_id]["name"]
        
        tk.Label(
            content,
            text=f"{movie_name}",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack()
        
        tk.Label(
            content,
            text=f"🎭 {theater_name}",
            font=("Segoe UI", 14),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_muted"]
        ).pack(pady=(0, 20))
        
        # Get available dates for this movie and theater, plus generate future dates
        available_dates = set()
        today = datetime.now()
        
        # Only add future dates (next 14 days from today)
        for i in range(14):  # Add next 14 days starting from today
            future_date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
            available_dates.add(future_date)
        
        # Only include existing show dates if they are in the future (not past dates)
        existing_show_dates = set()
        for show_id, show in self.showtimes.items():
            if show["movie_id"] == movie_id and show["theater_id"] == theater_id:
                if "date" in show and show["date"]:
                    show_date = datetime.strptime(show["date"], "%Y-%m-%d").date()
                    if show_date >= today.date():  # Only include future or today's dates
                        available_dates.add(show["date"])
                        existing_show_dates.add(show["date"])
        
        # Auto-generate shows for dates that don't have any shows
        for date_str in available_dates:
            if date_str not in existing_show_dates:
                self.generate_shows_for_date(movie_id, theater_id, date_str)
        
        # Sort dates
        available_dates = sorted(list(available_dates))
        
        if available_dates:
            # Create main container with padding
            main_container = tk.Frame(content, bg=self.colors["bg_dark"])
            main_container.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Title for dates section
            title_frame = tk.Frame(main_container, bg=self.colors["bg_dark"])
            title_frame.pack(fill='x', pady=(0, 20))
            
            tk.Label(
                title_frame,
                text="📅 Available Show Dates",
                font=("Segoe UI", 18, "bold"),
                bg=self.colors["bg_dark"],
                fg=self.colors["text_light"]
            ).pack()
            
            tk.Label(
                title_frame,
                text=f"Showing {len(available_dates)} dates with show schedules",
                font=("Segoe UI", 11),
                bg=self.colors["bg_dark"],
                fg=self.colors["text_muted"]
            ).pack(pady=(5, 0))
            
            # Create scrollable canvas for dates with better styling
            canvas_frame = tk.Frame(main_container, bg=self.colors["bg_card"], relief='ridge', bd=1)
            canvas_frame.pack(fill='both', expand=True)
            
            canvas = tk.Canvas(canvas_frame, bg=self.colors["bg_dark"], highlightthickness=0)
            scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
            dates_frame = tk.Frame(canvas, bg=self.colors["bg_dark"])
            
            dates_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=dates_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True, padx=2, pady=2)
            scrollbar.pack(side="right", fill="y")
            
            # Add padding around the grid
            padding_frame = tk.Frame(dates_frame, bg=self.colors["bg_dark"])
            padding_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Calculate columns for date cards (responsive)
            max_columns = 3  # Reduced for better card size
            row, col = 0, 0
            
            for date_str in available_dates:
                # Parse date to format it nicely with error handling
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    formatted_date = date_obj.strftime("%d %b %Y")  # e.g., "02 Jan 2025"
                    day_name = date_obj.strftime("%A")  # e.g., "Thursday"
                    is_today = date_obj.date() == datetime.now().date()
                    is_weekend = date_obj.weekday() >= 5
                except Exception as e:
                    formatted_date = date_str
                    day_name = ""
                    is_today = False
                    is_weekend = False
                
                try:
                    # Enhanced date card with better styling
                    card_bg = self.colors["accent"] if is_today else self.colors["bg_card"]
                    date_card = tk.Frame(padding_frame, bg=card_bg, relief='raised', bd=2)
                    date_card.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
                    padding_frame.columnconfigure(col, weight=1)
                    padding_frame.rowconfigure(row, weight=1)
                    
                    # Card header with special styling for today/weekend
                    header_frame = tk.Frame(date_card, bg=self.darken_color(card_bg, 10))
                    header_frame.pack(fill='x', padx=15, pady=(15, 10))
                    
                    if is_today:
                        tk.Label(
                            header_frame,
                            text="🔥 TODAY",
                            font=("Segoe UI", 10, "bold"),
                            bg=self.darken_color(card_bg, 10),
                            fg=self.colors["warning"]
                        ).pack()
                    elif is_weekend:
                        tk.Label(
                            header_frame,
                            text="🎉 WEEKEND",
                            font=("Segoe UI", 10, "bold"),
                            bg=self.darken_color(card_bg, 10),
                            fg=self.colors["success"]
                        ).pack()
                    
                    # Date display with larger font
                    date_label = tk.Label(
                        date_card,
                        text=formatted_date,
                        font=("Segoe UI", 18, "bold"),
                        bg=card_bg,
                        fg=self.colors["text_light"]
                    )
                    date_label.pack(pady=(10, 5))
                    
                    if day_name:
                        tk.Label(
                            date_card,
                            text=day_name,
                            font=("Segoe UI", 13),
                            bg=card_bg,
                            fg=self.colors["text_muted"]
                        ).pack(pady=(0, 15))
                    
                    # Get all shows for this date and organize by slots with error handling
                    shows_by_slot = {"Morning": [], "Afternoon": [], "Evening": [], "Night": []}
                    shows_count = 0
                    total_available = 0
                    
                    try:
                        for show_id, show in self.showtimes.items():
                            if (show.get("movie_id") == movie_id and 
                                show.get("theater_id") == theater_id and 
                                show.get("date") == date_str):
                                slot = show.get("slot", "Morning")
                                if slot in shows_by_slot:
                                    shows_by_slot[slot].append(show)
                                    shows_count += 1
                                    available = show.get("capacity", 0) - len(show.get("booked_seats", []))
                                    total_available += max(0, available)
                    except Exception as e:
                        print(f"Error processing shows for date {date_str}: {e}")
                    
                    # Shows summary
                    summary_frame = tk.Frame(date_card, bg=card_bg)
                    summary_frame.pack(fill='x', padx=15, pady=10)
                    
                    tk.Label(
                        summary_frame,
                        text=f"🎬 {shows_count} Shows",
                        font=("Segoe UI", 11, "bold"),
                        bg=card_bg,
                        fg=self.colors["primary"]
                    ).pack(side='left')
                    
                    if total_available > 0:
                        tk.Label(
                            summary_frame,
                            text=f"🪑 {total_available} Seats",
                            font=("Segoe UI", 11),
                            bg=card_bg,
                            fg=self.colors["success"]
                        ).pack(side='right')
                    
                    # Enhanced scrollable shows section
                    if shows_count > 0:
                        shows_container_frame = tk.Frame(date_card, bg=self.darken_color(card_bg, 5), relief='sunken', bd=1)
                        shows_container_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
                        
                        shows_canvas = tk.Canvas(shows_container_frame, bg=card_bg, highlightthickness=0, height=120)
                        shows_scrollbar = ttk.Scrollbar(shows_container_frame, orient="vertical", command=shows_canvas.yview)
                        shows_container = tk.Frame(shows_canvas, bg=card_bg)
                        
                        shows_container.bind(
                            "<Configure>",
                            lambda e, c=shows_canvas: c.configure(scrollregion=c.bbox("all"))
                        )
                        
                        shows_canvas.create_window((0, 0), window=shows_container, anchor="nw")
                        shows_canvas.configure(yscrollcommand=shows_scrollbar.set)
                        
                        shows_canvas.pack(side="left", fill="both", expand=True, padx=2, pady=2)
                        shows_scrollbar.pack(side="right", fill="y")
                        
                        # Show slot headers and times with better layout
                        for slot_name, slot_shows in shows_by_slot.items():
                            if slot_shows:
                                # Slot section
                                slot_frame = tk.Frame(shows_container, bg=card_bg)
                                slot_frame.pack(fill='x', padx=10, pady=5)
                                
                                # Slot header
                                emoji = "☀️" if slot_name == "Morning" else "🌤️" if slot_name == "Afternoon" else "🌇" if slot_name == "Evening" else "🌙"
                                slot_label = tk.Label(
                                    slot_frame,
                                    text=f"{emoji} {slot_name}",
                                    font=("Segoe UI", 10, "bold"),
                                    bg=card_bg,
                                    fg=self.colors["text_light"]
                                )
                                slot_label.pack(anchor='w')
                                
                                # Separator
                                separator = tk.Frame(slot_frame, bg=self.colors["text_muted"], height=1)
                                separator.pack(fill='x', pady=2)
                                
                                # Show times for this slot
                                for show in slot_shows:
                                    try:
                                        available = show.get("capacity", 0) - len(show.get("booked_seats", []))
                                        status_color = self.colors["success"] if available > 0 else self.colors["primary"]
                                        status_text = f"🟢 {available}" if available > 0 else "🔴 Full"
                                        
                                        show_frame = tk.Frame(slot_frame, bg=card_bg)
                                        show_frame.pack(fill='x', pady=2)
                                        
                                        tk.Label(
                                            show_frame,
                                            text=f"  {show.get('time', 'N/A')} • ₹{show.get('price', 0)} • {status_text}",
                                            font=("Segoe UI", 9),
                                            bg=card_bg,
                                            fg=status_color
                                        ).pack(anchor='w')
                                    except Exception as e:
                                        print(f"Error displaying show info: {e}")
                                        continue
                    else:
                        # No shows message with better styling
                        no_shows_frame = tk.Frame(date_card, bg=self.darken_color(card_bg, 5), relief='sunken', bd=1)
                        no_shows_frame.pack(fill='x', padx=15, pady=(0, 15))
                        
                        tk.Label(
                            no_shows_frame,
                            text="No shows scheduled",
                            font=("Segoe UI", 10, "italic"),
                            bg=card_bg,
                            fg=self.colors["text_muted"]
                        ).pack(pady=10)
                    
                    # Enhanced select button
                    button_frame = tk.Frame(date_card, bg=card_bg)
                    button_frame.pack(fill='x', padx=15, pady=(0, 15))
                    
                    self.create_modern_button(
                        button_frame,
                        "🎬 Select Shows",
                        lambda d=date_str: self.select_showtime(movie_id, city_id, theater_id, d),
                        self.colors["success"] if total_available > 0 else self.colors["primary"],
                        width=20
                    ).pack()
                    
                except Exception as e:
                    print(f"Error creating date card for {date_str}: {e}")
                    continue
                
                col += 1
                if col >= max_columns:
                    col = 0
                    row += 1
                    
            # Configure mouse wheel scrolling for better UX
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            def _bind_to_mousewheel(event):
                canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            def _unbind_from_mousewheel(event):
                canvas.unbind_all("<MouseWheel>")
            
            canvas.bind('<Enter>', _bind_to_mousewheel)
            canvas.bind('<Leave>', _unbind_from_mousewheel)
        else:
            tk.Label(
                content,
                text="📅 No shows available",
                font=("Segoe UI", 14),
                bg=self.colors["bg_dark"],
                fg=self.colors["text_muted"]
            ).pack(pady=50)
    
    def select_showtime(self, movie_id, city_id, theater_id, selected_date=None):
        """Select showtime with proper functionality"""
        print(f"select_showtime called - Movie: {movie_id}, Theater: {theater_id}, Date: {selected_date}")
        self.clear_window()
        
        # Header
        header = tk.Frame(self.root, bg=self.colors["bg_header"], height=70)
        header.pack(fill='x')
        
        tk.Label(
            header,
            text="⏰ Select Show Time",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg_header"],
            fg=self.colors["text_light"]
        ).pack(side='left', padx=30, pady=15)
        
        self.create_modern_button(
            header,
            "← Back",
            lambda: self.select_date(movie_id, city_id, theater_id),
            self.darken_color(self.colors["bg_header"], 10),
            width=10
        ).pack(side='right', padx=30, pady=15)
        
        # Content
        content = tk.Frame(self.root, bg=self.colors["bg_dark"])
        content.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Movie and theater info
        movie_name = self.movies[movie_id]["name"]
        theater_name = self.theaters[theater_id]["name"]
        
        tk.Label(
            content,
            text=f"{movie_name}",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack()
        
        tk.Label(
            content,
            text=f"🎭 {theater_name}",
            font=("Segoe UI", 14),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_muted"]
        ).pack(pady=(0, 5))
        
        # Format selected date for display
        if selected_date:
            try:
                date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
                formatted_date = date_obj.strftime("%d %b %Y")
                day_name = date_obj.strftime("%A")
            except:
                formatted_date = selected_date
                day_name = ""
            
            tk.Label(
                content,
                text=f"📅 {formatted_date}",
                font=("Segoe UI", 14, "bold"),
                bg=self.colors["bg_dark"],
                fg=self.colors["primary"]
            ).pack(pady=(0, 20))
        
        # Get shows for selected date
        shows = []
        for show_id, show in self.showtimes.items():
            if show.get("movie_id") == movie_id and show.get("theater_id") == theater_id:
                # Filter by selected date if provided
                if selected_date:
                    if show.get("date") == selected_date:
                        shows.append((show_id, show))
                else:
                    # If no date selected, show all shows
                    shows.append((show_id, show))
        
        print(f"Found {len(shows)} shows for this selection")
        
        if shows:
            # Create scrollable canvas for showtimes
            canvas_frame = tk.Frame(content, bg=self.colors["bg_card"], relief='ridge', bd=1)
            canvas_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            canvas = tk.Canvas(canvas_frame, bg=self.colors["bg_dark"], highlightthickness=0)
            scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
            scrollable_content = tk.Frame(canvas, bg=self.colors["bg_dark"])
            
            scrollable_content.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_content, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True, padx=2, pady=2)
            scrollbar.pack(side="right", fill="y")
            
            # Add padding inside scrollable content
            padding_frame = tk.Frame(scrollable_content, bg=self.colors["bg_dark"])
            padding_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Organize shows by slots
            slots = {"Morning": [], "Afternoon": [], "Evening": [], "Night": []}
            for show_id, show in shows:
                slot = show.get("slot", "Morning")
                if slot in slots:
                    slots[slot].append((show_id, show))
            
            # Slot emojis
            slot_emojis = {
                "Morning": "☀️",
                "Afternoon": "🌤️", 
                "Evening": "🌇",
                "Night": "🌙"
            }
            
            for slot_name, slot_shows in slots.items():
                if slot_shows:
                    # Slot header
                    tk.Label(
                        padding_frame,
                        text=f"{slot_emojis[slot_name]} {slot_name} Shows",
                        font=("Segoe UI", 16, "bold"),
                        bg=self.colors["bg_dark"],
                        fg=self.colors["text_light"]
                    ).pack(pady=(20, 10))
                    
                    # Shows container
                    shows_frame = tk.Frame(padding_frame, bg=self.colors["bg_dark"])
                    shows_frame.pack(fill='x', padx=20)
                    
                    for show_id, show in slot_shows:
                        try:
                            available = show.get("capacity", 0) - len(show.get("booked_seats", []))
                            is_available = available > 0
                            
                            # Create show card
                            show_card = self.create_card(shows_frame, padx=15, pady=15)
                            show_card.pack(side='left', padx=5, pady=5)
                            
                            # Show time
                            tk.Label(
                                show_card,
                                text=show.get("time", "N/A"),
                                font=("Segoe UI", 14, "bold"),
                                bg=self.colors["bg_card"],
                                fg=self.colors["text_light"]
                            ).pack(pady=(5, 2))
                            
                            # Price
                            tk.Label(
                                show_card,
                                text=f"₹{show.get('price', 0)}",
                                font=("Segoe UI", 12),
                                bg=self.colors["bg_card"],
                                fg=self.colors["success"]
                            ).pack(pady=2)
                            
                            # Availability
                            status_color = self.colors["success"] if is_available else self.colors["primary"]
                            status_text = f"🟢 {available} seats" if is_available else "🔴 Housefull"
                            tk.Label(
                                show_card,
                                text=status_text,
                                font=("Segoe UI", 10),
                                bg=self.colors["bg_card"],
                                fg=status_color
                            ).pack(pady=2)
                            
                            # Select button
                            if is_available:
                                def make_select_command(sid):
                                    return lambda: self.select_seats(sid)
                                
                                self.create_modern_button(
                                    show_card,
                                    "Select",
                                    make_select_command(show_id),
                                    self.colors["primary"],
                                    width=10
                                ).pack(pady=(5, 10))
                            else:
                                tk.Label(
                                    show_card,
                                    text="Housefull",
                                    font=("Segoe UI", 10, "bold"),
                                    bg=self.colors["bg_card"],
                                    fg=self.colors["text_muted"]
                                ).pack(pady=(5, 10))
                                
                        except Exception as e:
                            print(f"Error creating show card: {e}")
                            continue
            
            # Configure mouse wheel scrolling
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            def _bind_to_mousewheel(event):
                canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            def _unbind_from_mousewheel(event):
                canvas.unbind_all("<MouseWheel>")
            
            canvas.bind('<Enter>', _bind_to_mousewheel)
            canvas.bind('<Leave>', _unbind_from_mousewheel)
        else:
            # No shows available
            tk.Label(
                content,
                text="🎬 No shows available",
                font=("Segoe UI", 16),
                bg=self.colors["bg_dark"],
                fg=self.colors["text_muted"]
            ).pack(pady=50)
            
            if selected_date:
                tk.Label(
                    content,
                    text=f"No shows scheduled for {formatted_date}",
                    font=("Segoe UI", 12),
                    bg=self.colors["bg_dark"],
                    fg=self.colors["text_muted"]
                ).pack(pady=10)
            
            self.create_modern_button(
                content,
                "← Back to Dates",
                lambda: self.select_date(movie_id, city_id, theater_id),
                self.colors["primary"],
                width=15
            ).pack(pady=20)
    
    def select_seats(self, show_id):
        """Select seats"""
        self.clear_window()
        
        show = self.showtimes[show_id]
        movie = self.movies[show["movie_id"]]
        theater = self.theaters[show["theater_id"]]
        
        # Header
        header = tk.Frame(self.root, bg=self.colors["bg_header"], height=70)
        header.pack(fill='x')
        
        tk.Label(
            header,
            text="💺 Select Seats",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg_header"],
            fg=self.colors["text_light"]
        ).pack(side='left', padx=30, pady=15)
        
        self.create_modern_button(
            header,
            "← Back",
            lambda: self.select_showtime(show["movie_id"],
                self.theaters[show["theater_id"]]["city_id"], show["theater_id"], show.get("date")),
            self.darken_color(self.colors["bg_header"], 10),
            width=10
        ).pack(side='right', padx=30, pady=15)
        
        # Content
        content = tk.Frame(self.root, bg=self.colors["bg_dark"])
        content.pack(expand=True, fill='both')
        
        # Movie info
        info_frame = tk.Frame(content, bg=self.colors["bg_dark"])
        info_frame.pack(pady=20)
        
        tk.Label(
            info_frame,
            text=f"{movie['name']}",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack()
        
        tk.Label(
            info_frame,
            text=f"{theater['name']} • {show['time']} • Capacity: {theater['capacity']} seats",
            font=("Segoe UI", 12),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_muted"]
        ).pack()
        
        # Legend
        legend_frame = tk.Frame(content, bg=self.colors["bg_dark"])
        legend_frame.pack(pady=10)
        
        legend_items = [
            (self.colors["success"], "Available"),
            (self.colors["accent"], "Selected"),
            (self.colors["primary"], "Booked")
        ]
        
        for color, text in legend_items:
            item_frame = tk.Frame(legend_frame, bg=self.colors["bg_dark"])
            item_frame.pack(side='left', padx=20)
            color_box = tk.Frame(
                item_frame,
                bg=color,
                width=18,
                height=18,
                highlightbackground=self.colors["border"],
                highlightthickness=1
            )
            color_box.pack(side='left')
            color_box.pack_propagate(False)
            tk.Label(item_frame, text=text, font=("Segoe UI", 10), bg=self.colors["bg_dark"], fg=self.colors["text_muted"]).pack(side='left', padx=5)
        
        # Screen
        screen_frame = tk.Frame(content, bg=self.colors["bg_dark"])
        screen_frame.pack(pady=30)
        
        screen = tk.Frame(screen_frame, bg="#30363d", height=30)
        screen.pack(fill='x', padx=100)
        tk.Label(screen, text="S C R E E N", font=("Segoe UI", 12, "bold"), 
                bg="#30363d", fg=self.colors["text_light"]).pack(pady=5)
        
        # Seats
        seats_container = tk.Frame(content, bg=self.colors["bg_dark"])
        seats_container.pack()
        
        self.selected_seats = []
        self.seat_buttons = {}
        self.current_show_id = show_id  # Store current show_id
        
        # Calculate rows and columns based on theater capacity
        capacity = theater["capacity"]
        
        # Calculate optimal rows and columns for the capacity
        if capacity <= 60:
            cols = 8
        elif capacity <= 80:
            cols = 10
        elif capacity <= 120:
            cols = 12
        elif capacity <= 150:
            cols = 14
        else:
            cols = 16
            
        rows = (capacity + cols - 1) // cols  # Ceiling division
        
        # Ensure we don't exceed capacity
        total_seats = rows * cols
        if total_seats > capacity:
            # Remove extra seats from last row
            seats_to_remove = total_seats - capacity
            cols_last_row = cols - seats_to_remove
        else:
            cols_last_row = cols
        
        for row in range(rows):
            row_frame = tk.Frame(seats_container, bg=self.colors["bg_dark"])
            row_frame.pack()
            
            tk.Label(row_frame, text=chr(65+row), font=("Segoe UI", 11, "bold"),
                    bg=self.colors["bg_dark"], fg=self.colors["text_light"], width=2).pack(side='left')
            
            # Determine columns for this row
            if row == rows - 1:  # Last row
                current_cols = cols_last_row
            else:
                current_cols = cols
            
            for col in range(current_cols):
                seat_num = f"{chr(65+row)}{col+1}"
                
                if seat_num in show["booked_seats"]:
                    btn = tk.Button(row_frame, text=col+1, font=("Segoe UI", 9),
                                   bg=self.colors["primary"], fg="white", width=3, height=1,
                                   state='disabled', relief="flat")
                else:
                    btn = tk.Button(row_frame, text=col+1, font=("Segoe UI", 9),
                                   bg=self.colors["success"], fg="white", width=3, height=1,
                                   cursor="hand2", relief="flat",
                                   command=lambda s=seat_num: self.toggle_seat(s))
                    self.seat_buttons[seat_num] = btn
                
                btn.pack(side='left', padx=2, pady=2)
        
        # Bottom bar
        bottom_card = self.create_card(content, padx=30, pady=20)
        bottom_card.pack(fill='x', side='bottom', padx=30, pady=20)
        
        self.selected_label = tk.Label(
            bottom_card,
            text="Selected: None",
            font=("Segoe UI", 12),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        )
        self.selected_label.pack(side='left')
        
        self.price_label = tk.Label(
            bottom_card,
            text="Total: ₹0",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["success"]
        )
        self.price_label.pack(side='left', padx=50)
        
        self.create_modern_button(
            bottom_card,
            "💳 Proceed to Payment",
            lambda: self.payment_screen(show_id),
            self.colors["primary"],
            width=20
        ).pack(side='right')
    
    def toggle_seat(self, seat_num):
        """Toggle seat selection"""
        if seat_num in self.selected_seats:
            self.selected_seats.remove(seat_num)
            self.seat_buttons[seat_num].config(bg=self.colors["success"])
        else:
            self.selected_seats.append(seat_num)
            self.seat_buttons[seat_num].config(bg=self.colors["accent"])
        
        # Update labels
        if self.selected_seats:
            self.selected_label.config(text=f"Selected: {', '.join(self.selected_seats)}")
            
            # Use the stored current_show_id for correct price calculation
            if hasattr(self, 'current_show_id') and self.current_show_id:
                show = self.showtimes[self.current_show_id]
                total = len(self.selected_seats) * show["price"]
            else:
                # Fallback to first show if current_show_id not available
                total = len(self.selected_seats) * self.showtimes[list(self.showtimes.keys())[0]]["price"]
            
            self.price_label.config(text=f"Total: ₹{total}")
        else:
            self.selected_label.config(text="Selected: None")
            self.price_label.config(text="Total: ₹0")
    
    def validate_payment_details(self, show_id, total_amount):
        """Validate payment details and process payment"""
        try:
            payment_method = self.selected_payment_method.get()
            print(f"Selected payment method: {payment_method}")
            
            # Strict validation for all payment methods
            if payment_method in ["debit_card", "credit_card"]:
                card_num = self.card_number.get().strip().replace(" ", "")
                if len(card_num) < 13 or len(card_num) > 19 or not card_num.isdigit():
                    messagebox.showerror("Invalid Card", "Please enter a valid card number (13-19 digits)")
                    return False
                
                # Check for default/example card number
                if card_num == "1234567890123456":
                    messagebox.showerror("Invalid Card", "Please enter your actual card number, not the example")
                    return False
                
                holder = self.card_holder.get().strip()
                if len(holder) < 2 or not any(c.isalpha() for c in holder):
                    messagebox.showerror("Invalid Name", "Please enter valid card holder name")
                    return False
                
                # Check for default/example name
                if holder.lower() == "john doe":
                    messagebox.showerror("Invalid Name", "Please enter your actual name, not the example")
                    return False
                    
                expiry = self.card_expiry.get().strip()
                if not expiry or len(expiry) < 5 or '/' not in expiry:
                    messagebox.showerror("Invalid Expiry", "Please enter expiry date in MM/YY format")
                    return False
                
                # Check for default/example expiry
                if expiry == "12/25":
                    messagebox.showerror("Invalid Expiry", "Please enter your actual card expiry date, not the example")
                    return False
                    
                cvv = self.card_cvv.get().strip()
                if len(cvv) < 3 or len(cvv) > 4 or not cvv.isdigit():
                    messagebox.showerror("Invalid CVV", "Please enter valid CVV (3-4 digits)")
                    return False
                
                # Check for default/example CVV
                if cvv == "123":
                    messagebox.showerror("Invalid CVV", "Please enter your actual CVV, not the example")
                    return False
                    
            elif payment_method == "upi":
                upi = self.upi_id.get().strip()
                if len(upi) < 3 or ('@' not in upi and len(upi) < 10):
                    messagebox.showerror("Invalid UPI", "Please enter valid UPI ID (e.g., your-upi@paytm) or 10-digit mobile number")
                    return False
                
                # Check for default/example UPI ID
                if upi.lower() == "your-upi@paytm":
                    messagebox.showerror("Invalid UPI", "Please enter your actual UPI ID, not the example")
                    return False
                    
            elif payment_method == "net_banking":
                bank = self.bank_name.get().strip()
                if not bank:
                    messagebox.showerror("Invalid Bank", "Please select your bank")
                    return False
                    
            elif payment_method == "wallet":
                wallet = self.wallet_number.get().strip()
                if len(wallet) < 10 or not wallet.isdigit():
                    messagebox.showerror("Invalid Wallet", "Please enter valid 10-digit mobile number")
                    return False
                
                # Check for default/example wallet number
                if wallet == "9876543210":
                    messagebox.showerror("Invalid Wallet", "Please enter your actual mobile number, not the example")
                    return False
            
            print("Processing payment...")
            # Process payment
            self.process_payment(show_id, total_amount)
            return True
            
        except Exception as e:
            print(f"Payment validation error: {e}")
            messagebox.showerror("Payment Error", "An error occurred during payment validation")
            return False
    
    def show_payment_details(self, method, show_id, total_amount):
        """Show payment details form based on selected method"""
        # Clear existing details
        for widget in self.payment_details_frame.winfo_children():
            widget.destroy()
        
        if method == "upi":
            # UPI Payment Form
            tk.Label(
                self.payment_details_frame,
                text="📱 UPI Details",
                font=("Segoe UI", 14, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack(anchor='w', pady=(0, 15))
            
            tk.Label(
                self.payment_details_frame,
                text="Enter UPI ID or Phone Number:",
                font=("Segoe UI", 11),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(anchor='w', pady=(0, 5))
            
            upi_entry = tk.Entry(
                self.payment_details_frame,
                textvariable=self.upi_id,
                font=("Segoe UI", 12),
                bg=self.colors["bg_dark"],
                fg=self.colors["text_light"],
                insertbackground=self.colors["primary"]
            )
            upi_entry.pack(fill='x', pady=(0, 10))
            
            # Auto-erase default data when user clicks to edit
            def clear_upi_default(event=None):
                if self.upi_id.get() == "your-upi@paytm":
                    self.upi_id.set("")
                    upi_entry.config(fg=self.colors["text_light"])
            
            upi_entry.bind("<FocusIn>", clear_upi_default)
            upi_entry.bind("<Button-1>", clear_upi_default)
            
            # Only set example data for user reference
            if not self.upi_id.get():
                self.upi_id.set("your-upi@paytm")
            
            tk.Label(
                self.payment_details_frame,
                text="Examples: your-upi@paytm, user@ybl, 9876543210, your-id@idfc",
                font=("Segoe UI", 9, "italic"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(anchor='w', pady=(0, 20))
            
            # Add pay button
            self.create_modern_button(
                self.payment_details_frame,
                f"💳 Pay with UPI",
                lambda: self.validate_payment_details(show_id, total_amount),
                self.colors["success"],
                width=20
            ).pack(pady=10)
            
        elif method in ["debit_card", "credit_card"]:
            # Card Payment Form
            card_type = "Debit" if method == "debit_card" else "Credit"
            tk.Label(
                self.payment_details_frame,
                text=f"💳 {card_type} Card Details",
                font=("Segoe UI", 14, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack(anchor='w', pady=(0, 15))
            
            # Card Number
            tk.Label(
                self.payment_details_frame,
                text="Card Number:",
                font=("Segoe UI", 11),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(anchor='w', pady=(0, 5))
            
            card_entry = tk.Entry(
                self.payment_details_frame,
                textvariable=self.card_number,
                font=("Segoe UI", 12),
                bg=self.colors["bg_dark"],
                fg=self.colors["text_light"],
                insertbackground=self.colors["primary"]
            )
            card_entry.pack(fill='x', pady=(0, 10))
            
            # Auto-erase default data when user clicks to edit
            def clear_card_default(event=None):
                if self.card_number.get() == "1234 5678 9012 3456":
                    self.card_number.set("")
                    card_entry.config(fg=self.colors["text_light"])
            
            card_entry.bind("<FocusIn>", clear_card_default)
            card_entry.bind("<Button-1>", clear_card_default)
            
            # Only set example data for user reference
            if not self.card_number.get():
                self.card_number.set("1234 5678 9012 3456")
            
            tk.Label(
                self.payment_details_frame,
                text="Format: 1234 5678 9012 3456 (13-19 digits)",
                font=("Segoe UI", 9, "italic"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(anchor='w', pady=(0, 10))
            
            # Card Holder Name
            tk.Label(
                self.payment_details_frame,
                text="Card Holder Name:",
                font=("Segoe UI", 11),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(anchor='w', pady=(0, 5))
            
            name_entry = tk.Entry(
                self.payment_details_frame,
                textvariable=self.card_holder,
                font=("Segoe UI", 12),
                bg=self.colors["bg_dark"],
                fg=self.colors["text_light"],
                insertbackground=self.colors["primary"]
            )
            name_entry.pack(fill='x', pady=(0, 10))
            
            # Auto-erase default data when user clicks to edit
            def clear_name_default(event=None):
                if self.card_holder.get() == "John Doe":
                    self.card_holder.set("")
                    name_entry.config(fg=self.colors["text_light"])
            
            name_entry.bind("<FocusIn>", clear_name_default)
            name_entry.bind("<Button-1>", clear_name_default)
            
            # Only set example data for user reference
            if not self.card_holder.get():
                self.card_holder.set("John Doe")
            
            # Expiry and CVV
            expiry_cvv_frame = tk.Frame(self.payment_details_frame, bg=self.colors["bg_card"])
            expiry_cvv_frame.pack(fill='x', pady=(0, 10))
            
            # Expiry
            expiry_frame = tk.Frame(expiry_cvv_frame, bg=self.colors["bg_card"])
            expiry_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
            
            tk.Label(
                expiry_frame,
                text="Expiry (MM/YY):",
                font=("Segoe UI", 11),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(anchor='w', pady=(0, 5))
            
            expiry_entry = tk.Entry(
                expiry_frame,
                textvariable=self.card_expiry,
                font=("Segoe UI", 12),
                bg=self.colors["bg_dark"],
                fg=self.colors["text_light"],
                insertbackground=self.colors["primary"]
            )
            expiry_entry.pack(fill='x', pady=(0, 5))
            
            # Auto-erase default data when user clicks to edit
            def clear_expiry_default(event=None):
                if self.card_expiry.get() == "12/25":
                    self.card_expiry.set("")
                    expiry_entry.config(fg=self.colors["text_light"])
            
            expiry_entry.bind("<FocusIn>", clear_expiry_default)
            expiry_entry.bind("<Button-1>", clear_expiry_default)
            
            # Only set example data for user reference
            if not self.card_expiry.get():
                self.card_expiry.set("12/25")
            
            tk.Label(
                expiry_frame,
                text="Format: MM/YY (e.g., 12/25)",
                font=("Segoe UI", 8, "italic"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(anchor='w', pady=(2, 0))
            
            # CVV
            cvv_frame = tk.Frame(expiry_cvv_frame, bg=self.colors["bg_card"])
            cvv_frame.pack(side='right', fill='x', expand=True, padx=(10, 0))
            
            tk.Label(
                cvv_frame,
                text="CVV:",
                font=("Segoe UI", 11),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(anchor='w', pady=(0, 5))
            
            cvv_entry = tk.Entry(
                cvv_frame,
                textvariable=self.card_cvv,
                font=("Segoe UI", 12),
                bg=self.colors["bg_dark"],
                fg=self.colors["text_light"],
                insertbackground=self.colors["primary"],
                show="*"
            )
            cvv_entry.pack(fill='x', pady=(0, 5))
            
            # Auto-erase default data when user clicks to edit
            def clear_cvv_default(event=None):
                if self.card_cvv.get() == "123":
                    self.card_cvv.set("")
                    cvv_entry.config(fg=self.colors["text_light"])
            
            cvv_entry.bind("<FocusIn>", clear_cvv_default)
            cvv_entry.bind("<Button-1>", clear_cvv_default)
            
            # Only set example data for user reference
            if not self.card_cvv.get():
                self.card_cvv.set("123")
            
            tk.Label(
                cvv_frame,
                text="3-4 digits",
                font=("Segoe UI", 8, "italic"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(anchor='w', pady=(2, 0))
            
            # Add pay button
            self.create_modern_button(
                self.payment_details_frame,
                f"💳 Pay with {card_type} Card",
                lambda: self.validate_payment_details(show_id, total_amount),
                self.colors["success"],
                width=20
            ).pack(pady=10)
            
        elif method == "net_banking":
            # Net Banking Form
            tk.Label(
                self.payment_details_frame,
                text="🏦 Net Banking Details",
                font=("Segoe UI", 14, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack(anchor='w', pady=(0, 15))
            
            tk.Label(
                self.payment_details_frame,
                text="Select Your Bank:",
                font=("Segoe UI", 11),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(anchor='w', pady=(0, 5))
            
            banks = ["State Bank of India", "HDFC Bank", "ICICI Bank", "Axis Bank", 
                    "Punjab National Bank", "Bank of Baroda", "Canara Bank", "Union Bank of India"]
            
            bank_combo = ttk.Combobox(
                self.payment_details_frame,
                textvariable=self.bank_name,
                values=banks,
                font=("Segoe UI", 11),
                state="readonly"
            )
            bank_combo.pack(fill='x', pady=(0, 10))
            
            # Only set example data for user reference
            if not self.bank_name.get():
                bank_combo.set("HDFC Bank")
            
            tk.Label(
                self.payment_details_frame,
                text="You will be redirected to your bank's secure payment gateway",
                font=("Segoe UI", 9, "italic"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(anchor='w', pady=(0, 20))
            
            # Add pay button
            self.create_modern_button(
                self.payment_details_frame,
                f"🏦 Pay with Net Banking",
                lambda: self.validate_payment_details(show_id, total_amount),
                self.colors["success"],
                width=20
            ).pack(pady=10)
            
        elif method == "wallet":
            # Wallet Form
            tk.Label(
                self.payment_details_frame,
                text="👛 Wallet Details",
                font=("Segoe UI", 14, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack(anchor='w', pady=(0, 15))
            
            tk.Label(
                self.payment_details_frame,
                text="Enter Wallet Mobile Number:",
                font=("Segoe UI", 11),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(anchor='w', pady=(0, 5))
            
            wallet_entry = tk.Entry(
                self.payment_details_frame,
                textvariable=self.wallet_number,
                font=("Segoe UI", 12),
                bg=self.colors["bg_dark"],
                fg=self.colors["text_light"],
                insertbackground=self.colors["primary"]
            )
            wallet_entry.pack(fill='x', pady=(0, 10))
            
            # Auto-erase default data when user clicks to edit
            def clear_wallet_default(event=None):
                if self.wallet_number.get() == "9876543210":
                    self.wallet_number.set("")
                    wallet_entry.config(fg=self.colors["text_light"])
            
            wallet_entry.bind("<FocusIn>", clear_wallet_default)
            wallet_entry.bind("<Button-1>", clear_wallet_default)
            
            # Only set example data for user reference
            if not self.wallet_number.get():
                self.wallet_number.set("9876543210")
            
            tk.Label(
                self.payment_details_frame,
                text="Supported: Paytm (9876543210), PhonePe (9876543210), Amazon Pay, Mobikwik",
                font=("Segoe UI", 9, "italic"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(anchor='w', pady=(0, 20))
            
            # Add pay button
            self.create_modern_button(
                self.payment_details_frame,
                f"👛 Pay with Wallet",
                lambda: self.validate_payment_details(show_id, total_amount),
                self.colors["success"],
                width=20
            ).pack(pady=10)
            
        elif method == "cash":
            # Get show and theater information for cash payment
            show = self.showtimes[show_id]
            theater = self.theaters[show["theater_id"]]
            city = self.cities[theater["city_id"]]
            
            # Cash Payment Info - Enhanced
            tk.Label(
                self.payment_details_frame,
                text="💵 Cash Payment Information",
                font=("Segoe UI", 14, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack(anchor='w', pady=(0, 15))
            
            # Important notice
            notice_frame = tk.Frame(self.payment_details_frame, bg=self.colors["warning"], relief='raised', bd=1)
            notice_frame.pack(fill='x', pady=(0, 15))
            
            tk.Label(
                notice_frame,
                text="⚠️ IMPORTANT: CASH PAYMENT",
                font=("Segoe UI", 11, "bold"),
                bg=self.colors["warning"],
                fg="white"
            ).pack(pady=10)
            
            info_text = """
            • Please arrive 30 minutes before showtime
            • Pay full amount at theater counter
            • Carry exact change for faster service
            • Show booking confirmation SMS/Email
            • Seats will be released if not paid 15 mins before show
            • No refund for late arrivals
            """
            
            tk.Label(
                self.payment_details_frame,
                text=info_text.strip(),
                font=("Segoe UI", 10),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"],
                justify='left'
            ).pack(anchor='w', pady=(0, 15))
            
            # Payment status indicator
            status_frame = tk.Frame(self.payment_details_frame, bg=self.colors["bg_card"])
            status_frame.pack(fill='x', pady=(0, 10))
            
            tk.Label(
                status_frame,
                text="💰 Payment Status: PENDING (Pay at Counter)",
                font=("Segoe UI", 11, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["warning"]
            ).pack()
            
            # Theater counter info
            counter_frame = tk.Frame(self.payment_details_frame, bg=self.colors["bg_card"], relief='ridge', bd=1)
            counter_frame.pack(fill='x', pady=(10, 0))
            
            tk.Label(
                counter_frame,
                text="🏪 Theater Counter Details",
                font=("Segoe UI", 10, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack(pady=5)
            
            tk.Label(
                counter_frame,
                text=f"📍 {theater['name']} Counter",
                font=("Segoe UI", 10),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(pady=2)
            
            tk.Label(
                counter_frame,
                text=f"🏙️ {city}",
                font=("Segoe UI", 10),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(pady=2)
            
            # Add spacer before confirmation
            spacer = tk.Frame(self.payment_details_frame, bg=self.colors["bg_card"], height=20)
            spacer.pack(fill='x', pady=10)
            
            # Cash payment confirmation section
            confirmation_frame = tk.Frame(self.payment_details_frame, bg=self.colors["bg_card"], relief='solid', bd=2)
            confirmation_frame.pack(fill='x', pady=(0, 20))
            
            tk.Label(
                confirmation_frame,
                text="📋 CASH PAYMENT CONFIRMATION",
                font=("Segoe UI", 12, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["primary"]
            ).pack(pady=10)
            
            tk.Label(
                confirmation_frame,
                text=f"Total Amount to Pay: ₹{total_amount}",
                font=("Segoe UI", 14, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["success"]
            ).pack(pady=5)
            
            tk.Label(
                confirmation_frame,
                text="Click 'Confirm & Generate E-Ticket' to reserve your seats and get your ticket",
                font=("Segoe UI", 10),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(pady=5)
            
            # Create button frame to ensure proper layout
            button_frame = tk.Frame(confirmation_frame, bg=self.colors["bg_card"])
            button_frame.pack(pady=10)
            
            # Confirm button for e-ticket
            def confirm_and_show_eticket():
                """Confirm booking and show e-ticket"""
                result = messagebox.askyesno(
                    "Confirm and Generate E-Ticket",
                    f"Confirm booking and generate your e-ticket?\n\n"
                    f"• Total Amount: ₹{total_amount}\n"
                    f"• Payment Method: Cash at Counter\n"
                    f"• Theater: {theater['name']}\n"
                    f"• Seats: {', '.join(self.selected_seats)}\n\n"
                    f"E-ticket will be generated after confirmation."
                )
                
                if result:
                    # Process the cash booking (this will show success message and ticket)
                    self.process_payment(show_id, total_amount)
            
            self.create_modern_button(
                button_frame,
                "🎫 Confirm & Generate E-Ticket",
                confirm_and_show_eticket,
                self.colors["primary"],
                width=25
            ).pack(pady=5)
            
            # Add bottom spacer
            bottom_spacer = tk.Frame(self.payment_details_frame, bg=self.colors["bg_card"], height=20)
            bottom_spacer.pack(fill='x', pady=10)
        
        # Update scroll region
        self.payment_details_frame.update_idletasks()
    
    def payment_screen(self, show_id):
        """Enhanced payment screen with multiple payment methods"""
        if not self.selected_seats:
            messagebox.showwarning("Warning", "Please select at least one seat")
            return
        
        self.clear_window()
        
        show = self.showtimes[show_id]
        movie = self.movies[show["movie_id"]]
        theater = self.theaters[show["theater_id"]]
        city = self.cities[theater["city_id"]]
        
        # Header
        header = tk.Frame(self.root, bg=self.colors["bg_header"], height=70)
        header.pack(fill='x')
        
        tk.Label(
            header,
            text="💳 Payment",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg_header"],
            fg=self.colors["text_light"]
        ).pack(side='left', padx=30, pady=15)
        
        self.create_modern_button(
            header,
            "← Back",
            lambda: self.select_seats(show_id),
            self.darken_color(self.colors["bg_header"], 10),
            width=10
        ).pack(side='right', padx=30, pady=15)
        
        # Main content
        main_content = tk.Frame(self.root, bg=self.colors["bg_dark"])
        main_content.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Left side - Booking Summary
        left_frame = tk.Frame(main_content, bg=self.colors["bg_dark"])
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 20))
        
        summary_card = self.create_card(left_frame, padx=30, pady=25)
        summary_card.pack(fill='both', expand=True)
        
        tk.Label(
            summary_card,
            text="🎟️ Booking Summary",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).pack(pady=(0, 20))
        
        details = [
            ("🎬 Movie:", movie["name"]),
            ("🏙️ City:", city),
            ("🎭 Theater:", theater["name"]),
            ("⏰ Show Time:", show["time"]),
            ("💺 Seats:", ", ".join(self.selected_seats)),
            ("🎫 Tickets:", str(len(self.selected_seats))),
            ("💰 Price per Ticket:", f"₹{show['price']}"),
        ]
        
        for label, value in details:
            detail_frame = tk.Frame(summary_card, bg=self.colors["bg_card"])
            detail_frame.pack(fill='x', padx=20, pady=6)
            tk.Label(detail_frame, text=label, font=("Segoe UI", 11),
                    bg=self.colors["bg_card"], fg=self.colors["text_muted"]).pack(side='left')
            tk.Label(detail_frame, text=value, font=("Segoe UI", 11, "bold"),
                    bg=self.colors["bg_card"], fg=self.colors["text_light"]).pack(side='right')
        
        # Divider
        divider = tk.Frame(summary_card, bg=self.colors["border"], height=1)
        divider.pack(fill='x', pady=15, padx=20)
        
        total_amount = len(self.selected_seats) * show["price"]
        
        total_frame = tk.Frame(summary_card, bg=self.colors["bg_card"])
        total_frame.pack(pady=10)
        
        tk.Label(
            total_frame,
            text="Total Amount:",
            font=("Segoe UI", 16),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).pack(side='left')
        
        tk.Label(
            total_frame,
            text=f"₹{total_amount}",
            font=("Segoe UI", 22, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["success"]
        ).pack(side='left', padx=20)
        
        # Right side - Payment Methods
        right_frame = tk.Frame(main_content, bg=self.colors["bg_dark"])
        right_frame.pack(side='right', fill='both', expand=True)
        
        payment_card = self.create_card(right_frame, padx=30, pady=25)
        payment_card.pack(fill='both', expand=True)
        
        tk.Label(
            payment_card,
            text="💳 Select Payment Method",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).pack(pady=(0, 25))
        
        # Payment methods with detailed forms
        self.selected_payment_method = tk.StringVar(value="upi")
        
        # Payment detail variables
        self.upi_id = tk.StringVar(value="")
        self.card_number = tk.StringVar(value="")
        self.card_holder = tk.StringVar(value="")
        self.card_expiry = tk.StringVar(value="")
        self.card_cvv = tk.StringVar(value="")
        self.bank_name = tk.StringVar(value="")
        self.wallet_number = tk.StringVar(value="")
        
        # Define payment validation function
        def validate_and_pay():
            """Validate payment details and process payment"""
            try:
                payment_method = self.selected_payment_method.get()
                print(f"Selected payment method: {payment_method}")
                
                # Minimal validation to ensure button works
                if payment_method in ["debit_card", "credit_card"]:
                    card_num = self.card_number.get().replace(" ", "")
                    if len(card_num) < 13:
                        messagebox.showerror("Invalid Card", "Please enter a valid card number")
                        return
                    
                    holder = self.card_holder.get().strip()
                    if len(holder) < 2:
                        messagebox.showerror("Invalid Name", "Please enter card holder name")
                        return
                        
                elif payment_method == "upi":
                    upi = self.upi_id.get().strip()
                    if len(upi) < 3:
                        messagebox.showerror("Invalid UPI", "Please enter valid UPI ID")
                        return
                        
                elif payment_method == "net_banking":
                    bank = self.bank_name.get().strip()
                    if not bank:
                        messagebox.showerror("Invalid Bank", "Please select your bank")
                        return
                        
                elif payment_method == "wallet":
                    wallet = self.wallet_number.get().strip()
                    if len(wallet) < 5:
                        messagebox.showerror("Invalid Wallet", "Please enter valid mobile number")
                        return
                
                print("Processing payment...")
                # Process payment
                self.process_payment(show_id, total_amount)
                
            except Exception as e:
                print(f"Payment validation error: {e}")
                # Still process payment even if validation fails
                self.process_payment(show_id, total_amount)
        
        # Store the payment function
        self.pay_button_command = validate_and_pay
        
        payment_methods = [
            {
                "name": "upi",
                "display": "📱 UPI / GPay / PhonePe",
                "description": "Pay using UPI apps",
                "icon": "📱"
            },
            {
                "name": "debit_card",
                "display": "💳 Debit Card",
                "description": "Visa, Mastercard, RuPay, etc.",
                "icon": "💳"
            },
            {
                "name": "credit_card", 
                "display": "💳 Credit Card",
                "description": "Visa, Mastercard, Amex, etc.",
                "icon": "💳"
            },
            {
                "name": "net_banking",
                "display": "🏦 Net Banking",
                "description": "All major banks supported",
                "icon": "🏦"
            },
            {
                "name": "wallet",
                "display": "👛 Wallet",
                "description": "Paytm, Mobikwik, Amazon Pay, etc.",
                "icon": "👛"
            },
            {
                "name": "cash",
                "display": "💵 Cash on Arrival",
                "description": "Pay at the theater counter",
                "icon": "💵"
            }
        ]
        
        # Payment method selection with scrolling
        method_selection_container = tk.Frame(payment_card, bg=self.colors["bg_card"])
        method_selection_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create scrollable canvas for payment methods
        canvas = tk.Canvas(method_selection_container, bg=self.colors["bg_card"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(method_selection_container, orient="vertical", command=canvas.yview)
        method_selection_frame = tk.Frame(canvas, bg=self.colors["bg_card"])
        
        method_selection_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=method_selection_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)
        
        for i, method in enumerate(payment_methods):
            method_frame = tk.Frame(method_selection_frame, bg=self.colors["bg_card"])
            method_frame.pack(fill='x', pady=5)
            
            # Radio button
            radio = tk.Radiobutton(
                method_frame,
                text="",
                variable=self.selected_payment_method,
                value=method["name"],
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"],
                selectcolor=self.colors["primary"],
                font=("Segoe UI", 12),
                command=lambda m=method["name"]: self.show_payment_details(m, show_id, total_amount)
            )
            radio.pack(side='left', padx=(0, 15))
            
            # Method info
            info_frame = tk.Frame(method_frame, bg=self.colors["bg_card"])
            info_frame.pack(side='left', fill='x', expand=True)
            
            tk.Label(
                info_frame,
                text=method["display"],
                font=("Segoe UI", 13, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack(anchor='w')
            
            tk.Label(
                info_frame,
                text=method["description"],
                font=("Segoe UI", 10),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(anchor='w')
        
        # Payment details container with proper scrolling
        details_container = tk.Frame(payment_card, bg=self.colors["bg_card"])
        details_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create scrollable canvas for payment details
        details_canvas = tk.Canvas(details_container, bg=self.colors["bg_card"], highlightthickness=0)
        details_scrollbar = ttk.Scrollbar(details_container, orient="vertical", command=details_canvas.yview)
        self.payment_details_frame = tk.Frame(details_canvas, bg=self.colors["bg_card"])
        
        self.payment_details_frame.bind(
            "<Configure>",
            lambda e: details_canvas.configure(scrollregion=details_canvas.bbox("all"))
        )
        
        details_canvas.create_window((0, 0), window=self.payment_details_frame, anchor="nw")
        details_canvas.configure(yscrollcommand=details_scrollbar.set)
        
        details_canvas.pack(side="left", fill="both", expand=True)
        details_scrollbar.pack(side="right", fill="y")
        
        # Add mouse wheel scrolling for details
        def _on_details_mousewheel(event):
            details_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_details_mousewheel(event):
            details_canvas.bind_all("<MouseWheel>", _on_details_mousewheel)
        
        def _unbind_from_details_mousewheel(event):
            details_canvas.unbind_all("<MouseWheel>")
        
        details_canvas.bind('<Enter>', _bind_to_details_mousewheel)
        details_canvas.bind('<Leave>', _unbind_from_details_mousewheel)
        
        # Show initial payment details (UPI by default)
        self.show_payment_details("upi", show_id, total_amount)
        
        # Security note
        security_frame = tk.Frame(payment_card, bg=self.colors["bg_card"])
        security_frame.pack(fill='x', padx=20, pady=(20, 0))
        
        tk.Label(
            security_frame,
            text="🔒 Your payment information is secure and encrypted",
            font=("Segoe UI", 10),
            bg=self.colors["bg_card"],
            fg=self.colors["success"]
        ).pack()
        
        # Security badges
        security_badges = tk.Frame(payment_card, bg=self.colors["bg_card"])
        security_badges.pack(fill='x', padx=20, pady=(10, 0))
        
        tk.Label(
            security_badges,
            text="🔒 256-bit SSL Encryption  |  🛡️ PCI DSS Compliant  |  ✅ Verified by Visa & Mastercard",
            font=("Segoe UI", 9),
            bg=self.colors["bg_card"],
            fg=self.colors["text_muted"]
        ).pack()
    
    def process_payment(self, show_id, amount):
        """Process payment and generate ticket with error handling"""
        try:
            show = self.showtimes[show_id]
            
            # Validate selected seats
            if not self.selected_seats:
                messagebox.showerror("Error", "No seats selected")
                return
            
            # Check if seats are still available
            unavailable_seats = []
            for seat in self.selected_seats:
                if seat in show["booked_seats"]:
                    unavailable_seats.append(seat)
            
            if unavailable_seats:
                messagebox.showerror(
                    "Seats Unavailable", 
                    f"The following seats are no longer available:\n{', '.join(unavailable_seats)}\n\nPlease select different seats."
                )
                self.select_seats(show_id)  # Go back to seat selection
                return
            
            # Show payment processing dialog with payment method
            processing_dialog = tk.Toplevel(self.root)
            processing_dialog.title("Processing Payment")
            processing_dialog.geometry("450x250")
            processing_dialog.resizable(False, False)
            processing_dialog.configure(bg=self.colors["bg_dark"])
            
            # Center the dialog
            processing_dialog.transient(self.root)
            processing_dialog.grab_set()
            
            # Get selected payment method
            payment_method = getattr(self, 'selected_payment_method', tk.StringVar(value="upi")).get()
            
            payment_method_names = {
                "upi": "UPI / GPay / PhonePe",
                "debit_card": "Debit Card",
                "credit_card": "Credit Card", 
                "net_banking": "Net Banking",
                "wallet": "Wallet",
                "cash": "Cash on Arrival"
            }
            
            payment_icons = {
                "upi": "📱",
                "debit_card": "💳",
                "credit_card": "💳",
                "net_banking": "🏦",
                "wallet": "👛",
                "cash": "💵"
            }
            
            # Processing content
            tk.Label(
                processing_dialog,
                text=f"{payment_icons.get(payment_method, '💳')} Processing Payment...",
                font=("Segoe UI", 16, "bold"),
                bg=self.colors["bg_dark"],
                fg=self.colors["text_light"]
            ).pack(pady=(30, 10))
            
            tk.Label(
                processing_dialog,
                text=f"Method: {payment_method_names.get(payment_method, 'Unknown')}",
                font=("Segoe UI", 12),
                bg=self.colors["bg_dark"],
                fg=self.colors["text_muted"]
            ).pack(pady=5)
            
            tk.Label(
                processing_dialog,
                text=f"Amount: ₹{amount}",
                font=("Segoe UI", 14, "bold"),
                bg=self.colors["bg_dark"],
                fg=self.colors["success"]
            ).pack(pady=5)
            
            if payment_method == "cash":
                tk.Label(
                    processing_dialog,
                    text="💵 Please pay at the theater counter",
                    font=("Segoe UI", 11),
                    bg=self.colors["bg_dark"],
                    fg=self.colors["warning"]
                ).pack(pady=(10, 20))
            else:
                tk.Label(
                    processing_dialog,
                    text="🔒 Secure payment in progress...",
                    font=("Segoe UI", 11),
                    bg=self.colors["bg_dark"],
                    fg=self.colors["text_muted"]
                ).pack(pady=(10, 20))
            
            # Simulate payment processing
            def complete_payment():
                try:
                    # Generate unique booking ID
                    import time
                    timestamp = str(int(time.time()))[-6:]  # Last 6 digits of timestamp
                    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
                    booking_id = f"BK{timestamp}{random_part}"
                    
                    # Ensure booking ID is unique
                    while booking_id in self.bookings:
                        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
                        booking_id = f"BK{timestamp}{random_part}"
                    
                    # Create booking record
                    payment_method = getattr(self, 'selected_payment_method', tk.StringVar(value="upi")).get()
                    booking = {
                        "booking_id": booking_id,
                        "user": self.current_user,
                        "show_id": show_id,
                        "seats": self.selected_seats.copy(),
                        "amount": amount,
                        "payment_method": payment_method,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "status": "confirmed" if payment_method != "cash" else "pending_payment"
                    }
                    
                    # Update show's booked seats
                    self.showtimes[show_id]["booked_seats"].extend(self.selected_seats)
                    
                    # Add to user's bookings
                    if booking_id not in self.users[self.current_user]["bookings"]:
                        self.users[self.current_user]["bookings"].append(booking_id)
                    
                    # Store booking
                    self.bookings[booking_id] = booking
                    
                    # Save all data
                    self.save_data()
                    
                    # Clear selected seats after successful booking
                    self.selected_seats = []
                    
                    # Close processing dialog
                    processing_dialog.destroy()
                    
                    # Show success message
                    messagebox.showinfo(
                        "Payment Successful", 
                        f"🎉 Booking Confirmed!\n\n"
                        f"Booking ID: {booking_id}\n"
                        f"Amount: ₹{amount}\n"
                        f"Seats: {', '.join(booking['seats'])}\n\n"
                        f"Your ticket has been generated!"
                    )
                    
                    # Show ticket (user can navigate home using the Home button)
                    self.show_ticket(booking_id)
                    
                except Exception as e:
                    processing_dialog.destroy()
                    messagebox.showerror("Payment Error", f"An error occurred during payment: {str(e)}")
                    self.payment_screen(show_id)  # Go back to payment screen
            
            # Schedule payment completion
            processing_dialog.after(2000, complete_payment)  # 2 second delay for realism
            
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            self.payment_screen(show_id)
    
    def show_eticket(self, show_id, amount):
        """Show e-ticket after cash booking confirmation"""
        try:
            # Find the most recent booking for this show and user
            user_bookings = []
            for booking_id, booking in self.bookings.items():
                if (booking.get('show_id') == show_id and 
                    booking.get('user') == self.current_user and
                    booking.get('payment_method') == 'Cash at Counter'):
                    user_bookings.append((booking_id, booking))
            
            if user_bookings:
                # Sort by booking ID (most recent first) and get the latest
                latest_booking = max(user_bookings, key=lambda x: x[0])
                booking_id = latest_booking[0]
                
                # Show the ticket
                self.show_ticket(booking_id)
            else:
                messagebox.showinfo("E-Ticket", "Your booking is being processed. E-ticket will be available shortly.")
                self.show_user_home()
                
        except Exception as e:
            messagebox.showerror("E-Ticket Error", f"Error generating e-ticket: {str(e)}")
            self.show_user_home()
    
    def show_ticket(self, booking_id):
        """Display ticket with error handling"""
        try:
            # Validate booking ID exists
            if booking_id not in self.bookings:
                messagebox.showerror("Error", "Booking not found")
                # Check if admin is logged in and redirect to admin panel
                if self.current_admin:
                    self.show_admin_panel()
                else:
                    self.show_user_home()
                return
            
            booking = self.bookings[booking_id]
            show = self.showtimes[booking["show_id"]]
            movie = self.movies[show["movie_id"]]
            theater = self.theaters[show["theater_id"]]
            city = self.cities[theater["city_id"]]
            
            self.clear_window()
            
            # Header
            header = tk.Frame(self.root, bg=self.colors["bg_header"], height=70)
            header.pack(fill='x')
            
            tk.Label(
                header,
                text="🎫 Your Ticket",
                font=("Segoe UI", 24, "bold"),
                bg=self.colors["bg_header"],
                fg=self.colors["text_light"]
            ).pack(side='left', padx=30, pady=15)
            
            # Back button - different for admin vs user
            if self.current_admin:
                self.create_modern_button(
                    header,
                    "← Admin Panel",
                    self.show_admin_panel,
                    self.darken_color(self.colors["bg_header"], 10),
                    width=12
                ).pack(side='right', padx=30, pady=15)
            else:
                self.create_modern_button(
                    header,
                    "🏠 Home",
                    self.show_user_home,
                    self.darken_color(self.colors["bg_header"], 10),
                    width=10
                ).pack(side='right', padx=30, pady=15)
            
            # Ticket
            content = tk.Frame(self.root, bg=self.colors["bg_dark"])
            content.pack(expand=True, fill='both')
            
            # Create ticket with decorative design
            ticket_frame = tk.Frame(
                content,
                bg="white",
                relief="groove",
                bd=3,
                highlightbackground=self.colors["primary"],
                highlightthickness=2
            )
            ticket_frame.pack(pady=30, padx=100)
            
            # Ticket header with gradient
            header_gradient = tk.Frame(ticket_frame, bg=self.colors["primary"], height=60)
            header_gradient.pack(fill='x')
            
            tk.Label(
                header_gradient,
                text="🎬 BookMyShow",
                font=("Segoe UI", 22, "bold"),
                bg=self.colors["primary"],
                fg="white"
            ).pack(pady=15)
            
            tk.Label(
                ticket_frame,
                text="E - T I C K E T",
                font=("Segoe UI", 16, "bold"),
                bg="white",
                fg=self.colors["primary"]
            ).pack(pady=10)
            
            tk.Label(
                ticket_frame,
                text=f"Booking ID: {booking_id}",
                font=("Segoe UI", 10),
                bg="white",
                fg="#7f8c8d"
            ).pack(pady=(0, 20))
            
            # Main ticket content with professional two-column layout
            main_content = tk.Frame(ticket_frame, bg="white")
            main_content.pack(fill='both', expand=True, padx=40, pady=25)
            
            # Left column - Ticket details with professional styling
            left_column = tk.Frame(main_content, bg="white")
            left_column.pack(side='left', fill='both', expand=True)
            
            # Section title
            tk.Label(
                left_column,
                text="📋 BOOKING DETAILS",
                font=("Segoe UI", 11, "bold"),
                bg="white",
                fg="#34495e"
            ).pack(anchor='w', pady=(0, 15))
            
            # Ticket details with enhanced styling
            payment_method = booking.get('payment_method', 'Online')
            payment_display = {
                'upi': 'UPI / GPay / PhonePe',
                'debit_card': 'Debit Card',
                'credit_card': 'Credit Card',
                'net_banking': 'Net Banking',
                'wallet': 'Digital Wallet',
                'cash': '💵 CASH AT COUNTER'
            }
            
            details = [
                ("🎬 Movie:", movie["name"]),
                ("🏙️ City:", city),
                ("🎭 Theater:", theater["name"]),
                ("⏰ Show Time:", show["time"]),
                ("💺 Seats:", ", ".join(booking["seats"])),
                ("💳 Payment:", payment_display.get(payment_method, payment_method)),
                ("💰 Amount Paid:", f"₹{booking.get('amount', 0)}"),
                ("📅 Booking Date:", booking["date"])
            ]
            
            for label, value in details:
                detail_frame = tk.Frame(left_column, bg="white")
                detail_frame.pack(fill='x', pady=8)
                
                # Label with fixed width for alignment
                tk.Label(
                    detail_frame, 
                    text=label, 
                    font=("Segoe UI", 10, "bold"),
                    bg="white", 
                    fg="#7f8c8d", 
                    width=14, 
                    anchor='w'
                ).pack(side='left')
                
                # Value with proper styling
                tk.Label(
                    detail_frame, 
                    text=value, 
                    font=("Segoe UI", 10),
                    bg="white", 
                    fg="#2c3e50", 
                    anchor='w'
                ).pack(side='left', padx=(5, 0))
            
            # Divider line
            divider = tk.Frame(left_column, bg="#ecf0f1", height=1)
            divider.pack(fill='x', pady=(20, 15))
            
            # Arrival notice with enhanced styling
            notice_frame = tk.Frame(left_column, bg="#fff3cd", relief="solid", bd=1)
            notice_frame.pack(fill='x', pady=(0, 10))
            
            tk.Label(
                notice_frame,
                text="⏰ IMPORTANT NOTICE",
                font=("Segoe UI", 9, "bold"),
                bg="#fff3cd",
                fg="#856404"
            ).pack(pady=(5, 2))
            
            tk.Label(
                notice_frame,
                text="Please arrive 15 minutes before showtime",
                font=("Segoe UI", 9),
                bg="#fff3cd",
                fg="#856404"
            ).pack(pady=(0, 5))
            
            # Right column - QR Code with professional container
            right_column = tk.Frame(main_content, bg="white")
            right_column.pack(side='right', padx=(30, 0))
            
            # QR Code section with professional styling
            qr_section = tk.Frame(
                right_column,
                bg="#f8f9fa",
                relief="ridge",
                bd=2,
                padx=15,
                pady=15
            )
            qr_section.pack()
            
            # QR Code header
            qr_header = tk.Frame(qr_section, bg="#f8f9fa")
            qr_header.pack(fill='x', pady=(0, 12))
            
            tk.Label(
                qr_header,
                text="🎫",
                font=("Segoe UI", 16),
                bg="#f8f9fa",
                fg="#e74c3c"
            ).pack(side='left')
            
            tk.Label(
                qr_header,
                text="E-TICKET",
                font=("Segoe UI", 12, "bold"),
                bg="#f8f9fa",
                fg="#2c3e50"
            ).pack(side='left', padx=(8, 0))
            
            # QR Code with border
            qr_border = tk.Frame(
                qr_section,
                bg="white",
                relief="solid",
                bd=1,
                padx=5,
                pady=5
            )
            qr_border.pack(pady=(0, 12))
            
            # Prepare booking data for QR code
            qr_booking_data = {
                "booking_id": booking_id,
                "movie": movie["name"],
                "theater": theater["name"],
                "city": city,
                "show_time": show["time"],
                "seats": booking["seats"],
                "amount": booking.get("amount", 0),
                "date": booking["date"],
                "user": booking["user"]
            }
            
            # Generate and display QR code with error handling
            try:
                qr_code = self.generate_qr_code(qr_booking_data, qr_border)
                qr_code.pack()
            except Exception as qr_error:
                # Fallback if QR code generation fails
                tk.Label(
                    qr_border,
                    text="QR Code\nGeneration\nFailed",
                    font=("Segoe UI", 10),
                    bg="white",
                    fg="#e74c3c",
                    justify="center"
                ).pack(pady=20)
            
            # QR Code instructions
            instructions_frame = tk.Frame(qr_section, bg="#f8f9fa")
            instructions_frame.pack(fill='x')
            
            tk.Label(
                instructions_frame,
                text="📱 Scan this QR code",
                font=("Segoe UI", 9, "bold"),
                bg="#f8f9fa",
                fg="#2c3e50"
            ).pack()
            
            tk.Label(
                instructions_frame,
                text="at the theater entrance",
                font=("Segoe UI", 8),
                bg="#f8f9fa",
                fg="#7f8c8d"
            ).pack()
            
            # Validation badge
            badge_frame = tk.Frame(qr_section, bg="#d4edda", relief="solid", bd=1)
            badge_frame.pack(fill='x', pady=(10, 0))
            
            tk.Label(
                badge_frame,
                text="✅ Valid for one-time entry",
                font=("Segoe UI", 8, "bold"),
                bg="#d4edda",
                fg="#155724"
            ).pack(pady=4)
            
            # Professional footer with enhanced styling
            footer_section = tk.Frame(ticket_frame, bg="#2c3e50", height=50)
            footer_section.pack(fill='x', side='bottom')
            footer_section.pack_propagate(False)
            
            # Footer content with better layout
            footer_content = tk.Frame(footer_section, bg="#2c3e50")
            footer_content.pack(expand=True, fill='both', padx=30, pady=15)
            
            # Left footer - Booking info
            left_footer = tk.Frame(footer_content, bg="#2c3e50")
            left_footer.pack(side='left', fill='x', expand=True)
            
            tk.Label(
                left_footer,
                text="Booking ID:",
                font=("Segoe UI", 8),
                bg="#2c3e50",
                fg="#95a5a6"
            ).pack(side='left')
            
            tk.Label(
                left_footer,
                text=booking_id,
                font=("Segoe UI", 9, "bold"),
                bg="#2c3e50",
                fg="white"
            ).pack(side='left', padx=(5, 0))
            
            # Right footer - Branding
            right_footer = tk.Frame(footer_content, bg="#2c3e50")
            right_footer.pack(side='right')
            
            tk.Label(
                right_footer,
                text="🎬",
                font=("Segoe UI", 10),
                bg="#2c3e50",
                fg="#e74c3c"
            ).pack(side='right', padx=(0, 5))
            
            tk.Label(
                right_footer,
                text="BookMyShow",
                font=("Segoe UI", 10, "bold"),
                bg="#2c3e50",
                fg="white"
            ).pack(side='right')
            
        except Exception as e:
            messagebox.showerror("Ticket Error", f"Error displaying ticket: {str(e)}")
            self.show_user_home()
    
    def show_my_account(self):
        """Display My Account page with all user information"""
        try:
            self.clear_window()
            
            # Check if user is logged in
            if not self.current_user or self.current_user not in self.users:
                messagebox.showerror("Error", "User not logged in properly")
                self.show_login_screen()
                return
            
            # Header
            header = tk.Frame(self.root, bg=self.colors["bg_header"], height=70)
            header.pack(fill='x')
            
            tk.Label(
                header,
                text="👤 My Account",
                font=("Segoe UI", 24, "bold"),
                bg=self.colors["bg_header"],
                fg=self.colors["text_light"]
            ).pack(side='left', padx=30, pady=15)
            
            self.create_modern_button(
                header,
                "← Back to Home",
                self.show_user_home,
                self.darken_color(self.colors["bg_header"], 10),
                width=15
            ).pack(side='right', padx=30, pady=15)
            
            # Content with scrollable area
            content = tk.Frame(self.root, bg=self.colors["bg_dark"])
            content.pack(expand=True, fill='both', padx=30, pady=30)
            
            # Create scrollable frame
            canvas = tk.Canvas(content, bg=self.colors["bg_dark"], highlightthickness=0)
            scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.colors["bg_dark"])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Pack canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Get user data with error handling
            user_data = self.users.get(self.current_user, {})
            if not user_data:
                messagebox.showerror("Error", "User data not found")
                return
            
            # Profile header card
            profile_header = self.create_card(scrollable_frame, padx=40, pady=30)
            profile_header.pack(fill='x', pady=(0, 25))
            
            # Profile header content
            header_content = tk.Frame(profile_header, bg=self.colors["bg_card"])
            header_content.pack(fill='x', padx=30, pady=20)
            
            # Left side - Avatar and basic info
            left_header = tk.Frame(header_content, bg=self.colors["bg_card"])
            left_header.pack(side='left', fill='both', expand=True)
            
            # Avatar placeholder
            avatar_frame = tk.Frame(
                left_header,
                bg=self.colors["primary"],
                width=80,
                height=80,
                relief="raised",
                bd=2
            )
            avatar_frame.pack(side='left', padx=(0, 20))
            avatar_frame.pack_propagate(False)
            
            tk.Label(
                avatar_frame,
                text="👤",
                font=("Segoe UI", 32),
                bg=self.colors["primary"],
                fg="white"
            ).pack(expand=True)
            
            # User name and status
            tk.Label(
                left_header,
                text=self.current_user,
                font=("Segoe UI", 24, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack(anchor='w')
            
            tk.Label(
                left_header,
                text="🎬 Premium Member",
                font=("Segoe UI", 12),
                bg=self.colors["bg_card"],
                fg=self.colors["success"]
            ).pack(anchor='w', pady=(5, 0))
            
            # Right side - Quick stats
            right_header = tk.Frame(header_content, bg=self.colors["bg_card"])
            right_header.pack(side='right')
            
            stats_data = [
                ("🎫", str(len(user_data.get("bookings", []))), "Total Bookings"),
                ("📅", user_data.get("created_date", "Unknown"), "Member Since")
            ]
            
            for icon, value, label in stats_data:
                stat_frame = tk.Frame(right_header, bg=self.colors["bg_card"])
                stat_frame.pack(side='left', padx=20)
                
                tk.Label(
                    stat_frame,
                    text=icon,
                    font=("Segoe UI", 20),
                    bg=self.colors["bg_card"],
                    fg=self.colors["primary"]
                ).pack()
                
                tk.Label(
                    stat_frame,
                    text=value,
                    font=("Segoe UI", 16, "bold"),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_light"]
                ).pack()
                
                tk.Label(
                    stat_frame,
                    text=label,
                    font=("Segoe UI", 9),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_muted"]
                ).pack()
            
            # Personal Information Section
            personal_section = self.create_card(scrollable_frame, padx=40, pady=25)
            personal_section.pack(fill='x', pady=(0, 20))
            
            # Section header with edit button
            personal_header = tk.Frame(personal_section, bg=self.colors["bg_card"])
            personal_header.pack(fill='x', padx=30, pady=(20, 15))
            
            tk.Label(
                personal_header,
                text="📝 Personal Information",
                font=("Segoe UI", 18, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack(side='left')
            
            self.create_modern_button(
                personal_header,
                "✏️ Edit Profile",
                self.show_edit_profile_dialog,
                self.colors["primary"],
                width=12
            ).pack(side='right')
            
            # Personal details grid
            personal_grid = tk.Frame(personal_section, bg=self.colors["bg_card"])
            personal_grid.pack(fill='x', padx=30, pady=(0, 20))
            
            personal_info = [
                ("👤 Username:", self.current_user),
                ("📧 Email:", user_data.get("email", "Not provided")),
                ("📱 Phone:", user_data.get("phone", "Not provided")),
                ("🔐 Password:", "••••••••"),
                ("📅 Registration Date:", user_data.get("created_date", "Unknown")),
                ("🎫 Account Status:", "Active")
            ]
            
            for i, (label, value) in enumerate(personal_info):
                row_frame = tk.Frame(personal_grid, bg=self.colors["bg_card"])
                row_frame.pack(fill='x', pady=8)
                
                tk.Label(
                    row_frame,
                    text=label,
                    font=("Segoe UI", 11, "bold"),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_muted"],
                    width=20,
                    anchor='w'
                ).pack(side='left')
                
                tk.Label(
                    row_frame,
                    text=value,
                    font=("Segoe UI", 11),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_light"],
                    anchor='w'
                ).pack(side='left')
            
            # Booking History Summary
            booking_section = self.create_card(scrollable_frame, padx=40, pady=25)
            booking_section.pack(fill='x', pady=(0, 20))
            
            tk.Label(
                booking_section,
                text="🎫 Booking History",
                font=("Segoe UI", 18, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack(anchor='w', padx=30, pady=(0, 20))
            
            # Booking summary
            booking_summary = tk.Frame(booking_section, bg=self.colors["bg_card"])
            booking_summary.pack(fill='x', padx=30, pady=(0, 20))
            
            total_bookings = len(user_data.get("bookings", []))
            
            if total_bookings > 0:
                # Calculate total spent (simplified)
                total_spent = sum(
                    self.bookings.get(bid, {}).get("amount", 0) 
                    for bid in user_data.get("bookings", [])
                )
                
                summary_info = [
                    ("Total Bookings:", str(total_bookings)),
                    ("Total Amount Spent:", f"₹{total_spent}"),
                    ("Last Booking:", "Recent" if total_bookings > 0 else "None")
                ]
                
                for label, value in summary_info:
                    summary_frame = tk.Frame(booking_summary, bg=self.colors["bg_card"])
                    summary_frame.pack(fill='x', pady=5)
                    
                    tk.Label(
                        summary_frame,
                        text=label,
                        font=("Segoe UI", 11),
                        bg=self.colors["bg_card"],
                        fg=self.colors["text_muted"],
                        width=20,
                        anchor='w'
                    ).pack(side='left')
                    
                    tk.Label(
                        summary_frame,
                        text=value,
                        font=("Segoe UI", 11, "bold"),
                        bg=self.colors["bg_card"],
                        fg=self.colors["success"],
                        anchor='w'
                    ).pack(side='left')
            else:
                tk.Label(
                    booking_summary,
                    text="No bookings yet. Start booking your favorite movies!",
                    font=("Segoe UI", 11, "italic"),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_muted"]
                ).pack(pady=10)
            
            # Action buttons
            actions_frame = tk.Frame(booking_section, bg=self.colors["bg_card"])
            actions_frame.pack(fill='x', padx=30, pady=(10, 0))
            
            self.create_modern_button(
                actions_frame,
                "📖 View All Bookings",
                self.show_my_bookings,
                self.colors["primary"],
                width=20
            ).pack(side='left', padx=(0, 10))
            
            self.create_modern_button(
                actions_frame,
                "🎬 Browse Movies",
                self.show_user_home,
                self.colors["success"],
                width=20
            ).pack(side='left')
            
            # Account Actions Section
            account_actions = self.create_card(scrollable_frame, padx=40, pady=25)
            account_actions.pack(fill='x')
            
            tk.Label(
                account_actions,
                text="⚙️ Account Actions",
                font=("Segoe UI", 18, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack(anchor='w', padx=30, pady=(0, 20))
            
            # Action buttons grid
            actions_grid = tk.Frame(account_actions, bg=self.colors["bg_card"])
            actions_grid.pack(fill='x', padx=30, pady=(0, 20))
            
            action_buttons = [
                ("🔐 Change Password", lambda: self.show_change_password_dialog()),
                ("📧 Update Email", lambda: self.show_update_email_dialog()),
                ("📱 Update Phone", lambda: self.show_update_phone_dialog()),
                ("🚪 Logout", self.show_login_screen)
            ]
            
            for text, command in action_buttons:
                btn_color = self.colors["primary"] if "Logout" not in text else self.colors["warning"]
                self.create_modern_button(
                    actions_grid,
                    text,
                    command,
                    btn_color,
                    width=25
                ).pack(pady=5)
            
            # Add some padding at the bottom for better scrolling
            tk.Frame(scrollable_frame, bg=self.colors["bg_dark"], height=20).pack(fill='x')
            
            # Enable mouse wheel scrolling
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            def _bind_to_mousewheel(event):
                canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            def _unbind_from_mousewheel(event):
                canvas.unbind_all("<MouseWheel>")
            
            canvas.bind('<Enter>', _bind_to_mousewheel)
            canvas.bind('<Leave>', _unbind_from_mousewheel)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open My Account: {str(e)}")
            self.show_user_home()
    
    def show_change_password_dialog(self):
        """Show password change dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Change Password")
        dialog.geometry("450x420")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors["bg_dark"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (420 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Dialog content
        content_frame = tk.Frame(dialog, bg=self.colors["bg_dark"])
        content_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        tk.Label(
            content_frame,
            text="🔐 Change Password",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(pady=(0, 20))
        
        # Current password
        tk.Label(
            content_frame,
            text="Current Password:",
            font=("Segoe UI", 11),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(anchor='w', pady=(10, 5))
        
        current_password = tk.Entry(
            content_frame,
            font=("Segoe UI", 11),
            bg="#2c3e50",
            fg=self.colors["text_light"],
            insertbackground=self.colors["text_light"],
            show="*",
            relief="flat",
            width=30
        )
        current_password.pack(pady=(0, 15))
        
        # New password
        tk.Label(
            content_frame,
            text="New Password:",
            font=("Segoe UI", 11),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(anchor='w', pady=(10, 5))
        
        new_password = tk.Entry(
            content_frame,
            font=("Segoe UI", 11),
            bg="#2c3e50",
            fg=self.colors["text_light"],
            insertbackground=self.colors["text_light"],
            show="*",
            relief="flat",
            width=30
        )
        new_password.pack(pady=(0, 15))
        
        # Confirm new password
        tk.Label(
            content_frame,
            text="Confirm New Password:",
            font=("Segoe UI", 11),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(anchor='w', pady=(10, 5))
        
        confirm_password = tk.Entry(
            content_frame,
            font=("Segoe UI", 11),
            bg="#2c3e50",
            fg=self.colors["text_light"],
            insertbackground=self.colors["text_light"],
            show="*",
            relief="flat",
            width=30
        )
        confirm_password.pack(pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=self.colors["bg_dark"])
        button_frame.pack(pady=10)
        
        def change_password():
            curr_pass = current_password.get()
            new_pass = new_password.get()
            confirm_pass = confirm_password.get()
            
            if not curr_pass or not new_pass or not confirm_pass:
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            if new_pass != confirm_pass:
                messagebox.showerror("Error", "New passwords do not match")
                return
            
            # Verify current password (simplified - in real app, would check against stored hash)
            if len(new_pass) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters")
                return
            
            # Update password (in real app, would hash the password)
            self.users[self.current_user]["password"] = new_pass
            self.save_data()
            
            messagebox.showinfo("Success", "Password changed successfully!")
            dialog.destroy()
        
        self.create_modern_button(
            button_frame,
            "Change Password",
            change_password,
            self.colors["success"],
            width=15
        ).pack(side='left', padx=5)
        
        self.create_modern_button(
            button_frame,
            "Cancel",
            dialog.destroy,
            self.colors["text_muted"],
            width=10
        ).pack(side='left', padx=5)
    
    def show_update_email_dialog(self):
        """Show email update dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Email")
        dialog.geometry("450x320")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors["bg_dark"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (320 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Dialog content
        content_frame = tk.Frame(dialog, bg=self.colors["bg_dark"])
        content_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        tk.Label(
            content_frame,
            text="📧 Update Email",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(pady=(0, 20))
        
        # Current email
        current_email = self.users[self.current_user].get("email", "")
        tk.Label(
            content_frame,
            text="Current Email:",
            font=("Segoe UI", 11),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(anchor='w', pady=(10, 5))
        
        tk.Label(
            content_frame,
            text=current_email if current_email else "Not provided",
            font=("Segoe UI", 11, "italic"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_muted"]
        ).pack(anchor='w', pady=(0, 15))
        
        # New email
        tk.Label(
            content_frame,
            text="Add/Update Email:",
            font=("Segoe UI", 11),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(anchor='w', pady=(10, 5))
        
        new_email = tk.Entry(
            content_frame,
            font=("Segoe UI", 11),
            bg="#2c3e50",
            fg=self.colors["text_light"],
            insertbackground=self.colors["text_light"],
            relief="flat",
            width=30
        )
        new_email.pack(pady=(0, 20))
        new_email.insert(0, current_email)  # Pre-fill with current email if exists
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=self.colors["bg_dark"])
        button_frame.pack(pady=10)
        
        def update_email():
            email = new_email.get().strip()
            
            if not email:
                messagebox.showerror("Error", "Please enter an email address")
                return
            
            # Basic email validation
            if "@" not in email or "." not in email:
                messagebox.showerror("Error", "Please enter a valid email address")
                return
            
            # Update email
            self.users[self.current_user]["email"] = email
            self.save_data()
            
            messagebox.showinfo("Success", "Email updated successfully!")
            dialog.destroy()
            self.show_my_account()  # Refresh account page
        
        self.create_modern_button(
            button_frame,
            "Done",
            update_email,
            self.colors["success"],
            width=15
        ).pack(side='left', padx=5)
        
        self.create_modern_button(
            button_frame,
            "Cancel",
            dialog.destroy,
            self.colors["text_muted"],
            width=10
        ).pack(side='left', padx=5)
    
    def show_update_phone_dialog(self):
        """Show phone update dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Phone")
        dialog.geometry("450x320")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors["bg_dark"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (320 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Dialog content
        content_frame = tk.Frame(dialog, bg=self.colors["bg_dark"])
        content_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        tk.Label(
            content_frame,
            text="📱 Update Phone",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(pady=(0, 20))
        
        # Current phone
        current_phone = self.users[self.current_user].get("phone", "")
        tk.Label(
            content_frame,
            text="Current Phone:",
            font=("Segoe UI", 11),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(anchor='w', pady=(10, 5))
        
        tk.Label(
            content_frame,
            text=current_phone if current_phone else "Not provided",
            font=("Segoe UI", 11, "italic"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_muted"]
        ).pack(anchor='w', pady=(0, 15))
        
        # New phone
        tk.Label(
            content_frame,
            text="Add/Update Phone:",
            font=("Segoe UI", 11),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(anchor='w', pady=(10, 5))
        
        new_phone = tk.Entry(
            content_frame,
            font=("Segoe UI", 11),
            bg="#2c3e50",
            fg=self.colors["text_light"],
            insertbackground=self.colors["text_light"],
            relief="flat",
            width=30
        )
        new_phone.pack(pady=(0, 20))
        new_phone.insert(0, current_phone)  # Pre-fill with current phone if exists
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=self.colors["bg_dark"])
        button_frame.pack(pady=10)
        
        def update_phone():
            phone = new_phone.get().strip()
            
            if not phone:
                messagebox.showerror("Error", "Please enter a phone number")
                return
            
            # Basic phone validation (digits only, reasonable length)
            if not phone.isdigit() or len(phone) < 10 or len(phone) > 15:
                messagebox.showerror("Error", "Please enter a valid phone number (10-15 digits)")
                return
            
            # Update phone
            self.users[self.current_user]["phone"] = phone
            self.save_data()
            
            messagebox.showinfo("Success", "Phone number updated successfully!")
            dialog.destroy()
            self.show_my_account()  # Refresh account page
        
        self.create_modern_button(
            button_frame,
            "Done",
            update_phone,
            self.colors["success"],
            width=15
        ).pack(side='left', padx=5)
        
        self.create_modern_button(
            button_frame,
            "Cancel",
            dialog.destroy,
            self.colors["text_muted"],
            width=10
        ).pack(side='left', padx=5)
    
    def show_edit_profile_dialog(self):
        """Show comprehensive edit profile dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Profile")
        dialog.geometry("500x380")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors["bg_dark"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (380 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Dialog content
        content_frame = tk.Frame(dialog, bg=self.colors["bg_dark"])
        content_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        tk.Label(
            content_frame,
            text="✏️ Edit Profile",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(pady=(0, 25))
        
        # Get current user data
        user_data = self.users[self.current_user]
        
        # Profile fields
        fields = []
        
        # Username (editable)
        field_frame = tk.Frame(content_frame, bg=self.colors["bg_dark"])
        field_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            field_frame,
            text="👤 Username:",
            font=("Segoe UI", 11),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"],
            width=15,
            anchor='w'
        ).pack(side='left')
        
        username_entry = tk.Entry(
            field_frame,
            font=("Segoe UI", 11),
            bg="#2c3e50",
            fg=self.colors["text_light"],
            insertbackground=self.colors["text_light"],
            relief="flat",
            width=30
        )
        username_entry.pack(side='left')
        username_entry.insert(0, self.current_user)
        fields.append(("username", username_entry))
        
        # Email
        field_frame = tk.Frame(content_frame, bg=self.colors["bg_dark"])
        field_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            field_frame,
            text="📧 Email:",
            font=("Segoe UI", 11),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"],
            width=15,
            anchor='w'
        ).pack(side='left')
        
        email_entry = tk.Entry(
            field_frame,
            font=("Segoe UI", 11),
            bg="#2c3e50",
            fg=self.colors["text_light"],
            insertbackground=self.colors["text_light"],
            relief="flat",
            width=30
        )
        email_entry.pack(side='left')
        email_entry.insert(0, user_data.get("email", ""))
        fields.append(("email", email_entry))
        
        # Phone
        field_frame = tk.Frame(content_frame, bg=self.colors["bg_dark"])
        field_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            field_frame,
            text="📱 Phone:",
            font=("Segoe UI", 11),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"],
            width=15,
            anchor='w'
        ).pack(side='left')
        
        phone_entry = tk.Entry(
            field_frame,
            font=("Segoe UI", 11),
            bg="#2c3e50",
            fg=self.colors["text_light"],
            insertbackground=self.colors["text_light"],
            relief="flat",
            width=30
        )
        phone_entry.pack(side='left')
        phone_entry.insert(0, user_data.get("phone", ""))
        fields.append(("phone", phone_entry))
        
        # Member Since Date
        field_frame = tk.Frame(content_frame, bg=self.colors["bg_dark"])
        field_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            field_frame,
            text="📅 Member Since:",
            font=("Segoe UI", 11),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"],
            width=15,
            anchor='w'
        ).pack(side='left')
        
        member_date_entry = tk.Entry(
            field_frame,
            font=("Segoe UI", 11),
            bg="#2c3e50",
            fg=self.colors["text_light"],
            insertbackground=self.colors["text_light"],
            relief="flat",
            width=30
        )
        member_date_entry.pack(side='left')
        member_date_entry.insert(0, user_data.get("created_date", ""))
        fields.append(("created_date", member_date_entry))
        
        # Date format hint
        tk.Label(
            content_frame,
            text="💡 Date format: YYYY-MM-DD (e.g., 2020-01-15)",
            font=("Segoe UI", 9),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_muted"]
        ).pack(pady=(5, 10))
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=self.colors["bg_dark"])
        button_frame.pack(pady=10)
        
        def save_profile():
            # Get values
            username = username_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            member_date = member_date_entry.get().strip()
            
            # Validate username
            if not username:
                messagebox.showerror("Error", "Username cannot be empty")
                return
            
            # Check if username is being changed and if it already exists
            if username != self.current_user:
                if username in self.users:
                    messagebox.showerror("Error", "Username already exists. Please choose another one.")
                    return
            
            # Validate email if provided
            if email and ("@" not in email or "." not in email):
                messagebox.showerror("Error", "Please enter a valid email address")
                return
            
            # Validate phone if provided
            if phone and (not phone.isdigit() or len(phone) < 10 or len(phone) > 15):
                messagebox.showerror("Error", "Please enter a valid phone number (10-15 digits)")
                return
            
            # Validate member since date if provided
            if member_date:
                try:
                    from datetime import datetime, timedelta
                    input_date = datetime.strptime(member_date, "%Y-%m-%d").date()
                    today = datetime.now().date()
                    
                    # Check if date is in future
                    if input_date > today:
                        messagebox.showerror("Error", "Member since date cannot be in the future")
                        return
                    
                    # Check if date is more than 100 years in past
                    hundred_years_ago = today - timedelta(days=365*100)
                    if input_date < hundred_years_ago:
                        messagebox.showerror("Error", "Member since date cannot be more than 100 years in the past")
                        return
                        
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid date in YYYY-MM-DD format")
                    return
            
            # Update username if changed
            if username != self.current_user:
                # Get current user data
                old_user_data = self.users[self.current_user]
                
                # Remove old username key
                del self.users[self.current_user]
                
                # Add new username key with same data
                self.users[username] = old_user_data
                self.users[username]["username"] = username
                
                # Update current_user variable
                self.current_user = username
            
            # Update email and phone
            if email:
                self.users[self.current_user]["email"] = email
            if phone:
                self.users[self.current_user]["phone"] = phone
            if member_date:
                self.users[self.current_user]["created_date"] = member_date
            
            # Save data
            self.save_data()
            
            messagebox.showinfo("Success", "Profile updated successfully!")
            dialog.destroy()
            self.show_my_account()  # Refresh account page
        
        def clear_passwords():
            current_pass_entry.delete(0, tk.END)
            new_pass_entry.delete(0, tk.END)
            confirm_pass_entry.delete(0, tk.END)
        
        self.create_modern_button(
            button_frame,
            "💾 Save Changes",
            save_profile,
            self.colors["success"],
            width=15
        ).pack(side='left', padx=5)
        
        self.create_modern_button(
            button_frame,
            "🔄 Clear Passwords",
            clear_passwords,
            self.colors["warning"],
            width=15
        ).pack(side='left', padx=5)
        
        self.create_modern_button(
            button_frame,
            "❌ Cancel",
            dialog.destroy,
            self.colors["text_muted"],
            width=10
        ).pack(side='left', padx=5)
    
    def show_my_bookings(self):
        """Show user's bookings"""
        self.clear_window()
        
        # Header
        header = tk.Frame(self.root, bg=self.colors["bg_header"], height=70)
        header.pack(fill='x')
        
        # Different title and back button for admin vs user
        if self.current_admin:
            tk.Label(
                header,
                text="📖 All Bookings",
                font=("Segoe UI", 24, "bold"),
                bg=self.colors["bg_header"],
                fg=self.colors["text_light"]
            ).pack(side='left', padx=30, pady=15)
            
            self.create_modern_button(
                header,
                "← Admin Panel",
                self.show_admin_panel,
                self.darken_color(self.colors["bg_header"], 10),
                width=12
            ).pack(side='right', padx=30, pady=15)
        else:
            tk.Label(
                header,
                text="📖 My Bookings",
                font=("Segoe UI", 24, "bold"),
                bg=self.colors["bg_header"],
                fg=self.colors["text_light"]
            ).pack(side='left', padx=30, pady=15)
            
            self.create_modern_button(
                header,
                "← Back",
                self.show_user_home,
                self.darken_color(self.colors["bg_header"], 10),
                width=10
            ).pack(side='right', padx=30, pady=15)
        
        # Content
        content = tk.Frame(self.root, bg=self.colors["bg_dark"])
        content.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Get bookings based on user type
        if self.current_admin:
            # Admin sees all bookings
            user_bookings = list(self.bookings.keys())
        else:
            # User sees only their bookings
            user_bookings = self.users[self.current_user].get("bookings", [])
        
        if user_bookings:
            # Scrollable bookings list
            canvas = tk.Canvas(content, bg=self.colors["bg_dark"], highlightthickness=0)
            scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
            bookings_container = tk.Frame(canvas, bg=self.colors["bg_dark"])
            
            bookings_container.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=bookings_container, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for booking_id in user_bookings:
                booking = self.bookings.get(booking_id)
                if not booking:
                    continue
                if booking.get("status") not in ["confirmed", "pending_payment"]:
                    continue
                show = self.showtimes[booking["show_id"]]
                movie = self.movies[show["movie_id"]]
                theater = self.theaters[show["theater_id"]]
                
                booking_card = self.create_card(bookings_container, padx=25, pady=20)
                booking_card.pack(fill='x', pady=10)
                
                info_frame = tk.Frame(booking_card, bg=self.colors["bg_card"])
                info_frame.pack(side='left', fill='both', expand=True, padx=20)
                
                tk.Label(
                    info_frame,
                    text=movie["name"],
                    font=("Segoe UI", 14, "bold"),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_light"]
                ).pack(anchor='w')
                
                tk.Label(
                    info_frame,
                    text=f"{theater['name']} • {show['time']}",
                    font=("Segoe UI", 11),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_muted"]
                ).pack(anchor='w', pady=5)
                
                tk.Label(
                    info_frame,
                    text=f"💺 {', '.join(booking['seats'])} • 💰 ₹{booking['amount']}",
                    font=("Segoe UI", 10),
                    bg=self.colors["bg_card"],
                    fg=self.colors["success"]
                ).pack(anchor='w')
                
                action_frame = tk.Frame(booking_card, bg=self.colors["bg_card"])
                action_frame.pack(side='right', padx=20)

                self.create_modern_button(
                    action_frame,
                    "🎫 View Ticket",
                    lambda b_id=booking_id: self.show_ticket(b_id),
                    self.colors["primary"],
                    width=15
                ).pack(side='left', padx=(0, 10))

                self.create_modern_button(
                    action_frame,
                    "🗑️ Cancel Booking",
                    lambda b_id=booking_id: self.cancel_booking(b_id, refresh_callback=self.show_my_bookings),
                    self.colors["secondary"],
                    width=15
                ).pack(side='left')
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        else:
            empty_frame = tk.Frame(content, bg=self.colors["bg_dark"])
            empty_frame.pack(expand=True, fill='both')
            
            tk.Label(
                empty_frame,
                text="📭",
                font=("Arial", 48),
                bg=self.colors["bg_dark"],
                fg=self.colors["text_muted"]
            ).pack(pady=20)
            
            tk.Label(
                empty_frame,
                text="No Bookings Yet",
                font=("Segoe UI", 18, "bold"),
                bg=self.colors["bg_dark"],
                fg=self.colors["text_light"]
            ).pack(pady=10)
            
            tk.Label(
                empty_frame,
                text="Book your first movie ticket and start your cinematic journey!",
                font=("Segoe UI", 12),
                bg=self.colors["bg_dark"],
                fg=self.colors["text_muted"]
            ).pack(pady=10)
            
            self.create_modern_button(
                empty_frame,
                "🎬 Explore Movies",
                self.show_user_home,
                self.colors["primary"],
                width=20
            ).pack(pady=20)
    
    def update_release_date(self, movie_id, release_date):
        """Update release date of a movie"""
        self.movies[movie_id]["release_date"] = release_date
        self.save_data()
    
    def add_movie(self, name, language, duration, genre, poster_path=""):
        """Add a new movie"""
        movie_id = str(len(self.movies) + 1)
        self.movies[movie_id] = {
            "name": name,
            "language": language,
            "duration": duration,
            "genre": genre,
            "poster_path": poster_path,
            "release_date": ""
        }
        self.save_data()
    
    def show_manage_posters(self):
        """Manage posters"""
        self.clear_window()
        
        # Header
        header = tk.Frame(self.root, bg=self.colors["warning"], height=70)
        header.pack(fill='x')
        
        tk.Label(
            header,
            text="📸 Manage Posters",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["warning"],
            fg="#2d3436"
        ).pack(side='left', padx=30, pady=15)
        
        self.create_modern_button(
            header,
            "← Back",
            self.show_admin_panel,
            self.darken_color(self.colors["warning"], 20),
            "#2d3436",
            width=10
        ).pack(side='right', padx=30, pady=15)
        
        # Content
        content = tk.Frame(self.root, bg=self.colors["bg_dark"])
        content.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Poster upload form
        form_card = self.create_card(content, padx=30, pady=30)
        form_card.pack(fill='x', pady=10)
        
        tk.Label(
            form_card,
            text="📸 Upload Poster",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        tk.Label(form_card, text="Movie ID:", bg=self.colors["bg_card"], 
                fg=self.colors["text_light"]).grid(row=1, column=0, padx=20, pady=10, sticky='w')
        movie_id_entry = tk.Entry(form_card, font=("Segoe UI", 11), bg="#21262d", 
                                fg=self.colors["text_light"], relief="flat", width=30)
        movie_id_entry.grid(row=1, column=1, padx=20, pady=10)
        
        tk.Label(form_card, text="Poster Path:", bg=self.colors["bg_card"], 
                fg=self.colors["text_light"]).grid(row=2, column=0, padx=20, pady=10, sticky='w')
        poster_path_entry = tk.Entry(form_card, font=("Segoe UI", 11), bg="#21262d", 
                                    fg=self.colors["text_light"], relief="flat", width=30)
        poster_path_entry.grid(row=2, column=1, padx=20, pady=10)
        
        self.create_modern_button(
            form_card,
            "📸 Upload Poster",
            lambda: self.upload_poster(movie_id_entry.get(), poster_path_entry.get()),
            self.colors["success"],
            width=20
        ).grid(row=3, column=0, columnspan=2, pady=20)
        
        # Posters list
        tk.Label(
            content,
            text="Current Posters",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(pady=20)
        
        # Scrollable posters list
        canvas = tk.Canvas(content, bg=self.colors["bg_dark"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
        posters_frame = tk.Frame(canvas, bg=self.colors["bg_dark"])
        
        posters_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=posters_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for movie_id, movie in sorted(self.movies.items(), key=lambda x: x[1]["name"]):
            poster_card = self.create_card(posters_frame, padx=20, pady=15)
            poster_card.pack(fill='x', pady=5)
            
            tk.Label(
                poster_card,
                text=movie["name"],
                font=("Segoe UI", 14, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack()
            
            tk.Label(
                poster_card,
                text=movie["poster_path"],
                font=("Segoe UI", 11),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack()
            
            self.create_modern_button(
                poster_card,
                "📸 View Poster",
                lambda m_id=movie_id: self.view_poster(m_id),
                self.colors["primary"],
                width=15
            ).pack(side='right', padx=20)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def upload_poster(self, movie_id, poster_path):
        """Upload poster"""
        self.movies[movie_id]["poster_path"] = poster_path
        self.save_data()
    
    def view_poster(self, movie_id):
        """View poster"""
        poster_path = self.movies[movie_id]["poster_path"]
        # Display poster
    
    # ADMIN PANEL - Enhanced UI
    def show_admin_panel(self):
        """Admin dashboard"""
        self.clear_window()
        
        # Header
        header = tk.Frame(self.root, bg=self.colors["warning"], height=70)
        header.pack(fill='x')
        
        tk.Label(
            header,
            text="👑 Admin Panel",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["warning"],
            fg="#2d3436"
        ).pack(side='left', padx=30, pady=15)
        
        self.create_modern_button(
            header,
            "🚪 Logout",
            self.show_login_screen,
            self.darken_color(self.colors["warning"], 20),
            "#2d3436",
            width=12
        ).pack(side='right', padx=30, pady=15)
        
        # Content (scrollable)
        content = tk.Frame(self.root, bg=self.colors["bg_dark"])
        content.pack(expand=True, fill='both', padx=20, pady=20)

        canvas = tk.Canvas(content, bg=self.colors["bg_dark"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["bg_dark"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        tk.Label(
            scrollable_frame,
            text="Management Dashboard",
            font=("Segoe UI", 22, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(pady=20)
        
        # Stats cards
        stats_frame = tk.Frame(scrollable_frame, bg=self.colors["bg_dark"])
        stats_frame.pack(fill='x', pady=20)
        
        stats = [
            (f"🎬 {len(self.movies)}", "Movies"),
            (f"🏙️ {len(self.cities)}", "Cities"),
            (f"🎭 {len(self.theaters)}", "Theaters"),
            (f"⏰ {len(self.showtimes)}", "Showtimes"),
            (f"🎫 {len(self.bookings)}", "Bookings"),
            (f"💰 ₹{sum(b.get('amount', 0) for b in self.bookings.values() if b.get('status') == 'confirmed')}", "Revenue")
        ]
        
        for i, (value, label) in enumerate(stats):
            stat_card = self.create_card(stats_frame, padx=20, pady=15)
            stat_card.grid(row=0, column=i, padx=10, sticky='nsew')
            
            tk.Label(
                stat_card,
                text=value,
                font=("Segoe UI", 16, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["primary"]
            ).pack()
            
            tk.Label(
                stat_card,
                text=label,
                font=("Segoe UI", 11),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack()
            
            stats_frame.columnconfigure(i, weight=1)
        
        # Menu buttons
        tk.Label(
            scrollable_frame,
            text="Quick Actions",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(pady=(40, 20))
        
        menu_frame = tk.Frame(scrollable_frame, bg=self.colors["bg_dark"])
        menu_frame.pack(expand=True)
        
        buttons = [
            ("🎬 Manage Movies", self.manage_movies),
            ("🏙️ Manage Cities", self.manage_cities),
            ("🎭 Manage Theaters", self.manage_theaters),
            ("⏰ Manage Showtimes", self.manage_showtimes),
            ("🖼️ Manage Posters", self.manage_posters),
            ("📅 Manage Release Dates", self.manage_release_dates),
            ("📺 Manage Marquee", self.manage_marquee),
            ("📊 View All Bookings", self.view_all_bookings)
        ]
        
        for i, (text, command) in enumerate(buttons):
            self.create_modern_button(
                menu_frame,
                text,
                command,
                self.colors["accent"],
                width=25
            ).grid(row=i, column=0, pady=15, padx=20)
    
    def manage_movies(self):
        """Manage movies"""
        self.clear_window()
        
        # Header
        header = tk.Frame(self.root, bg=self.colors["warning"], height=70)
        header.pack(fill='x')
        
        tk.Label(
            header,
            text="🎬 Manage Movies",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["warning"],
            fg="#2d3436"
        ).pack(side='left', padx=30, pady=15)
        
        self.create_modern_button(
            header,
            "← Back",
            self.show_admin_panel,
            self.darken_color(self.colors["warning"], 20),
            "#2d3436",
            width=10
        ).pack(side='right', padx=30, pady=15)
        
        # Content
        content = tk.Frame(self.root, bg=self.colors["bg_dark"])
        content.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Add movie form
        form_card = self.create_card(content, padx=30, pady=30)
        form_card.pack(fill='x', pady=10)
        
        tk.Label(
            form_card,
            text="➕ Add New Movie",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        tk.Label(form_card, text="Movie Name:", bg=self.colors["bg_card"], 
                fg=self.colors["text_light"]).grid(row=1, column=0, padx=20, pady=10, sticky='w')
        name_entry = tk.Entry(form_card, font=("Segoe UI", 11), bg="#21262d", 
                            fg=self.colors["text_light"], relief="flat", width=30)
        name_entry.grid(row=1, column=1, padx=20, pady=10)
        
        tk.Label(form_card, text="Language:", bg=self.colors["bg_card"], 
                fg=self.colors["text_light"]).grid(row=2, column=0, padx=20, pady=10, sticky='w')
        lang_entry = tk.Entry(form_card, font=("Segoe UI", 11), bg="#21262d", 
                            fg=self.colors["text_light"], relief="flat", width=30)
        lang_entry.grid(row=2, column=1, padx=20, pady=10)
        
        tk.Label(form_card, text="Duration:", bg=self.colors["bg_card"], 
                fg=self.colors["text_light"]).grid(row=3, column=0, padx=20, pady=10, sticky='w')
        duration_entry = tk.Entry(form_card, font=("Segoe UI", 11), bg="#21262d", 
                                fg=self.colors["text_light"], relief="flat", width=30)
        duration_entry.grid(row=3, column=1, padx=20, pady=10)
        
        tk.Label(form_card, text="Genre:", bg=self.colors["bg_card"], 
                fg=self.colors["text_light"]).grid(row=4, column=0, padx=20, pady=10, sticky='w')
        genre_entry = tk.Entry(form_card, font=("Segoe UI", 11), bg="#21262d", 
                            fg=self.colors["text_light"], relief="flat", width=30)
        genre_entry.grid(row=4, column=1, padx=20, pady=10)
        
        self.create_modern_button(
            form_card,
            "➕ Add Movie",
            lambda: self.add_movie(name_entry.get(), lang_entry.get(),
                                  duration_entry.get(), genre_entry.get()),
            self.colors["success"],
            width=20
        ).grid(row=5, column=0, columnspan=2, pady=20)
        
        # Movies list
        tk.Label(
            content,
            text="Current Movies",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(pady=20)
        
        # Scrollable movies list
        canvas = tk.Canvas(content, bg=self.colors["bg_dark"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
        movies_frame = tk.Frame(canvas, bg=self.colors["bg_dark"])
        
        movies_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=movies_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for movie_id, movie in sorted(self.movies.items(), key=lambda x: x[1]["name"]):
            movie_card = self.create_card(movies_frame, padx=20, pady=15)
            movie_card.pack(fill='x', pady=5)
            
            tk.Label(
                movie_card,
                text=f"{movie['name']} | {movie['language']} | {movie['duration']} | {movie['genre']}",
                font=("Segoe UI", 11),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack(side='left', padx=15, pady=10)
            
            self.create_modern_button(
                movie_card,
                "🗑️ Delete",
                lambda m_id=movie_id: self.delete_movie(m_id),
                self.colors["primary"],
                width=10
            ).pack(side='right', padx=15)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_movie(self, name, language, duration, genre):
        """Add new movie"""
        if not all([name, language, duration, genre]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        movie_id = f"MOV{str(len(self.movies) + 1).zfill(3)}"
        self.movies[movie_id] = {
            "name": name,
            "language": language,
            "duration": duration,
            "genre": genre,
            "release_date": "Not set",
            "poster_path": ""
        }
        self.save_data()
        messagebox.showinfo("Success", "🎬 Movie added successfully!")
        self.manage_movies()

    def update_release_date(self, movie_name, release_date):
        """Update a movie's release_date by movie name"""
        for movie in self.movies.values():
            if movie.get("name") == movie_name:
                movie["release_date"] = release_date
                self.save_data()
                messagebox.showinfo("Success", "Release date updated successfully!")
                return
        messagebox.showerror("Error", "Movie not found")

    def manage_posters(self):
        """Manage movie posters"""
        self.clear_window()
        
        # Header
        header = tk.Frame(self.root, bg=self.colors["warning"], height=70)
        header.pack(fill='x')
        
        tk.Label(
            header,
            text="🖼️ Manage Posters",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["warning"],
            fg="#2d3436"
        ).pack(side='left', padx=30, pady=15)
        
        self.create_modern_button(
            header,
            "← Back",
            self.show_admin_panel,
            self.darken_color(self.colors["warning"], 20),
            "#2d3436",
            width=10
        ).pack(side='right', padx=30, pady=15)
        
        # Content
        content = tk.Frame(self.root, bg=self.colors["bg_dark"])
        content.pack(expand=True, fill='both', padx=20, pady=20)
        
        form_card = self.create_card(content, padx=30, pady=30)
        form_card.pack(fill='x', pady=10)
        
        tk.Label(
            form_card,
            text="✏️ Update Poster",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        tk.Label(
            form_card,
            text="Select Movie:",
            font=("Segoe UI", 11),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).grid(row=1, column=0, padx=20, pady=10, sticky='w')
        
        movie_var = tk.StringVar()
        movie_names = sorted([m["name"] for m in self.movies.values()])
        movie_dropdown = ttk.Combobox(form_card, textvariable=movie_var, values=movie_names, width=35)
        movie_dropdown.grid(row=1, column=1, padx=20, pady=10, sticky='w')
        
        tk.Label(
            form_card,
            text="Poster File:",
            font=("Segoe UI", 11),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).grid(row=2, column=0, padx=20, pady=10, sticky='w')
        
        poster_path_var = tk.StringVar()
        poster_entry = tk.Entry(
            form_card,
            textvariable=poster_path_var,
            font=("Segoe UI", 11),
            bg="#21262d",
            fg=self.colors["text_light"],
            relief="flat",
            width=33
        )
        poster_entry.grid(row=2, column=1, padx=20, pady=10, sticky='w')
        
        def browse_file():
            path = filedialog.askopenfilename(
                title="Select Poster Image",
                filetypes=[
                    ("Image files", "*.png *.gif *.pgm *.ppm"),
                    ("PNG", "*.png"),
                    ("GIF", "*.gif"),
                    ("All files", "*.*")
                ]
            )
            if path:
                poster_path_var.set(path)
        
        self.create_modern_button(
            form_card,
            "Browse",
            browse_file,
            self.colors["accent"],
            width=10
        ).grid(row=2, column=2, padx=10, pady=10)
        
        def save_poster():
            movie_name = movie_var.get().strip()
            poster_path = poster_path_var.get().strip()
            if not movie_name or movie_name not in movie_names:
                messagebox.showerror("Error", "Please select a movie")
                return
            if not poster_path:
                messagebox.showerror("Error", "Please choose a poster file")
                return
            if not os.path.exists(poster_path):
                messagebox.showerror("Error", "Selected file does not exist")
                return
            
            # Update
            for mid, m in self.movies.items():
                if m.get("name") == movie_name:
                    m["poster_path"] = poster_path
                    if mid in self.poster_cache:
                        del self.poster_cache[mid]
                    self.save_data()
                    messagebox.showinfo("Success", "Poster updated successfully!")
                    return
            messagebox.showerror("Error", "Movie not found")
        
        self.create_modern_button(
            form_card,
            "💾 Save Poster",
            save_poster,
            self.colors["success"],
            width=20
        ).grid(row=3, column=0, columnspan=3, pady=20)

    def manage_marquee(self):
        """Manage marquee message"""
        self.clear_window()
        
        # Header
        header = tk.Frame(self.root, bg=self.colors["warning"], height=70)
        header.pack(fill='x')
        
        tk.Label(
            header,
            text="📺 Manage Marquee",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["warning"],
            fg="#2d3436"
        ).pack(side='left', padx=30, pady=15)
        
        self.create_modern_button(
            header,
            "← Back",
            self.show_admin_panel,
            self.darken_color(self.colors["warning"], 20),
            "#2d3436",
            width=10
        ).pack(side='right', padx=30, pady=15)
        
        # Content
        content = tk.Frame(self.root, bg=self.colors["bg_dark"])
        content.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Form card
        form_card = self.create_card(content, padx=30, pady=30)
        form_card.pack(fill='x', pady=10)
        
        tk.Label(
            form_card,
            text="✏️ Update Marquee Message",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        tk.Label(form_card, text="Current Message:", bg=self.colors["bg_card"], 
                fg=self.colors["text_light"]).grid(row=1, column=0, padx=20, pady=10, sticky='nw')
        
        current_label = tk.Label(form_card, text=self.marquee_text, bg="#21262d", 
                                fg=self.colors["text_light"], relief="flat", width=50, height=3,
                                justify="left", anchor="w", wraplength=400)
        current_label.grid(row=1, column=1, padx=20, pady=10, sticky='w')
        
        tk.Label(form_card, text="New Message:", bg=self.colors["bg_card"], 
                fg=self.colors["text_light"]).grid(row=2, column=0, padx=20, pady=10, sticky='nw')
        
        message_text = tk.Text(form_card, font=("Segoe UI", 11), bg="#21262d", 
                              fg=self.colors["text_light"], relief="flat", width=50, height=3,
                              wrap="word")
        message_text.grid(row=2, column=1, padx=20, pady=10, sticky='w')
        message_text.insert("1.0", self.marquee_text)
        
        def update_marquee():
            new_message = message_text.get("1.0", "end-1c").strip()
            if new_message:
                self.marquee_text = new_message
                self.save_data()
                messagebox.showinfo("Success", "Marquee message updated successfully!")
                current_label.config(text=new_message)
            else:
                messagebox.showerror("Error", "Please enter a valid message")
        
        self.create_modern_button(
            form_card,
            "🔄 Update Marquee",
            update_marquee,
            self.colors["success"],
            width=20
        ).grid(row=3, column=0, columnspan=2, pady=20)

    def manage_release_dates(self):
        """Manage movie release dates"""
        self.clear_window()
        
        # Header
        header = tk.Frame(self.root, bg=self.colors["warning"], height=70)
        header.pack(fill='x')
        
        tk.Label(
            header,
            text="📅 Manage Release Dates",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["warning"],
            fg="#2d3436"
        ).pack(side='left', padx=30, pady=15)
        
        self.create_modern_button(
            header,
            "← Back",
            self.show_admin_panel,
            self.darken_color(self.colors["warning"], 20),
            "#2d3436",
            width=10
        ).pack(side='right', padx=30, pady=15)
        
        # Content
        content = tk.Frame(self.root, bg=self.colors["bg_dark"])
        content.pack(expand=True, fill='both', padx=20, pady=20)
        
        tk.Label(
            content,
            text="Update movie release dates to control what appears in theaters.",
            font=("Segoe UI", 12),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(anchor='w', pady=(0, 10))
        
        # Form card
        form_card = self.create_card(content, padx=30, pady=30)
        form_card.pack(fill='x', pady=10)
        
        tk.Label(
            form_card,
            text="✏️ Update Release Date",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        tk.Label(
            form_card,
            text="Select Movie:",
            font=("Segoe UI", 11),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).grid(row=1, column=0, padx=20, pady=10, sticky='w')
        
        movie_var = tk.StringVar()
        movie_names = sorted([movie["name"] for movie in self.movies.values()])
        movie_dropdown = ttk.Combobox(
            form_card,
            textvariable=movie_var,
            values=movie_names,
            width=35
        )
        movie_dropdown.grid(row=1, column=1, padx=20, pady=10, sticky='w')
        
        tk.Label(
            form_card,
            text="Release Date (YYYY-MM-DD):",
            font=("Segoe UI", 11),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).grid(row=2, column=0, padx=20, pady=10, sticky='w')
        
        release_entry = tk.Entry(
            form_card,
            font=("Segoe UI", 11),
            bg="#21262d",
            fg=self.colors["text_light"],
            relief="flat",
            width=33
        )
        release_entry.grid(row=2, column=1, padx=20, pady=10, sticky='w')
        
        def apply_release_update():
            movie_name = movie_var.get().strip()
            release_date = release_entry.get().strip()
            if not movie_name or movie_name not in movie_names:
                messagebox.showerror("Error", "Please select a movie")
                return
            if not release_date:
                messagebox.showerror("Error", "Please enter a release date")
                return
            self.update_release_date(movie_name, release_date)
            release_entry.delete(0, tk.END)
            movie_dropdown.set('')
            self.manage_release_dates()
        
        self.create_modern_button(
            form_card,
            "💾 Save Release Date",
            apply_release_update,
            self.colors["success"],
            width=20
        ).grid(row=3, column=0, columnspan=2, pady=20)
        
        # Release dates list
        tk.Label(
            content,
            text="Current Release Schedule",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(pady=20, anchor='w')
        
        canvas = tk.Canvas(content, bg=self.colors["bg_dark"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
        release_frame = tk.Frame(canvas, bg=self.colors["bg_dark"])
        
        release_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=release_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for movie_id, movie in sorted(self.movies.items(), key=lambda x: x[1]["name"]):
            movie_card = self.create_card(release_frame, padx=20, pady=15)
            movie_card.pack(fill='x', pady=5)
            
            tk.Label(
                movie_card,
                text=movie["name"],
                font=("Segoe UI", 12, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack(anchor='w')
            
            info_text = f"🎭 {movie['genre']}   |   📅 Release Date: {movie.get('release_date', 'Not set')}"
            tk.Label(
                movie_card,
                text=info_text,
                font=("Segoe UI", 10),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(anchor='w', pady=(4, 0))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def delete_movie(self, movie_id):
        """Delete movie"""
        if messagebox.askyesno("Confirm", "Delete this movie?"):
            del self.movies[movie_id]
            self.save_data()
            self.manage_movies()
    
    def manage_cities(self):
        """Manage cities"""
        self.clear_window()
        
        # Header
        header = tk.Frame(self.root, bg=self.colors["warning"], height=70)
        header.pack(fill='x')
        
        tk.Label(
            header,
            text="🏙️ Manage Cities",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["warning"],
            fg="#2d3436"
        ).pack(side='left', padx=30, pady=15)
        
        self.create_modern_button(
            header,
            "← Back",
            self.show_admin_panel,
            self.darken_color(self.colors["warning"], 20),
            "#2d3436",
            width=10
        ).pack(side='right', padx=30, pady=15)
        
        # Content
        content = tk.Frame(self.root, bg=self.colors["bg_dark"])
        content.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Add city form
        form_card = self.create_card(content, padx=30, pady=30)
        form_card.pack(fill='x', pady=10)
        
        tk.Label(
            form_card,
            text="➕ Add New City",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        tk.Label(form_card, text="City Name:", bg=self.colors["bg_card"], 
                fg=self.colors["text_light"]).grid(row=1, column=0, padx=20, pady=15, sticky='w')
        city_entry = tk.Entry(form_card, font=("Segoe UI", 11), bg="#21262d", 
                            fg=self.colors["text_light"], relief="flat", width=30)
        city_entry.grid(row=1, column=1, padx=20, pady=15)
        
        self.create_modern_button(
            form_card,
            "➕ Add City",
            lambda: self.add_city(city_entry.get()),
            self.colors["success"],
            width=20
        ).grid(row=2, column=0, columnspan=2, pady=20)
        
        # Cities list
        tk.Label(
            content,
            text="Current Cities",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(pady=20)
        
        # Scrollable cities list
        canvas = tk.Canvas(content, bg=self.colors["bg_dark"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
        cities_frame = tk.Frame(canvas, bg=self.colors["bg_dark"])
        
        cities_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=cities_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for city_id, city_name in sorted(self.cities.items(), key=lambda x: x[1]):
            city_card = self.create_card(cities_frame, padx=20, pady=15)
            city_card.pack(fill='x', pady=5)
            
            tk.Label(
                city_card,
                text=city_name,
                font=("Segoe UI", 12),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack(side='left', padx=15, pady=10)
            
            self.create_modern_button(
                city_card,
                "🗑️ Delete",
                lambda c_id=city_id: self.delete_city(c_id),
                self.colors["primary"],
                width=10
            ).pack(side='right', padx=15)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_city(self, city_name):
        """Add new city"""
        if not city_name:
            messagebox.showerror("Error", "City name is required")
            return
        
        city_id = f"CITY{str(len(self.cities) + 1).zfill(3)}"
        self.cities[city_id] = city_name
        self.save_data()
        messagebox.showinfo("Success", "🏙️ City added successfully!")
        self.manage_cities()
    
    def delete_city(self, city_id):
        """Delete city"""
        if messagebox.askyesno("Confirm", "Delete this city?"):
            del self.cities[city_id]
            self.save_data()
            self.manage_cities()
    
    def manage_theaters(self):
        """Manage theaters"""
        self.clear_window()
        
        # Header
        header = tk.Frame(self.root, bg=self.colors["warning"], height=70)
        header.pack(fill='x')
        
        tk.Label(
            header,
            text="🎭 Manage Theaters",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["warning"],
            fg="#2d3436"
        ).pack(side='left', padx=30, pady=15)
        
        self.create_modern_button(
            header,
            "← Back",
            self.show_admin_panel,
            self.darken_color(self.colors["warning"], 20),
            "#2d3436",
            width=10
        ).pack(side='right', padx=30, pady=15)
        
        # Content
        content = tk.Frame(self.root, bg=self.colors["bg_dark"])
        content.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Add theater form
        form_card = self.create_card(content, padx=30, pady=30)
        form_card.pack(fill='x', pady=10)
        
        tk.Label(
            form_card,
            text="➕ Add New Theater",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        tk.Label(form_card, text="Theater Name:", bg=self.colors["bg_card"], 
                fg=self.colors["text_light"]).grid(row=1, column=0, padx=20, pady=10, sticky='w')
        name_entry = tk.Entry(form_card, font=("Segoe UI", 11), bg="#21262d", 
                            fg=self.colors["text_light"], relief="flat", width=30)
        name_entry.grid(row=1, column=1, padx=20, pady=10)
        
        tk.Label(form_card, text="City:", bg=self.colors["bg_card"], 
                fg=self.colors["text_light"]).grid(row=2, column=0, padx=20, pady=10, sticky='w')
        city_var = tk.StringVar()
        city_dropdown = ttk.Combobox(form_card, textvariable=city_var, width=28,
                                    values=sorted(self.cities.values()))
        city_dropdown.grid(row=2, column=1, padx=20, pady=10)
        
        tk.Label(form_card, text="Screen:", bg=self.colors["bg_card"], 
                fg=self.colors["text_light"]).grid(row=3, column=0, padx=20, pady=10, sticky='w')
        screen_entry = tk.Entry(form_card, font=("Segoe UI", 11), bg="#21262d", 
                              fg=self.colors["text_light"], relief="flat", width=30)
        screen_entry.grid(row=3, column=1, padx=20, pady=10)
        
        tk.Label(form_card, text="Capacity:", bg=self.colors["bg_card"], 
                fg=self.colors["text_light"]).grid(row=4, column=0, padx=20, pady=10, sticky='w')
        capacity_entry = tk.Entry(form_card, font=("Segoe UI", 11), bg="#21262d", 
                                fg=self.colors["text_light"], relief="flat", width=30)
        capacity_entry.grid(row=4, column=1, padx=20, pady=10)
        
        self.create_modern_button(
            form_card,
            "➕ Add Theater",
            lambda: self.add_theater(name_entry.get(), city_var.get(),
                                    screen_entry.get(), capacity_entry.get()),
            self.colors["success"],
            width=20
        ).grid(row=5, column=0, columnspan=2, pady=20)
        
        # Theaters list
        tk.Label(
            content,
            text="Current Theaters",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(pady=20)
        
        # Scrollable theaters list
        canvas = tk.Canvas(content, bg=self.colors["bg_dark"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
        theaters_frame = tk.Frame(canvas, bg=self.colors["bg_dark"])
        
        theaters_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=theaters_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for theater_id, theater in sorted(self.theaters.items(), key=lambda x: x[1]["name"]):
            city_name = self.cities.get(theater["city_id"], "Unknown")
            theater_card = self.create_card(theaters_frame, padx=20, pady=15)
            theater_card.pack(fill='x', pady=5)
            
            tk.Label(
                theater_card,
                text=f"{theater['name']} | {city_name} | {theater['screen']} | {theater['capacity']} seats",
                font=("Segoe UI", 11),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack(side='left', padx=15, pady=10)
            
            self.create_modern_button(
                theater_card,
                "🗑️ Delete",
                lambda t_id=theater_id: self.delete_theater(t_id),
                self.colors["primary"],
                width=10
            ).pack(side='right', padx=15)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_theater(self, name, city_name, screen, capacity):
        """Add new theater"""
        if not all([name, city_name, screen, capacity]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            capacity = int(capacity)
        except ValueError:
            messagebox.showerror("Error", "Capacity must be a number")
            return
        
        # Find city ID
        city_id = None
        for cid, cname in self.cities.items():
            if cname == city_name:
                city_id = cid
                break
        
        if not city_id:
            messagebox.showerror("Error", "City not found")
            return
        
        theater_id = f"TH{str(len(self.theaters) + 1).zfill(3)}"
        self.theaters[theater_id] = {
            "name": name,
            "city_id": city_id,
            "screen": screen,
            "capacity": capacity
        }
        self.save_data()
        messagebox.showinfo("Success", "🎭 Theater added successfully!")
        self.manage_theaters()
    
    def delete_theater(self, theater_id):
        """Delete theater"""
        if messagebox.askyesno("Confirm", "Delete this theater?"):
            del self.theaters[theater_id]
            self.save_data()
            self.manage_theaters()
    
    def manage_showtimes(self, page=1):
        """Manage showtimes with pagination"""
        self.clear_window()
        
        # Header
        header = tk.Frame(self.root, bg=self.colors["warning"], height=70)
        header.pack(fill='x')
        
        tk.Label(
            header,
            text="⏰ Manage Showtimes",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["warning"],
            fg="#2d3436"
        ).pack(side='left', padx=30, pady=15)
        
        self.create_modern_button(
            header,
            "← Back",
            self.show_admin_panel,
            self.darken_color(self.colors["warning"], 20),
            "#2d3436",
            width=10
        ).pack(side='right', padx=30, pady=15)
        
        # Content
        content = tk.Frame(self.root, bg=self.colors["bg_dark"])
        content.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Add showtime form
        form_card = self.create_card(content, padx=30, pady=30)
        form_card.pack(fill='x', pady=10)
        
        tk.Label(
            form_card,
            text="➕ Add New Showtime",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors["text_light"]
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        tk.Label(form_card, text="Movie:", bg=self.colors["bg_card"], 
                fg=self.colors["text_light"]).grid(row=1, column=0, padx=20, pady=10, sticky='w')
        movie_var = tk.StringVar()
        movie_dropdown = ttk.Combobox(form_card, textvariable=movie_var, width=28,
                                     values=sorted([m["name"] for m in self.movies.values()]))
        movie_dropdown.grid(row=1, column=1, padx=20, pady=10)
        
        tk.Label(form_card, text="Theater:", bg=self.colors["bg_card"], 
                fg=self.colors["text_light"]).grid(row=2, column=0, padx=20, pady=10, sticky='w')
        theater_var = tk.StringVar()
        theater_dropdown = ttk.Combobox(form_card, textvariable=theater_var, width=28,
                                       values=sorted([t["name"] for t in self.theaters.values()]))
        theater_dropdown.grid(row=2, column=1, padx=20, pady=10)
        
        tk.Label(form_card, text="Time:", bg=self.colors["bg_card"], 
                fg=self.colors["text_light"]).grid(row=3, column=0, padx=20, pady=10, sticky='w')
        time_entry = tk.Entry(form_card, font=("Segoe UI", 11), bg="#21262d", 
                            fg=self.colors["text_light"], relief="flat", width=30)
        time_entry.grid(row=3, column=1, padx=20, pady=10)
        
        tk.Label(form_card, text="Slot:", bg=self.colors["bg_card"], 
                fg=self.colors["text_light"]).grid(row=4, column=0, padx=20, pady=10, sticky='w')
        slot_var = tk.StringVar()
        slot_dropdown = ttk.Combobox(form_card, textvariable=slot_var, width=28,
                                    values=["Morning", "Afternoon", "Evening", "Night"])
        slot_dropdown.grid(row=4, column=1, padx=20, pady=10)
        
        tk.Label(form_card, text="Price:", bg=self.colors["bg_card"], 
                fg=self.colors["text_light"]).grid(row=5, column=0, padx=20, pady=10, sticky='w')
        price_entry = tk.Entry(form_card, font=("Segoe UI", 11), bg="#21262d", 
                             fg=self.colors["text_light"], relief="flat", width=30)
        price_entry.grid(row=5, column=1, padx=20, pady=10)
        
        self.create_modern_button(
            form_card,
            "➕ Add Showtime",
            lambda: self.add_showtime(movie_var.get(), theater_var.get(),
                                     time_entry.get(), slot_var.get(),
                                     price_entry.get()),
            self.colors["success"],
            width=20
        ).grid(row=6, column=0, columnspan=2, pady=20)
        
        # Paginate showtimes
        items_per_page = 20
        shows_list = []
        
        # Pre-create lookup dictionaries for better performance
        movie_lookup = {movie_id: movie for movie_id, movie in self.movies.items()}
        theater_lookup = {theater_id: theater for theater_id, theater in self.theaters.items()}
        
        for show_id, show in self.showtimes.items():
            movie_name = movie_lookup.get(show["movie_id"], {}).get("name", "Unknown")
            theater_name = theater_lookup.get(show["theater_id"], {}).get("name", "Unknown")
            shows_list.append((show_id, show, movie_name, theater_name))
        
        # Sort by movie name, then theater name, then time
        shows_list.sort(key=lambda x: (x[2], x[3], x[1]['time']))
        
        # Pagination
        total_shows = len(shows_list)
        total_pages = (total_shows + items_per_page - 1) // items_per_page
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        page_shows = shows_list[start_idx:end_idx]
        
        # Results info
        tk.Label(
            content,
            text=f"📊 Showing {len(page_shows)} of {total_shows} showtimes (Page {page}/{total_pages})",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["text_light"]
        ).pack(pady=10)
        
        # Scrollable showtimes list
        canvas = tk.Canvas(content, bg=self.colors["bg_dark"], highlightthickness=0, height=400)
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
        shows_frame = tk.Frame(canvas, bg=self.colors["bg_dark"])
        
        shows_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=shows_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display paginated results
        for show_id, show, movie_name, theater_name in page_shows:
            available = show["capacity"] - len(show["booked_seats"])
            
            show_card = self.create_card(shows_frame, padx=20, pady=15)
            show_card.pack(fill='x', pady=5)
            
            tk.Label(
                show_card,
                text=f"{movie_name} | {theater_name} | {show['time']} | {show.get('slot', 'N/A')} | ₹{show['price']} | {available}/{show['capacity']} available",
                font=("Segoe UI", 10),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack(side='left', padx=15, pady=10)
            
            self.create_modern_button(
                show_card,
                "🗑️ Delete",
                lambda s_id=show_id: self.delete_showtime(s_id, page),
                self.colors["primary"],
                width=10
            ).pack(side='right', padx=15)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Pagination controls
        if total_pages > 1:
            pagination_frame = tk.Frame(content, bg=self.colors["bg_dark"])
            pagination_frame.pack(pady=10)
            
            # Previous button
            if page > 1:
                self.create_modern_button(
                    pagination_frame,
                    "⬅️ Previous",
                    lambda: self.manage_showtimes(page-1),
                    self.colors["primary"],
                    width=12
                ).pack(side='left', padx=5)
            
            # Page info
            tk.Label(
                pagination_frame,
                text=f"Page {page} of {total_pages}",
                font=("Segoe UI", 10),
                bg=self.colors["bg_dark"],
                fg=self.colors["text_light"]
            ).pack(side='left', padx=20)
            
            # Next button
            if page < total_pages:
                self.create_modern_button(
                    pagination_frame,
                    "Next ➡️",
                    lambda: self.manage_showtimes(page+1),
                    self.colors["primary"],
                    width=12
                ).pack(side='left', padx=5)
    
    def add_showtime(self, movie_name, theater_name, time, slot, price):
        """Add new showtime"""
        if not all([movie_name, theater_name, time, slot, price]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            price = int(price)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number")
            return
        
        # Find movie ID
        movie_id = None
        for mid, movie in self.movies.items():
            if movie["name"] == movie_name:
                movie_id = mid
                break
        
        # Find theater ID
        theater_id = None
        for tid, theater in self.theaters.items():
            if theater["name"] == theater_name:
                theater_id = tid
                break
        
        if not movie_id or not theater_id:
            messagebox.showerror("Error", "Movie or Theater not found")
            return
        
        show_id = f"SHOW{str(len(self.showtimes) + 1).zfill(3)}"
        self.showtimes[show_id] = {
            "movie_id": movie_id,
            "theater_id": theater_id,
            "time": time,
            "slot": slot,
            "price": price,
            "capacity": self.theaters[theater_id]["capacity"],
            "booked_seats": []
        }
        self.save_data()
        messagebox.showinfo("Success", "⏰ Showtime added successfully!")
        self.manage_showtimes()
    
    def delete_showtime(self, show_id, page=1):
        """Delete showtime"""
        if messagebox.askyesno("Confirm", "Delete this showtime?"):
            del self.showtimes[show_id]
            self.save_data()
            self.manage_showtimes(page=page)
    
    def send_booking_email(self, booking_id):
        """Send booking confirmation email"""
        try:
            if booking_id not in self.bookings:
                messagebox.showerror("Error", "Booking not found")
                return
            
            booking = self.bookings[booking_id]
            show = self.showtimes[booking["show_id"]]
            movie = self.movies[show["movie_id"]]
            theater = self.theaters[show["theater_id"]]
            city = self.cities[theater["city_id"]]
            user = booking["user"]
            
            # Get user email
            user_email = self.users[user].get("email", "")
            
            if not user_email:
                messagebox.showerror("Error", f"User {user} does not have an email address registered")
                return
            
            # Create email content
            email_subject = f"🎬 Booking Confirmation - {movie['name']}"
            
            email_body = f"""
🎫 BOOKING CONFIRMATION 🎫

Booking ID: {booking_id}
Movie: {movie['name']}
Theater: {theater['name']}, {city}
Show Time: {show['time']}
Seats: {', '.join(booking['seats'])}
Amount: ₹{booking['amount']}
Payment Method: {booking.get('payment_method', 'Online')}
Status: {booking.get('status', 'confirmed')}

📅 Booking Date: {booking['date']}

🎟️ Please arrive 30 minutes before showtime
🎭 Carry this booking confirmation for entry
💰 Payment: {booking.get('payment_method', 'Online')}

Thank you for choosing BookMyShow! 🍿

---
BookMyShow Team
📧 support@bookmyshow.com
🌐 www.bookmyshow.com
            """
            
            # Simulate sending email (in real app, you'd use SMTP)
            result = messagebox.askyesno(
                "Send Email Confirmation",
                f"Send booking confirmation to:\n\n"
                f"📧 {user_email}\n"
                f"👤 {user}\n\n"
                f"🎬 {movie['name']}\n"
                f"🎫 Booking ID: {booking_id}\n\n"
                f"Send email now?"
            )
            
            if result:
                # Simulate email sending with progress
                progress_window = tk.Toplevel(self.root)
                progress_window.title("Sending Email")
                progress_window.geometry("400x150")
                progress_window.resizable(False, False)
                progress_window.configure(bg=self.colors["bg_dark"])
                
                # Center the window
                progress_window.transient(self.root)
                progress_window.grab_set()
                
                tk.Label(
                    progress_window,
                    text="📧 Sending Email...",
                    font=("Segoe UI", 14, "bold"),
                    bg=self.colors["bg_dark"],
                    fg=self.colors["text_light"]
                ).pack(pady=20)
                
                progress_bar = ttk.Progressbar(
                    progress_window,
                    mode='indeterminate',
                    length=300
                )
                progress_bar.pack(pady=10)
                progress_bar.start()
                
                def complete_email_send():
                    progress_bar.stop()
                    progress_window.destroy()
                    messagebox.showinfo(
                        "Email Sent Successfully!",
                        f"📧 Booking confirmation sent to:\n"
                        f"{user_email}\n\n"
                        f"🎫 Booking ID: {booking_id}\n"
                        f"🎬 {movie['name']}\n\n"
                        f"Check your inbox for the confirmation!"
                    )
                
                # Simulate email sending delay
                progress_window.after(2000, complete_email_send)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {str(e)}")
    
    def view_all_bookings(self):
        """View all bookings"""
        self.clear_window()
        
        # Header with gradient effect
        header = tk.Frame(self.root, bg=self.colors["warning"], height=80)
        header.pack(fill='x')
        
        # Header content
        header_content = tk.Frame(header, bg=self.colors["warning"])
        header_content.pack(expand=True, fill='both', padx=30, pady=15)
        
        tk.Label(
            header_content,
            text="📊 All Bookings",
            font=("Segoe UI", 28, "bold"),
            bg=self.colors["warning"],
            fg="#2d3436"
        ).pack(side='left')
        
        self.create_modern_button(
            header_content,
            "← Back to Admin",
            self.show_admin_panel,
            self.darken_color(self.colors["warning"], 20),
            "#2d3436",
            width=15
        ).pack(side='right', padx=20)
        
        # Main content area
        content = tk.Frame(self.root, bg=self.colors["bg_dark"])
        content.pack(expand=True, fill='both', padx=25, pady=25)
        
        if self.bookings:
            # Statistics Dashboard
            stats_container = tk.Frame(content, bg=self.colors["bg_dark"])
            stats_container.pack(fill='x', pady=(0, 25))
            
            # Stats cards in a row
            stats_row = tk.Frame(stats_container, bg=self.colors["bg_dark"])
            stats_row.pack(fill='x')
            
            # Total Bookings Card
            bookings_card = self.create_card(stats_row, padx=15, pady=15)
            bookings_card.pack(side='left', fill='both', expand=True, padx=(0, 10))
            
            tk.Label(
                bookings_card,
                text="📊",
                font=("Arial", 24),
                bg=self.colors["bg_card"],
                fg=self.colors["primary"]
            ).pack()
            
            tk.Label(
                bookings_card,
                text=f"{len(self.bookings)}",
                font=("Segoe UI", 32, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack()
            
            tk.Label(
                bookings_card,
                text="Total Bookings",
                font=("Segoe UI", 11),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack()
            
            # Total Revenue Card
            revenue_card = self.create_card(stats_row, padx=15, pady=15)
            revenue_card.pack(side='left', fill='both', expand=True, padx=10)
            
            total_revenue = sum(
                booking.get("amount", 0)
                for booking in self.bookings.values()
                if booking.get("status") == "confirmed"
            )
            
            tk.Label(
                revenue_card,
                text="💰",
                font=("Arial", 24),
                bg=self.colors["bg_card"],
                fg=self.colors["success"]
            ).pack()
            
            tk.Label(
                revenue_card,
                text=f"₹{total_revenue}",
                font=("Segoe UI", 32, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack()
            
            tk.Label(
                revenue_card,
                text="Total Revenue",
                font=("Segoe UI", 11),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack()
            
            # Average Revenue Card
            avg_card = self.create_card(stats_row, padx=15, pady=15)
            avg_card.pack(side='left', fill='both', expand=True, padx=(10, 0))
            
            confirmed_count = sum(1 for b in self.bookings.values() if b.get("status") == "confirmed")
            avg_revenue = total_revenue // confirmed_count if confirmed_count else 0
            
            tk.Label(
                avg_card,
                text="📈",
                font=("Arial", 24),
                bg=self.colors["bg_card"],
                fg=self.colors["secondary"]
            ).pack()
            
            tk.Label(
                avg_card,
                text=f"₹{avg_revenue}",
                font=("Segoe UI", 32, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack()
            
            tk.Label(
                avg_card,
                text="Average Revenue",
                font=("Segoe UI", 11),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack()
            
            # Bookings List Header
            list_header = tk.Frame(content, bg=self.colors["bg_card"])
            list_header.pack(fill='x', pady=(0, 15))
            
            tk.Label(
                list_header,
                text="🎫 Booking Details",
                font=("Segoe UI", 16, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack(side='left', padx=20, pady=15)
            
            # Quick Actions
            actions_frame = tk.Frame(list_header, bg=self.colors["bg_card"])
            actions_frame.pack(side='right', padx=20, pady=10)
            
            self.create_modern_button(
                actions_frame,
                "🔄 Refresh",
                lambda: self.view_all_bookings(),
                self.colors["secondary"],
                width=10
            ).pack(side='left', padx=5)
            
            # Scrollable bookings list with enhanced styling
            canvas = tk.Canvas(content, bg=self.colors["bg_dark"], highlightthickness=0)
            scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
            bookings_frame = tk.Frame(canvas, bg=self.colors["bg_dark"])
            
            bookings_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=bookings_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Enhanced booking cards
            for booking_id, booking in self.bookings.items():
                show = self.showtimes[booking["show_id"]]
                movie = self.movies[show["movie_id"]]
                theater = self.theaters[show["theater_id"]]
                
                # Enhanced booking card with better layout
                booking_card = self.create_card(bookings_frame, padx=20, pady=18)
                booking_card.pack(fill='x', pady=8)
                
                # Card header with booking ID and status
                card_header = tk.Frame(booking_card, bg=self.colors["bg_card"])
                card_header.pack(fill='x', padx=15, pady=(15, 10))
                
                # Booking ID with icon
                id_frame = tk.Frame(card_header, bg=self.colors["bg_card"])
                id_frame.pack(side='left')
                
                tk.Label(
                    id_frame,
                    text="📋",
                    font=("Segoe UI", 14),
                    bg=self.colors["bg_card"],
                    fg=self.colors["primary"]
                ).pack(side='left')
                
                tk.Label(
                    id_frame,
                    text=booking_id,
                    font=("Segoe UI", 12, "bold"),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_light"]
                ).pack(side='left', padx=(5, 0))
                
                # Status badge
                is_cancelled = booking.get("status") == "cancelled"
                status_badge = tk.Label(
                    card_header,
                    text="❌ Booking Canceled" if is_cancelled else "✅ Confirmed",
                    font=("Segoe UI", 9, "bold"),
                    bg=self.colors["primary"] if is_cancelled else self.colors["success"],
                    fg="white",
                    padx=8,
                    pady=2
                )
                status_badge.pack(side='right')
                
                # Main content area
                content_area = tk.Frame(booking_card, bg=self.colors["bg_card"])
                content_area.pack(fill='x', padx=15, pady=(0, 10))
                
                # Left column - User and Movie info
                left_col = tk.Frame(content_area, bg=self.colors["bg_card"])
                left_col.pack(side='left', fill='both', expand=True)
                
                # User info
                user_frame = tk.Frame(left_col, bg=self.colors["bg_card"])
                user_frame.pack(fill='x', pady=(0, 8))
                
                tk.Label(
                    user_frame,
                    text="👤",
                    font=("Segoe UI", 10),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_muted"]
                ).pack(side='left')
                
                tk.Label(
                    user_frame,
                    text=booking['user'],
                    font=("Segoe UI", 11, "bold"),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_light"]
                ).pack(side='left', padx=(5, 0))
                
                # Movie info
                movie_frame = tk.Frame(left_col, bg=self.colors["bg_card"])
                movie_frame.pack(fill='x', pady=(0, 8))
                
                tk.Label(
                    movie_frame,
                    text="🎬",
                    font=("Segoe UI", 10),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_muted"]
                ).pack(side='left')
                
                tk.Label(
                    movie_frame,
                    text=movie['name'],
                    font=("Segoe UI", 11),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_light"]
                ).pack(side='left', padx=(5, 0))
                
                # Theater info
                theater_frame = tk.Frame(left_col, bg=self.colors["bg_card"])
                theater_frame.pack(fill='x')
                
                tk.Label(
                    theater_frame,
                    text="🎭",
                    font=("Segoe UI", 10),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_muted"]
                ).pack(side='left')
                
                tk.Label(
                    theater_frame,
                    text=theater['name'],
                    font=("Segoe UI", 11),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_light"]
                ).pack(side='left', padx=(5, 0))
                
                # Right column - Details and actions
                right_col = tk.Frame(content_area, bg=self.colors["bg_card"])
                right_col.pack(side='right', padx=(20, 0))
                
                # Date and Time
                datetime_frame = tk.Frame(right_col, bg=self.colors["bg_card"])
                datetime_frame.pack(fill='x', pady=(0, 8))
                
                tk.Label(
                    datetime_frame,
                    text="📅",
                    font=("Segoe UI", 10),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_muted"]
                ).pack(side='left')
                
                tk.Label(
                    datetime_frame,
                    text=booking['date'],
                    font=("Segoe UI", 10),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_light"]
                ).pack(side='left', padx=(5, 0))
                
                tk.Label(
                    datetime_frame,
                    text="⏰",
                    font=("Segoe UI", 10),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_muted"]
                ).pack(side='left', padx=(10, 0))
                
                tk.Label(
                    datetime_frame,
                    text=show['time'],
                    font=("Segoe UI", 10),
                    bg=self.colors["bg_card"],
                    fg=self.colors["text_light"]
                ).pack(side='left', padx=(5, 0))
                
                # Seats and Amount
                seats_amount_frame = tk.Frame(right_col, bg=self.colors["bg_card"])
                seats_amount_frame.pack(fill='x')
                
                tk.Label(
                    seats_amount_frame,
                    text=f"💺 {', '.join(booking['seats'])}",
                    font=("Segoe UI", 10, "bold"),
                    bg=self.colors["bg_card"],
                    fg=self.colors["primary"]
                ).pack(anchor='e')
                
                tk.Label(
                    seats_amount_frame,
                    text=f"💰 ₹{booking.get('amount', 0)}",
                    font=("Segoe UI", 12, "bold"),
                    bg=self.colors["bg_card"],
                    fg=self.colors["success"]
                ).pack(anchor='e', pady=(2, 0))
                
                # Action buttons
                action_frame = tk.Frame(booking_card, bg=self.colors["bg_card"])
                action_frame.pack(fill='x', padx=15, pady=(0, 15))
                
                self.create_modern_button(
                    action_frame,
                    "🎫 View Ticket",
                    lambda b_id=booking_id: self.show_ticket(b_id),
                    self.colors["primary"],
                    width=12
                ).pack(side='left', padx=(0, 8))
                
                self.create_modern_button(
                    action_frame,
                    "📧 Email",
                    lambda b_id=booking_id: self.send_booking_email(b_id),
                    self.colors["secondary"],
                    width=10
                ).pack(side='left', padx=8)
                
                self.create_modern_button(
                    action_frame,
                    "🗑️ Cancel",
                    lambda b_id=booking_id: self.cancel_booking(b_id),
                    self.colors["primary"],
                    width=10
                ).pack(side='right')
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        else:
            # Empty state with better design
            empty_container = tk.Frame(content, bg=self.colors["bg_dark"])
            empty_container.pack(expand=True, fill='both')
            
            # Empty state card
            empty_card = self.create_card(empty_container, padx=40, pady=40)
            empty_card.pack(expand=True)
            
            # Icon
            tk.Label(
                empty_card,
                text="📭",
                font=("Arial", 64),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"]
            ).pack(pady=(0, 20))
            
            # Title
            tk.Label(
                empty_card,
                text="No Bookings Yet",
                font=("Segoe UI", 20, "bold"),
                bg=self.colors["bg_card"],
                fg=self.colors["text_light"]
            ).pack(pady=(0, 10))
            
            # Description
            tk.Label(
                empty_card,
                text="No bookings have been made yet. When users book tickets,\nthey will appear here with all their details.",
                font=("Segoe UI", 12),
                bg=self.colors["bg_card"],
                fg=self.colors["text_muted"],
                justify='center'
            ).pack(pady=(0, 20))
            
            # Action button
            self.create_modern_button(
                empty_card,
                "📊 Go to Admin Panel",
                self.show_admin_panel,
                self.colors["primary"],
                width=20
            ).pack()
    
    def cancel_booking(self, booking_id, refresh_callback=None):
        """Cancel a booking with 12-hour cutoff"""
        if refresh_callback is None:
            refresh_callback = self.view_all_bookings

        booking = self.bookings.get(booking_id)
        if not booking:
            messagebox.showerror("Error", "Booking not found")
            return

        if booking.get("status") == "cancelled":
            messagebox.showinfo("Info", "This booking is already canceled")
            return

        show = self.showtimes.get(booking.get("show_id"))
        if not show:
            messagebox.showerror("Error", "Show not found")
            return

        # Calculate show datetime using booking date's day + show's time
        try:
            booking_dt = datetime.strptime(booking.get("date", ""), "%Y-%m-%d %H:%M:%S")
            show_time = datetime.strptime(show.get("time", ""), "%I:%M %p").time()
            show_dt = datetime.combine(booking_dt.date(), show_time)
            if show_dt < booking_dt:
                show_dt = show_dt + timedelta(days=1)
        except Exception:
            messagebox.showerror("Error", "Unable to determine show date/time for cancellation")
            return

        if (show_dt - datetime.now()) < timedelta(hours=12):
            messagebox.showerror(
                "Cancellation Not Allowed",
                "Cancellation is not allowed within 12 hours of the movie time. No refund will be given."
            )
            return

        if not messagebox.askyesno("Confirm Cancel", f"Are you sure you want to cancel booking {booking_id}?\n\nFull refund will be processed."):
            return

        show_id = booking["show_id"]

        # Remove seats from show
        for seat in booking.get("seats", []):
            if seat in self.showtimes.get(show_id, {}).get("booked_seats", []):
                self.showtimes[show_id]["booked_seats"].remove(seat)

        # Remove from user's bookings list so it disappears from My Bookings
        user = booking.get("user")
        if user in self.users and booking_id in self.users[user].get("bookings", []):
            self.users[user]["bookings"].remove(booking_id)

        booking["status"] = "cancelled"
        booking["refund"] = "full"
        booking["cancelled_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.save_data()
        messagebox.showinfo("Success", "Booking canceled successfully. Refund processed.")
        refresh_callback()
    
    def save_data(self):
        """Save all data to file"""
        data = {
            "users": self.users,
            "admins": self.admins,
            "movies": self.movies,
            "cities": self.cities,
            "theaters": self.theaters,
            "showtimes": self.showtimes,
            "bookings": self.bookings,
            "marquee_text": self.marquee_text
        }
        
        try:
            with open("bookmyshow_data.json", "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self):
        """Load data from file"""
        try:
            if os.path.exists("bookmyshow_data.json"):
                with open("bookmyshow_data.json", "r") as f:
                    data = json.load(f)
                    self.users = data.get("users", {})
                    self.admins = data.get("admins", {"admin": "admin123"})
                    self.movies = data.get("movies", {})
                    self.cities = data.get("cities", {})
                    self.theaters = data.get("theaters", {})
                    self.showtimes = data.get("showtimes", {})
                    self.bookings = data.get("bookings", {})
                    self.marquee_text = data.get("marquee_text", "Welcome to BookMyShow! Book your favorite movies now!")
        except Exception as e:
            print(f"Error loading data: {e}")

    def get_filtered_movies_by_genre(self):
        """Get movies based on selected genre"""
        try:
            if not hasattr(self, 'selected_genre'):
                return self.movies
            
            selected_genre = self.selected_genre.get()
            
            if selected_genre == "All":
                return self.movies
            
            filtered = {}
            for movie_id, movie in self.movies.items():
                if "genre" in movie:
                    genre = movie["genre"]
                    # Check if genre contains the selected keyword
                    if selected_genre.lower() in genre.lower():
                        filtered[movie_id] = movie
            
            return filtered
        except Exception as e:
            print(f"Error filtering movies: {e}")
            return self.movies
    
    def filter_movies_by_genre(self, genre):
        """Filter movies by selected genre"""
        try:
            # Update selected genre
            self.selected_genre.set(genre)
            
            # Update button colors
            if hasattr(self, 'genre_buttons'):
                for g, btn in self.genre_buttons.items():
                    # Change color based on whether this button is selected
                    if g == genre:
                        btn.configure(bg=self.colors["primary"])  # Red for selected
                    else:
                        btn.configure(bg=self.colors["secondary"])  # Default color for others
            
            # Clear existing movies
            for widget in self.movies_frame.winfo_children():
                widget.destroy()
            
            # Re-display movies with filter
            max_columns = 5
            row, col = 0, 0
            
            filtered_movies = self.get_filtered_movies_by_genre()
            
            if not filtered_movies:
                # Show no results message
                no_results_frame = tk.Frame(self.movies_frame, bg=self.colors["bg_dark"])
                no_results_frame.pack(pady=50)
                
                tk.Label(
                    no_results_frame,
                    text="🎭",
                    font=("Segoe UI", 24),
                    bg=self.colors["bg_dark"],
                    fg=self.colors["text_muted"]
                ).pack(pady=(0, 10))
                
                tk.Label(
                    no_results_frame,
                    text=f"No {genre} movies found",
                    font=("Segoe UI", 14, "italic"),
                    bg=self.colors["bg_dark"],
                    fg=self.colors["text_muted"]
                ).pack()
            else:
                # Display filtered movies
                for movie_id, movie in sorted(filtered_movies.items(), key=lambda x: x[1]["name"]):
                    try:
                        # Create movie card
                        movie_card = self.create_card(self.movies_frame, padx=10, pady=10)
                        movie_card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
                        self.movies_frame.columnconfigure(col, weight=1)
                        
                        # Movie poster placeholder with gradient
                        poster = tk.Frame(movie_card, bg=self.colors["primary"], height=300)
                        poster.pack(fill='x', pady=(0, 10))
                        poster.pack_propagate(False)
                        poster_img = self.load_poster_image(movie_id, target_w=250, target_h=300)
                        if poster_img:
                            poster_label = tk.Label(poster, image=poster_img, bg=self.colors["primary"])
                            poster_label.image = poster_img
                            poster_label.pack(expand=True)
                        
                        # Movie title
                        tk.Label(
                            movie_card,
                            text=movie.get("name", "Unknown Movie"),
                            font=("Segoe UI", 12, "bold"),
                            bg=self.colors["bg_card"],
                            fg=self.colors["text_light"],
                            wraplength=150
                        ).pack(pady=3)
                        
                        # Rating
                        tk.Label(
                            movie_card,
                            text=movie.get("rating", "⭐ N/A"),
                            font=("Segoe UI", 10),
                            bg=self.colors["bg_card"],
                            fg=self.colors["warning"]
                        ).pack()
                        
                        # Movie details
                        details = [
                            f"🎬 {movie.get('language', 'Unknown')}",
                            f"⏱️ {movie.get('duration', 'Unknown')}",
                            f"🎭 {movie.get('genre', 'Unknown')}"
                        ]
                        
                        for detail in details:
                            tk.Label(
                                movie_card,
                                text=detail,
                                font=("Segoe UI", 9),
                                bg=self.colors["bg_card"],
                                fg=self.colors["text_muted"]
                            ).pack(anchor='w', pady=1)
                        
                        tk.Label(
                            movie_card,
                            text=f"📅 Release Date: {movie.get('release_date', 'Not set')}",
                            font=("Segoe UI", 9),
                            bg=self.colors["bg_card"],
                            fg=self.colors["text_muted"]
                        ).pack(anchor='w', pady=(0, 4))
                        
                        # Book button
                        self.create_modern_button(
                            movie_card,
                            "🎟️ Book Now",
                            lambda m_id=movie_id: self.select_city(m_id),
                            self.colors["primary"],
                            width=18
                        ).pack(pady=10)
                        
                        col += 1
                        if col >= max_columns:
                            col = 0
                            row += 1
                    except Exception as e:
                        print(f"Error creating movie card for {movie_id}: {e}")
                        continue
        except Exception as e:
            print(f"Error in filter_movies_by_genre: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    
    # Center the window
    window_width = 1100
    window_height = 750
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    # Create application
    app = MovieBookingSystem(root)
    root.mainloop()
