import re

from django.core.exceptions import ValidationError


class YouTubeValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, data):
        value = data.get(self.field)

        if value:
            youtube_pattern = r"(https?://)?(www\.)?(youtube\.com)/.+"

            if not re.match(youtube_pattern, value):
                raise ValidationError(
                    {self.field: "Разрешены только ссылки на YouTube"}
                )

        return data
