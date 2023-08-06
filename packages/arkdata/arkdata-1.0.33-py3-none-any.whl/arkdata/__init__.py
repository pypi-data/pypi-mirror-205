from . import models
from .import blueprints


def create_all():
    blueprints.create_all_blueprints()
    models.create_all_models()


def clear_all():
    blueprints.clear_all_blueprints()
    models.clear_all_models()


def drop_all():
    blueprints.drop_all_blueprints()
    models.drop_all_models()


def seed_all():
    blueprints.seed_all_blueprints()
    models.seed_all_models()


__all__ = ['models', 'blueprints']
