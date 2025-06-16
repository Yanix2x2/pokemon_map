import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon in Pokemon.objects.all():
        for pokemon_entity in PokemonEntity.objects.all():
            moscow_time = timezone.localtime(timezone.now())
            if pokemon_entity.appeared_at < moscow_time < pokemon_entity.disappeared_at: 
                add_pokemon(
                    folium_map, 
                    pokemon_entity.lat,
                    pokemon_entity.lon,
                    get_image_url(request, pokemon)
                )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': get_image_url(request, pokemon),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:   
        add_pokemon(
            folium_map, 
            pokemon_entity.lat,
            pokemon_entity.lon,
            get_image_url(request, pokemon)
        )

    pokemon_on_page = {
        'pokemon_id': pokemon.id,
        'img_url': get_image_url(request, pokemon),
        'title_ru': pokemon.title,
        'title_jp': pokemon.title_jp,
        'title_en': pokemon.title_en,
        'description': pokemon.description,
    }

    if pokemon.evolution_from:
        pokemon_on_page['previous_evolution'] = {
            'title_ru': pokemon.evolution_from.title,
            'pokemon_id': pokemon.evolution_from.id,
            'img_url': get_image_url(request, pokemon.evolution_from),
        }    

    if pokemon.evolution_to:
        pokemon_on_page['next_evolution'] = {
            'title_ru': pokemon.evolution_to.title,
            'pokemon_id': pokemon.evolution_to.id,
            'img_url': get_image_url(request, pokemon.evolution_to)
        }  

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 
        'pokemon': pokemon_on_page
    })


def get_image_url(request, pokemon):
    img_url = pokemon.image.url if pokemon.image else None
    if img_url:
        img_url = request.build_absolute_uri(img_url)
    return img_url
