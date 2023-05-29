import json
import logging
from unittest import TestCase, skipIf

from parameterized import parameterized, param

from tests import utils
from tests.utils.hvac_integration_test_case import HvacIntegrationTestCase


@skipIf(
    utils.vault_version_lt("1.5.0"),
    "Password policy support available >= Vault 1.5.0",
)
class TestPasswordPolicy(HvacIntegrationTestCase, TestCase):
    TEST_POLICY_NAME = "test-password-policy"

    def tearDown(self):
        self.client.sys.delete_password_policy(
            name=self.TEST_POLICY_NAME,
        )
        super().tearDown()

    @parameterized.expand(
        [
            param(
                "success",
            ),
            param(
                "pretty print false",
                pretty_print=False,
            ),
        ]
    )
    def test_create_or_update_password_policy(self, label, pretty_print=True):
        test_password_policy = """
            length=12

            rule "charset" {
              charset = "abcdefghijklmnopqrstuvwxyz"
              min-chars = 1
            }

            rule "charset" {
              charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
              min-chars = 1
            }

            rule "charset" {
              charset = "0123456789"
              min-chars = 1
            }
        """
        create_password_policy_response = self.client.sys.create_or_update_password_policy(
            name=self.TEST_POLICY_NAME,
            policy=test_password_policy,
            pretty_print=pretty_print,
        )
        logging.debug("create_password_policy_response: %s" % create_password_policy_response)
        self.assertEqual(
            first=bool(create_password_policy_response),
            second=True,
        )

        read_password_policy_response = self.client.sys.read_password_policy(
            name=self.TEST_POLICY_NAME,
        )
        logging.debug("read_password_policy_response: %s" % read_password_policy_response)
        self.assertEqual(
            read_password_policy_response["data"]["policy"],
            test_password_policy,
        )

        changed_password_policy = """
            length=17

            rule "charset" {
              charset = "abcdefghijklmnopqrstuvwxyz"
              min-chars = 2
            }

            rule "charset" {
              charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
              min-chars = 2
            }

            rule "charset" {
              charset = "0123456789"
              min-chars = 2
            }

            rule "charset" {
              charset = "~!@#%^&*()_+-=|{};:,.<>/?"
              min-chars = 2
            }
        """
        create_password_policy_response = self.client.sys.create_or_update_password_policy(
            name=self.TEST_POLICY_NAME,
            policy=changed_password_policy,
            pretty_print=pretty_print,
        )
        logging.debug("create_password_policy_response: %s" % create_password_policy_response)
        self.assertEqual(
            first=bool(create_password_policy_response),
            second=True,
        )

        parsed_password_policy = self.client.get_password_policy(self.TEST_POLICY_NAME)
        self.assertEqual(parsed_password_policy, changed_password_policy)

    def test_read_password_policy(self, pretty_print=True):
        test_password_policy = """
            length=17

            rule "charset" {
              charset = "abcdefghijklmnopqrstuvwxyz"
              min-chars = 2
            }

            rule "charset" {
              charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
              min-chars = 2
            }

            rule "charset" {
              charset = "0123456789"
              min-chars = 2
            }

            rule "charset" {
              charset = "~!@#%^&*()_+-=|{};:,.<>/?"
              min-chars = 2
            }
        """
        create_password_policy_response = self.client.sys.create_or_update_password_policy(
            name=self.TEST_POLICY_NAME,
            policy=test_password_policy,
            pretty_print=pretty_print,
        )
        read_password_policy_response = self.client.sys.read_password_policy(
            name=self.TEST_POLICY_NAME,
        )
        logging.debug("read_password_policy_response: %s" % read_password_policy_response)

    def test_generate_password_from_policy(self, pretty_print=True):
        test_password_policy = """
            length=17

            rule "charset" {
              charset = "abcdefghijklmnopqrstuvwxyz"
              min-chars = 2
            }

            rule "charset" {
              charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
              min-chars = 2
            }

            rule "charset" {
              charset = "0123456789"
              min-chars = 2
            }

            rule "charset" {
              charset = "~!@#%^&*()_+-=|{};:,.<>/?"
              min-chars = 2
            }
        """
        create_password_policy_response = self.client.sys.create_or_update_password_policy(
            name=self.TEST_POLICY_NAME,
            policy=test_password_policy,
            pretty_print=pretty_print,
        )
        generate_password_response = self.client.sys.generate_password_from_policy(self.TEST_POLICY_NAME)
        self.assertIsNotNone(generate_password_response)
        logging.debug("generate_password_from_policy response: %s" % generate_password_response)

    def test_delete_password_policy(self, pretty_print=True):
        test_password_policy = """
            length=17

            rule "charset" {
              charset = "abcdefghijklmnopqrstuvwxyz"
              min-chars = 2
            }

            rule "charset" {
              charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
              min-chars = 2
            }

            rule "charset" {
              charset = "0123456789"
              min-chars = 2
            }

            rule "charset" {
              charset = "~!@#%^&*()_+-=|{};:,.<>/?"
              min-chars = 2
            }
        """
        create_password_policy_response = self.client.sys.create_or_update_password_policy(
            name=self.TEST_POLICY_NAME,
            policy=test_password_policy,
            pretty_print=pretty_print,
        )
        self.client.sys.delete_password_policy(
            name=self.TEST_POLICY_NAME,
        )
        self.assertIsNone(self.client.get_password_policy(self.TEST_POLICY_NAME))
