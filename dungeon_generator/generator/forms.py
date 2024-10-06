from django.core.exceptions import ValidationError
from django.forms import Form
from django import forms


class DungeonGenerationForm(Form):
    height = forms.IntegerField(min_value=3, max_value=100, initial=70)
    width = forms.IntegerField(min_value=3, max_value=100, initial=70)
    room_size_method = forms.ChoiceField(
        choices=[
            ("fixed", "Fixed"),
            ("range", "Range"),
            ("factor", "Factor of dungeon size"),
        ],
        initial="range",
        widget=forms.Select(
            attrs={
                "onchange": "toggleMethod()",
                "id": "room-size-method",
            }
        ),
    )
    room_height = forms.IntegerField(
        required=False, min_value=3, max_value=100, initial="12"
    )
    room_width = forms.IntegerField(
        required=False, min_value=3, max_value=100, initial="12"
    )
    room_min_height = forms.IntegerField(
        required=False, min_value=3, max_value=100, initial="8"
    )
    room_max_height = forms.IntegerField(
        required=False, min_value=3, max_value=100, initial="12"
    )
    room_min_width = forms.IntegerField(
        required=False, min_value=3, max_value=100, initial="8"
    )
    room_max_width = forms.IntegerField(
        required=False, min_value=3, max_value=100, initial="12"
    )
    room_min_height_factor = forms.FloatField(
        required=False, min_value=0, max_value=1, initial="0.1"
    )
    room_max_height_factor = forms.FloatField(
        required=False, min_value=0, max_value=1, initial="0.2"
    )
    room_min_width_factor = forms.FloatField(
        required=False, min_value=0, max_value=1, initial="0.1"
    )
    room_max_width_factor = forms.FloatField(
        required=False, min_value=0, max_value=1, initial="0.2"
    )
    name = forms.CharField(max_length=100, empty_value="new_dungeon")
    notes = forms.CharField(required=False)

    def clean(self):
        data = super().clean()
        room_size = (data.get("room_height"), data.get("room_width"))
        room_min_height = data.get("room_min_height")
        room_max_height = data.get("room_max_height")
        room_min_width = data.get("room_min_width")
        room_max_width = data.get("room_max_width")
        room_range = (room_min_height, room_max_height, room_min_width, room_max_width)
        room_min_height_factor = data.get("room_min_height_factor")
        room_max_height_factor = data.get("room_max_height_factor")
        room_min_width_factor = data.get("room_min_width_factor")
        room_max_width_factor = data.get("room_max_width_factor")
        room_factor = (
            room_min_height_factor,
            room_max_height_factor,
            room_min_width_factor,
            room_max_width_factor,
        )
        room_size_selected_method = data.get("room_size_method")
        mapping = {
            "fixed": room_size,
            "range": room_range,
            "factor": room_factor,
        }

        for method, object in mapping.items():
            if method == room_size_selected_method:
                if None in mapping[method]:
                    raise ValidationError(
                        f"You selected a room size method '{method}', please "
                        f"fill its arguments."
                    )
        if room_max_height:
            if room_min_height:
                if room_max_height < room_min_height:
                    raise ValidationError(
                        "Minimum dimension has to be smaller than the maximum one."
                    )
            if room_max_height > data.get("height"):
                raise ValidationError(
                    "Maximum room height cannot be larger than the height of the "
                    "dungeon."
                )
        if room_max_width:
            if room_min_width:
                if room_max_width < room_min_width:
                    raise ValidationError(
                        "Minimum dimension has to be smaller than the maximum one."
                    )
            if room_max_width > data.get("width"):
                raise ValidationError(
                    "Maximum room width cannot be larger than the width of the "
                    "dungeon."
                )
