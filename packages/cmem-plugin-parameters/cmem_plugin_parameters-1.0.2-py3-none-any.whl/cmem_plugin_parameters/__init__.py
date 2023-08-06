"""Entities generation plugin to configure tasks in workflows."""
from typing import Sequence

from cmem_plugin_base.dataintegration.context import (
    ExecutionContext,
    ExecutionReport,
)
from cmem_plugin_base.dataintegration.description import Plugin, PluginParameter
from cmem_plugin_base.dataintegration.entity import (
    Entities,
    Entity,
    EntityPath,
    EntitySchema,
)
from cmem_plugin_base.dataintegration.parameter.multiline import (
    MultilineStringParameterType,
)
from cmem_plugin_base.dataintegration.plugins import WorkflowPlugin
from yaml import safe_load, YAMLError

DESCRIPTION = """Connect this task to a config port of another task in order to set
or overwrite the parameter values of this task."""

YAML_EXAMPLE = """
```
url: http://example.org
method: GET
query: |
    SELECT ?s
    WHERE {{
      ?s ?p ?o
    }}
execute_once: True
limit: 5
```
"""

DOCUMENTATION = f"""{DESCRIPTION}

To configure this task, add one `key: value` pair per line to the Parameter
Configuration multiline field (YAML syntax). `key` is the ID of the parameter
you want to set or update, `value` is the new value to set.

You can also use multiline values with `|`
(be aware of the correct indentation with spaces, not tabs).

Example parameter configuration:

{YAML_EXAMPLE}
"""

DESC_PARAMETERS = f"""Your parameter configuration in YAML Syntax.
One 'parameter: value' pair per line.

{YAML_EXAMPLE}
"""


def yaml_to_entities(yaml_string: str):
    """Generate entities from the yaml string."""
    parameters = safe_load(yaml_string)
    if not isinstance(parameters, dict):
        raise ValueError("We need at least one line 'key: value' here.")
    value_counter = 0
    values = []
    paths = []
    for key, value in parameters.items():
        if type(value) in (str, int, float, bool):
            paths.append(EntityPath(path=key))
            values.append([str(value)])
            value_counter += 1
    entities = [Entity(uri="urn:Parameter", values=values)]
    return (
        Entities(
            entities=entities,
            schema=EntitySchema(type_uri="urn:ParameterSettings", paths=paths),
        ),
        value_counter,
    )


@Plugin(
    label="Set or Overwrite parameter values",
    plugin_id="cmem_plugin_parameters-ParametersPlugin",
    description=DESCRIPTION,
    documentation=DOCUMENTATION,
    parameters=[
        PluginParameter(
            name="parameters",
            label="Parameter Configuration",
            param_type=MultilineStringParameterType(),
            description=DESC_PARAMETERS,
        )
    ],
)
class ParametersPlugin(WorkflowPlugin):
    """Entities generation plugin to configure tasks in workflows."""

    def __init__(self, parameters: str) -> None:
        try:
            self.entities, self.total_params = yaml_to_entities(parameters)
        except YAMLError as error:
            raise ValueError(f"Error in parameter input: {str(error)}") from error

    def execute(
        self, inputs: Sequence[Entities], context: ExecutionContext
    ) -> Entities:
        context.report.update(
            ExecutionReport(
                entity_count=self.total_params,
                operation="write",
                operation_desc="parameters",
            )
        )
        return self.entities
