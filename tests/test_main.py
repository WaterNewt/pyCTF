import sys
import os
import unittest
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
import main


class TestVerify(unittest.TestCase):
    def setUp(self):
        main.app.config["TESTING"] = True
        self.app = main.app.test_client()

    def test_verify_flag(self):
        request = self.app.get("/verify/?id=0&flag=pyCTF{test}")
        self.assertEqual(request.json['success'], True)


class TestDownloads(unittest.TestCase):
    def setUp(self):
        main.app.config["TESTING"] = True
        self.app = main.app.test_client()

    def test_download(self):
        request = self.app.get("/downloads/?id=0&file=test.txt")
        self.assertEqual(request.status_code == 200 and request.text == "pyCTF{test}", True)

if __name__ == "__main__":
    unittest.main()
