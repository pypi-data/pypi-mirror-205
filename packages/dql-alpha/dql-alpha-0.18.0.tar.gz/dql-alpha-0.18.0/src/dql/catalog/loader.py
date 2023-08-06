import os
from importlib import import_module

from dql.catalog import Catalog
from dql.data_storage import SQLiteDataStorage


def get_catalog(client_config=None) -> Catalog:
    db_adapter_import_path = os.environ.get("DQL_DB_ADAPTER")
    if db_adapter_import_path:
        # DB Adapter paths are specified as (for example):
        # dql.data_storage.SQLiteDataStorage
        if "." not in db_adapter_import_path:
            raise RuntimeError(
                f"Invalid DQL_DB_ADAPTER import path: {db_adapter_import_path}"
            )
        module_name, _, class_name = db_adapter_import_path.rpartition(".")
        db_adapter = import_module(module_name)
        db_adapter_class = getattr(db_adapter, class_name)
    else:
        db_adapter_class = SQLiteDataStorage
    return Catalog(db_adapter_class(), client_config=client_config)
