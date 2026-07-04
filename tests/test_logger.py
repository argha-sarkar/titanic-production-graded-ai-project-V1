from src.logger.logger import logger

def test_logger():
    
    logger.info("logger test.")
    
    assert logger is not None