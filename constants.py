GCP_CLOUD = "gcp"
AWS_CLOUD = "aws"

PROJECT = "project"
REGION = "region"
CLOUD_PROVIDER = "cloud_provider"

VPC_RESOURCE = "vpc"
ZONE_MAPPING = "zone_mapping"
SUBNET_RESOURCE = "subnets"
CERTIFICATE_RESOURCE = "certificate"
DD_ARCHIVAL_RESOURCE = "dd_archival"
S3_INGEST_FUNCTION_RESOURCE = "s3_ingest"
AMAGI_SECRET_RESOURCE = "amagi_secret"
DB_CLUSTER = "db_cluster"
LIVE_CONFIG = "cp_live"
REDIS_CONFIG = "redis"
CLUSTER_SETUP = "cluster_setup"
K8S_CLUSTER = "kubernetes_cluster"
PRIVATE_DEPLOYMENT = "private"
PUBLIC_DEPLOYMENT = "public"
DEPLOYMENT_TYPE = [PRIVATE_DEPLOYMENT, PUBLIC_DEPLOYMENT]

IAM_ROLE_BASED_FOR_AWS = "IAM_ROLE_BASED_FOR_AWS"
NOT_REQUIRED_FOR_AWS = "NOT_REQUIRED_FOR_AWS"

LOCAL_DEPLOY_REPO_PATH = "/tmp/deploy_repo/"
LOCAL_CONFIG_REPO_PATH = "/tmp/config_repo/"

S3_INGEST_ZIP_PATH = "./s3_ingest.zip"
GCP_LAMBDA_RUNTIME = "nodejs10"


GCP_RESOURCES = [
    VPC_RESOURCE,
    ZONE_MAPPING,
    CERTIFICATE_RESOURCE,
    DB_CLUSTER,
    LIVE_CONFIG,
    REDIS_CONFIG,
    CLUSTER_SETUP,
    K8S_CLUSTER,
]

AWS_RESOURCES = [
    VPC_RESOURCE,
    CERTIFICATE_RESOURCE,
    DB_CLUSTER,
    K8S_CLUSTER,
]

AMAGI_SECRET_TEMPLATE = {
    "auths": {
        "https://index.docker.io/v1/": {
            "username": "amagidevops",
            "password": "beefed0108",
            "email": "devops@amagi.com",
        }
    }
}

RDS_MASTER_USERNAME = "root"
RDS_DB_NAME = "cloudport"
RDS_CLUSTER_ENGINE = "5.7.mysql_aurora.2.07.2"

CIDR_RANGE_PATTERN = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/([0-9]|[1-2][0-9]|3[0-2]))$"

GCP_REGIONS = [
    "asia-east1",
    "asia-east2",
    "asia-northeast1",
    "asia-northeast2",
    "asia-northeast3",
    "asia-south1",
    "asia-south2",
    "asia-southeast1",
    "asia-southeast2",
    "australia-southeast1",
    "australia-southeast2",
    "europe-central2",
    "europe-north1",
    "europe-west1",
    "europe-west2",
    "europe-west3",
    "europe-west4",
    "europe-west6",
    "europe-west8",
    "northamerica-northeast1",
    "northamerica-northeast2",
    "southamerica-east1",
    "southamerica-west1",
    "us-central1",
    "us-east1",
    "us-east4",
    "us-west1",
    "us-west2",
    "us-west3",
    "us-west4",
]

GKE_VERSION_PATTERN = r"1\.[0-9]{,2}\.[0-9]{,2}-gke\.[0-9]{,4}"

NODEPOOL_REQUIRED_KEYS = [
    "az",
    "capacities",
    "instance_type",
    "name",
    "spot_instances",
    "tags",
]

ENTERPRISE_MAIN_SECTIONS = [
    "argo_cd_setup",
    CLOUD_PROVIDER,
    "cp_live",
    "db_cluster",
    "dd_archival_buckets",
    "deployment_type",
    "enterprise",
    "kubernetes_cluster",
    "redis",
    "s3_ingest_config",
    "vpc",
    "zone_mapping",
]

