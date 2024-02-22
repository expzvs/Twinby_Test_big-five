from requests import Response
import json

class Assertions:

    @staticmethod
    def assert_json(response: Response):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in Json format, Res text is '{response.text}'"

        return response_as_dict

    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        # try:
        #     response_as_dict = response.json()
        # except json.JSONDecodeError:
        #     assert False, f"Response is not in Json format, Res text is '{response.text}'"

        response_as_dict = Assertions.assert_json(response)

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        # try:
        #     response_as_dict = response.json()
        # except json.JSONDecodeError:
        #     assert False, f"Response is not in Json format, Res text is '{response.text}'"

        response_as_dict = Assertions.assert_json(response)

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        # try:
        #     response_as_dict = response.json()
        # except json.JSONDecodeError:
        #     assert False, f"Response is not in Json format, Res text is '{response.text}'"

        response_as_dict = Assertions.assert_json(response)

        for name in names:
            assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_dict_has_keys(response_as_dict: dict, names: list):
        # try:
        #     response_as_dict = response.json()
        # except json.JSONDecodeError:
        #     assert False, f"Response is not in Json format, Res text is '{response.text}'"

        for name in names:
            assert name in response_as_dict, f"Dict doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        # try:
        #     response_as_dict = response.json()
        # except json.JSONDecodeError:
        #     assert False, f"Response is not in Json format, Res text is '{response.text}'"

        response_as_dict = Assertions.assert_json(response)

        assert name not in response_as_dict, f"Response JSON shouldn't have key '{name}'. But it's present"

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
        f"Wrong status code! Expected {expected_status_code}, Actual {response.status_code}"

