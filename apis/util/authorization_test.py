import unittest
import os
import logging
from apis.util.authorization import has_access


class AuthorizationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)

    def test_missing_ladon(self) -> None:
        old_ladon_url = ""
        try:
            old_ladon_url = os.environ["LADON_URL"]
        except KeyError:
            pass
        os.environ["LADON_URL"] = ""
        self.assertFalse(has_access("", "", ""))
        if old_ladon_url != "":
            os.environ["LADON_URL"] = old_ladon_url

    @unittest.skipIf("LADON_URL" not in os.environ, "LADON_URL not set")
    def test_admin(self) -> None:
        self.assertTrue(has_access("admin", "/test", "GET"))

    @unittest.skipIf("LADON_URL" not in os.environ, "LADON_URL not set")
    def test_user_no_access(self) -> None:
        self.assertFalse(has_access("user", "/this-path-does-not-exist", "GET"))

if __name__ == '__main__':
    unittest.main()
