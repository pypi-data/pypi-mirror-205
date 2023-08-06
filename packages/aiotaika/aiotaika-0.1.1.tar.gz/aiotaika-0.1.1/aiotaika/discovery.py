from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class DiscoveredTaikaController:
    """Dataclass representing a Taika Controller."""

    host: str
    port: int


async def discover_controllers() -> List[DiscoveredTaikaController]:
    """
    Returns a list of Taika CentralUnits coverable from the local network.

    :raises NotImplementedError: This function is not implemented yet!
    :return: A list of the discovered Taika CentralUnits in the local network.
    :rtype: List[:class:`DiscoveredTaikaController`]
    """
    raise NotImplementedError()
    ret: List[DiscoveredTaikaController] = []

    return ret
