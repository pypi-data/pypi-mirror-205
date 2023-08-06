from django.apps import AppConfig as DjangoAppConfig


class BuildTestAppConfig(DjangoAppConfig):
    name = 'build_test'
    label = "build_test"
    verbose_name = "Wagtail Reoako Test app"
