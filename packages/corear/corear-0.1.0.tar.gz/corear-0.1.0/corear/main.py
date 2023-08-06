import os
import sys
from types import ModuleType
import importlib

class Agent:
    def run(self, example):
        print("Agent.run() called with", example)

def check_core_files():
    core_files = ["core/core.bf", "master.bf", "src/RUNME.bf"]

    for file in core_files:
        if not os.path.exists(file):
            print(f"Missing core files. Please visit aysnc.jaseunda.com")
            return False

    return True

def create_agent_module():
    agent_module = ModuleType("agent")
    agent_module.Agent = Agent
    sys.modules["agent"] = agent_module

def wrap_bot_run(module_name):
    if not check_core_files():
        return

    original_module = importlib.import_module(module_name)
    setattr(original_module, "bot", Agent())

def main():
    wrap_bot_run("example_module")
