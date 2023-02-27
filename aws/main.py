from pulumi import get_stack, Config

from . import network
from . import utils
from . import database_instance

from logger import logger

# from bootstrap.cluster_setup import ClusterSetup
from constants import AWS_CLOUD, NOT_REQUIRED_FOR_AWS, IAM_ROLE_BASED_FOR_AWS

class AWS(object):
    def __init__(self, config):
        self.config = config

        self.configuration_issues = utils.validate_config(self.config)
        if not self.configuration_issues:
            self.stack = get_stack()
            self.zone_mapping = self.config["zone_mapping"]
            self.region = Config("aws").get("region")
            self.create_resources = True

        else:
            logger.error(
                "*******************************************************************"
            )
            logger.error(
                "STACK FILE MISCONFIGURATIONS:\n{}".format(
                    "\n".join(map(str, self.configuration_issues))
                )
            )
            logger.error(
                "*******************************************************************"
            )
            self.create_resources = False

    def create(self):
        if not self.create_resources:
            print(
                "Since there are configuration issues in the STACK file no resources will be provisioned. Do NOT proceed with execution."
            )
            return

        vpc = network.Vpc(
            self.stack,
            network.VpcArgs(
                vpc_configs=self.config["vpc"],
                zone_mapping=self.zone_mapping,
            ),
        )

        db_cluster = database_instance.DbInstance(
            f"{self.stack}-cluster",
            database_instance.DbInstanceArgs(
                db_configs=self.config["db_cluster"],
                zone_mapping = self.config["zone_mapping"]
            ),
        )


