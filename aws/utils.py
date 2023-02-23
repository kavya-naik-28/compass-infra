import re
import os

from pulumi import Config

from constants import (
    AMAGI_MANAGED_MAIN_SECTIONS,
    CLUSTER_SETUP_KEYS,
    ENTERPRISE_MAIN_SECTIONS,
    LIST_OF_REGIONS,
    PRIVATE_DEPLOYMENT,
    VPC_KEYS,
    EXISTING_VPC_KEYS,
    ARGOCD_CONFIG_KEYS,
    RDS_CLUSTER_KEYS,
    CIDR_RANGE_PATTERN,
    ZONE_PATTERN,
    SUBNET_KEYS,
    KUBERNETES_CLUSTER_KEYS,
    K8S_VERSIONS,
    NODEGROUP_KEYS,
    CAPACITIES_KEYS,
    DEPLOYMENT_TYPE,
)

CONFIGURATION_ISSUES = []


def validate_config(config):
    region = Config("aws").get("region")

    is_enterprise = config.get("enterprise", "")
    if is_enterprise is None:
        CONFIGURATION_ISSUES.append("enterprise flag is missing")
    else:
        validate_region(region)
        # validate_sections(config, is_enterprise)
        # validate_zone_mapping(config.get("zone_mapping"), region)
        # validate_deployment_type(config.get("deployment_type"),is_enterprise)
        # validate_vpc(config.get("vpc"), is_enterprise)
        # if is_enterprise:
        #     validate_argo_cd_setup(config.get("argo_cd_setup"))
        # else:
        #     validate_cluster_setup(config.get("cluster_setup"))
        # validate_db_cluster(config.get("db_cluster"))
        # validate_kubernetes_cluster(config.get("kubernetes_cluster"), is_enterprise)

    return CONFIGURATION_ISSUES


def validate_sections(config, is_enterprise):
    if is_enterprise:
        if not list(config.keys()) == ENTERPRISE_MAIN_SECTIONS:
            CONFIGURATION_ISSUES.append(
                "Following section(s) are missing from STACK file: "
                + str(
                    [
                        item
                        for item in ENTERPRISE_MAIN_SECTIONS
                        if item not in list(config.keys())
                    ]
                ),
            )
    else:
        if not list(config.keys()) == AMAGI_MANAGED_MAIN_SECTIONS:
            CONFIGURATION_ISSUES.append(
                "Following section(s) are missing from STACK file: "
                + str(
                    [
                        item
                        for item in AMAGI_MANAGED_MAIN_SECTIONS
                        if item not in list(config.keys())
                    ]
                ),
            )


def validate_region(region):
    if not region in LIST_OF_REGIONS:
        CONFIGURATION_ISSUES.append("Incorrect region configured.")


def validate_zone_mapping(zone_mapping, region):
    az_pattern = region + "[a-z]{1}$"
    zones = [zone for zone in list(zone_mapping.keys()) if re.match(ZONE_PATTERN, zone)]
    azs = [az for az in list(zone_mapping.values()) if re.match(az_pattern, az)]
    if not len(zones) == len(azs):
        CONFIGURATION_ISSUES.append("Zone Mapping incorrectly configured")


def validate_deployment_type(deployment_type, is_enterprise):
    if not deployment_type in DEPLOYMENT_TYPE:
        CONFIGURATION_ISSUES.append(
            "deployment_type incorrectly configured, supported values public / private ."
        )
    if deployment_type==PRIVATE_DEPLOYMENT and not is_enterprise:
        CONFIGURATION_ISSUES.append(
        "deployment_type and enterprise misconfigured. Private deployment of amagi-managed infra is not yet supported. "
    )


def validate_new_vpc_configuration(vpc):
    if not list(vpc.keys()) == VPC_KEYS:
        CONFIGURATION_ISSUES.append(
            "Missing key(s) from VPC config: "
            + str([item for item in VPC_KEYS if item not in list(vpc.keys())]),
        )

    for cidr_range in vpc.get("cidr-range"):
        if not re.match(
            CIDR_RANGE_PATTERN, cidr_range
        ):
            CONFIGURATION_ISSUES.append("VPC CIDR range is incorrect. Example: 10.1.0.0/16")

    subnets = vpc.get("subnets")
    public_subnet_count = 0
    private_subnet_count = 0

    for subnet in subnets:
        if not list(subnet.keys()) == SUBNET_KEYS:
            CONFIGURATION_ISSUES.append("Subnet missing an attribute")

        if not re.match(ZONE_PATTERN, subnet.get("zone")):
            CONFIGURATION_ISSUES.append(
                "Subnet zone configured incorrectly. Example: zone-a"
            )

        if not re.match(CIDR_RANGE_PATTERN, subnet.get("cidr-range")):
            CONFIGURATION_ISSUES.append(
                "Subnet CIDR range is incorrect. Example: 10.1.0.0/16"
            )

        if not type(subnet.get("public")) == bool:
            CONFIGURATION_ISSUES.append("Subnet type is a boolean. Example: true/false")

        if subnet.get("public"):
            public_subnet_count += 1
        else:
            private_subnet_count += 1

    if public_subnet_count < 2 or private_subnet_count < 2:
        CONFIGURATION_ISSUES.append(
            "Configure atleast 2 Public and Private subnets"
        )


