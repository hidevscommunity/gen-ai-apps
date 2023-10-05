import os
import glob
import importlib
from utils.helpers import annotate

# Get a list of all Python files (agents) in the current directory
agent_files = glob.glob(os.path.dirname(__file__) + "/*.py")

# Exclude __init__.py itself
agent_files = [f for f in agent_files if not f.endswith("__init__.py")  and not '$' in f]

# Import all agent modules dynamically and populate the agents_classes dictionary
agents_classes = {}
for agent_file in agent_files:
    module_name = os.path.basename(agent_file)[:-3]  # Remove '.py' extension
    module = importlib.import_module(f".{module_name}", package=__name__)

    #agent_class = getattr(module, f"Agent{module_name[-1]}")  # Assuming the class name follows a pattern
    agents_classes[f'{module.name}'] = {'func': module.agent,'arguments':module.arguments,'annotated':annotate(module.annotated,module.arguments)}

# Expose the agents_classes dictionary as part of the package's public interface
__all__ = ['agents_classes']