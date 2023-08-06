import json
import tempfile
from pathlib import Path
from unittest import TestCase, mock

from gitlab_search.config import Config

MODULE_PATH = "gitlab_search.config"


class TestConfig(TestCase):
    def test_should_create_minimal_object(self):
        # when
        obj = Config()
        # then
        self.assertIsNone(obj.token)
        self.assertIsInstance(obj.url, str)

    @mock.patch(MODULE_PATH + ".Config.path", spec=True)
    def test_should_load_from_config_file(self, mock_path):
        config = {"token": "my-token", "url": "my-url"}
        _, path_str = tempfile.mkstemp(text=True)
        path = Path(path_str)
        with path.open("w") as fp:
            json.dump(config, fp)
        # given
        mock_path.return_value = path
        # when
        obj = Config.load()
        # then
        self.assertEqual(obj.token, "my-token")
        self.assertEqual(obj.url, "my-url")
        ...
        path.unlink()
