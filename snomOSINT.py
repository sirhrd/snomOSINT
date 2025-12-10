import requests
import re
from bs4 import BeautifulSoup
import time
import json
import urllib.parse
import instaloader
import sys
from datetime import datetime

class SocialMediaAnalyzer:
    def __init__(self):
        self.loader = instaloader.Instaloader()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        self.colors = {
            'label': '\033[1;32m',
            'data': '\033[0;37m',
            'error': '\033[1;31m',
            'reset': '\033[0m'
        }
        
        self.countries_list = {
            'السعودية': ['السعودية', 'المملكة العربية السعودية', 'Saudi Arabia', 'KSA', 'SAUDI'],
            'مصر': ['مصر', 'جمهورية مصر العربية', 'Egypt', 'EGY', 'MASR'],
            'الإمارات': ['الإمارات', 'دولة الإمارات', 'UAE', 'United Arab Emirates', 'EMIRATES'],
            'العراق': ['العراق', 'جمهورية العراق', 'Iraq', 'IRQ'],
            'الأردن': ['الأردن', 'المملكة الأردنية', 'Jordan', 'JOR'],
            'الكويت': ['الكويت', 'دولة الكويت', 'Kuwait', 'KWT'],
            'قطر': ['قطر', 'دولة قطر', 'Qatar', 'QAT'],
            'عمان': ['عمان', 'سلطنة عمان', 'Oman', 'OMN'],
            'البحرين': ['البحرين', 'مملكة البحرين', 'Bahrain', 'BHR'],
            'اليمن': ['اليمن', 'الجمهورية اليمنية', 'Yemen', 'YEM'],
            'سوريا': ['سوريا', 'الجمهورية العربية السورية', 'Syria', 'SYR'],
            'لبنان': ['لبنان', 'الجمهورية اللبنانية', 'Lebanon', 'LBN'],
            'فلسطين': ['فلسطين', 'Palestine', 'PSE'],
            'السودان': ['السودان', 'جمهورية السودان', 'Sudan', 'SDN'],
            'ليبيا': ['ليبيا', 'دولة ليبيا', 'Libya', 'LBY'],
            'تونس': ['تونس', 'الجمهورية التونسية', 'Tunisia', 'TUN'],
            'الجزائر': ['الجزائر', 'الجمهورية الجزائرية', 'Algeria', 'DZ', 'DZA'],
            'المغرب': ['المغرب', 'المملكة المغربية', 'Morocco', 'MAR'],
            'موريتانيا': ['موريتانيا', 'الجمهورية الإسلامية الموريتانية', 'Mauritania', 'MRT'],
            'الولايات المتحدة': ['الولايات المتحدة', 'أمريكا', 'USA', 'United States', 'US'],
            'كندا': ['كندا', 'Canada', 'CAN'],
            'بريطانيا': ['بريطانيا', 'المملكة المتحدة', 'UK', 'United Kingdom', 'GBR'],
            'فرنسا': ['فرنسا', 'France', 'FRA'],
            'ألمانيا': ['ألمانيا', 'Germany', 'DEU'],
            'إيطاليا': ['إيطاليا', 'Italy', 'ITA'],
            'إسبانيا': ['إسبانيا', 'Spain', 'ESP'],
            'تركيا': ['تركيا', 'Turkey', 'TUR'],
            'روسيا': ['روسيا', 'Russia', 'RUS'],
            'الصين': ['الصين', 'China', 'CHN'],
            'الهند': ['الهند', 'India', 'IND'],
            'باكستان': ['باكستان', 'Pakistan', 'PAK'],
            'إندونيسيا': ['إندونيسيا', 'Indonesia', 'IDN'],
            'نيجيريا': ['نيجيريا', 'Nigeria', 'NGA'],
            'البرازيل': ['البرازيل', 'Brazil', 'BRA'],
            'المكسيك': ['المكسيك', 'Mexico', 'MEX'],
            'اليابان': ['اليابان', 'Japan', 'JPN'],
            'الفلبين': ['الفلبين', 'Philippines', 'PHL'],
            'فيتنام': ['فيتنام', 'Vietnam', 'VNM'],
            'تايلاند': ['تايلاند', 'Thailand', 'THA'],
            'كوريا الجنوبية': ['كوريا الجنوبية', 'South Korea', 'KOR']
        }

    def display_old_banner(self):
        banner = r"""
         ⠀⠀⠀⠀⢀⣻⣿⣿⣿⣷⣿⣾⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⢠⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⡆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⠋⣸⡿⠋⣿⣿⣿⣿⣿⣿⣿⠉⢿⣇⠹⠿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀  ⠀⠀⠀⠀⢻⠇⠀⠻⣿⣿⣿⣿⣿⠟⠁⠸⡟⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⠀⠀⠀⣀⣀⣾⣿⣷⡀⠀⠀⠀⠀⣀⣀⣀⣀⣀⠀⠀
⠀⠀⠀⢀⣴⡿⠿⠿⠿⠿⠿⢿⣿⣷⣶⣿⣿⣿⣿⣿⣿⣿⣵⣾⣿⡿⠿⠿⠻⠿⠿⢿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣿⣏⠉⣩⣿⣿⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⣿⣾⣿⣿⠿⣿⣿⣷⣾⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⡇⠀⢸⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⣿⣿⠟⠁⠀⠀⠀⠀⠀⠈⠻⣿⣿⡷⠀⠀⠀⠀⠀⠀

⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀By HRD ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""
        print(banner)

    def display_tiktok_banner(self):
        banner = """
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡏⠉⠉⠉⢻⢦⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠈⣷⣇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠈⠻⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠈⠉⠓⠒⣦⡀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⡷⣽⡆
⠀⠀⠀⢀⣠⠴⠒⠚⠛⠛⣦⡀⢸⡇⠀⠀⠀⢸⡻⣶⣤⣄⣀⣀⣟⢾⡇
⠀⢀⡴⠋⠀⠀⠀⠀⠀⠀⡟⢿⢸⡇⠀⠀⠀⢸⣝⡏⠙⠳⠬⢷⣌⣿⠇
⢠⠏⠀⠀⠀⠀⢀⡤⢤⡴⣟⢾⢸⡇⠀⠀⠀⢸⣌⡇⠀⠀⠀⠀⠀⠀⠀
⡞⠀⠀⠀⠀⡴⢯⣙⣦⠽⠾⠿⢸⡇⠀⠀⠀⢸⣌⡇⠀⠀⠀⠀⠀⠀⠀
⡇⠀⠀⠀⢸⡓⢤⠟⠀⠀⠀⠀⢸⡇⠀⠀⠀⢸⣌⡇⠀⠀⠀⠀⠀⠀⠀
⣇⠀⠀⠀⠈⢿⣾⠀⠀⠀⠀⢀⡾⠀⠀⠀⠀⡾⢮⡇⠀⠀⠀⠀⠀⠀⠀
⠹⡄⠀⠀⠀⠀⠙⠳⠤⠤⠖⠋⠀⠀⠀⠀⣰⡛⢦⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡼⢧⣙⡞⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠹⢶⣤⣄⣀⣀⣀⣀⣠⣤⠾⣏⠙⣦⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠙⠳⠽⣮⣻⣌⣳⣬⠷⠞⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        
           SNOM TikTok
