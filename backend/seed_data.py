"""
AgriSmart Database Seeder
Populates initial rich authentic data for Indian agriculture:
- Default Farmer Account & Farms
- Crops & Agronomic profiles
- Plant Diseases
- Pests & Integrated Pest Management
- Pesticides & Safety Guidelines
- Fertilizers & Nutrient Guidelines
- Government Schemes & Portals
- Educational Articles
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import FarmerProfile
from crops.models import Crop
from diseases.models import Disease
from pests.models import Pest
from pesticides.models import Pesticide
from fertilizers.models import Fertilizer
from farms.models import Farm
from articles.models import Article, GovernmentResource

def seed():
    print("Seeding AgriSmart Database...")

    # 1. Create Default Demo Farmer
    if not User.objects.filter(username='farmer').exists():
        user = User.objects.create_user(
            username='farmer',
            email='farmer@agrismart.in',
            password='Farmer@123',
            first_name='Ramesh',
            last_name='Patel'
        )
        FarmerProfile.objects.create(
            user=user,
            full_name='Ramesh Patel',
            mobile_number='9876543210',
            village='Sonapur',
            district='Nagpur',
            state='Maharashtra',
            farm_size_acres=5.5,
            soil_type='Black Soil',
            main_crop='Cotton',
            preferred_language='en'
        )
        print("Created demo farmer account: username='farmer', password='Farmer@123'")
    else:
        user = User.objects.get(username='farmer')

    # 2. Demo Farms
    farms_data = [
        {
            'farm_name': 'North Orchard & Field',
            'village': 'Sonapur',
            'area_acres': 3.5,
            'soil_type': 'Black Soil',
            'current_crop': 'Cotton',
            'sowing_date': '2026-06-20',
            'irrigation_type': 'Drip Irrigation',
            'expected_harvest_date': '2026-11-15',
            'stage': 'Flowering',
            'notes': 'Applied neem cake at basal sowing; installed 15 yellow sticky traps for whitefly monitoring.'
        },
        {
            'farm_name': 'Riverbed Plot B',
            'village': 'Sonapur',
            'area_acres': 2.0,
            'soil_type': 'Alluvial Soil',
            'current_crop': 'Soybean',
            'sowing_date': '2026-07-02',
            'irrigation_type': 'Sprinkler Irrigation',
            'expected_harvest_date': '2026-10-10',
            'stage': 'Vegetative',
            'notes': 'Rhizobium bio-inoculant used at seed treatment.'
        }
    ]
    for f in farms_data:
        Farm.objects.get_or_create(user=user, farm_name=f['farm_name'], defaults=f)

    # 3. Crops
    crops_data = [
        {
            'name': 'Cotton', 'slug': 'cotton', 'scientific_name': 'Gossypium hirsutum',
            'season': 'Kharif', 'water_requirement': 'Moderate',
            'ideal_soil': 'Black Soil (Regur)', 'optimal_temp_range': '21°C - 30°C',
            'optimal_rainfall_range': '500 - 1000 mm', 'optimal_ph_range': '6.0 - 8.0',
            'maturity_days': 160, 'sowing_window': 'May - June', 'harvest_window': 'November - January',
            'description': 'Known as White Gold. Primary commercial fiber crop in Maharashtra, Gujarat, and Telangana. Requires deep black soil with good moisture holding capacity.',
            'image_url': 'https://images.unsplash.com/photo-1605000797499-95a51c5269ae?w=600&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Rice', 'slug': 'rice', 'scientific_name': 'Oryza sativa',
            'season': 'Kharif', 'water_requirement': 'Very High',
            'ideal_soil': 'Clay Soil, Alluvial Soil', 'optimal_temp_range': '22°C - 32°C',
            'optimal_rainfall_range': '1000 - 1500 mm', 'optimal_ph_range': '5.5 - 7.0',
            'maturity_days': 125, 'sowing_window': 'June - July', 'harvest_window': 'October - November',
            'description': 'Staple food grain of India. Requires prolonged standing water or saturated soil conditions during tillering and panicle development.',
            'image_url': 'https://images.unsplash.com/photo-1536704689225-7033580554c1?w=600&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Wheat', 'slug': 'wheat', 'scientific_name': 'Triticum aestivum',
            'season': 'Rabi', 'water_requirement': 'Moderate',
            'ideal_soil': 'Alluvial Soil, Loamy Soil', 'optimal_temp_range': '15°C - 25°C',
            'optimal_rainfall_range': '400 - 750 mm', 'optimal_ph_range': '6.0 - 7.5',
            'maturity_days': 130, 'sowing_window': 'October - November', 'harvest_window': 'March - April',
            'description': 'Premier winter cereal crop of northern and central India. Sensitive to high temperatures during grain-filling stage.',
            'image_url': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=600&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Maize', 'slug': 'maize', 'scientific_name': 'Zea mays',
            'season': 'Kharif', 'water_requirement': 'Moderate',
            'ideal_soil': 'Loamy Soil, Alluvial Soil', 'optimal_temp_range': '21°C - 27°C',
            'optimal_rainfall_range': '500 - 800 mm', 'optimal_ph_range': '5.5 - 7.5',
            'maturity_days': 95, 'sowing_window': 'June - July', 'harvest_window': 'September - October',
            'description': 'Queen of Cereals with multiple uses: human consumption, livestock feed, and industrial starch. Highly responsive to nitrogen.',
            'image_url': 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=600&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Soybean', 'slug': 'soybean', 'scientific_name': 'Glycine max',
            'season': 'Kharif', 'water_requirement': 'Moderate',
            'ideal_soil': 'Black Soil, Loamy Soil', 'optimal_temp_range': '20°C - 30°C',
            'optimal_rainfall_range': '600 - 900 mm', 'optimal_ph_range': '6.0 - 7.5',
            'maturity_days': 100, 'sowing_window': 'June - July', 'harvest_window': 'October',
            'description': 'Premier oilseed and protein crop. Fixes atmospheric nitrogen through symbiotic root nodules.',
            'image_url': 'https://images.unsplash.com/photo-1599423300746-b62533397364?w=600&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Chickpea', 'slug': 'chickpea', 'scientific_name': 'Cicer arietinum',
            'season': 'Rabi', 'water_requirement': 'Low',
            'ideal_soil': 'Black Soil, Sandy Loam', 'optimal_temp_range': '18°C - 24°C',
            'optimal_rainfall_range': '300 - 500 mm', 'optimal_ph_range': '6.0 - 8.0',
            'maturity_days': 110, 'sowing_window': 'October - November', 'harvest_window': 'February - March',
            'description': 'Major pulse crop (Chana). Drought-tolerant, enriches soil fertility, thrives in cool dry weather.',
            'image_url': 'https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?w=600&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Sugarcane', 'slug': 'sugarcane', 'scientific_name': 'Saccharum officinarum',
            'season': 'All Seasons', 'water_requirement': 'Very High',
            'ideal_soil': 'Deep Alluvial Soil, Heavy Clay Loam', 'optimal_temp_range': '20°C - 35°C',
            'optimal_rainfall_range': '1200 - 1800 mm', 'optimal_ph_range': '6.5 - 7.5',
            'maturity_days': 365, 'sowing_window': 'January - March / October', 'harvest_window': 'December - April',
            'description': 'Long-duration cash crop driving the sugar and ethanol industry. Demands abundant water and deep nutrient reserves.',
            'image_url': 'https://images.unsplash.com/photo-1589923188900-85dae523342b?w=600&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Tomato', 'slug': 'tomato', 'scientific_name': 'Solanum lycopersicum',
            'season': 'All Seasons', 'water_requirement': 'Moderate',
            'ideal_soil': 'Sandy Loam, Red Loam', 'optimal_temp_range': '18°C - 27°C',
            'optimal_rainfall_range': '400 - 600 mm', 'optimal_ph_range': '6.0 - 7.0',
            'maturity_days': 85, 'sowing_window': 'Year-round with irrigation', 'harvest_window': 'Continuous',
            'description': 'High-value horticulture vegetable. Requires regular staking, pruning, and protection from foliar blights.',
            'image_url': 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=600&auto=format&fit=crop&q=80'
        }
    ]
    for c in crops_data:
        Crop.objects.get_or_create(slug=c['slug'], defaults=c)

    # 4. Diseases
    diseases_data = [
        {
            'disease_name': 'Tomato Early Blight',
            'scientific_name': 'Alternaria solani',
            'crop': 'Tomato',
            'severity': 'Moderate',
            'symptoms': 'Dark concentric ring spots resembling targets on older lower leaves. Defoliation exposes fruits to sunscald.',
            'possible_causes': 'High humidity, warm temperatures, soil splashing, unpruned dense canopy.',
            'organic_management': 'Spray neem oil 5ml/L, Bordeaux mixture 1%, prune lower foliage 1 foot above soil.',
            'chemical_management': 'Mancozeb 75% WP @ 2.5 g/L or Azoxystrobin 23% SC @ 1 ml/L.',
            'prevention': 'Rotate away from Solanaceae crops for 3 years. Use drip irrigation instead of overhead sprinklers.',
            'when_to_consult_expert': 'Consult KVK officer if stem lesions appear or if defoliation exceeds 25%.'
        },
        {
            'disease_name': 'Rice Blast',
            'scientific_name': 'Magnaporthe oryzae',
            'crop': 'Rice / Paddy',
            'severity': 'High',
            'symptoms': 'Spindle-shaped diamond spots with grey centers on leaves; neck blast breaks panicles leading to empty grains.',
            'possible_causes': 'Excess urea application, prolonged dew or drizzle, night temperature around 20°C.',
            'organic_management': 'Pseudomonas fluorescens @ 10 g/L, fermented cow urine spray.',
            'chemical_management': 'Tricyclazole 75% WP @ 0.6 g/L or Isoprothiolane 40% EC @ 1.5 ml/L.',
            'prevention': 'Balanced NPK dosage, treat seeds with Trichoderma harzianum @ 10 g/kg seed.',
            'when_to_consult_expert': 'Immediate consultation required if neck rot is spotted at heading stage.'
        },
        {
            'disease_name': 'Cotton Leaf Curl Disease (CLCuD)',
            'scientific_name': 'Begomovirus (Whitefly vector)',
            'crop': 'Cotton',
            'severity': 'High',
            'symptoms': 'Upward and downward curling of leaves, vein thickening, leaf-like enations on undersides.',
            'possible_causes': 'Heavy whitefly infestation carrying the virus during early crop stages.',
            'organic_management': 'Yellow sticky traps @ 20/acre, neem oil spray, protect ladybird beetles.',
            'chemical_management': 'Control whiteflies using Diafenthiuron 50% WP @ 1.2 g/L or Flonicamid 50% WG @ 0.3 g/L.',
            'prevention': 'Grow resistant Bt hybrids; destroy weed hosts around field margins.',
            'when_to_consult_expert': 'Consult district agricultural officer if symptoms show before squaring stage.'
        },
        {
            'disease_name': 'Potato Late Blight',
            'scientific_name': 'Phytophthora infestans',
            'crop': 'Potato',
            'severity': 'High',
            'symptoms': 'Water-soaked brown spots that rapidly blacken and destroy entire foliage in humid weather.',
            'possible_causes': 'Cool, misty weather (15-20°C) with high humidity (>90%).',
            'organic_management': 'Prophylactic copper oxychloride spray; cut haulms before digging tubers.',
            'chemical_management': 'Metalaxyl 8% + Mancozeb 64% WP @ 2.5 g/L or Cymoxanil + Mancozeb.',
            'prevention': 'Use certified disease-free tubers; ensure high earthing up around roots.',
            'when_to_consult_expert': 'Emergency reporting recommended as late blight can wipe out entire district harvests in 7 days.'
        }
    ]
    for d in diseases_data:
        Disease.objects.get_or_create(disease_name=d['disease_name'], defaults=d)

    # 5. Pests
    pests_data = [
        {
            'pest_name': 'Pink Bollworm',
            'scientific_name': 'Pectinophora gossypiella',
            'affected_crops': 'Cotton',
            'identification': 'Caterpillar is creamy white with distinct pink bands on dorsal side in later instars. Adult is a small greyish-brown moth.',
            'symptoms': 'Rosetted flowers (petals remain twisted together), borehole in cotton bolls plugged with excreta, stained lint and damaged seeds.',
            'life_cycle': 'Eggs laid on squares/bolls (3-5 days), larval period inside boll (10-14 days), pupation in soil litter, adult life 10-14 days.',
            'prevention': 'Adopt timely sowing, avoid extending cotton crop beyond 150 days, install pheromone traps @ 5/acre for monitoring.',
            'organic_control': 'Release egg parasitoid Trichogramma bactrae @ 60,000/acre at weekly intervals. Spray Neem Seed Kernel Extract (NSKE 5%).',
            'chemical_control': 'When ETL reaches 8 moths/trap/night: spray Emamectin Benzoate 5% SG @ 0.5 g/L or Chlorantraniliprole 18.5% SC @ 0.3 ml/L.',
            'safety_precautions': 'Rotate chemical classes to prevent insect resistance. Avoid daytime spraying to protect honeybees.'
        },
        {
            'pest_name': 'Whitefly',
            'scientific_name': 'Bemisia tabaci',
            'affected_crops': 'Cotton, Tomato, Chilli, Brinjal, Soybean, Pulses',
            'identification': 'Tiny, 1 mm long insects with powdery white wings and yellow bodies. Found feeding in clusters on the undersides of leaves.',
            'symptoms': 'Yellowing and chlorosis of foliage, sooty mold growth due to sticky honeydew secretion, vector for viral leaf curl diseases.',
            'life_cycle': 'Egg to adult cycle completed in 14-21 days during warm summer months.',
            'prevention': 'Erect border crops (maize/sorghum) to act as wind and vector barriers. Avoid excessive nitrogenous fertilizers.',
            'organic_control': 'Install yellow sticky traps @ 15-20 per acre. Spray neem oil (1500 ppm) @ 5 ml/L or Verticillium lecanii bio-fungicide.',
            'chemical_control': 'Spiromesifen 22.9% SC @ 1 ml/L or Diafenthiuron 50% WP @ 1.2 g/L or Pyriproxyfen 10% EC @ 2 ml/L.',
            'safety_precautions': 'Ensure full coverage of leaf undersides with hollow cone nozzle. Wear protective mask and gloves.'
        },
        {
            'pest_name': 'Yellow Stem Borer',
            'scientific_name': 'Scirpophaga incertulas',
            'affected_crops': 'Rice / Paddy',
            'identification': 'Adult female moth is yellow with a prominent black spot on each forewing. Larvae bore into internal tillers.',
            'symptoms': '"Dead heart" in vegetative stage (central tiller dries up and easily pulls out); "White earhead" in reproductive stage (empty erect white panicle).',
            'life_cycle': 'Eggs laid in clusters covered with buff-colored hairs on upper leaf tips.',
            'prevention': 'Clip leaf tips before transplanting seedlings to eliminate egg masses. Install sex pheromone traps.',
            'organic_control': 'Release Trichogramma japonicum @ 40,000/acre 3-4 times. Spray Bacillus thuringiensis (Bt) @ 2 g/L.',
            'chemical_control': 'Cartap Hydrochloride 50% SP @ 2 g/L or Chlorantraniliprole 0.4% GR @ 4 kg/acre in standing water.',
            'safety_precautions': 'Do not drain paddy water for 48 hours after granular application. Maintain personal hygiene.'
        },
        {
            'pest_name': 'Aphids (Plant Lice)',
            'scientific_name': 'Aphis gossypii / Lipaphis erysimi',
            'affected_crops': 'Mustard, Wheat, Cotton, Vegetables, Legumes',
            'identification': 'Soft-bodied, pear-shaped tiny green, black, or yellow insects congregating on tender shoots and leaf buds.',
            'symptoms': 'Curled, crinkled leaves, stunted vegetative growth, honeydew deposits inviting black sooty mold fungus.',
            'life_cycle': 'Rapid reproduction by parthenogenesis; generation time 7-10 days under favorable cool weather.',
            'prevention': 'Early sowing of mustard/wheat escapes peak aphid flight. Encourage natural predators.',
            'organic_control': 'Conserve ladybird beetles and syrphid fly larvae. Spray 5% neem extract or fish oil rosin soap.',
            'chemical_control': 'Imidacloprid 17.8% SL @ 0.3 ml/L or Thiamethoxam 25% WG @ 0.3 g/L.',
            'safety_precautions': 'Strictly avoid spraying during peak bee foraging hours (9 AM to 3 PM) to prevent colony collapse.'
        },
        {
            'pest_name': 'Fall Armyworm',
            'scientific_name': 'Spodoptera frugiperda',
            'affected_crops': 'Maize, Sorghum, Millets, Sugarcane',
            'identification': 'Larva has inverted yellow "Y" on head and 4 raised black spots arranged in a square on the eighth abdominal segment.',
            'symptoms': 'Window-paning on leaf whorls, extensive ragging of leaves with large quantity of sawdust-like fecal frass in the central whorl.',
            'life_cycle': 'Complete lifecycle lasts 30-40 days. Voracious feeder capable of devastating whole fields.',
            'prevention': 'Intercrop maize with cowpea or desmodium. Clean field boundaries of grass weeds.',
            'organic_control': 'Whorl application of sand + wood ash (9:1 ratio). Spray Metarhizium rileyi or Beauveria bassiana @ 5 g/L.',
            'chemical_control': 'Chlorantraniliprole 18.5% SC @ 0.4 ml/L or Spinetoram 11.7% SC @ 0.5 ml/L directed into the whorl.',
            'safety_precautions': 'Direct spray lance strictly into the leaf whorl where larvae hide. Use personal protective gear.'
        }
    ]
    for p in pests_data:
        Pest.objects.get_or_create(pest_name=p['pest_name'], defaults=p)

    # 6. Pesticides
    pesticides_data = [
        {
            'product_name': 'Neem Oil (Azadirachtin 1500 PPM)',
            'active_ingredient': 'Azadirachtin (Botanical)',
            'chemical_class': 'Organic Botanical Antifeedant & Repellent',
            'toxicity_label': 'Bio',
            'target_pests': 'Aphids, Whiteflies, Thrips, Mites, Early instar Caterpillars',
            'target_crops': 'All vegetable, cereal, and cash crops',
            'mode_of_action': 'Antifeedant, insect growth regulator (IGR), disrupts insect moulting, oviposition deterrent.',
            'general_usage_info': 'Mix 4-5 ml per liter of water with 1 ml of mild liquid soap/emulsifier. Best applied early morning or late afternoon.',
            'safety_precautions': 'Safe for mammals, earthworms, and pollinators. Store in cool dark place away from direct sunlight.',
            'ppe_requirements': 'Basic eye protection and rubber gloves during mixing.',
            'pre_harvest_interval_days': 1,
            'storage_guidelines': 'Store at 10-25°C in original container. Shelf life 2 years.',
            'environmental_precautions': 'Eco-friendly and biodegradable with zero hazardous soil residues.',
            'disclaimer': 'Always follow the product label, local agricultural authority guidance, and advice from a qualified agriculture professional before application.'
        },
        {
            'product_name': 'Coragen (Chlorantraniliprole 18.5% SC)',
            'active_ingredient': 'Chlorantraniliprole 18.5% SC',
            'chemical_class': 'Anthranilic Diamide (Group 28 Insecticide)',
            'toxicity_label': 'Green',
            'target_pests': 'Pink Bollworm, American Bollworm, Stem Borer, Fall Armyworm, Diamondback Moth',
            'target_crops': 'Cotton, Rice, Maize, Sugarcane, Tomato, Cabbage',
            'mode_of_action': 'Ryanodine receptor modulator; activates calcium release in muscle cells causing paralysis and feeding cessation within hours.',
            'general_usage_info': 'Apply at first detection of egg hatch or economic threshold level (ETL). Recommended rate: 60 ml per acre in 200L water.',
            'safety_precautions': 'Low toxicity to mammals and beneficial insects when used as directed. Do not exceed recommended concentrations.',
            'ppe_requirements': 'Wear protective chemical-resistant gloves, protective eye goggles, face mask, and cotton overalls.',
            'pre_harvest_interval_days': 14,
            'storage_guidelines': 'Store under lock and key away from food, animal feeds, and children.',
            'environmental_precautions': 'Do not contaminate waterways, ponds, or fish tanks with spray equipment washing.',
            'disclaimer': 'Always follow the product label, local agricultural authority guidance, and advice from a qualified agriculture professional before application.'
        },
        {
            'product_name': 'Dithane M-45 (Mancozeb 75% WP)',
            'active_ingredient': 'Mancozeb (Polymeric dithiocarbamate)',
            'chemical_class': 'Broad Spectrum Contact Protectant Fungicide (FRAC M03)',
            'toxicity_label': 'Blue',
            'target_pests': 'Early Blight, Late Blight, Tikka Leaf Spot, Downy Mildew, Rust, Anthracnose',
            'target_crops': 'Potato, Tomato, Groundnut, Wheat, Grapes, Apple, Chilli',
            'mode_of_action': 'Multi-site contact action; disrupts fungal cellular lipid metabolism and ATP production.',
            'general_usage_info': 'Apply prophylactically before disease onset or immediately on initial spotting. 2.0 to 2.5 g per liter of water.',
            'safety_precautions': 'Purely protective action; will not cure already infected tissues. Spray uniformly on both leaf sides.',
            'ppe_requirements': 'N95 or particulate dust mask, full chemical gloves, protective boots, long apron.',
            'pre_harvest_interval_days': 7,
            'storage_guidelines': 'Keep dry; moisture causes decomposition and loss of fungicidal potency.',
            'environmental_precautions': 'Toxic to aquatic organisms. Maintain a 10-meter untreated buffer zone near open water bodies.',
            'disclaimer': 'Always follow the product label, local agricultural authority guidance, and advice from a qualified agriculture professional before application.'
        },
        {
            'product_name': 'Confidor (Imidacloprid 17.8% SL)',
            'active_ingredient': 'Imidacloprid',
            'chemical_class': 'Neonicotinoid Systemic Insecticide (Group 4A)',
            'toxicity_label': 'Blue',
            'target_pests': 'Aphids, Jassids, Thrips, Brown Planthopper (BPH)',
            'target_crops': 'Cotton, Paddy, Sugarcane, Mango, Sunflower',
            'mode_of_action': 'Systemic translaminar action; binds nicotinic acetylcholine receptors in the insect central nervous system.',
            'general_usage_info': '0.3 to 0.5 ml per liter of water. Suitable for both foliar spray and seedling root dip.',
            'safety_precautions': 'Highly toxic to bees. NEVER apply during crop bloom or when pollinators are active.',
            'ppe_requirements': 'Chemical goggles, nitrile gloves, breathing respirator mask, and protective rubber footwear.',
            'pre_harvest_interval_days': 21,
            'storage_guidelines': 'Keep container tightly closed in well-ventilated dedicated chemical store.',
            'environmental_precautions': 'High groundwater leaching hazard in sandy soils. Prohibited near apiary sites.',
            'disclaimer': 'Always follow the product label, local agricultural authority guidance, and advice from a qualified agriculture professional before application.'
        }
    ]
    for pest_prod in pesticides_data:
        Pesticide.objects.get_or_create(product_name=pest_prod['product_name'], defaults=pest_prod)

    # 7. Fertilizers
    fertilizers_data = [
        {
            'name': 'Urea (Neem Coated)',
            'category': 'Chemical Nitrogenous',
            'nutrient_composition': '46% Total Nitrogen (N)',
            'suitable_soil': 'All soil types (Black, Red, Alluvial, Loamy)',
            'suitable_crops': 'Cereals, Millets, Cotton, Sugarcane, Vegetables, Cash Crops',
            'general_information': 'Most widely utilized source of concentrated nitrogen. Essential for vegetative foliage development, chlorophyll formation, and rapid plant growth.',
            'application_method': 'Apply in 2 to 3 split doses (basal, tillering, and flowering). Avoid broadcasting on dry or waterlogged soil.',
            'safety_environmental': 'Excessive application causes nitrate leaching into groundwater and promotes succulent growth vulnerable to insect attacks.'
        },
        {
            'name': 'DAP (Di-Ammonium Phosphate 18:46:0)',
            'category': 'Chemical Phosphatic',
            'nutrient_composition': '18% Ammoniacal Nitrogen (N) + 46% Phosphorus (P2O5)',
            'suitable_soil': 'Neutral to slightly acidic and black soils with low phosphorus',
            'suitable_crops': 'Wheat, Paddy, Soybean, Chickpea, Cotton, Groundnut',
            'general_information': 'Premier source of plant-available phosphate. Stimulates rapid root elongation, early seedling vigor, and strong floral initiation.',
            'application_method': 'Apply strictly as a basal placement 4-5 cm below seed depth during sowing or transplanting.',
            'safety_environmental': 'Phosphorus binds tightly in alkaline soils; avoid surface broadcasting to prevent immobilization.'
        },
        {
            'name': 'MOP (Muriate of Potash 0:0:60)',
            'category': 'Chemical Potassic',
            'nutrient_composition': '60% Potash (K2O)',
            'suitable_soil': 'All soils except saline-alkaline or chloride-sensitive soils',
            'suitable_crops': 'Sugarcane, Potato, Banana, Cotton, Maize, Rice',
            'general_information': 'Key regulator of plant osmotic balance, stomatal conductance, enzyme activation, and disease resistance. Enhances grain weight and fruit sweetness.',
            'application_method': 'Split into basal application and top-dressing at flowering or tuber bulking.',
            'safety_environmental': 'Chlorine content requires caution in tobacco and chloride-sensitive horticulture crops.'
        },
        {
            'name': 'Vermicompost (Earthworm Castings)',
            'category': 'Organic & Bio',
            'nutrient_composition': '1.5-2.5% N, 1.0-1.8% P, 1.2-2.0% K + Micronutrients & Beneficial Microbes',
            'suitable_soil': 'All degraded, saline, low organic carbon, and depleted soils',
            'suitable_crops': 'All horticultural crops, organic farming, kitchen gardens, field crops',
            'general_information': 'Rich organic amendment loaded with plant hormones (auxins, gibberellins), humic substances, and beneficial microbial flora. Drastically improves soil moisture retention.',
            'application_method': 'Incorporate 2 to 5 tonnes per acre into topsoil during field preparation or around root basin.',
            'safety_environmental': '100% safe, non-toxic, enriches soil biodiversity and sequesters soil organic carbon.'
        },
        {
            'name': 'Zinc Sulphate Monohydrate (33% Zn)',
            'category': 'Micronutrients',
            'nutrient_composition': '33% Zinc (Zn) + 15% Sulphur (S)',
            'suitable_soil': 'Alluvial and Black soils deficient in Zinc (widespread across India)',
            'suitable_crops': 'Paddy (Khaira disease prevention), Maize, Wheat, Cotton, Citrus',
            'general_information': 'Crucial micronutrient for auxin synthesis, enzyme metabolism, and prevention of interveinal chlorosis (white bud in maize, khaira in paddy).',
            'application_method': 'Soil application @ 10 kg/acre every 2-3 years, or foliar spray @ 0.5% (5g/L) neutralized with slaked lime.',
            'safety_environmental': 'Do not mix directly in the spray tank with phosphatic fertilizers (DAP/SSP) to avoid insoluble zinc phosphate precipitation.'
        }
    ]
    for f in fertilizers_data:
        Fertilizer.objects.get_or_create(name=f['name'], defaults=f)

    # 8. Government Schemes & Resources
    resources_data = [
        {
            'name': 'PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)',
            'category': 'Income Support Scheme',
            'official_url': 'https://pmkisan.gov.in/',
            'ministry_department': 'Department of Agriculture and Farmers Welfare',
            'helpline': '155261 / 1800-115-526',
            'description': 'Central sector scheme providing income support of ₹6,000 per year in three equal installments to landholding farmer families across the country.',
            'beneficiary_criteria': 'All landholding farmer families with cultivable land in their names, subject to statutory exclusion criteria.'
        },
        {
            'name': 'PMFBY (Pradhan Mantri Fasal Bima Yojana)',
            'category': 'Crop Insurance Scheme',
            'official_url': 'https://pmfby.gov.in/',
            'ministry_department': 'Ministry of Agriculture & Farmers Welfare',
            'helpline': '1800-180-1551',
            'description': 'Comprehensive crop insurance covering non-preventable natural risks from pre-sowing to post-harvest stages at nominal premium rates (2% for Kharif, 1.5% for Rabi, 5% for commercial/horticulture).',
            'beneficiary_criteria': 'All farmers growing notified crops in notified areas including sharecroppers and tenant farmers.'
        },
        {
            'name': 'Soil Health Card Scheme',
            'category': 'Soil Testing & Advisory',
            'official_url': 'https://soilhealth.dac.gov.in/',
            'ministry_department': 'Ministry of Agriculture & Farmers Welfare',
            'helpline': '011-23382012',
            'description': 'Provides farmers with printed Soil Health Cards detailing 12 parameters (N, P, K, S, Zn, Fe, Cu, Mn, Bo, pH, EC, OC) and crop-wise fertilizer dosage recommendations.',
            'beneficiary_criteria': 'Open to all Indian agricultural landholders every 2 years.'
        },
        {
            'name': 'Kisan Call Centre (KCC)',
            'category': 'Official Agricultural Advisory Toll-Free Hotline',
            'official_url': 'https://mkisan.gov.in/',
            'ministry_department': 'Ministry of Agriculture & Farmers Welfare',
            'helpline': '1800-180-1551 (Toll Free, 6 AM to 10 PM daily)',
            'description': 'Direct telephone access to agricultural graduates and scientists answering farmer queries in 22 local Indian languages.',
            'beneficiary_criteria': 'Universal access for all Indian farmers.'
        },
        {
            'name': 'e-NAM (National Agriculture Market)',
            'category': 'Agri-Trading Portal',
            'official_url': 'https://enam.gov.in/',
            'ministry_department': 'Small Farmers Agribusiness Consortium (SFAC)',
            'helpline': '1800-270-0224',
            'description': 'Pan-India electronic trading portal networking existing APMC mandis to create a unified national market for agricultural commodities.',
            'beneficiary_criteria': 'Farmers, traders, and Farmer Producer Organizations (FPOs).'
        }
    ]
    for r in resources_data:
        GovernmentResource.objects.get_or_create(name=r['name'], defaults=r)

    # 9. Articles
    articles_data = [
        {
            'title': 'Integrated Pest Management (IPM) in Bt Cotton: A Practical Field Guide',
            'slug': 'ipm-bt-cotton-practical-guide',
            'category': 'Pest Management',
            'summary': 'Key strategies to control pink bollworm and sucking pests while conserving natural predators and minimizing chemical costs.',
            'content': """Integrated Pest Management (IPM) combines cultural, biological, and chemical tools to maintain pest populations below the Economic Threshold Level (ETL).

