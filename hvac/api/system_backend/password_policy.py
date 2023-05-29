import json

from hvac import utils
from hvac.api.system_backend.system_backend_mixin import SystemBackendMixin


class PasswordPolicy(SystemBackendMixin):
    def read_password_policy(self, name):
        """Retrieve the policy body for the named password policy.

        Supported methods:
            GET: /sys/policies/password/{name}. Produces: 200 application/json

        :param name: The name of the password policy to retrieve.
        :type name: str | unicode
        :return: The response of the request
        :rtype: dict
        """
        api_path = utils.format_url("/v1/sys/policies/password/{name}", name=name)
        return self._adapter.get(
            url=api_path,
        )

    def create_or_update_password_policy(self, name, policy, pretty_print=True):
        """Add a new or update an existing password policy.

        Once a policy is updated, it takes effect immediately to all associated users.

        Supported methods:
            PUT: /sys/policies/password/{name}. Produces: 204 (empty body)

        :param name: Specifies the name of the password policy to create.
        :type name: str | unicode
        :param policy: Specifies the password policy document.
        :type policy: str | unicode | dict
        :param pretty_print: If True, and provided a dict for the policy argument, send the policy JSON to Vault with
            "pretty" formatting.
        :type pretty_print: bool
        :return: The response of the request.
        :rtype: requests.Response
        """
        if isinstance(policy, dict):
            if pretty_print:
                policy = json.dumps(policy, indent=4, sort_keys=True)
            else:
                policy = json.dumps(policy)
        params = {
            "policy": policy,
        }
        api_path = utils.format_url("/v1/sys/policies/password/{name}", name=name)
        return self._adapter.put(
            url=api_path,
            json=params,
        )

    def delete_password_policy(self, name):
        """Delete the password policy with the given name.

        This will immediately affect all users associated with this policy.

        Supported methods:
            DELETE: /sys/policies/password/{name}. Produces: 204 (empty body)

        :param name: Specifies the name of the password policy to delete.
        :type name: str | unicode
        :return: The response of the request.
        :rtype: requests.Response
        """
        api_path = utils.format_url("/v1/sys/policies/password/{name}", name=name)
        return self._adapter.delete(
            url=api_path,
        )

    def generate_password_from_policy(self, name):
        """Generate a password using the named password policy.

        Supported methods:
            GET: /sys/policies/password/{name}/generate. Produces: 200 application/json

        :return: The JSON response of the request.
        :rtype: dict
        """
        api_path = utils.format_url("/v1/sys/policies/password/{name}/generate", name=name)
        return self._adapter.get(
            url=api_path,
        )


