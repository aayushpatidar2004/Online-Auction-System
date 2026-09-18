"""
Soil Analysis & Health Card Service
Based on ICAR (Indian Council of Agricultural Research) soil classification standards.
"""

SOIL_CROP_MAPPING = {
    'Black Soil': {
        'characteristics': 'High clay content, rich in calcium carbonate, potassium, and magnesium. Excellent moisture retention, ideal for dryland farming.',
        'crops': ['Cotton', 'Soybean', 'Wheat', 'Pigeonpeas (Tur)', 'Sorghum (Jowar)', 'Chickpea'],
        'irrigation_factor': 'Moderate water requirement due to high moisture retentivity.'
    },
    'Red Soil': {
        'characteristics': 'Rich in iron oxides, porous, low nitrogen, phosphorus, and organic matter. Highly responsive to irrigation and manure.',
        'crops': ['Groundnut', 'Millets (Ragi)', 'Pulses', 'Tobacco', 'Oilseeds', 'Pomegranate'],
        'irrigation_factor': 'Frequent light irrigation recommended due to quick drainage.'
    },
    'Alluvial Soil': {
        'characteristics': 'Formed by river silt deposits, exceptionally fertile, balanced potash and lime, highly productive.',
        'crops': ['Rice (Paddy)', 'Wheat', 'Sugarcane', 'Maize', 'Jute', 'Mustard', 'Vegetables'],
        'irrigation_factor': 'Regular controlled irrigation ensures bumper yields.'
    },
    'Laterite Soil': {
        'characteristics': 'Formed under heavy tropical rainfall, acidic, depleted in lime and silica, rich in iron and aluminium.',
        'crops': ['Cashew Nut', 'Coconut', 'Coffee', 'Tea', 'Rubber', 'Arecanut'],
        'irrigation_factor': 'Mulching and organic conservation critical to retain moisture.'
    },
    'Sandy Soil': {
        'characteristics': 'Large soil particles, excessive aeration, very low water holding capacity, prone to rapid nutrient leaching.',
        'crops': ['Watermelon', 'Muskmelon', 'Mothbeans', 'Groundnut', 'Barley', 'Carrot'],
        'irrigation_factor': 'Drip irrigation with fertigation strongly recommended.'
    },
    'Clay Soil': {
        'characteristics': 'Fine textured, compact, sticky when wet, prone to waterlogging, high nutrient adsorption capacity.',
        'crops': ['Paddy Rice', 'Broccoli', 'Cabbage', 'Blackgram', 'Kidneybeans'],
        'irrigation_factor': 'Ensure proper field drainage to avoid root rot.'
    },
    'Loamy Soil': {
        'characteristics': 'The gold standard for farming. Ideal balance of sand, silt, and clay. Excellent tilth, aeration, and drainage.',
        'crops': ['Tomato', 'Potato', 'Onion', 'Chilli', 'Papaya', 'Banana', 'Wheat', 'Maize'],
        'irrigation_factor': 'Balanced irrigation schedule as per crop growth stages.'
    }
}

def evaluate_ph(ph):
    if ph < 5.5:
        return {'status': 'Strongly Acidic', 'rating': 'Poor', 'badge': 'danger', 'action': 'Apply Agricultural Lime (Calcium Carbonate) @ 200-400 kg/acre to neutralize acidity.'}
    elif 5.5 <= ph < 6.5:
        return {'status': 'Slightly Acidic', 'rating': 'Moderate', 'badge': 'warning', 'action': 'Apply well-decomposed FYM and wood ash to gradually buffer pH.'}
    elif 6.5 <= ph <= 7.5:
        return {'status': 'Neutral (Optimal)', 'rating': 'Optimal', 'badge': 'success', 'action': 'Ideal soil reaction. Maintain current organic management.'}
    elif 7.5 < ph <= 8.5:
        return {'status': 'Moderately Alkaline', 'rating': 'Moderate', 'badge': 'warning', 'action': 'Incorporate organic green manure (Dhaincha/Sunn hemp) to lower alkalinity.'}
    else:
        return {'status': 'Strongly Alkaline / Saline', 'rating': 'Poor', 'badge': 'danger', 'action': 'Apply Agricultural Gypsum (Calcium Sulphate) @ 300-500 kg/acre followed by leaching.'}

def evaluate_nutrient(val, low_limit, high_limit, nutrient_name):
    if val < low_limit:
        return {
            'value': val,
            'status': 'Low',
            'rating': 'Low',
            'badge': 'danger',
            'recommendation': f"Deficient in {nutrient_name}. Increase recommended application by 25-30%."
        }
    elif val <= high_limit:
        return {
            'value': val,
            'status': 'Medium (Adequate)',
            'rating': 'Medium',
            'badge': 'success',
            'recommendation': f"Adequate {nutrient_name}. Apply standard maintenance dosage."
        }
    else:
        return {
            'value': val,
            'status': 'High',
            'rating': 'High',
            'badge': 'primary',
            'recommendation': f"High in {nutrient_name}. Reduce or withhold supplementary application to prevent soil toxicity."
        }