1. Cultural Controls:
- Plant non-Bt refuge crops or pigeon pea around field perimeters.
- Avoid extending the crop beyond 150-160 days to prevent pink bollworm diapause.
- Deep summer ploughing exposes pupae to scorching sunlight and predatory birds.

2. Monitoring:
- Install 5 pheromone traps per acre at 45 days after sowing.
- ETL for pink bollworm: 8 male moths caught per trap per night for 3 consecutive nights, or 10% damaged green bolls with live larvae.

3. Biological Suppression:
- Release Trichogramma bactrae egg parasitoids @ 60,000/acre weekly once flowering commences.
- Spray 5% Neem Seed Kernel Extract (NSKE) at early squaring.

4. Targeted Chemical Application:
- Apply chemicals only after ETL is reached. Rotate modes of action between anthranilic diamides, avermectins, and chitin synthesis inhibitors. Never tank-mix incompatible chemicals.""",
            'official_source_url': 'https://cicr.icar.gov.in/',
            'read_time_minutes': 5,
            'is_government_scheme': False,
            'image_url': 'https://images.unsplash.com/photo-1605000797499-95a51c5269ae?w=600&auto=format&fit=crop&q=80'
        },
        {
            'title': 'How to Read and Apply Your Soil Health Card Recommendations',
            'slug': 'how-to-read-soil-health-card',
            'category': 'Soil Health',
            'summary': 'Understand your NPK, pH, and organic carbon ratings to calculate exact fertilizer requirements and save on unnecessary input costs.',
            'content': """A Soil Health Card (SHC) provides a comprehensive diagnostic status of your field's soil nutrient reserves.

