import importlib
from collections.abc import MutableMapping
from pathlib import Path

from pydantic.v1 import ValidationError
from rich.console import Console

from blurry.settings import SETTINGS
from blurry.settings import update_settings


class Config:
    extra = "forbid"


def validate_front_matter_as_schema(
    path: Path, front_matter: MutableMapping, console: Console
):
    """
    Validates schema data using pydantic_schemaorg, disallowing extra fields
    """
    update_settings()

    schema_type = front_matter["@type"]

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

    schema_model = getattr(pydantic_schemaorg_model_module, schema_type)

    # Create new Pydantic model that forbids extra fields
    class NonExtraSchemaModel(schema_model, extra="forbid"):  # type: ignore
        pass

    # Validate model and print errors
    try:
        non_schema_variable_prefix = SETTINGS["FRONTMATTER_NON_SCHEMA_VARIABLE_PREFIX"]
        schema_front_matter = {
            k: v
            for k, v in front_matter.items()
            if not k.startswith(non_schema_variable_prefix)
        }
        NonExtraSchemaModel(**schema_front_matter)
    except ValidationError as e:
        for error in e.errors():
            msg = error["msg"]
            loc = error["loc"]
            console.print(
                f"{path}: {schema_type} schema validation error: {msg}: {loc}"
            )