"""
        print(banner)

    def display_instagram_banner(self):
        banner = """
 ⠀⠀⣀⣴⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣀⠀⠀⠀ 
⠀⢠⣾⣿⣿⠿⠛⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠛⠿⣿⣿⣷⡄⠀
⢰⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⢀⣤ ⣤⠈⢻⣿⣿
⣾⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⢾⣿⣿⣿⠀⢻⣿⣷
⣿⣿⡇⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠈⠙⠋⠁⠀⢸⣿⣿
⣿⣿⡇⠀⠀⠀⠀⠀⣰⣿⣿⠟⠋⠁⠀⠀⠈⠉⠻⣿⣿⣆⠀⠀⠀⠀⠀⢸⣿⣿
⣿⣿⡇⠀⠀⠀⠀⢸⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⡇⠀⠀⠀⠀⢸⣿⣿
⣿⣿⡇⠀⠀⠀⠀⢸⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⢸⣿⣿
⣿⣿⡇⠀⠀⠀⠀⢸⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⡇⠀⠀⠀⠀⢸⣿⣿
⣿⣿⡇⠀⠀⠀⠀⠀⠹⣿⣿⣦⣄⡀⠀⠀⢀⣀⣴⣿⣿⠏⠀⠀⠀⠀⠀⢸⣿⣿
⣿⣿⡇⠀⠀⠀⠀⠀⠀⠈⠻⢿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⢸⣿⣿
⢿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⡿
⠘⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⠇
⠀⠘⢿⣿⣿⣶⣤⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣤⣶⣿⣿⡿⠃⠀
⠀⠀⠀⠉⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠟⠉⠀⠀⠀
         
             SNOM Instagram
