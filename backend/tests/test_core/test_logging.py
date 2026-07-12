import unittest
import os
import tempfile
import json
import threading
from core.logging import (
    LoggerFactory,
    ConsoleHandler,
    FileHandler,
    NullHandler,
    JsonFormatter,
    ConsoleFormatter,
    get_logging_context,
    set_logging_context,
    clear_logging_context
)
from core.logging.exceptions import InvalidLogLevelError, InvalidHandlerError

class TestLogging(unittest.TestCase):
    def setUp(self):
        LoggerFactory.clear_loggers()
        clear_logging_context()

    def test_logger_creation_and_caching(self):
        logger1 = LoggerFactory.get_logger("test_log", "DEBUG")
        logger2 = LoggerFactory.get_logger("test_log")
        self.assertIs(logger1, logger2)
        self.assertEqual(logger1.level, "DEBUG")

    def test_invalid_log_level(self):
        with self.assertRaises(InvalidLogLevelError):
            LoggerFactory.get_logger("bad_log", "INVALID")

    def test_duplicate_handlers(self):
        logger = LoggerFactory.get_logger("dup_test")
        handler1 = ConsoleHandler()
        logger.add_handler(handler1)
        with self.assertRaises(InvalidHandlerError):
            logger.add_handler(ConsoleHandler())

    def test_duplicate_file_handlers(self):
        logger = LoggerFactory.get_logger("dup_file")
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            handler1 = FileHandler(tmp_path)
            logger.add_handler(handler1)
            with self.assertRaises(InvalidHandlerError):
                logger.add_handler(FileHandler(tmp_path))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_json_formatter(self):
        formatter = JsonFormatter()
        set_logging_context(correlation_id="corr-123", engine_name="TestEngine")
        result = formatter.format("INFO", "Test log message", {"extra_key": "extra_val"})
        
        data = json.loads(result)
        self.assertEqual(data["level"], "INFO")
        self.assertEqual(data["message"], "Test log message")
        self.assertEqual(data["context"]["correlation_id"], "corr-123")
        self.assertEqual(data["context"]["engine_name"], "TestEngine")
        self.assertEqual(data["extra"]["extra_key"], "extra_val")

    def test_console_formatter(self):
        formatter = ConsoleFormatter()
        set_logging_context(correlation_id="corr-999", stage_id="stage-1")
        result = formatter.format("WARNING", "Alert")
        self.assertIn("WARNING", result)
        self.assertIn("Alert", result)
        self.assertIn("corr-999", result)
        self.assertIn("stage-1", result)

    def test_file_handler_emission(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name
            
        try:
            logger = LoggerFactory.get_logger("file_test", "INFO")
            handler = FileHandler(tmp_path)
            logger.add_handler(handler)
            
            logger.info("Message written to file")
            
            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            data = json.loads(content.strip())
            self.assertEqual(data["message"], "Message written to file")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_thread_safety_context(self):
        set_logging_context(correlation_id="parent")
        
        def run_thread():
            set_logging_context(correlation_id="child")
            ctx = get_logging_context()
            self.assertEqual(ctx["correlation_id"], "child")
            
        t = threading.Thread(target=run_thread)
        t.start()
        t.join()
        
        self.assertEqual(get_logging_context()["correlation_id"], "parent")

if __name__ == "__main__":
    unittest.main()