AMAGI_MANAGED_MAIN_SECTIONS = [
    CLOUD_PROVIDER,
    CLUSTER_SETUP,
    "cp_live",
    "db_cluster",
    "dd_archival_buckets",
    "deployment_type",
    "enterprise",
    "kubernetes_cluster",
    "redis",
    "s3_ingest_config",
    "vpc",
    "zone_mapping",
]

LIST_OF_REGIONS = [
    "us-east-2",
    "us-east-1",
    "us-west-1",
    "us-west-2",
    "af-south-1",
    "ap-east-1",
    "ap-southeast-3",
    "ap-south-1",
    "ap-northeast-3",
    "ap-northeast-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-northeast-1",
    "ca-central-1",
    "eu-central-1",
    "eu-west-1",
    "eu-west-2",
    "eu-south-1",
    "eu-west-3",
    "eu-north-1",
    "me-south-1",
    "sa-east-1",
    "us-gov-east-1",
    "us-gov-west-1",
]

VPC_KEYS = ["cidr-range", "create", "subnets"]

EXISTING_VPC_KEYS = ["create", "existing_vpc_details"]

SUBNET_KEYS = ["cidr-range", "public", "zone"]

CLUSTER_SETUP_KEYS = [
  'amagi_services_values',
  'amagi_services_version',
  'chart_museum_endpoint',
  'gitops_repo',
  'operator_setup',
  'stage'
]

ARGOCD_CONFIG_KEYS = [
    "amagi_services_values",
    "amagi_services_version",
    "chart_museum_endpoint",
    "chart_museum_password",
    "chart_museum_username",
    "gitops_repo",
    "operator_setup",
    "platform_release_version",
    "platform_values",
    "stage",
]

RDS_CLUSTER_KEYS = ["instance_type", "launch_reader_writer", "root_password", "zones"]

ZONE_PATTERN = "zone-" + "[a-z]{1}$"

KUBERNETES_CLUSTER_KEYS = ["k8s_version", "nodegroups", "update_ami_on_nodegroups", "zones"]

K8S_VERSIONS = ["1.20", "1.21"]

NODEGROUP_KEYS = [
    "bootstrap_commands",
    "capacities",
    "instance_types",
    "name",
    "spot_instances",
    "tags",
    "zones",
]

CAPACITIES_KEYS = ["desired", "max", "min"]


REDIS_PORT = 6379

REDIS_MAINTENANCE_WINDOW = "sun:05:00-sun:09:00"

REDIS_ENGINE = "redis"

REDIS_ENGINE_VERSION = "5.0.5"

# ECR Repo link can be extracted from here: https://github.com/awsdocs/amazon-eks-user-guide/blob/master/doc_source/add-ons-images.md
# VPC CNI Image tag versions can be extracted from here: https://github.com/awsdocs/amazon-eks-user-guide/blob/master/doc_source/managing-vpc-cni.md#updating-vpc-cni-add-on

VPC_CNI_ADDON_IMAGE = "602401143452.dkr.ecr.us-east-1.amazonaws.com/amazon-k8s-cni:v1.11.3-eksbuild.1"

VPC_CNI_ADDON_INIT_IMAGE = "602401143452.dkr.ecr.us-east-1.amazonaws.com/amazon-k8s-cni-init:v1.11.3-eksbuild.1"

README_FOR_DEPLOY_REPO = r"""# Commit Amagi Custom resources here
Add files in the following format ```{CURRENT_PATH}/<NAMESPACE>/<SERVICE>/```

Replace `NAMESPACE` and `SERVICE` by following the examples given below:

Examples
```
- {CURRENT_PATH}/customername-automation/automation/
- {CURRENT_PATH}/customername-automation/account/
- {CURRENT_PATH}/customername-automation/channel/
- {CURRENT_PATH}/amagi-components/serverless/
- {ALT_CURRENT_PATH}/cp-fluentd/
- {ALT_CURRENT_PATH}/cp-capsequo-server/
```
"""
