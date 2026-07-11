import logging
import sys

def setup_logger():
    logger = logging.getLogger("stem_ai")
    logger.setLevel(logging.INFO)
    
    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(ch)
        
    return logger

def get_logger(name: str = "stem_ai"):
    return logging.getLogger(name)
