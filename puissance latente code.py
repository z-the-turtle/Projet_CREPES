def puissance_latente(latitude, longitude, is_day):
    """
    Calcule la puissance latente Φ en W/m² selon la latitude, longitude et le moment (jour/nuit).
    """

    Lv = 2.26e6  # chaleur latente de vaporisation en J/kg

    # Attribution de zones selon lat/lon
    if abs(latitude) < 10:
        # Zone équatoriale : forêt tropicale
        phi = 2.0e-5
    elif abs(latitude) > 60 and is_snowy_region(latitude, longitude):
        # Zone froide et enneigée
        phi = 0.5e-6
    elif abs(latitude) > 60:
        # Zone froide (glace / neige)
        phi = 1.0e-6
    elif is_desert(latitude, longitude):
        # Désert chaud (ex: Sahara, Australie centrale)
        phi = 2.0e-6
    elif is_forest(latitude, longitude):
        # Forêt tempérée
        phi = 2.0e-5
    elif is_ocean(latitude, longitude):
        phi = 1.3e-5
    else:
        # Sol nu (par défaut)
        phi = 5.0e-6

    # Signe de Φ selon jour/nuit
    signe = +1 if is_day else -1

    # Calcul de la puissance latente
    phi_latente = signe * Lv * phi  # en W/m²

    return phi_latente
