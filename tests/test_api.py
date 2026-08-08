"""Basic API tests; run with: python -m unittest discover -s tests."""
import unittest

from backend.app import create_app


class ChatApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app = create_app({"TESTING": True})
        cls.client = app.test_client()

    def test_health_check(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.get_json()["faq_count"], 150)

    def test_valid_chat_question(self):
        response = self.client.post("/api/chat", json={"message": "How can I pay my fees?"})
        body = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("answer", body)
        self.assertIn("confidence", body)

    def test_empty_chat_question(self):
        response = self.client.post("/api/chat", json={"message": "   "})
        self.assertEqual(response.status_code, 400)

    def test_invalid_payload(self):
        response = self.client.post("/api/chat", json={"question": "fees"})
        self.assertEqual(response.status_code, 400)

    def test_faq_search(self):
        response = self.client.get("/api/faqs?search=library")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["faqs"])


if __name__ == "__main__":
    unittest.main()
