import tempfile
import unittest
from pathlib import Path

from comsol_mcp_server.recipes import get_recipe, list_recipes
from comsol_mcp_server.tools import collect_outputs, inspect_batch_log


class ToolTests(unittest.TestCase):
    def test_recipes_available(self):
        names = list_recipes()
        self.assertIn("batch_stdout", names)
        self.assertTrue(get_recipe("batch_stdout")["ok"])

    def test_inspect_batch_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "batch.log"
            log.write_text("progress 10%\nUndefined variable: T\n当前进度: 20 %\n", encoding="utf-8")
            result = inspect_batch_log(str(log))
            self.assertTrue(result["ok"])
            self.assertTrue(result["errors"])
            self.assertTrue(result["last_progress"])

    def test_collect_outputs_excludes_heavy_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = tmp_path / "src"
            src.mkdir()
            (src / "a.csv").write_text("x\n1\n", encoding="utf-8")
            (src / "model.mph").write_text("heavy", encoding="utf-8")
            (src / "run.log").write_text("log", encoding="utf-8")
            result = collect_outputs(str(src), str(tmp_path / "out.zip"))
            self.assertTrue(result["ok"])
            self.assertEqual(result["file_count"], 1)


if __name__ == "__main__":
    unittest.main()
