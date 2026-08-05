COUNTRY_ALIASES = {
    # Amériques
    "usa": "US",
    "u.s.a": "US",
    "u.s.": "US",
    "america": "US",
    "united states": "US",
    "united states of america": "US",
    "canada": "CA",
    "brazil": "BR",
    "brésil": "BR",
    "mexico": "MX",
    "mexique": "MX",
    
    # Europe
    "uk": "GB",
    "u.k.": "GB",
    "britain": "GB",
    "england": "GB",
    "united kingdom": "GB",
    "royaume-uni": "GB",
    "germany": "DE",
    "allemagne": "DE",
    "france": "FR",
    "italy": "IT",
    "italie": "IT",
    "spain": "ES",
    "espagne": "ES",
    "netherlands": "NL",
    "pays-bas": "NL",
    "holland": "NL",
    "belgium": "BE",
    "belgique": "BE",
    "switzerland": "CH",
    "suisse": "CH",
    "russia": "RU",
    "russie": "RU",
    "turkey": "TR",
    "turquie": "TR",
    
    # Moyen-Orient & Asie
    "uae": "AE",
    "dubai": "AE",
    "united arab emirates": "AE",
    "émirats arabes unis": "AE",
    "qatar": "QA",
    "saudi arabia": "SA",
    "arabie saoudite": "SA",
    "india": "IN",
    "inde": "IN",
    "bangladesh": "BD",
    "japan": "JP",
    "japon": "JP",
    "china": "CN",
    "chine": "CN",
    "south korea": "KR",
    "korea": "KR",
    "corée du sud": "KR",
    "singapore": "SG",
    "singapour": "SG",
    "malaysia": "MY",
    "malaisie": "MY",
    "thailand": "TH",
    "thaïlande": "TH",
    "indonesia": "ID",
    "indonésie": "ID",
    "vietnam": "VN",
    "nepal": "NP",
    
    # Afrique de l'Ouest & Centrale
    "togo": "TG",
    "république togolaise": "TG",
    "benin": "BJ",
    "bénin": "BJ",
    "ghana": "GH",
    "ivory coast": "CI",
    "côte d'ivoire": "CI",
    "cote d'ivoire": "CI",
    "nigeria": "NG",
    "nigéria": "NG",
    "senegal": "SN",
    "sénégal": "SN",
    "burkina faso": "BF",
    "burkina": "BF",
    "mali": "ML",
    "niger": "NE",
    "cameroon": "CM",
    "cameroun": "CM",
    "gabon": "GA",
    "congo": "CG",
    
    # Afrique du Nord & Sud
    "morocco": "MA",
    "maroc": "MA",
    "tunisia": "TN",
    "tunisie": "TN",
    "egypt": "EG",
    "égypte": "EG",
    "south africa": "ZA",
    "afrique du sud": "ZA",
    
    # Océanie
    "australia": "AU",
    "australie": "AU",
}


