""" Unit tests """
import unittest
import os
from pathlib import Path
import shutil
import yaml

from config_yml import Config


class Testing(unittest.TestCase):
    """Unittesting class"""

    def test_000_yaml_merge_dictionary(self):
        """Test for merging configs"""
        # Root is dictionary
        config_template = {
            "single": "singlevalue",
            "singlemerge": "template",
            "fruits": ["orange", "apple", "banana"],
        }
        config1 = {
            "vehicles": ["car", "truck"],
            "fruits": ["mango"],
            "single2": "singlevalue2",
            "singlemerge": "second",
        }
        Config._merge_config(config1, config_template)  # pylint: disable=protected-access

        expected_value = {
            "single": "singlevalue",
            "singlemerge": "second",
            "fruits": ["orange", "apple", "banana", "mango"],
            "vehicles": ["car", "truck"],
            "single2": "singlevalue2",
        }

        self.assertEqual(config_template, expected_value)

    def test_001_yaml_merge_list(self):
        """Test for _summary_"""
        # Root is list
        config_template = [
            {
                "single": "singlevalue",
                "singlemerge": "template",
                "fruits": ["orange", "apple", "banana"],
            },
            {
                "single2": "singlevalue2",
                "singlemerge2": "template",
                "fruits2": ["mango", "lemon", "banana"],
            },
        ]
        config_mismatch = {"test": "test"}

        # Exception TypeError must be raised fot this test to succeed
        with self.assertRaises(TypeError):
            Config._merge_config(config_mismatch, config_template)  # pylint: disable=protected-access

        config_template2 = [
            {
                "single3": "singlevalue",
                "singlemerge": "template",
                "fruits": ["orange", "apple", "banana"],
            }
        ]
        Config._merge_config(config_template2, config_template)  # pylint: disable=protected-access

        expected_merge = [
            {
                "single": "singlevalue",
                "singlemerge": "template",
                "fruits": ["orange", "apple", "banana"],
            },
            {
                "single2": "singlevalue2",
                "singlemerge2": "template",
                "fruits2": ["mango", "lemon", "banana"],
            },
            {
                "single3": "singlevalue",
                "singlemerge": "template",
                "fruits": ["orange", "apple", "banana"],
            },
        ]
        self.assertEqual(config_template, expected_merge)

    def test_002_from_scrath(self):
        """ Remove config file, to start from scratch """
        var_config_path = Config.get_config_path("baseutils_tests", "config_new.yml")
        if os.path.exists(var_config_path):
            os.remove(Config.getConfigPath("baseutils_tests", "config_new.yml"))

        # Instatiate a config file from scratch, based only on template
        # Will be automatically writen to file
        template_path = f'{Path(__file__).parent}/data/config_template.yml'
        _ = Config(
                    package_name="baseutils_tests",
                    template_path=template_path,
                    config_file_name="config_new.yml",
                  )

        try:
            # Check that resulting config file equals the template file
            with open(var_config_path, "r", encoding="utf-8") as config_file:
                config_read = yaml.load(config_file, Loader=yaml.FullLoader)
                with open(template_path, "r", encoding="utf-8") as template_config_file:
                    template_config_read = yaml.load(template_config_file, Loader=yaml.FullLoader)
                    self.assertEqual(config_read, template_config_read)
        except IOError as ex:
            self.assertFalse(f"File not found: {ex}")
        finally:
            os.remove(Config.get_config_path("baseutils_tests", "config_new.yml"))

    def test_003_update_config(self):
        """Test updating a config
        """
        # Copy already-made config to var destination
        existing_path = f"{Path(__file__).parent}/data/config_existing.yml"
        var_config_path = Config.get_config_path(
            "baseutils_tests", "config_existing.yml"
        )
        shutil.copy(existing_path, var_config_path)

        # Instatiate a config file from scratch, with an updated template, with an existing config
        template_path = f'{Path(__file__).parent}/data/config_template.yml'
        config = Config(
                        package_name="baseutils_tests",
                        template_path=template_path,
                        config_file_name="config_existing.yml",
                       )

        expected_merged = {
                            "key_template1": "template",
                            "key_template2": "changed",
                            "key_template3": "new in config",
                          }

        # Check memory matches
        self.assertEqual(config.get_dict(), expected_merged)

        config.write()

        try:
            # Check that resulting config file equals the template file
            with open(var_config_path, "r", encoding="utf-8") as config_file:
                config_read = yaml.load(config_file, Loader=yaml.FullLoader)
                expected_merged = {
                                    "key_template1": "template",
                                    "key_template2": "changed",
                                    "key_template3": "new in config",
                                  }
                self.assertEqual(config_read, expected_merged)
        except IOError as ex:
            self.assertFalse(f"File not found: {ex}")
        finally:
            os.remove(Config.get_config_path("baseutils_tests", "config_existing.yml"))


if __name__ == "__main__":
    unittest.main()
