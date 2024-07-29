from loguru import logger

log_format = "{level}: {time:YYYY-MM-DD HH:mm:ss} | {message}"

def logging_details(message, level, filename):

    logger.remove()
    logger.add(f'logs/{filename}.log', format=log_format, level=level)

    if level == "DEBUG":
        logger.debug(message)
    elif level == "INFO":
        logger.info(message)
    elif level == "WARNING":
        logger.warning(message)
    elif level == "ERROR":
        logger.error(message)
    else:
        logger.info(message)
    
    return "logged"