def validate_existing_vpc_configuration(vpc):
    if not list(vpc.keys()) == EXISTING_VPC_KEYS:
        CONFIGURATION_ISSUES.append(
            "Missing key(s) from VPC config: ",
            [item for item in EXISTING_VPC_KEYS if item not in list(vpc.keys())],
        )
    for cidr_range in vpc.get("existing_vpc_details").get("cidr-range"):
        if not re.match(
            CIDR_RANGE_PATTERN, cidr_range
        ):
            CONFIGURATION_ISSUES.append("VPC CIDR range is incorrect. Example: 10.1.0.0/16")

    public_subnets = vpc.get("existing_vpc_details").get("public_subnets")

    incorrect_public_keys = [
        key for key in list(public_subnets.keys()) if not re.match(ZONE_PATTERN, key)
    ]

    incorrect_public_values = [
        value for value in list(public_subnets.values()) if not value
    ]

    if incorrect_public_keys or incorrect_public_values:
        CONFIGURATION_ISSUES.append("Public subnets key/values are misconfigured")

    private_subnets = vpc.get("existing_vpc_details").get("private_subnets")

    incorrect_private_keys = [
        key for key in list(private_subnets.keys()) if not re.match(ZONE_PATTERN, key)
    ]

    incorrect_private_values = [
        value for value in list(private_subnets.values()) if not value
    ]

    if incorrect_private_keys or incorrect_private_values:
        CONFIGURATION_ISSUES.append("Private subnets key/valaues are misconfigured")


def validate_vpc(vpc, is_enterprise):
    if vpc["create"] and not is_enterprise:
        validate_new_vpc_configuration(vpc)

    elif not vpc["create"] and is_enterprise:
        validate_existing_vpc_configuration(vpc)

    elif not vpc["create"] and not is_enterprise:
        validate_existing_vpc_configuration(vpc)

    else:
        CONFIGURATION_ISSUES.append(
            "VPC and Enterprise misconfigured. VPCs are not created with enterprise setup. Amagi Managed setups can work with existing VPCs or can create a new VPC too."
        )


def validate_cluster_setup(cluster_setup_config):
    keys = [key for key in list(cluster_setup_config.keys()) if key]
    values = [value for value in list(cluster_setup_config.values()) if value]

    if not keys == CLUSTER_SETUP_KEYS or not len(keys) == len(values):
        CONFIGURATION_ISSUES.append(
            "'cluster_setup' Section is missing a few keys/values."
        )
    if cluster_setup_config["gitops_repo"]["config"]["ssh_priv_key"]:
        if not os.path.isfile(cluster_setup_config["gitops_repo"]["config"]["ssh_priv_key"]):
            CONFIGURATION_ISSUES.append("Config Gitops key file doesn't exists")
        else:
            config_file_perm = os.stat(cluster_setup_config["gitops_repo"]["config"]["ssh_priv_key"])
            if not oct(config_file_perm.st_mode)[-3:] in ["400", "600"]:
                CONFIGURATION_ISSUES.append("Config Gitops key file permission should be 400 or 600")
    if cluster_setup_config["gitops_repo"]["deploy"]["ssh_priv_key"]:
        if not os.path.isfile(cluster_setup_config["gitops_repo"]["deploy"]["ssh_priv_key"]):
            CONFIGURATION_ISSUES.append("Deploy Gitops key file doesn't exists")
        else:
            deploy_file_perm = os.stat(cluster_setup_config["gitops_repo"]["deploy"]["ssh_priv_key"])
            if not oct(deploy_file_perm.st_mode)[-3:] in ["400", "600"]:
                CONFIGURATION_ISSUES.append("Deploy Gitops key file permission should be 400 or 600")

