class IdentityVaultRouter:
    """
    Router che dirige i modelli di identity_vault verso il database 'identity_db'
    e tutti gli altri verso il database 'default'.

    Questo garantisce che i dati identificativi (nomi, CF) siano fisicamente
    separati dai dati clinici pseudonimizzati.
    """
    identity_app = 'identity_vault'

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.identity_app:
            return 'identity_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.identity_app:
            return 'identity_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Non permettere relazioni tra i due database
        app1 = obj1._meta.app_label
        app2 = obj2._meta.app_label
        if app1 == self.identity_app or app2 == self.identity_app:
            return app1 == app2
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == self.identity_app:
            return db == 'identity_db'
        return db == 'default'
