import sys, importlib.util
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent

def __import_agent_runner():
    """Import agent_runner module from .agents/tools/"""
    p = PROJECT / ".agents" / "tools" / "lib" / "agent-runner.py"
    spec = importlib.util.spec_from_file_location("agent_runner", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_ar = __import_agent_runner()
run_agent = _ar.run_agent
launch_agent = _ar.launch_agent
get_agent_command = _ar.get_agent_command
