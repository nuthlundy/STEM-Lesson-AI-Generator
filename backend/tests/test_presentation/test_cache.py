import unittest
from services.presentation.utils.cache import PresentationAICache

class TestPresentationAICache(unittest.TestCase):
    def test_cache_hashing_and_retrieval(self):
        cache = PresentationAICache()
        prompt = "Hello AI"
        params = {"model": "gemini-flash"}
        
        self.assertIsNone(cache.get(prompt, params))
        
        response = {"output": "Hi human"}
        cache.set(prompt, response, params)
        
        self.assertEqual(cache.get(prompt, params), response)
        self.assertIsNone(cache.get(prompt, {"model": "gemini-pro"}))

    def test_cache_empty_params(self):
        cache = PresentationAICache()
        cache.set("prompt", {"out": 1})
        self.assertEqual(cache.get("prompt"), {"out": 1})

    def test_cache_different_prompts(self):
        cache = PresentationAICache()
        cache.set("prompt1", {"out": 1})
        cache.set("prompt2", {"out": 2})
        self.assertEqual(cache.get("prompt1"), {"out": 1})
        self.assertEqual(cache.get("prompt2"), {"out": 2})

    def test_cache_overwrite(self):
        cache = PresentationAICache()
        cache.set("prompt", {"out": 1})
        cache.set("prompt", {"out": 2})
        self.assertEqual(cache.get("prompt"), {"out": 2})

    def test_cache_none_get(self):
        cache = PresentationAICache()
        self.assertIsNone(cache.get("non_existent"))

if __name__ == "__main__":
    unittest.main()
