"""JVM metadata parsing must tolerate unrelated empty Java properties."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("capture_all", Path(__file__).with_name("capture-all.py"))
CAPTURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CAPTURE)


class JavaRuntimeTests(unittest.TestCase):
    @patch.object(CAPTURE.subprocess, "run")
    def test_reads_version_with_empty_and_multiline_properties(self, run):
        run.return_value.stdout = ""
        run.return_value.stderr = (
            "Property settings:\n"
            "    java.version = 27.0.1.0.3\n"
            "    java.vendor = Oracle Corporation\n"
            "    java.vm.name = OpenJDK 64-Bit Server VM\n"
            "    java.class.path = \n"
            "    line.separator = \\n \n"
            "    java.library.path = /first/path\n"
            "        /second/path\n")
        self.assertEqual(CAPTURE.get_java_runtime("java"), {
            "version": "27.0.1.0.3", "vendor": "Oracle Corporation", "vm": "OpenJDK 64-Bit Server VM"
        })

    @patch.object(CAPTURE.subprocess, "run")
    def test_missing_metadata_fails_explicitly(self, run):
        run.return_value.stdout = ""
        run.return_value.stderr = "    java.version = \n"
        with self.assertRaisesRegex(RuntimeError, "java.version"):
            CAPTURE.get_java_runtime("java")


if __name__ == "__main__":
    unittest.main()
