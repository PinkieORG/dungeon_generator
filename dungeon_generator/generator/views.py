from django.contrib import messages
from django.shortcuts import redirect, render
from hamingja_dungeon.utils.ascii_dungeon_generator.ascii_dungeon_generator import (
    ASCIIDungeonGenerator,
)

from .config_map.mapping import get_dungeon_generator_config
from .forms import DungeonGenerationForm
from .models import Dungeon

MAPPING_FILE_PATH = "dungeon_generator/generator/config_map/mapping.yaml"


def home(request):
    if request.method == "GET":
        generation_form_data = request.session.get("generation_form_data")
        if generation_form_data:
            generation_form = DungeonGenerationForm(generation_form_data)
        else:
            generation_form = DungeonGenerationForm()
        dungeons = Dungeon.objects.all()
        context = {"dungeons": dungeons, "generation_form": generation_form}
        return render(request, "generator/home.html", context)
    elif request.method == "POST":
        if "generate_dungeon" in request.POST:
            Dungeon.objects.all().delete()
            generation_form = DungeonGenerationForm(request.POST)
            request.session["generation_form_data"] = request.POST
            if generation_form.is_valid():
                form_data = generation_form.cleaned_data
                config = get_dungeon_generator_config(form_data, MAPPING_FILE_PATH)
                generator = ASCIIDungeonGenerator(config)
                dungeon = generator.generate()
                Dungeon.objects.create(content=dungeon.content)
            else:
                messages.error(request, "Please correct the following errors:")
        elif "remove_dungeons" in request.POST:
            Dungeon.objects.all().delete()
    return redirect("home")
