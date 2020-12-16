class Router:
    def db_for_read(self, model, **hints):
        return 'demo' if model._meta.app_label == 'airdata' else None

    def db_for_write(self, model, **hints):
        return 'demo' if model._meta.app_label == 'airdata' else None

    def allow_relation(self, obj1, obj2, **hints):
        return 'demo' if obj1._meta.app_label == 'airdata' and obj2._meta.app_label == 'airdata' else None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return False if app_label == 'demo' else None
