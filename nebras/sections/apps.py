from django.apps import AppConfig


class SectionsConfig(AppConfig):
    name = 'sections'

    def ready(self):
        import sections.signals
