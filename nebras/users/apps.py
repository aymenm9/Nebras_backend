from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals
        from django.db.models.signals import post_migrate
        from users.signals import create_default_superuser
        post_migrate.connect(create_default_superuser, sender=self)
