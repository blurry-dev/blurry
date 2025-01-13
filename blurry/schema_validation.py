import importlib
from collections.abc import MutableMapping
from pathlib import Path

from pydantic.v1 import ValidationError
from rich.console import Console

from blurry.settings import SETTINGS


def validate_front_matter_as_schema(
    path: Path, schema_variables: MutableMapping, console: Console
):
    """
    Validates schema data using pydantic_schemaorg, disallowing extra fields
    """
    schema_type = schema_variables["@type"]

    if mapped_schema_type := SETTINGS["TEMPLATE_SCHEMA_TYPES"].get(schema_type):
        schema_type = mapped_schema_type

    # Import pydantic_schemaorg model
    try:
        pydantic_schemaorg_model_module = importlib.import_module(
            f"pydantic2_schemaorg.{schema_type}"
        )
    except ModuleNotFoundError:
        console.print(
            f"{path}: Could not find Schema type for {schema_type}. Skipping."
        )
        return

    SchemaModel = getattr(pydantic_schemaorg_model_module, schema_type)

    # Create new Pydantic model that forbids extra fields
    class SchemaModelWithoutExtraFields(SchemaModel, extra="forbid"):  # type: ignore
        pass

    # Validate model and print errors
    try:
        SchemaModelWithoutExtraFields(**schema_variables)
    except ValidationError as e:
        for error in e.errors():
            msg = error["msg"]
            loc = error["loc"]
            console.print(
                f"{path}: {schema_type} schema validation error: {msg}: {loc}"
            )
