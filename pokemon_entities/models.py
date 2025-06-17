from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Имя')
    image = models.ImageField(
        upload_to='media',
        null=True,
        verbose_name='Картинка'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    title_en = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Имя на английском'
    )
    title_jp = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Имя на японском'
    )
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='next_evolutions',
        verbose_name='Эволюционировал из' 
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Покемон'
        verbose_name_plural = 'Покемоны'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Покемон',
        related_name='pokemon_entities'
    )
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(null=True, verbose_name='Появится в')
    disappeared_at = models.DateTimeField(null=True, verbose_name='Исчезнет в')
    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, blank=True, verbose_name='Сила')
    defence = models.IntegerField(null=True, blank=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='Выносливость')

    def __str__(self):
        return f'{self.id} {self.pokemon.title}'

    class Meta:
        verbose_name = 'Экземпляр покемона'
        verbose_name_plural = 'Экземпляры покемонов'
