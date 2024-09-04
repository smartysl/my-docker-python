"""
    All available drivers for network
"""
from .bridge_driver import BridgeDriver


drivers = {
    "bridge": BridgeDriver()
}