"""
        print(banner)

    def display_facebook_banner(self):
        banner = """
  ______             _                 _     
 |  ____|           | |               | |    
 | |__ __ _  ___ ___| |__   ___   ___ | | __ 
 |  __/ _` |/ __/ _ \ '_ \ / _ \ / _ \| |/ / 
 | | | (_| | (_|  __/ |_) | (_) | (_) |   <  
 |_|  \__,_|\___\___|_.__/ \___/ \___/|_|\_\ 
                                             
             SNOM Facebook
                       
"""
        print(banner)

    def display_x_banner(self):
        banner = """
              
|‾‾‾\/‾‾‾| 
 \  /   /  
  \/˙  /   
  //  /\   
 /   /  \  
|„  /\„  | 
 ‾‾‾  ‾‾‾  
SNOM X
"""
        print(banner)

    def display_telegram_banner(self):
        banner = """
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣾⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣶⣿⣿⡿⠿⠛⢙⣿⣿⠃ 
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣶⣾⣿⣿⠿⠛⠋⠁⠀⠀⠀⣸⣿⣿⠀
⠀⠀⠀⠀⣀⣤⣴⣾⣿⣿⡿⠟⠛⠉⠀⠀⣠⣤⠞⠁⠀⠀⣿⣿⡇⠀
⠀⣴⣾⣿⣿⡿⠿⠛⠉⠀⠀⠀⢀⣠⣶⣿⠟⠁⠀⠀⠀⢸⣿⣿⠀⠀
⠸⣿⣿⣿⣧⣄⣀⠀⠀⣀⣴⣾⣿⣿⠟⠁⠀⠀⠀⠀⠀⣼⣿⡿⠀⠀
⠀⠈⠙⠻⠿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⢠⣿⣿⠇⠀⠀
⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⡇⠀⣀⣄⡀⠀⠀⠀⠀⢸⣿⣿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣠⣾⣿⣿⣿⣦⡀⠀⠀⣿⣿⡏⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⡿⠋⠈⠻⣿⣿⣦⣸⣿⣿⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠁⠀⠀⠀⠀⠈⠻⣿⣿⣿⠏⠀⠀⠀⠀
       SNOM Telegram
        """
        print(banner)

    def display_snapchat_banner(self):
        banner = """
 ⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣶⣶⣶⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣀⡀⠀⠀⠀
⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠈⠙⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠋⠁⠀⠀⠀
⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⠀⠀⠀
⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄
⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃
⠀⠀⠉⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⠉⠀⠀
⠀⠀⠀⠀⠈⠛⠛⠋⠙⠿⣿⣿⣿⣿⣿⣿⠿⠋⠙⠛⠛⠁⠀⠀⠀⠀
                  
                    SNOM  Snapchat                                   
        
"""
        print(banner)

    def check_facebook_username(self, username):
        url = f"https://www.facebook.com/{username}"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                error_messages = [
                    "This page isn't available", "الصفحة غير متاحة", "Page Not Found",
                    "Content Not Found", "Sorry, this content isn't available",
                    "عذراً، هذا المحتوى غير متاح", "لم يتم العثور على", "غير موجود",
                    "doesn't exist", "existiert nicht", "n'existe pas", "not found", ""
                ]
                
                page_text = soup.get_text()
                
                for error_msg in error_messages:
                    if error_msg.lower() in page_text.lower():
                        return False
                
                return True
                
            elif response.status_code == 404:
                return False
            else:
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"{self.colors['error']}حدث خطأ في الاتصال: {e}{self.colors['reset']}")
            return None

    def check_twitter_username(self, username):
        """تحسين وظيفة التحقق من اسم المستخدم في تويتر"""
        url = f"https://twitter.com/{username}"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'ar,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0'
            }
            
            response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
            
            # إذا كان هناك تحويل، قد يعني أن الحساب غير موجود أو محذوف
            if response.history and len(response.history) > 0:
                final_url = response.url
                if "account/suspended" in final_url:
                    return "موقوف"
                elif "search" in final_url or "login" in final_url:
                    return False
                elif "i/flow/signup" in final_url:
                    return False
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # البحث عن علامات تشير إلى أن الحساب غير موجود
                error_indicators = [
                    "هذا الحساب غير موجود", "This account doesn't exist", 
                    "لم يتم العثور", "not found", "غير موجود", "exist",
                    "Esta cuenta no existe", "n'existe pas", "existiert nicht",
                    "Account suspended", "الحساب موقوف", "تعذر العثور"
                ]
                
                page_text = soup.get_text()
                
                # التحقق من وجود أي من رسائل الخطأ
                for error_msg in error_indicators:
                    if error_msg.lower() in page_text.lower():
                        return False
                
                # البحث عن علامات تشير إلى وجود حساب حقيقي
                profile_indicators = [
                    "data-testid=\"UserName\"", "data-testid=\"UserDescription\"",
                    "data-testid=\"UserProfileHeader_Items\"", "data-testid=\"primaryColumn\"",
                    "data-testid=\"UserCell\"", "following", "followers"
                ]
                
                # إذا وجدنا أي من علامات الملف الشخصي، نعتبر الحساب موجوداً
                html_content = response.text
                for indicator in profile_indicators:
                    if indicator in html_content:
                        return True
                
                # طريقة إضافية: البحث عن بيانات وصفية خاصة بتويتر
                meta_tags = soup.find_all('meta')
                for tag in meta_tags:
                    if 'name' in tag.attrs and 'content' in tag.attrs:
                        if 'twitter:app:url' in tag.get('name', '') or 'twitter:creator' in tag.get('name', ''):
                            return True
                
                # إذا لم نجد أي دليل على وجود الحساب، نعتبره غير موجود
                return False
                
            elif response.status_code in [404, 403, 400]:
                return False
            else:
                # في حالة وجود أخطاء أخرى، نعيد None للإشارة إلى عدم القدرة على التحقق
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"{self.colors['error']}حدث خطأ في الاتصال: {e}{self.colors['reset']}")
            return None

    def run_facebook_checker(self):
        self.display_facebook_banner()
        
        while True:
            username = input(f"\n{self.colors['label']}أدخل اسم المستخدم في الفيسبوك (أو اكتب 'خروج' للإنهاء): {self.colors['reset']}").strip()
            
            if username.lower() in ['خروج', 'exit', 'quit']:
                print("شكراً لاستخدامك الأداة. إلى اللقاء!")
                break
                
            if not username:
                print(f"{self.colors['error']}يرجى إدخال اسم مستخدم صحيح.{self.colors['reset']}")
                continue
                
            print(f"{self.colors['label']}جاري التحقق من '{username}'...{self.colors['reset']}")
            result = self.check_facebook_username(username)
            
            if result is True:
                print(f"{self.colors['data']}اسم المستخدم '{username}' موجود في الفيسبوك{self.colors['reset']}")
            elif result is False:
                print(f"{self.colors['error']}اسم المستخدم '{username}' غير موجود في الفيسبوك{self.colors['reset']}")
            else:
                print(f"{self.colors['error']}تعذر التحقق من وجود اسم المستخدم بسبب مشكلة في الاتصال{self.colors['reset']}")
            
            while True:
                again = input(f"\n{self.colors['label']}هل تريد التحقق من اسم مستخدم آخر؟ (نعم/لا): {self.colors['reset']}").strip().lower()
                if again in ['نعم', 'yes', 'y', 'ن']:
                    break
                elif again in ['لا', 'no', 'n', 'ل']:
                    print("شكراً لاستخدامك الأداة. توكل!")
                    return
                else:
                    print(f"{self.colors['error']}يرجى الإجابة بنعم أو لا{self.colors['reset']}")

    def run_x_checker(self):
        self.display_x_banner()
        
        while True:
            username = input(f"\n{self.colors['label']}أدخل اسم المستخدم في X (تويتر) (أو اكتب 'خروج' للإنهاء): {self.colors['reset']}").strip()
            
            if username.lower() in ['خروج', 'exit', 'quit']:
                print("شكراً لاستخدامك الأداة. إلى اللقاء!")
                break
                
            if not username:
                print(f"{self.colors['error']}يرجى إدخال اسم مستخدم صحيح.{self.colors['reset']}")
                continue
                
            print(f"{self.colors['label']}جاري التحقق من '{username}'...{self.colors['reset']}")
            result = self.check_twitter_username(username)
            
            if result is True:
                print(f"{self.colors['data']}✓ اسم المستخدم '{username}' موجود في X (تويتر){self.colors['reset']}")
            elif result is False:
                print(f"{self.colors['error']}✗ اسم المستخدم '{username}' غير موجود في X (تويتر){self.colors['reset']}")
            elif result == "موقوف":
                print(f"{self.colors['error']}✗ اسم المستخدم '{username}' موقوف في X (تويتر){self.colors['reset']}")
            else:
                print(f"{self.colors['error']}? تعذر التحقق من وجود اسم المستخدم بسبب مشكلة في الاتصال{self.colors['reset']}")
            
            while True:
                again = input(f"\n{self.colors['label']}هل تريد التحقق من اسم مستخدم آخر؟ (نعم/لا): {self.colors['reset']}").strip().lower()
                if again in ['نعم', 'yes', 'y', 'ن']:
                    break
                elif again in ['لا', 'no', 'n', 'ل']:
                    print("شكراً لاستخدامك الأداة. توكل!")
                    return
                else:
                    print(f"{self.colors['error']}يرجى الإجابة بنعم أو لا{self.colors['reset']}")

    def get_tiktok_user_info(self):
        """استخراج معلومات مستخدم تيك توك"""
        self.display_tiktok_banner()
        
        while True:
            identifier = input(f"\n{self.colors['label']}أدخل اسم المستخدم في TikTok (أو اكتب 'خروج' للإنهاء): {self.colors['reset']}").strip()
            
            if identifier.lower() in ['خروج', 'exit', 'quit']:
                print("شكراً لاستخدامك الأداة. إلى اللقاء!")
                break
                
            if not identifier:
                print(f"{self.colors['error']}يرجى إدخال اسم مستخدم صحيح.{self.colors['reset']}")
                continue
                
            url = f"https://www.tiktok.com/@{identifier}"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                html_content = response.text
                
                try:
                    soup = BeautifulSoup(html_content, 'lxml')
                except:
                    soup = BeautifulSoup(html_content, 'html.parser')
                
                patterns = {
                    'user_id': r'"webapp.user-detail":{"userInfo":{"user":{"id":"(\d+)"',
                    'unique_id': r'"uniqueId":"(.*?)"',
                    'nickname': r'"nickname":"(.*?)"',
                    'followers': r'"followerCount":(\d+)',
                    'following': r'"followingCount":(\d+)',
                    'likes': r'"heartCount":(\d+)',
                    'videos': r'"videoCount":(\d+)',
                    'signature': r'"signature":"(.*?)"',
                    'verified': r'"verified":(true|false)',
                    'secUid': r'"secUid":"(.*?)"',
                    'commentSetting': r'"commentSetting":(\d+)',
                    'privateAccount': r'"privateAccount":(true|false)',
                    'region': r'"ttSeller":false,"region":"([^"]*)"',
                    'heart': r'"heart":(\d+)',
                    'diggCount': r'"diggCount":(\d+)',
                    'friendCount': r'"friendCount":(\d+)',
                    'profile_pic': r'"avatarLarger":"(.*?)"'
                }
                
                info = {}
                for key, pattern in patterns.items():
                    match = re.search(pattern, html_content)
                    info[key] = match.group(1) if match else f"لم يتم العثور على {key}"
                
                if "profile_pic" in info:
                    info['profile_pic'] = info['profile_pic'].replace('\\u002F', '/')
                
                social_links = []
                bio = info.get('signature', "")
                
                link_urls = re.findall(r'href="(https://www\.tiktok\.com/link/v2\?[^"]*?scene=bio_url[^"]*?target=([^"&]+))"', html_content)
                for full_url, target in link_urls:
                    target_decoded = urllib.parse.unquote(target)
                    text_pattern = rf'href="{re.escape(full_url)}"[^>]*>.*?<span[^>]*SpanLink[^>]*>([^<]+)</span>'
                    text_match = re.search(text_pattern, html_content, re.DOTALL)
                    if text_match:
                        link_text = text_match.group(1)
                    else:
                        link_text = target_decoded
                        
                    if not any(target_decoded in s for s in social_links):
                        social_links.append(f"رابط: {link_text} - {target_decoded}")
                    
                span_links = re.findall(r'<span[^>]*class="[^"]*SpanLink[^"]*">([^<]+)</span>', html_content)
                for span_text in span_links:
                    if '.' in span_text and ' ' not in span_text and not any(span_text in s for s in social_links):
                        social_links.append(f"رابط: {span_text} - {span_text}")
                
                all_targets = re.findall(r'scene=bio_url[^"]*?target=([^"&]+)', html_content)
                for target in all_targets:
                    target_decoded = urllib.parse.unquote(target)
                    if not any(target_decoded in s for s in social_links):
                        text_pattern = rf'target={re.escape(target)}[^>]*>.*?<span[^>]*>([^<]+)</span>'
                        text_match = re.search(text_pattern, html_content, re.DOTALL)
                        if text_match:
                            link_text = text_match.group(1)
                        else:
                            link_text = target_decoded
                        
                        social_links.append(f"رابط: {link_text} - {target_decoded}")
                
                bio_link_pattern = r'"bioLink":{"link":"([^"]+)","risk":(\d+)}'
                bio_links_matches = re.findall(bio_link_pattern, html_content)

                for link, risk in bio_links_matches:
                    clean_link = link.replace('\\u002F', '/')
                    if not any(clean_link in s for s in social_links):
                        social_links.append(f"{clean_link}")

                shared_links_pattern = r'"shareUrl":"([^"]+)"'
                shared_links_matches = re.findall(shared_links_pattern, html_content)

                for shared_url in shared_links_matches:
                    clean_url = shared_url.replace('\\u002F', '/')
                    if not any(clean_url in s for s in social_links):
                        social_links.append(f"{clean_url}")

                share_links_div_pattern = re.compile(r'<div[^>]*class="[^"]*DivShareLinks[^"]*"[^>]*>(.*?)</div>', re.DOTALL)
                for div_match in share_links_div_pattern.finditer(html_content):
                    div_content = div_match.group(1)
                    
                    div_links = re.finditer(r'<a[^>]*href="[^"]*scene=bio_url[^"]*target=([^"&]+)"[^>]*>.*?<span[^>]*class="[^"]*SpanLink["]*">([^<]+)</span>', div_content, re.DOTALL)
                    
                    for link_match in div_links:
                        target = urllib.parse.unquote(link_match.group(1))
                        link_text = link_match.group(2)
                        
                        if not any(target in s or link_text in s for s in social_links):
                            social_links.append(f"{link_text} {target}")
                
                span_matches = re.findall(r'<span[^>]*class="[^"]*SpanLink[^"]*">([^<]+)</span>', html_content)
                for span_text in span_matches:
                    if '.' in span_text and not any(span_text in s for s in social_links):
                        social_links.append(f"رابط: {span_text} - {span_text}")
                
                biolink_matches = re.findall(r'class="[^"]*ABioLink[^"]*"[^>]*>.*?<span[^>]*class="[^"]*SpanLink[^"]*">([^<]+)</span>', html_content, re.DOTALL)
                for span_text in biolink_matches:
                    if not any(span_text in s for s in social_links):
                        social_links.append(f"رابط: {span_text} - {span_text}")
                
                ig_pattern = re.search(r'[iI][gG]:\s*@?([a-zA-Z0-9._]+)', bio)
                if ig_pattern:
                    instagram_username = ig_pattern.group(1)
                    if not any(f"إنستغرام: @{instagram_username}" in s for s in social_links):
                        social_links.append(f"إنستغرام: @{instagram_username}")
                
                social_patterns = {
                    'snapchat': r'([sS][cC]|[sS]napchat):\s*@?([a-zA-Z0-9._]+)',
                    'twitter': r'([tT]witter|[xX]):\s*@?([a-zA-Z0-9._]+)',
                    'facebook': r'[fF][bB]:\s*@?([a-zA-Z0-9._]+)',
                    'youtube': r'([yY][tT]|[yY]outube):\s*@?([a-zA-Z0-9._]+)',
                    'telegram': r'[t]elegram:\s*@?([a-zA-Z0-9._]+)'
                }
                
                for platform, pattern in social_patterns.items():
                    match = re.search(pattern, bio)
                    if match:
                        username = match.group(2) if len(match.groups()) > 1 else match.group(1)
                        if platform == 'snapchat':
                            social_link = f"سناب شات: {username}"
                        elif platform == 'twitter':
                            social_link = f"تويتر/إكس: @{username}"
                        elif platform == 'facebook':
                            social_link = f"فيسبوك: {username}"
                        elif platform == 'youtube':
                            social_link = f"يوتيوب: {username}"
                        elif platform == 'telegram':
                            social_link = f"تيليجرام: @{username}"
                        
                        if not any(social_link in s for s in social_links):
                            social_links.append(social_link)
                
                email_pattern = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', bio)
                if email_pattern:
                    email = email_pattern.group(0)
                    if not any(email in s for s in social_links):
                        social_links.append(f"بريد إلكتروني: {email}")
                
                info['social_links'] = social_links

                print("\n" + "="*50)
                print("معلومات المستخدم")
                print("="*50)
                print(f"معرف المستخدم: {info['user_id']}")
                print(f"اسم المستخدم: {info['unique_id']}")
                print(f"الاسم المستعار: {info['nickname']}")
                print(f"حساب موثوق: {info['verified']}")
                print(f"حساب خاص: {info['privateAccount']}")
                print(f"المنطقة: {info['region']}")
                print(f"المتابعون: {info['followers']}")
                print(f"المتابَعون: {info['following']}")
                print(f"الإعجابات: {info['likes']}")
                print(f"الفيديوهات: {info['videos']}")
                print(f"الأصدقاء: {info['friendCount']}")
                print(f"القلوب: {info['heart']}")
                print(f"عدد التقييمات: {info['diggCount']}")
                print(f"معرف الأمان: {info['secUid']}")
                
                print("\n" + "="*50)
                print("السيرة الذاتية")
                print("="*50)
                print(info['signature'].replace('\\n', '\n'))
                
                if social_links:
                    print("\n" + "="*50)
                    print("الروابط الاجتماعية")
                    print("="*50)
                    for link in social_links:
                        print(f"{link}")
                else:
                    print("\nلم يتم العثور على روابط اجتماعية.")
                
                print(f"\nرابط الملف الشخصي: https://www.tiktok.com/@{info['unique_id']}")

                if "profile_pic" in info and info["profile_pic"].startswith("http"):
                    print(f"\nرابط صورة الملف الشخصي: {info['profile_pic']}")
                
                return info
            else:
                print(f"\nخطأ: تعذر جلب الملف الشخصي. رمز الحالة: {response.status_code}")
                print("قد يكون الحساب خاصاً أو غير موجود")
                return None

    def get_instagram_profile_info(self, username):
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            return profile
        except Exception as e:
            print(f"{self.colors['error']}خطأ: {str(e)}{self.colors['reset']}")
            return None

    def format_number(self, num):
        if num is None:
            return "غير متاح"
        return f"{num:,}"

    def format_bool(self, value):
        return "نعم" if value else "لا"

    def format_date(self, date):
        if not date:
            return "غير متاح"
        return date.strftime("%Y-%m-%d %H:%M:%S")

    def detect_language(self, text):
        if not text:
            return "غير معروف"
        arabic_chars = set('ءآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوىي')
        if any(char in arabic_chars for char in text):
            return "العربية"
        return "الإنجليزية (تقديري)"

    def extract_mentions(self, text):
        if not text:
            return []
        return [word[1:] for word in text.split() if word.startswith('@')]

    def analyze_instagram_profile(self, profile):
        print(f"{self.colors['label']}اسم المستخدم:{self.colors['data']} {profile.username}")
        print(f"{self.colors['label']}الاسم الكامل:{self.colors['data']} {profile.full_name or 'غير متاح'}")
        print(f"{self.colors['label']}الرقم التعريفي:{self.colors['data']} {profile.userid}")
        print(f"{self.colors['label']}حساب موثّق:{self.colors['data']} {self.format_bool(profile.is_verified)}")
        print(f"{self.colors['label']}حساب خاص:{self.colors['data']} {self.format_bool(profile.is_private)}")
        print(f"{self.colors['label']}حساب محظور:{self.colors['data']} {self.format_bool(getattr(profile, 'is_blocked', False))}")
        print(f"{self.colors['label']}الحساب نشط:{self.colors['data']} {'نعم' if profile.mediacount > 0 else 'لا'}")

        print(f"{self.colors['label']}حساب تجاري:{self.colors['data']} {self.format_bool(profile.is_business_account)}")
        if profile.is_business_account:
            print(f"{self.colors['label']}فئة العمل:{self.colors['data']} {profile.business_category_name or 'غير متاح'}")
            print(f"{self.colors['label']}البلد:{self.colors['data']} {getattr(profile, 'business_location', 'غير متاح')}")
            print(f"{self.colors['label']}البريد الإلكتروني للعمل:{self.colors['data']} {getattr(profile, 'business_email', 'غير متاح')}")
            print(f"{self.colors['label']}رقم الهاتف للعمل:{self.colors['data']} {getattr(profile, 'business_phone', 'غير متاح')}")

        print(f"{self.colors['label']}رابط الصورة:{self.colors['data']} {profile.profile_pic_url}")
        print(f"{self.colors['label']}السيرة الذاتية:{self.colors['data']} {profile.biography or 'غير متاح'}")
        print(f"{self.colors['label']}لغة السيرة الذاتية:{self.colors['data']} {self.detect_language(profile.biography)}")
        
        mentions = self.extract_mentions(profile.biography)
        print(f"{self.colors['label']}العلامات المذكورة:{self.colors['data']} {', '.join(mentions) if mentions else 'غير متاح'}")
        
        print(f"{self.colors['label']}الرابط الخارجي:{self.colors['data']} {profile.external_url or 'غير متاح'}")

        print(f"{self.colors['label']}حساب Threads مرتبط:{self.colors['data']} {self.format_bool(getattr(profile, 'has_threads', False))}")

        print(f"{self.colors['label']}عدد المتابعين:{self.colors['data']} {self.format_number(profile.followers)}")
        print(f"{self.colors['label']}عدد المتابعات:{self.colors['data']} {self.format_number(profile.followees)}")
        print(f"{self.colors['label']}عدد المنشورات:{self.colors['data']} {self.format_number(profile.mediacount)}")
        print(f"{self.colors['label']}عدد مقاطع IGTV:{self.colors['data']} {self.format_number(profile.igtvcount)}")
        print(f"{self.colors['label']}عدد الهايلايتس:{self.colors['data']} {self.format_number(getattr(profile, 'highlight_reel_count', None))}")
        print(f"{self.colors['label']}عدد العلامات:{self.colors['data']} {self.format_number(getattr(profile, 'tagged_count', None))}")
        
        avg_engagement = round((profile.followers / profile.mediacount) * 100 if profile.mediacount > 0 else 0, 2)
        print(f"{self.colors['label']}متوسط التفاعل:{self.colors['data']} {avg_engagement}%")
        print(f"{self.colors['label']}آخر نشاط:{self.colors['data']} {'نشط' if profile.mediacount > 0 and profile.followers > 0 else 'غير نشط'}")

    def run_instagram_analyzer(self):
        while True:
            username = input(f"{self.colors['label']}أدخل اسم المستخدم (أو اكتب 'خروج' للإنهاء): {self.colors['reset']}").strip()
            
            if username.lower() in ['خروج', 'exit', 'quit']:
                print("شكراً لاستخدامك الأداة. إلى اللقاء!")
                break
                
            if not username:
                print(f"{self.colors['error']}يجب إدخال اسم مستخدم!{self.colors['reset']}")
                continue
                
            profile = self.get_instagram_profile_info(username)
            
            if profile:
                self.analyze_instagram_profile(profile)
            
            choice = input(f"{self.colors['label']}هل تريد تحليل حساب آخر؟ (نعم/لا): {self.colors['reset']}").strip().lower()
            if choice not in ['نعم', 'yes', 'y', '']:
                print("شكراً لاستخدامك للأداة. انقلع!")
                break

    # Telegram Functions
    def extract_telegram_public_info(self, username):
        username = username.replace('@', '').strip()
        
        try:
            url = f"https://t.me/{username}"
            response = self.session.get(url, timeout=15)
            
            if response.status_code != 200:
                return {"error": "لم يتم العثور على الحساب"}
            
            return self.parse_telegram_html(response.text, username)
            
        except Exception as e:
            return {"error": f"خطأ في الاتصال: {str(e)}"}
    
    def parse_telegram_html(self, html, username):
        soup = BeautifulSoup(html, 'html.parser')
        info = {}
        
        info['اسم المستخدم'] = f"@{username}"
        info['رابط الحساب'] = f"https://t.me/{username}"
        
        title_tag = soup.find('meta', property='og:title')
        if title_tag:
            info['الاسم'] = title_tag.get('content', '')
        
        description_tag = soup.find('meta', property='og:description')
        if description_tag:
            description = description_tag.get('content', '')
            info['السيرة الذاتية'] = description
        
        image_tag = soup.find('meta', property='og:image')
        if image_tag:
            info['رابط الصورة'] = image_tag.get('content', '')
        
        extra_div = soup.find('div', class_=re.compile('tgme_page_extra'))
        if extra_div:
            extra_text = extra_div.get_text(strip=True)
            info['معلومات إضافية'] = extra_text
        
        info['الدولة'] = self.detect_country(info)
        
        verified = soup.find('i', class_=re.compile('verified', re.IGNORECASE))
        info['الحساب الموثق'] = "نعم" if verified else "لا"
        
        info['الحساب الرسمي'] = self.check_official_account(info)
        info['هل لديه منشورات'] = self.check_posts(soup)
        info['نوع الحساب'] = self.detect_account_type(info)
        info['اللغة المستخدمة'] = self.detect_language(info)
        info['البريد الإلكتروني'] = self.extract_emails(info)
        info['الروابط الاجتماعية'] = self.extract_social_links(info)
        info['أرقام الهاتف'] = self.extract_phone_numbers(info)
        
        return info
    
    def extract_phone_numbers(self, info):
        all_text = ""
        for key in ['الاسم', 'السيرة الذاتية', 'معلومات إضافية']:
            if key in info and info[key]:
                all_text += str(info[key]) + " "
        
        patterns = [
            r'\+\d{1,3}[\s-]?\d{1,4}[\s-]?\d{1,4}[\s-]?\d{1,4}',
            r'\d{3}[\s-]?\d{3}[\s-]?\d{4}',
            r'\(\d{3}\)[\s-]?\d{3}[\s-]?\d{4}',
        ]
        
        found_numbers = []
        for pattern in patterns:
            numbers = re.findall(pattern, all_text)
            found_numbers.extend(numbers)
        
        return found_numbers if found_numbers else None
    
    def extract_emails(self, info):
        all_text = ""
        for key in ['الاسم', 'السيرة الذاتية', 'معلومات إضافية']:
            if key in info and info[key]:
                all_text += str(info[key]) + " "
        
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', all_text)
        return emails if emails else None
    
    def extract_social_links(self, info):
        all_text = ""
        for key in ['الاسم', 'السيرة الذاتية', 'معلومات إضافية']:
            if key in info and info[key]:
                all_text += str(info[key]) + " "
        
        social_platforms = ['instagram', 'twitter', 'facebook', 'youtube', 'tiktok', 'linkedin']
        found_links = []
        
        for platform in social_platforms:
            if platform in all_text.lower():
                found_links.append(platform)
        
        return found_links if found_links else None
    
    def detect_country(self, info):
        all_text = ""
        for key in ['الاسم', 'السيرة الذاتية', 'معلومات إضافية']:
            if key in info and info[key]:
                all_text += str(info[key]) + " "
        
        found_countries = []
        for country, keywords in self.countries_list.items():
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, all_text, re.IGNORECASE):
                    if country not in found_countries:
                        found_countries.append(country)
                    break
        
        return " ".join(found_countries) if found_countries else "غير معروف"
    
    def check_official_account(self, info):
        official_keywords = ['رسمي', 'official', 'الرسمي', 'مؤسسة', 'شركة']
        all_text = ""
        for key in ['الاسم', 'السيرة الذاتية', 'معلومات إضافية']:
            if key in info and info[key]:
                all_text += str(info[key]) + " "
        
        return "نعم" if any(keyword in all_text.lower() for keyword in official_keywords) else "لا"
    
    def check_posts(self, soup):
        return "نعم" if soup.find('div', class_=re.compile('post', re.IGNORECASE)) else "لا"
    
    def detect_account_type(self, info):
        all_text = ""
        for key in ['الاسم', 'السيرة الذاتية', 'معلومات إضافية']:
            if key in info and info[key]:
                all_text += str(info[key]) + " "
        
        business_keywords = ['تاجر', 'متجر', 'بيع', 'شراء', 'خدمات', 'business', 'تجاري']
        
        return "حساب تجاري" if any(keyword in all_text.lower() for keyword in business_keywords) else "حساب شخصي"
    
    def display_telegram_results(self, info):
        print("\n" + "=" * 50)
        print("نتائج تحليل Telegram")
        print("=" * 50)
        
        if 'error' in info:
            print(info['error'])
            return
        
        for key, value in info.items():
            if value:
                if isinstance(value, list):
                    if value:
                        print(f"{key}: {', '.join(map(str, value))}")
                else:
                    print(f"{key}: {value}")

    def run_telegram_analyzer(self):
        self.display_telegram_banner()
        
        while True:
            username = input(f"\n{self.colors['label']}أدخل اسم المستخدم في Telegram (أو اكتب 'خروج' للإنهاء): {self.colors['reset']}").strip()
            
            if username.lower() in ['خروج', 'exit', 'quit']:
                print("شكراً لاستخدامك الأداة. إلى اللقاء!")
                break
                
            if not username:
                print(f"{self.colors['error']}يرجى إدخال اسم مستخدم صحيح.{self.colors['reset']}")
                continue
                
            print(f"{self.colors['label']}جاري تحليل '{username}'...{self.colors['reset']}")
            result = self.extract_telegram_public_info(username)
            
            self.display_telegram_results(result)
            
            while True:
                again = input(f"\n{self.colors['label']}هل تريد تحليل حساب آخر؟ (نعم/لا): {self.colors['reset']}").strip().lower()
                if again in ['نعم', 'yes', 'y', 'ن']:
                    break
                elif again in ['لا', 'no', 'n', 'ل']:
                    print("شكراً لاستخدامك الأداة. توكل!")
                    return
                else:
                    print(f"{self.colors['error']}يرجى الإجابة بنعم أو لا{self.colors['reset']}")

    # Snapchat Functions
    class SnapchatInfoExtractor:
        def __init__(self):
            self.base_url = "https://www.snapchat.com/add/"
            self.graphql_url = "https://story.share.snapchat.com/graphql"
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'ar,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
            }
            
        def display_logo(self):
            logo = """
 ⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣶⣶⣶⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣀⡀⠀⠀⠀
⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠈⠙⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠋⠁⠀⠀⠀
⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⠀⠀⠀
⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄
⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃
⠀⠀⠉⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⠉⠀⠀
⠀⠀⠀⠀⠈⠛⠛⠋⠙⠿⣿⣿⣿⣿⣿⣿⠿⠋⠙⠛⠛⠁⠀⠀⠀⠀
                     
                    SNOM Snapchat
       
"""
            print(logo)
            print("أداة استخراج معلومات حسابات سناب شات - النسخة الزنجية")
            print("=" * 60)
        
        def get_username(self):
            """طلب اسم المستخدم من المستخدم"""
            print("\nمرحبًا بك في أداة استخراج معلومات سناب شات!")
            print("=" * 50)
            username = input("يرجى إدخال اسم المستخدم الذي تريد استخراج معلوماته: ").strip().replace('@', '')
            
            if not username:
                print("لم تدخل أي اسم مستخدم. يرجى المحاولة مرة أخرى.")
                return self.get_username()
                
            return username
        
        def fetch_snapchat_data(self, username):
            """جلب بيانات سناب شات باستخدام طرق متعددة"""
            url = f"{self.base_url}{username}"
            
            try:
                print(f"جاري البحث عن معلومات الحساب: {username}")
                

                response = requests.get(url, headers=self.headers, timeout=15)
                
                if response.status_code != 200:
                    return {"error": f"لم يتم العثور على الحساب أو خطأ في الاتصال (رمز الحالة: {response.status_code})"}
                
                soup = BeautifulSoup(response.text, 'html.parser')
                

                script_tags = soup.find_all('script')
                user_data = None
                
                for script in script_tags:
                    if script.string and 'window.__PRELOADED_STATE__' in script.string:
                        json_str = script.string.split('window.__PRELOADED_STATE__ = ')[1].split(';</script>')[0]
                        user_data = json.loads(json_str)
                        break
                

                if not user_data:
                    for script in script_tags:
                        if script.get('type') == 'application/json' or 'preloaded' in str(script).lower():
                            try:
                                user_data = json.loads(script.string)
                                break
                            except:
                                continue
                
            
                if not user_data:
                    return self.extract_info_with_regex(response.text, username)
                
                return self.parse_user_data(user_data, username, url)
                
            except requests.exceptions.RequestException as e:
                return {"error": f"خطأ في الاتصال: {str(e)}"}
            except Exception as e:
                return {"error": f"حدث خطأ غير متوقع: {str(e)}"}
        
        def extract_info_with_regex(self, html, username):
            """"""
            print("استخدام طريقة بديلة لاستخراج المعلومات...")
            
            # البحث عن الاسم
            name_match = re.search(r'<title[^>]*>([^<]+)</title>', html)
            name = name_match.group(1).replace('| Snapchat', '').strip() if name_match else username
            
            # البحث عن البايو
            bio_match = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', html)
            bio = bio_match.group(1) if bio_match else "غير متوفر"
            
            # البحث عن إذا كان الحساب موثق
            verified = "نعم" if "verified" in html.lower() or "موثق" in html else "لا"
            
            # تحديد إذا كان الحساب نشط
            active = "نعم" if not re.search(r'(غير متوفر|غير موجود|not available|account not found)', html, re.IGNORECASE) else "لا"
            
            # البحث عن الروابط الخارجية
            links = re.findall(r'https?://[^\s"<>]+', html)
            external_links = [link for link in links if 'snapchat.com' not in link][:5] or "غير متوفر"
            
            return {
                "اسم المستخدم": username,
                "رابط الحساب": f"https://www.snapchat.com/add/{username}",
                "الاسم": name,
                "السيرة الذاتية": bio,
                "عدد المتابعين": "غير متوفر (معلومة خاصة)",
                "عدد المنشورات": "غير متوفر (معلومة خاصة)",
                "الحساب موثق": verified,
                "نوع الحساب": "شخصي ()",
                "الحساب نشط": active,
                "الحساب محظور": "لا ()",
                "الروابط الخارجية": external_links
            }
        
        def parse_user_data(self, user_data, username, url):
            """تحليل بيانات المستخدم المستخرجة"""
            try:


                user_info = {}
                
                # البحث المتكرر في JSON للعثور على معلومات المستخدم
                def find_user_info(obj, path=[]):
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            new_path = path + [key]
                            if key in ['displayName', 'name', 'title', 'username'] and value:
                                user_info['الاسم'] = value
                            elif key in ['bio', 'description', 'subtitle'] and value:
                                user_info['السيرة الذاتية'] = value
                            elif key in ['isVerified', 'verified']:
                                user_info['الحساب موثق'] = "نعم" if value else "لا"
                            elif key in ['snapchatScore', 'score'] and value:
                                user_info['عدد المنشورات'] = value
                            elif key in ['externalUrl', 'website'] and value:
                                if 'الروابط الخارجية' not in user_info:
                                    user_info['الروابط الخارجية'] = []
                                user_info['الروابط الخارجية'].append(value)
                            
                            find_user_info(value, new_path)
                    elif isinstance(obj, list):
                        for item in obj:
                            find_user_info(item, path)
                
                find_user_info(user_data)
                
                # تعيين القيم إذا لم يتم العثور على المعلومات
                result = {
                    "اسم المستخدم": username,
                    "رابط الحساب": url,
                    "الاسم": user_info.get('الاسم', username),
                    "السيرة الذاتية": user_info.get('السيرة الذاتية', "غير متوفر"),
                    "عدد المتابعين": user_info.get('عدد المتابعين', "غير متوفر (معلومة خاصة)"),
                    "عدد المنشورات": user_info.get('عدد المنشورات', "غير متوفر (معلومة خاصة)"),
                    "الحساب موثق": user_info.get('الحساب موثق', "لا"),
                    "نوع الحساب": "شخصي ()",
                    "الحساب نشط": "نعم ()",
                    "الحساب محظور": "لا ()",
                    "الروابط الخارجية": user_info.get('الروابط الخارجية', "غير متوفر")
                }
                
                return result
                
            except Exception as e:
                return self.extract_info_with_regex(str(user_data), username)
        
        def display_info(self, info):
            """عرض المعلومات المستخرجة"""
            print("\n" + "=" * 60)
            
            if "error" in info:
                print(f"خطأ: {info['error']}")
                print("=" * 60)
                return
            
            print("تم استخراج المعلومات بنجاح!")
            print("=" * 60)
            
            for key, value in info.items():
                if key == "الروابط الخارجية" and value != "غير متوفر" and isinstance(value, list):
                    print(f"{key}:")
                    for i, link in enumerate(value, 1):
                        print(f"  {i}. {link}")
                else:
                    print(f"{key}: {value}")
            
            print("=" * 60)
        
        def ask_for_another(self):
            """السؤال إذا كان المستخدم يريد استخراج معلومات حساب آخر"""
            choice = input("\nهل تريد استخراج معلومات حساب آخر؟ (نعم/لا): ").strip().lower()
            return choice in ['نعم', 'yes', 'y', 'ن', 'y']

    def run_snapchat_analyzer(self):
        self.display_snapchat_banner()
        extractor = self.SnapchatInfoExtractor()
        
        while True:
            username = extractor.get_username()
            info = extractor.fetch_snapchat_data(username)
            extractor.display_info(info)
            
            if not extractor.ask_for_another():
                print("\nشكرًا لاستخدامك أداة!")
                break
            
            print("\n" + "=" * 50)

    def run(self):
        self.display_old_banner()
        
        while True:
            print("\n" + "="*50)
            print("اختر نوع البرنامج:")
            print("="*50)
            print("1 إنستغرام")
            print("2 تيك توك")
            print("3 فيسبوك")
            print("4 X (تويتر)")
            print("5 تيليجرام")
            print("6 سناب شات")
            print("0 خروج")
            print("="*50)
            
            choice = input("أدخل رقم الاختيار: ").strip()
            
            if choice == '0':
                print("شكراً لاستخدامك الأداة. إلى اللقاء!")
                break
            elif choice == '1':
                self.display_instagram_banner()
                self.run_instagram_analyzer()
            elif choice == '2':
                self.display_tiktok_banner()
                self.get_tiktok_user_info()
                
                choice = input(f"\n{self.colors['label']}هل تريد تحليل حساب آخر؟ (نعم/لا): {self.colors['reset']}").strip().lower()
                if choice not in ['نعم', 'yes', 'y', '']:
                    print("شكراً لاستخدامك للأداة. انقلع!")
                    break
            elif choice == '3':
                self.run_facebook_checker()
            elif choice == '4':
                self.run_x_checker()
            elif choice == '5':
                self.run_telegram_analyzer()
            elif choice == '6':
                self.run_snapchat_analyzer()
            else:
                print("اختيار غير صحيح! يرجى المحاولة مرة أخرى.")

if __name__ == "__main__":
    analyzer = SocialMediaAnalyzer()
    analyzer.run()