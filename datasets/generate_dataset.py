"""
Generate realistic agricultural dataset for Indian crops.
Based on ICAR agronomic profiles and standard benchmark distributions.
Fields: N, P, K, temperature, humidity, ph, rainfall, label
"""

import os
import random
import csv

CROP_PROFILES = {
    'rice': {'N': (60, 100), 'P': (35, 60), 'K': (35, 50), 'temp': (20, 28), 'hum': (80, 95), 'ph': (5.0, 7.5), 'rain': (180, 300)},
    'maize': {'N': (60, 100), 'P': (40, 60), 'K': (15, 25), 'temp': (18, 28), 'hum': (55, 75), 'ph': (5.5, 7.0), 'rain': (60, 110)},
    'chickpea': {'N': (20, 60), 'P': (55, 80), 'K': (75, 85), 'temp': (17, 22), 'hum': (14, 20), 'ph': (6.0, 8.5), 'rain': (65, 95)},
    'kidneybeans': {'N': (10, 40), 'P': (55, 80), 'K': (15, 25), 'temp': (15, 24), 'hum': (18, 25), 'ph': (5.5, 6.0), 'rain': (60, 150)},
    'pigeonpeas': {'N': (15, 40), 'P': (55, 75), 'K': (15, 25), 'temp': (27, 38), 'hum': (30, 65), 'ph': (4.5, 7.5), 'rain': (90, 200)},
    'mothbeans': {'N': (10, 35), 'P': (35, 60), 'K': (15, 25), 'temp': (24, 32), 'hum': (40, 65), 'ph': (3.5, 9.5), 'rain': (30, 75)},
    'mungbean': {'N': (10, 35), 'P': (35, 60), 'K': (15, 25), 'temp': (27, 30), 'hum': (80, 90), 'ph': (6.2, 7.2), 'rain': (35, 60)},
    'blackgram': {'N': (30, 60), 'P': (55, 80), 'K': (15, 25), 'temp': (25, 35), 'hum': (60, 70), 'ph': (6.5, 7.5), 'rain': (60, 75)},
    'lentil': {'N': (15, 40), 'P': (55, 80), 'K': (15, 25), 'temp': (18, 30), 'hum': (60, 70), 'ph': (6.0, 7.8), 'rain': (35, 55)},
    'pomegranate': {'N': (15, 40), 'P': (10, 30), 'K': (35, 45), 'temp': (18, 25), 'hum': (85, 95), 'ph': (5.5, 7.2), 'rain': (100, 115)},
    'banana': {'N': (90, 120), 'P': (70, 95), 'K': (45, 55), 'temp': (25, 30), 'hum': (75, 85), 'ph': (5.5, 6.5), 'rain': (90, 120)},
    'mango': {'N': (10, 40), 'P': (15, 35), 'K': (25, 35), 'temp': (27, 36), 'hum': (45, 55), 'ph': (4.5, 7.0), 'rain': (85, 105)},
    'grapes': {'N': (10, 40), 'P': (120, 145), 'K': (195, 205), 'temp': (8, 42), 'hum': (80, 85), 'ph': (5.5, 6.5), 'rain': (65, 75)},
    'watermelon': {'N': (80, 120), 'P': (5, 30), 'K': (45, 55), 'temp': (24, 27), 'hum': (80, 90), 'ph': (6.0, 7.0), 'rain': (40, 60)},
    'muskmelon': {'N': (80, 120), 'P': (5, 30), 'K': (45, 55), 'temp': (27, 30), 'hum': (90, 95), 'ph': (6.0, 6.8), 'rain': (20, 30)},
    'apple': {'N': (10, 40), 'P': (120, 145), 'K': (195, 205), 'temp': (21, 24), 'hum': (90, 95), 'ph': (5.5, 6.5), 'rain': (100, 125)},
    'orange': {'N': (10, 40), 'P': (5, 30), 'K': (5, 15), 'temp': (15, 35), 'hum': (90, 95), 'ph': (6.0, 8.0), 'rain': (100, 120)},
    'papaya': {'N': (30, 70), 'P': (45, 70), 'K': (45, 55), 'temp': (23, 44), 'hum': (90, 95), 'ph': (6.5, 7.0), 'rain': (140, 250)},
    'coconut': {'N': (15, 40), 'P': (5, 30), 'K': (25, 35), 'temp': (25, 30), 'hum': (95, 100), 'ph': (5.5, 6.5), 'rain': (130, 225)},
    'cotton': {'N': (100, 140), 'P': (35, 60), 'K': (15, 25), 'temp': (22, 26), 'hum': (75, 85), 'ph': (6.0, 8.0), 'rain': (60, 100)},
    'jute': {'N': (60, 100), 'P': (35, 60), 'K': (35, 45), 'temp': (23, 27), 'hum': (70, 90), 'ph': (6.0, 7.5), 'rain': (150, 200)},
    'coffee': {'N': (80, 120), 'P': (15, 40), 'K': (25, 35), 'temp': (23, 28), 'hum': (50, 70), 'ph': (6.0, 7.5), 'rain': (115, 195)},
}

def generate_dataset(output_path, samples_per_crop=100):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    random.seed(42)
    rows = []
    
    for crop, p in CROP_PROFILES.items():
        for _ in range(samples_per_crop):
            n = round(random.uniform(*p['N']) + random.gauss(0, 3), 1)
            ph_val = round(min(9.5, max(3.5, random.uniform(*p['ph']) + random.gauss(0, 0.2))), 2)
            k = round(max(5, random.uniform(*p['K']) + random.gauss(0, 2)), 1)
            p_val = round(max(5, random.uniform(*p['P']) + random.gauss(0, 2)), 1)
            temp = round(random.uniform(*p['temp']) + random.gauss(0, 0.8), 2)
            hum = round(min(100, max(10, random.uniform(*p['hum']) + random.gauss(0, 2))), 2)
            rain = round(max(10, random.uniform(*p['rain']) + random.gauss(0, 5)), 2)
            
            rows.append({
                'N': max(0, n),
                'P': max(0, p_val),
                'K': max(0, k),
                'temperature': temp,
                'humidity': hum,
                'ph': ph_val,
                'rainfall': rain,
                'label': crop
            })
            
    random.shuffle(rows)
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label'])
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Generated {len(rows)} records for {len(CROP_PROFILES)} crops at {output_path}")

if __name__ == '__main__':
    target = os.path.join(os.path.dirname(__file__), 'agriculture_dataset.csv')
    generate_dataset(target)

