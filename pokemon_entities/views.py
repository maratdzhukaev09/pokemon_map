import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon
from .models import PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in Pokemon.objects.all():
        for pokemon_entity in PokemonEntity.objects.filter(pokemon=pokemon):
            add_pokemon(
                folium_map,
                pokemon_entity.lat,
                pokemon_entity.lon,
                pokemon.title_ru,
                request.build_absolute_uri(pokemon.picture.url)
            )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.picture.url,
            'title_ru': pokemon.title_ru,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=int(pokemon_id))
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon_next_evolution_dict = None
    pokemon_previous_evolution_dict = None
    pokemon_next_evolution = requested_pokemon.next_evolution.first()
    pokemon_previous_evolution = requested_pokemon.previous_evolution
    if pokemon_next_evolution:
        pokemon_next_evolution_dict = {
            "title_ru": pokemon_next_evolution.title_ru,
            "pokemon_id": pokemon_next_evolution.id,
            "img_url": pokemon_next_evolution.picture.url
        }
    if pokemon_previous_evolution:
        pokemon_previous_evolution_dict = {
            "title_ru": pokemon_previous_evolution.title_ru,
            "pokemon_id": pokemon_previous_evolution.id,
            "img_url": pokemon_previous_evolution.url
        }

    pokemon_dict = {
        "pokemon_id": requested_pokemon.id,
        "title_ru": requested_pokemon.title_ru,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "description": requested_pokemon.description,
        "img_url": requested_pokemon.photo.url,
        "next_evolution": pokemon_next_evolution_dict,
        "previous_evolution": pokemon_previous_evolution_dict
    }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.filter(pokemon=requested_pokemon):
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon.title_ru,
            request.build_absolute_uri(pokemon.photo.url)
        )

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_dict})
