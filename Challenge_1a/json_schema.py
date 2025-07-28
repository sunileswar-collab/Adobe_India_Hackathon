# D:\CONNECTING_DOTS\Challenge_1a\json_schema.py

import json
import jsonschema # Make sure you have this installed: pip install jsonschema
import logging

try:
    from utils.logger import setup_logger
    logger = setup_logger()
except ImportError:
    # Fallback if utils.logger is not available (e.g., for direct testing)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


def load_schema(schema_path):
    """
    Loads a JSON schema from the specified file path.

    Args:
        schema_path (str): The path to the JSON schema file.

    Returns:
        dict: The loaded JSON schema.

    Raises:
        FileNotFoundError: If the schema file does not exist.
        json.JSONDecodeError: If the schema file contains invalid JSON.
    """
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        logger.debug(f"Schema loaded successfully from {schema_path}")
        return schema
    except FileNotFoundError:
        logger.error(f"Error: Schema file not found at {schema_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error: Invalid JSON in schema file {schema_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred while loading schema {schema_path}: {e}")
        raise


def validate_output(data, schema):
    """
    Validates a given data dictionary against a JSON schema.

    Args:
        data (dict): The data dictionary to validate.
        schema (dict): The JSON schema to validate against.

    Raises:
        jsonschema.ValidationError: If the data does not conform to the schema.
    """
    try:
        jsonschema.validate(instance=data, schema=schema)
        logger.debug("Output data successfully validated against schema.")
    except jsonschema.ValidationError as e:
        logger.error(f"JSON schema validation failed: {e.message}") # e.message provides a more concise error
        # print(e.path) # You can uncomment this for more detailed path info if needed
        # print(e.instance) # And the instance that caused the error
        raise # Re-raise the exception so process_pdfs.py can catch it
    except Exception as e:
        logger.error(f"An unexpected error occurred during schema validation: {e}")
        raise

