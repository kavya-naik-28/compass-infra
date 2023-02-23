import sys
from pulumi import Config, get_stack

from logger import logger
from constants import *
from checks import pre_setup_checks

cfg = Config()

if __name__ == "__main__":
    # if pre_setup_checks(get_stack()):
    #     logger.info("INFO: Completed pre-setup checks...")
    # else:
    #     logger.error("ERROR: Failed pre-setup checks...")
    #     sys.exit(True)

    config_data = cfg.get_object("infra")

    if config_data:
        if config_data.get(CLOUD_PROVIDER):
            cloud_provider = config_data[CLOUD_PROVIDER]
            if cloud_provider.lower() == GCP_CLOUD:
                from gcp.main import GCP
                gcp_sdk = GCP(config=config_data)
                gcp_sdk.create()
            elif cloud_provider.lower() == AWS_CLOUD:
                from aws.main import AWS
                aws_sdk = AWS(config=config_data)
                aws_sdk.create()
            else:
                logger.error("__main__: Wrong Cloud Provider choice. Exiting...")
                sys.exit(True)
        else:
            logger.error(f"__main__: Key missing {CLOUD_PROVIDER} choice. Exiting...")
            sys.exit(True)
    else:
        logger.error(
            "__main__: Infra config not provided, Check {Pulumi.STAGE.yml} file. Exiting..."
        )
        sys.exit(True)