def analyze_soil(soil_type, ph, nitrogen, phosphorus, potassium, moisture, organic_carbon):
    ph_eval = evaluate_ph(ph)
    # Standard ICAR benchmark ranges (kg/ha)
    n_eval = evaluate_nutrient(nitrogen, 280, 560, 'Nitrogen')
    p_eval = evaluate_nutrient(phosphorus, 10, 25, 'Phosphorus')
    k_eval = evaluate_nutrient(potassium, 110, 280, 'Potassium')

    # Organic carbon evaluation
    if organic_carbon < 0.5:
        oc_status = {'value': organic_carbon, 'status': 'Low (<0.5%)', 'badge': 'danger', 'action': 'Incorporate 5-8 tonnes of vermicompost or composted FYM per acre.'}
    elif organic_carbon <= 0.75:
        oc_status = {'value': organic_carbon, 'status': 'Medium (0.5-0.75%)', 'badge': 'warning', 'action': 'Practice mulching and crop residue recycling.'}
    else:
        oc_status = {'value': organic_carbon, 'status': 'High (>0.75%)', 'badge': 'success', 'action': 'Excellent microbial soil health. Continue organic recycling.'}

    # Moisture status
    if moisture < 35:
        moisture_status = {'value': moisture, 'status': 'Critically Dry', 'badge': 'danger', 'action': 'Immediate irrigation needed to prevent moisture stress.'}
    elif moisture <= 65:
        moisture_status = {'value': moisture, 'status': 'Optimal Moisture', 'badge': 'success', 'action': 'Soil moisture is in the ideal field capacity zone.'}
    else:
        moisture_status = {'value': moisture, 'status': 'Waterlogged / Excessive', 'badge': 'warning', 'action': 'Ensure drainage channels are clear to prevent root asphyxiation.'}

    # Calculate overall health score (0-100)
    score = 100
    if ph_eval['rating'] == 'Poor': score -= 25
    elif ph_eval['rating'] == 'Moderate': score -= 10
    
    if n_eval['rating'] == 'Low': score -= 15
    if p_eval['rating'] == 'Low': score -= 15
    if k_eval['rating'] == 'Low': score -= 15
    if oc_status['status'].startswith('Low'): score -= 15
    if moisture_status['status'].startswith('Critically'): score -= 15

    health_score = max(20, min(100, score))
    if health_score >= 80:
        health_label = "Prime Fertile Soil"
        health_badge = "success"
    elif health_score >= 60:
        health_label = "Moderately Healthy Soil"
        health_badge = "info"
    else:
        health_label = "Requires Soil Amendment & Regeneration"
        health_badge = "warning"

    type_info = SOIL_CROP_MAPPING.get(soil_type, SOIL_CROP_MAPPING['Black Soil'])

    # Tailored fertilizer schedule recommendations
    fertilizer_plan = []
    if n_eval['status'] == 'Low':
        fertilizer_plan.append("Urea (46% N) @ 45 kg/acre in 2 split doses, or Neem-coated Urea.")
    if p_eval['status'] == 'Low':
        fertilizer_plan.append("DAP (18-46-0) @ 50 kg/acre or Single Super Phosphate (SSP) @ 100 kg/acre at basal sowing.")
    if k_eval['status'] == 'Low':
        fertilizer_plan.append("Muriate of Potash (MOP 60% K2O) @ 25 kg/acre at sowing.")
    if not fertilizer_plan:
        fertilizer_plan.append("Standard balanced NPK 19:19:19 @ 15 kg/acre with micronutrient spray (Zinc + Boron).")

    return {
        'soil_type': soil_type,
        'soil_characteristics': type_info['characteristics'],
        'health_score': health_score,
        'health_label': health_label,
        'health_badge': health_badge,
        'ph_assessment': ph_eval,
        'nutrients': {
            'nitrogen': n_eval,
            'phosphorus': p_eval,
            'potassium': k_eval,
            'organic_carbon': oc_status,
            'moisture': moisture_status
        },
        'suitable_crops': type_info['crops'],
        'irrigation_recommendation': type_info['irrigation_factor'] + " " + moisture_status['action'],
        'fertilizer_recommendations': fertilizer_plan,
        'soil_health_card': {
            'ph': f"{ph} ({ph_eval['rating']})",
            'nitrogen': n_eval['status'],
            'phosphorus': p_eval['status'],
            'potassium': k_eval['status'],
            'moisture': f"{moisture}% ({moisture_status['status']})",
            'organic_carbon': f"{organic_carbon}% ({oc_status['status']})",
            'top_suitable_crop': type_info['crops'][0]
        }
    }

