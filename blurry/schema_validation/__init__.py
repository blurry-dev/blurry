from collections.abc import MutableMapping
from pathlib import Path

from pydantic import ValidationError
from rich.console import Console

from blurry.schema_validation import models
from blurry.settings import get_settings


def validate_front_matter_as_schema(
    path: Path, schema_variables: MutableMapping, console: Console
):
    """
    Validates schema data using partial Schema.org types based on Google's support for them:
    https://developers.google.com/search/docs/appearance/structured-data/search-gallery
    """
    SETTINGS = get_settings()
    schematype = schema_variables["@type"]

    if mapped_schematype_ := SETTINGS["TEMPLATE_SCHEMA_TYPES"].get(schematype):
        schematype = mapped_schematype_

    # Validate model and print errors
    try:
        SchemaModel = getattr(models, schematype)
        SchemaModel(**schema_variables)
    except AttributeError:
        console.print(
            f"{path}: validation not yet supported for {schematype}. Skipping."
        )
    except ValidationError as err:
        for error in err.errors():
            msg = error["msg"]
            loc = error["loc"]
            if len(loc) == 1:
                loc = loc[0]
            console.print(f"{path}: {schematype} schema validation error: {msg}: {loc}")
