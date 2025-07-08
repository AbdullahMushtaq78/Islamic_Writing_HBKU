import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from Configs.configs import *
from agents import function_tool
import requests





@function_tool

def fetch_quran_ayah(surah_num:int, ayah_num:int, translation:str='en.asad')->dict:
    """
    Fetch a specific Quran ayah by its surah number and ayah number.
    
    Args:
        surah_num (int): The number of the surah (e.g., 1 for Al-Fatihah)
        ayah_num (int): The number of the ayah within the surah
        translation (str): The translation to use (default: 'en.asad')
        
    Returns:
        dict: A dictionary containing:
            - surah (str): The name of the surah
            - translation (str): The translation of the surah
            - surah_number (int): The number of the surah
            - ayah_number (int): The number of the ayah
            - global_ayah (int): The global number of the ayah
            - text_arabic (str): The text of the ayah in Arabic
            - text_english (str): The text of the ayah in English
            - reference (str): The reference of the ayah
    """
    print(f"Fetching Quran ayah: {surah_num}:{ayah_num} with translation: {translation}")
    # Step 1: Get meta data to build surah → global ayah map
    meta_url = "http://api.alquran.cloud/v1/meta"
    meta_res = requests.get(meta_url)
    if meta_res.status_code != 200:
        raise Exception("Failed to fetch Quran metadata.")
    meta_data = meta_res.json()
    
    # Step 2: Build surah starting ayah map
    surah_refs = meta_data['data']['surahs']['references']
    surah_map = {}
    current_ayah = 1
    for surah in surah_refs:
        surah_map[surah['number']] = {
            'start_ayah': current_ayah,
            'englishName': surah['englishName'],
            'englishNameTranslation': surah['englishNameTranslation']
        }
        current_ayah += surah['numberOfAyahs']
    
    if surah_num not in surah_map:
        raise ValueError("Invalid surah number.")
    
    global_ayah = surah_map[surah_num]['start_ayah'] + ayah_num - 1
    
    # Step 3: Fetch the ayah using global number
    ayah_url = f"http://api.alquran.cloud/v1/ayah/{global_ayah}/{translation}"
    ayah_res = requests.get(ayah_url)
    if ayah_res.status_code != 200:
        raise Exception("Failed to fetch Quran ayah.")
    ayah_data = ayah_res.json()['data']
    
    # Step 4: Return structured info
    return {
        'surah': surah_map[surah_num]['englishName'],
        'translation': surah_map[surah_num]['englishNameTranslation'],
        'surah_number': surah_num,
        'ayah_number': ayah_num,
        'global_ayah': global_ayah,
        'text_arabic': ayah_data['text'],
        'text_english': ayah_data['edition']['name'] + ": " + ayah_data['text'],
        'reference': f"{surah_map[surah_num]['englishName']} ({surah_num}:{ayah_num})"
    }
