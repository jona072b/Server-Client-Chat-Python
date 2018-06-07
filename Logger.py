import logging


def Main(logMessage, numOfBadWords):
    LOG_FORMAT = "%(levelname)\t %(asctime)\t - %(message)"
    logging.basicConfig(filename="logger.log",
    level=logging.DEBUG,
    format=LOG_FORMAT)

    logger = logging.getLogger()

    if numOfBadWords == 1:
        logger.warning(logMessage)
    elif numOfBadWords == 2:
        logger.error(logMessage)
    elif numOfBadWords >= 3:
        logger.critical(logMessage)

