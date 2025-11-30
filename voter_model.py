from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

class Voter(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def choice(self) -> str:
        pass

    @abstractmethod
    def get_weight(self) -> int:
        pass

    @abstractmethod
    def get_proxy_count(self) -> int:
        pass

class SimpleVoter(Voter):
    def __init__(self, name: str, choice: str):
        self._name = name
        self._choice = choice

    @property
    def name(self) -> str:
        return self._name

    @property
    def choice(self) -> str:
        return self._choice

    def get_weight(self) -> int:
        return 1

    def get_proxy_count(self) -> int:
        return 0

class MaxThreeProxiesSpec:
    """Specification to enforce the maximum of 3 proxies rule."""
    MAX_PROXIES = 3

    def calculate_allowed_proxies(self, total_proxies: int) -> int:
        return min(total_proxies, self.MAX_PROXIES)

@dataclass
class ProxyVoter(Voter):
    principal: Voter
    proxies: List[Voter]
    spec: MaxThreeProxiesSpec = MaxThreeProxiesSpec()

    @property
    def name(self) -> str:
        return self.principal.name

    @property
    def choice(self) -> str:
        return self.principal.choice

    def get_weight(self) -> int:
        base_weight = self.principal.get_weight()
        proxy_count = len(self.proxies)
        allowed_proxies = self.spec.calculate_allowed_proxies(proxy_count)
        return base_weight + allowed_proxies

    def get_proxy_count(self) -> int:
        return len(self.proxies)
