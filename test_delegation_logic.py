import unittest
from voter_model import SimpleVoter, ProxyVoter

class TestDelegationLogic(unittest.TestCase):
    def test_simple_voter_weight(self):
        v = SimpleVoter("Test", "Approvo")
        self.assertEqual(v.get_weight(), 1)

    def test_proxy_voter_weight_under_limit(self):
        principal = SimpleVoter("Principal", "Approvo")
        proxies = [SimpleVoter(f"Proxy{i}", "DELEGATED") for i in range(2)]
        v = ProxyVoter(principal, proxies)
        # 1 principal + 2 proxies = 3
        self.assertEqual(v.get_weight(), 3)

    def test_proxy_voter_weight_at_limit(self):
        principal = SimpleVoter("Principal", "Approvo")
        proxies = [SimpleVoter(f"Proxy{i}", "DELEGATED") for i in range(3)]
        v = ProxyVoter(principal, proxies)
        # 1 principal + 3 proxies = 4
        self.assertEqual(v.get_weight(), 4)

    def test_proxy_voter_weight_over_limit(self):
        principal = SimpleVoter("Principal", "Approvo")
        proxies = [SimpleVoter(f"Proxy{i}", "DELEGATED") for i in range(5)]
        v = ProxyVoter(principal, proxies)
        # 1 principal + 3 (capped) = 4
        self.assertEqual(v.get_weight(), 4)

if __name__ == '__main__':
    unittest.main()
