from pulumi import export, get_stack, ComponentResource, ResourceOptions
from pulumi_aws import rds

from constants import RDS_CLUSTER_ENGINE, RDS_MASTER_USERNAME, RDS_DB_NAME


class DbInstanceArgs:
    def __init__(self, db_configs={}, zone_mapping= {}):
        self.instance_type = db_configs["instance_class"]
        self.password = db_configs["password"]
        self.username = db_configs["username"]
        self.zone = zone_mapping["zone-b"]


class DbInstance(ComponentResource):
    def __init__(self, name: str, args: DbInstanceArgs, opts: ResourceOptions = None):

        super().__init__("custom:resource:DbInstance", name, {}, opts)

        self.name = name
        self.__args = args
        self.stack = get_stack()
        self.__rds_instance()
        self.__exports()
        self.register_outputs({})

    def __rds_instance(self):
        self.db_instance_name = f"{self.stack}-postgres"
        self.db_instance = rds.Instance(self.db_instance_name,
            allocated_storage=40,
            instance_class="db.t3.micro",
            availability_zone= self.__args.zone,
            engine="postgres",
            engine_version="13.7",
            db_name= "resources",
            storage_type= "gp2",
            license_model="postgresql-license",
            username=self.__args.username,
            password=self.__args.password,
            option_group_name="default:postgres-13",
            parameter_group_name="default.postgres13",
            publicly_accessible= True,
            backup_retention_period= 0,
            backup_window="06:13-06:43",
            skip_final_snapshot= True,
            apply_immediately= True
            )


    def __exports(self):
        export(
            "db_instance",
            {
                "instance": self.db_instance,
            }
        )
