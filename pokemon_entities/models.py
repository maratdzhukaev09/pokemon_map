from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name="название на русском")
    title_en = models.CharField(max_length=200, default="", verbose_name="название на английском", blank=True)
    title_jp = models.CharField(max_length=200, default="", verbose_name="название на японском", blank=True)
    picture = models.ImageField(blank=True, null=True, verbose_name="изображение")
    description = models.TextField(default="", verbose_name="описание", blank=True)
    previous_evolution = models.ForeignKey("Pokemon",
                                           on_delete=models.SET_NULL,
                                           null=True,
                                           blank=True,
                                           related_name='next_evolution',
                                           verbose_name="эволюционировал из"
                                           )

    def __str__(self):
        return f"{self.title_ru}"


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()

    appeared_at = models.DateTimeField(blank=True, null=True)
    disappeared_at = models.DateTimeField(blank=True, null=True)

    level = models.IntegerField(blank=True, null=True)
    health = models.IntegerField(blank=True, null=True)
    strength = models.IntegerField(blank=True, null=True)
    defence = models.IntegerField(blank=True, null=True)
    stamina = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.pokemon.title_ru} {self.lat} {self.lon}"
