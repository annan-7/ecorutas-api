from src.application.dto.route_dtos import CreateRouteDTO
from src.application.services.route_service import RouteService

# Catálogo inicial de rutas chilenas conocidas. Los datos operativos son referenciales.
ROUTES = [
    ("Circuito W Torres del Paine", "Magallanes", -50.9423, -73.4068),
    ("Circuito O Torres del Paine", "Magallanes", -50.9423, -73.4068),
    ("Mirador Base Torres", "Magallanes", -50.9658, -72.8749),
    ("Valle del Francés", "Magallanes", -51.0417, -73.0608),
    ("Glaciar Grey", "Magallanes", -50.9546, -73.2179),
    ("Dientes de Navarino", "Magallanes", -54.9477, -67.6561),
    ("Cerro Bandera", "Magallanes", -54.9462, -67.6427),
    ("Laguna Esmeralda", "Magallanes", -54.7055, -68.1231),
    ("Sendero Alerces Costero", "Los Ríos", -40.1834, -73.4372),
    ("Reserva Huilo Huilo", "Los Ríos", -39.8792, -71.9433),
    ("Volcán Choshuenco", "Los Ríos", -39.9275, -72.0272),
    ("Parque Oncol", "Los Ríos", -39.7001, -73.3158),
    ("Cerro Castillo", "Aysén", -46.0816, -72.0708),
    ("Laguna Cerro Castillo", "Aysén", -46.0837, -72.0649),
    ("Laguna San Rafael", "Aysén", -46.6736, -73.8603),
    ("Glaciar Exploradores", "Aysén", -46.5824, -73.1921),
    ("Jeinimeni Piedra Clavada", "Aysén", -46.8173, -71.9354),
    ("Laguna Tigre Sur", "Aysén", -45.4385, -72.1745),
    ("Ventisquero Colgante", "Aysén", -44.4713, -72.5399),
    ("Bosque Encantado Queulat", "Aysén", -44.4117, -72.5628),
    ("Volcán Villarrica", "La Araucanía", -39.4208, -71.9392),
    ("Sierra Nevada Conguillío", "La Araucanía", -38.6966, -71.6255),
    ("Sendero Los Carpinteros", "La Araucanía", -38.6616, -71.6803),
    ("Cráter Navidad", "La Araucanía", -38.6931, -71.7308),
    ("Cerro Ñielol", "La Araucanía", -38.7288, -72.5817),
    ("Parque Nacional Huerquehue", "La Araucanía", -39.1415, -71.7148),
    ("Termas de Río Blanco", "La Araucanía", -38.4932, -71.5514),
    ("Volcán Osorno", "Los Lagos", -41.1055, -72.4967),
    ("Paso Desolación", "Los Lagos", -41.1261, -72.5518),
    ("Valle de Cochamó", "Los Lagos", -41.4947, -72.2325),
    ("Laguna Fría", "Los Lagos", -41.5012, -72.1861),
    ("Parque Pumalín Cascadas Escondidas", "Los Lagos", -42.6573, -72.5686),
    ("Volcán Chaitén", "Los Lagos", -42.8358, -72.6469),
    ("Sendero El Tepual", "Los Lagos", -41.4808, -72.9379),
    ("Cerro Provincia", "Metropolitana", -33.3744, -70.4266),
    ("Cerro Manquehue", "Metropolitana", -33.3504, -70.5804),
    ("Cerro Pochoco", "Metropolitana", -33.3551, -70.5053),
    ("Aguas de Ramón", "Metropolitana", -33.4387, -70.5163),
    ("Salto de Apoquindo", "Metropolitana", -33.4487, -70.4895),
    ("Glaciar El Morado", "Metropolitana", -33.7277, -70.0645),
    ("Monumento El Morado", "Metropolitana", -33.8256, -70.0507),
    ("Cerro La Campana", "Valparaíso", -32.9583, -71.1264),
    ("Palmas de Ocoa", "Valparaíso", -32.9292, -71.0622),
    ("Sendero Los Peumos", "Valparaíso", -33.0632, -71.0968),
    ("Altos de Lircay Enladrillado", "Maule", -35.6059, -70.9768),
    ("Laguna del Alto", "Maule", -35.6136, -70.9363),
    ("Reserva Radal Siete Tazas", "Maule", -35.4576, -71.0275),
    ("Nevados de Chillán", "Ñuble", -36.8688, -71.3776),
    ("Laguna del Huemul", "Ñuble", -36.9128, -71.4546),
    ("Piedra del Águila Nahuelbuta", "La Araucanía", -37.8087, -73.0126),
    ("Laguna Chica San Pedro", "Biobío", -36.8503, -73.1011),
    ("Parque Nonguén", "Biobío", -36.8747, -72.9952),
    ("Valle de la Luna", "Antofagasta", -22.9252, -68.2865),
    ("Garganta del Diablo", "Antofagasta", -22.8646, -68.1968),
    ("Termas de Puritama", "Antofagasta", -22.7265, -68.0531),
    ("Cerro Toco", "Antofagasta", -22.9531, -67.7794),
    ("Salar de Tara", "Antofagasta", -23.0617, -67.3058),
    ("Parque Nacional Pan de Azúcar", "Atacama", -26.1456, -70.6505),
    ("Sendero Quebrada Castillo", "Atacama", -26.1439, -70.6472),
    ("Dunas de Copiapó", "Atacama", -27.4088, -70.4393),
    ("Parque Nacional Fray Jorge", "Coquimbo", -30.6687, -71.6721),
    ("Valle del Encanto", "Coquimbo", -30.6996, -71.4391),
    ("Cerro Mamalluca", "Coquimbo", -29.9908, -70.6977),
    ("Sendero Chungará", "Arica y Parinacota", -18.2493, -69.1648),
    ("Lagunas de Cotacotani", "Arica y Parinacota", -18.2095, -69.2278),
]


def build_seed_data() -> list[CreateRouteDTO]:
    data: list[CreateRouteDTO] = []
    for index, (name, region, latitude, longitude) in enumerate(ROUTES):
        difficulty = ("facil", "moderada", "dificil", "experto")[index % 4]
        distance = 4.0 + (index % 18) * 2.5
        data.append(
            CreateRouteDTO(
                name=name,
                description=(
                    f"Ruta de naturaleza ubicada en la región de {region}, Chile."
                ),
                interesting_fact=(
                    f"El recorrido permite conocer ecosistemas de {region}."
                ),
                image_url="https://images.unsplash.com/photo-1551632811-561732d1e306",
                location=region,
                distance_km=distance,
                difficulty=difficulty,
                route_type="senderismo" if index % 3 else "trekking",
                duration_hours=max(1, round(distance / 3)),
                latitude=latitude,
                longitude=longitude,
                altitude_meters=100 + (index % 20) * 120,
            )
        )
    return data


async def seed_routes(service: RouteService) -> tuple[int, int]:
    return await service.create_missing_routes(build_seed_data())
