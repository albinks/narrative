import warnings
from typing import Any

# Suppress specific deprecation warnings
warnings.filterwarnings(
    "ignore",
    message=(
        "autorefs `span` elements are deprecated in favor of " "`autoref` elements"
    ),
    category=DeprecationWarning,
)


# Define a hook function to be used in mkdocs.yml
def on_config(config: Any) -> Any:
    # This function will be called when MkDocs loads the configuration
    return config