Key Parameters to Inspect:
1. Soil Reaction (pH):
- 6.5 to 7.5 is ideal. Below 6.0 indicates acidity; apply agricultural lime. Above 8.0 indicates alkalinity; incorporate gypsum or green manuring.

2. Organic Carbon (OC):
- Less than 0.5% indicates poor biological activity. Incorporate 5 tonnes/acre of farmyard manure or vermicompost to rejuvenate microflora.

3. Primary Macronutrients:
- Nitrogen (N): Available N below 280 kg/ha is Low.
- Phosphorus (P): Available P below 10 kg/ha is Low. Apply DAP or SSP directly in the root furrow.
- Potassium (K): Available K below 110 kg/ha is Low. Apply Muriate of Potash (MOP).

Adhering to card dosages prevents fertilizer over-application, balances soil biology, and reduces input expenditure by up to 25%.""",
            'official_source_url': 'https://soilhealth.dac.gov.in/',
            'read_time_minutes': 4,
            'is_government_scheme': True,
            'image_url': 'https://images.unsplash.com/photo-1592982537447-7440770cbfc9?w=600&auto=format&fit=crop&q=80'
        },
        {
            'title': 'Pradhan Mantri Fasal Bima Yojana (PMFBY): Complete Enrollment & Claim Process',
            'slug': 'pmfby-complete-enrollment-claim-guide',
            'category': 'Government Schemes',
            'summary': 'Step-by-step guide for Indian farmers to secure subsidized crop insurance and submit claims during droughts, floods, or pest attacks.',
            'content': """The Pradhan Mantri Fasal Bima Yojana (PMFBY) is India's flagship crop insurance scheme ensuring income stability against yield loss.