COUNTRY_MAIN_AIRPORT = {
    # Amériques
    "US": "JFK",  # New York John F. Kennedy
    "CA": "YYZ",  # Toronto Pearson
    "BR": "GRU",  # São Paulo Guarulhos
    "MX": "MEX",  # Mexico City Juarez
    
    # Europe
    "GB": "LHR",  # London Heathrow
    "DE": "FRA",  # Frankfurt
    "FR": "CDG",  # Paris Charles de Gaulle
    "IT": "FCO",  # Rome Fiumicino
    "ES": "MAD",  # Madrid Barajas
    "NL": "AMS",  # Amsterdam Schiphol
    "BE": "BRU",  # Bruxelles National
    "CH": "ZRH",  # Zurich
    "RU": "SVO",  # Moscou Sheremetyevo
    "TR": "IST",  # Istanbul
    
    # Moyen-Orient & Asie
    "AE": "DXB",  # Dubai International
    "QA": "DOH",  # Doha Hamad
    "SA": "JED",  # Djeddah King Abdulaziz
    "IN": "DEL",  # Delhi Indira Gandhi
    "BD": "DAC",  # Dhaka Hazrat Shahjalal
    "JP": "NRT",  # Tokyo Narita
    "CN": "PEK",  # Pékin Capital
    "KR": "ICN",  # Séoul Incheon
    "SG": "SIN",  # Singapour Changi
    "MY": "KUL",  # Kuala Lumpur
    "TH": "BKK",  # Bangkok Suvarnabhumi
    "ID": "CGK",  # Jakarta Soekarno-Hatta
    "VN": "SGN",  # Hô Chi Minh-Ville
    "NP": "KTM",  # Katmandou
    
    # Afrique
    "TG": "LFW",  # Lomé-Tokoin
    "BJ": "COO",  # Cotonou Cadjehoun
    "GH": "ACC",  # Accra Kotoka
    "CI": "ABJ",  # Abidjan Félix Houphouët-Boigny
    "NG": "LOS",  # Lagos Murtala Muhammed
    "SN": "DSS",  # Dakar Blaise Diagne
    "BF": "OUA",  # Ouagadougou
    "ML": "BKO",  # Bamako-Sénou
    "NE": "NIM",  # Niamey Diori Hamani
    "CM": "DLA",  # Douala
    "GA": "LBV",  # Libreville Leon M'ba
    "MA": "CMN",  # Casablanca Mohammed V
    "TN": "TUN",  # Tunis-Carthage
    "EG": "CAI",  # Le Caire
    "ZA": "JNB",  # Johannesbourg OR Tambo
    
    # Océanie
    "AU": "SYD",  # Sydney Kingsford Smith
}

CITY_MAIN_AIRPORT = {
    # Asie & Moyen-Orient
    "dhaka": "DAC",
    "delhi": "DEL",
    "new delhi": "DEL",
    "mumbai": "BOM",
    "kolkata": "CCU",
    "chennai": "MAA",
    "bangalore": "BLR",
    "bengaluru": "BLR",
    "tokyo": "NRT",
    "osaka": "KIX",
    "kyoto": "KIX",
    "pekin": "PEK",
    "beijing": "PEK",
    "shanghai": "PVG",
    "hong kong": "HKG",
    "seoul": "ICN",
    "séoul": "ICN",
    "singapore": "SIN",
    "singapour": "SIN",
    "kuala lumpur": "KUL",
    "bangkok": "BKK",
    "jakarta": "CGK",
    "ho chi minh": "SGN",
    "saigon": "SGN",
    "dubai": "DXB",
    "dubaï": "DXB",
    "doha": "DOH",
    "jeddah": "JED",
    "djeddah": "JED",
    "riyadh": "RUH",
    "riyad": "RUH",
    "istanbul": "IST",
    "kathmandu": "KTM",
    "katmandou": "KTM",
    
    # Amériques & Océanie
    "new york": "JFK",
    "los angeles": "LAX",
    "miami": "MIA",
    "toronto": "YYZ",
    "montreal": "YUL",
    "montréal": "YUL",
    "sao paulo": "GRU",
    "são paulo": "GRU",
    "rio de janeiro": "GIG",
    "mexico": "MEX",
    "sydney": "SYD",
    
    # Europe
    "london": "LHR",
    "londres": "LHR",
    "paris": "CDG",
    "rome": "FCO",
    "madrid": "MAD",
    "frankfurt": "FRA",
    "francfort": "FRA",
    "amsterdam": "AMS",
    "bruxelles": "BRU",
    "brussels": "BRU",
    "zurich": "ZRH",
    "geneve": "GVA",
    "genève": "GVA",
    "moscou": "SVO",
    "moscow": "SVO",
    
    # Afrique
    "lome": "LFW",
    "lomé": "LFW",
    "cotonou": "COO",
    "accra": "ACC",
    "abidjan": "ABJ",
    "lagos": "LOS",
    "abuja": "ABV",
    "dakar": "DSS",
    "ouagadougou": "OUA",
    "bamako": "BKO",
    "niamey": "NIM",
    "douala": "DLA",
    "yaounde": "NSI",
    "yaoundé": "NSI",
    "libreville": "LBV",
    "brazzaville": "BZV",
    "casablanca": "CMN",
    "tunis": "TUN",
    "le caire": "CAI",
    "cairo": "CAI",
    "johannesburg": "JNB",
    "johannesbourg": "JNB",
}
    