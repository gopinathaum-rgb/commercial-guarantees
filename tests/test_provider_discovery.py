import unittest
from scripts.provider_discovery import Links

class ProviderDiscoveryTests(unittest.TestCase):
    def test_extracts_only_india_partner_profile_links(self):
        html = '''
        <a href="/partners/india/acme-consulting">Acme Consulting</a>
        <a href="/partners/usa/acme">Not India</a>
        <a href="https://example.com">External</a>
        <a href="/partners/india/another-partner">Another Partner</a>
        '''
        parser=Links(); parser.feed(html)
        self.assertEqual(parser.items, [
            ("Acme Consulting","https://frappe.io/partners/india/acme-consulting"),
            ("Another Partner","https://frappe.io/partners/india/another-partner")
        ])

    def test_ignores_empty_profile_anchor(self):
        parser=Links(); parser.feed('<a href="/partners/india/empty">  </a>')
        self.assertEqual(parser.items, [])

if __name__=="__main__": unittest.main()