1. Subsidized Farmer Premiums:
- Kharif Crops (Food & Oilseeds): Maximum 2.0% of sum insured.
- Rabi Crops (Food & Oilseeds): Maximum 1.5% of sum insured.
- Commercial & Annual Horticultural Crops: Maximum 5.0% of sum insured.

2. Covered Risks:
- Prevented Sowing / Planting risk.
- Standing crop loss due to drought, flood, inundation, pests, and natural diseases.
- Post-harvest losses for crops kept in field for drying up to 14 days after harvesting.
- Localized calamities like hailstorm, landslide, cloudburst.

3. Claim Reporting Protocol:
- Intimate crop loss within 72 hours of the event via the Crop Insurance App, local bank branch, or toll-free number 1800-180-1551.""",
            'official_source_url': 'https://pmfby.gov.in/',
            'read_time_minutes': 6,
            'is_government_scheme': True,
            'image_url': 'https://images.unsplash.com/photo-1536704689225-7033580554c1?w=600&auto=format&fit=crop&q=80'
        },
        {
            'title': 'Modern Micro-Irrigation: Drip vs Sprinkler Water Management',
            'slug': 'modern-micro-irrigation-drip-sprinkler',
            'category': 'Irrigation',
            'summary': 'Save 40-60% water and achieve higher yields with precision drip fertigation tailored to row and field crops.',
            'content': """With erratic monsoons and receding water tables, micro-irrigation is an indispensable technology for modern farming.

Drip Irrigation Advantages:
- Delivers water and soluble nutrients directly to the root zone with up to 90% water use efficiency.
- Reduces weed germination since inter-row spaces remain dry.
- Ideal for cotton, sugarcane, banana, vegetables, and orchard fruits.

Sprinkler Irrigation Advantages:
- Simulates natural rainfall; suitable for undulating terrain and close-growing crops like wheat, pulses, groundnut, and soybean.
- Moderates microclimatic temperature extremes during heatwaves.

Government Subsidies:
Under the Pradhan Mantri Krishi Sinchayee Yojana (PMKSY - Per Drop More Crop), small and marginal farmers can avail 55% subsidy (45% for other farmers) for micro-irrigation installations.""",
            'official_source_url': 'https://pmksy.gov.in/',
            'read_time_minutes': 5,
            'is_government_scheme': False,
            'image_url': 'https://images.unsplash.com/photo-1563514227147-6d2ff665a6a0?w=600&auto=format&fit=crop&q=80'
        }
    ]
    for a in articles_data:
        Article.objects.get_or_create(slug=a['slug'], defaults=a)

    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed()