def validate_argo_cd_setup(argo_cd_setup):
    keys = [key for key in list(argo_cd_setup.keys()) if key]
    values = [value for value in list(argo_cd_setup.values()) if value]

    if not keys == ARGOCD_CONFIG_KEYS or not len(keys) == len(values):
        CONFIGURATION_ISSUES.append("Argo CD setup is missing a few keys/values.")
    if argo_cd_setup["gitops_repo"]["config"]["ssh_priv_key"]:
        if not os.path.isfile(argo_cd_setup["gitops_repo"]["config"]["ssh_priv_key"]):
            CONFIGURATION_ISSUES.append("Config Private PEM file doesn't exists")
    if argo_cd_setup["gitops_repo"]["deploy"]["ssh_priv_key"]:
        if not os.path.isfile(argo_cd_setup["gitops_repo"]["deploy"]["ssh_priv_key"]):
            CONFIGURATION_ISSUES.append("Deploy Private PEM file doesn't exists")


def validate_db_cluster(db_cluster):
    keys = [key for key in list(db_cluster.keys()) if key]
    db_cluster_zones = db_cluster.get("zones")

    if (
        not keys == RDS_CLUSTER_KEYS
        or not db_cluster.get("instance_type")
        or not db_cluster.get("root_password")
        or not db_cluster_zones
        or not type(db_cluster.get("launch_reader_writer")) == bool
    ):
        CONFIGURATION_ISSUES.append("RDS Cluster is missing a few keys/values")

    if len(db_cluster_zones) < 2:
        CONFIGURATION_ISSUES.append("RDS Subnet Group requires atleast 2 Zones")

    incorrect_zones = [
        zone for zone in db_cluster_zones if not re.match(ZONE_PATTERN, zone)
    ]
    if incorrect_zones:
        CONFIGURATION_ISSUES.append(
            "DB Cluster Zone(s) incorrectly configured. Example: zone-a"
        )


def validate_kubernetes_cluster(kubernetes_cluster, is_enterprise):
    global KUBERNETES_CLUSTER_KEYS
    keys = [key for key in list(kubernetes_cluster.keys()) if key]

    keys.remove("additional_sg_id")

    if is_enterprise:
        if "argo_cd" in keys:
            keys.remove("argo_cd")

    if not keys == KUBERNETES_CLUSTER_KEYS:
        CONFIGURATION_ISSUES.append("Kubernetes Cluster is missing a few keys/values")

    k8s_cluster_zones = kubernetes_cluster.get("zones")

    if len(k8s_cluster_zones) < 2:
        CONFIGURATION_ISSUES.append("EKS requires atleast 2 Zones")

    incorrect_zones = [
        zone for zone in k8s_cluster_zones if not re.match(ZONE_PATTERN, zone)
    ]
    if incorrect_zones:
        CONFIGURATION_ISSUES.append(
            "Kubernetes Cluster Zone(s) incorrectly configured. Example: zone-a"
        )

    if kubernetes_cluster.get("k8s_version") not in K8S_VERSIONS:
        CONFIGURATION_ISSUES.append("Kubernetes version can only be 1.20 or 1.21")

    for nodegroup in kubernetes_cluster.get("nodegroups"):
        nodegroup_keys = list(nodegroup.keys())
        if "taints" in nodegroup_keys:
            nodegroup_keys.remove("taints")
        if "labels" in nodegroup_keys:
            nodegroup_keys.remove("labels")
        if (
            nodegroup_keys != NODEGROUP_KEYS
            or not nodegroup.get("bootstrap_commands")
            or not nodegroup.get("capacities")
            or not nodegroup.get("instance_types")
            or not nodegroup.get("name")
            or not nodegroup.get("tags")
            or not nodegroup.get("zones")
            or type(nodegroup.get("spot_instances")) != bool
        ):
            CONFIGURATION_ISSUES.append(
                f"{nodegroup.get('name')} nodeGroup missing an attribute"
            )

        if any(True for zone in nodegroup["zones"] if not re.match(ZONE_PATTERN, zone)):
            CONFIGURATION_ISSUES.append(
                "NodeGroup zone configured incorrectly. Example: zone-a"
            )

        if not list(nodegroup.get("capacities").keys()) == CAPACITIES_KEYS or not len(
            list(nodegroup.get("capacities").keys())
        ) == len(list(nodegroup.get("capacities").values())):
            CONFIGURATION_ISSUES.append(
                "NodeGroup capacities configured incorrectly. Example:- desired: 2"
            )

        tags_keys = [key for key in list(nodegroup.get("tags").keys()) if key]
        tags_values = [value for value in list(nodegroup.get("tags").values()) if value]

        if not len(tags_keys) == len(tags_values):
            CONFIGURATION_ISSUES.append(
                "NodeGroup tags configured incorrectly. Example:- description: Management Node group across Zone A and B"
            )
