# -*- coding: utf-8 -*-
"""
This class defines all the Network resources required for
Cloudport to work. Namely, a VPC, Subnets, Internet
Gateway and Route table.
"""

from pulumi import export, get_stack, ComponentResource, ResourceOptions
from pulumi_aws import ec2


class VpcArgs:
    def __init__(self, vpc_configs={}, zone_mapping={}):
        self.vpc_create = vpc_configs["create"]
        if self.vpc_create:
            self.cidr_range = vpc_configs["cidr-range"]
            self.subnet_configs = vpc_configs["subnets"]
            self.zone_mapping = zone_mapping
        else:
            self.existing_vpc_details = vpc_configs["existing_vpc_details"]


class Vpc(ComponentResource):
    def __init__(self, name: str, args: VpcArgs, opts: ResourceOptions = None):

        super().__init__("custom:resource:VPC", name, {}, opts)

        self.name = name
        self.__args = args
        if self.__args.vpc_create:
            self.stack = get_stack()
            self.lb = ec2.Eip("lb",
                vpc=True)
            self.__vpc()
            self.__igw()
            self.__route_table()
            self.__subnets()
        else:
            self.__set_vpc_details()

        self.__exports()
        self.register_outputs({})

    def __vpc(self):
        cidr_range = self.__args.cidr_range[0]
        self.vpc = ec2.Vpc(
            self.name,
            cidr_block=cidr_range,
            instance_tenancy="default",
            enable_dns_hostnames=True,
            enable_dns_support=True,
            tags={"Name": self.name, "Stack": self.stack},
            opts=ResourceOptions(parent=self),
        )

        self.id = self.vpc.id
        self.cidr_range = [self.vpc.cidr_block]

    def __igw(self):
        igw_name = f"{self.name}-igw"
        self.igw = ec2.InternetGateway(
            igw_name,
            vpc_id=self.vpc.id,
            tags={"Name": igw_name, "Stack": self.stack},
            opts=ResourceOptions(parent=self.vpc, depends_on=self.vpc),
        )

    def __route_table(self):
        route_table_public_name = f"{self.stack}-rt-public"
        self.route_table_public = ec2.RouteTable(
            route_table_public_name,
            vpc_id=self.vpc.id,
            routes=[
                ec2.RouteTableRouteArgs(
                    cidr_block="0.0.0.0/0",
                    gateway_id=self.igw.id,
                )
            ],
            tags={"Name": route_table_public_name, "Stack": self.stack},
            opts=ResourceOptions(parent=self.vpc, depends_on=[self.vpc, self.igw]),
        )

    def __subnets(self):
        self.public_subnets = {}
        self.private_subnets = {}
        subnet_configs = self.__args.subnet_configs
        zone_mapping = self.__args.zone_mapping

        for zone in subnet_configs:
            subnet_az = zone_mapping[zone["zone"]]
            subnet_type = "public" if zone["public"] else "private"
            subnet_cidr_range = zone["cidr-range"]
            subnet_name = f"{self.stack}-{subnet_az.replace('-', '')}-{subnet_type}"
            vpc_subnet = ec2.Subnet(
                subnet_name,
                assign_ipv6_address_on_creation=False,
                vpc_id=self.vpc.id,
                map_public_ip_on_launch=True,
                cidr_block=subnet_cidr_range,
                availability_zone=subnet_az,
                tags={"Name": subnet_name, "Stack": self.stack},
                opts=ResourceOptions(parent=self.vpc, depends_on=self.vpc),
            )
            if subnet_type == "public":
                ec2.RouteTableAssociation(
                    f"{self.stack}-rt-assoc-public-{subnet_az.replace('-', '')}",
                    route_table_id=self.route_table_public.id,
                    subnet_id=vpc_subnet.id,
                    opts=ResourceOptions(parent=vpc_subnet),
                )
                self.public_subnets[zone["zone"]] = vpc_subnet.id
                if zone["zone"] == "zone-a":
                    self.nat = ec2.NatGateway("example-nat",
                        allocation_id = self.lb,
                        subnet_id=vpc_subnet.id
                    )
            elif zone["zone"] == "zone-a":
                route_table_private_zone_a_name = f"{self.stack}-rt-private-{zone['zone']}"
                self.route_table_private_zone_a = ec2.RouteTable(
                    route_table_private_zone_a_name,
                    vpc_id=self.vpc.id,
                    routes=[
                        ec2.RouteTableRouteArgs(
                            cidr_block="0.0.0.0/0",
                            nat_gateway_id=self.nat.id,
                        )
                    ],
                    tags={"Name": route_table_private_zone_a_name, "Stack": self.stack},
                    opts=ResourceOptions(parent=self.vpc, depends_on=[self.vpc, self.nat]),
                )
                ec2.RouteTableAssociation(
                    f"{self.stack}-rt-assoc-private-{subnet_az.replace('-', '')}",
                    route_table_id=self.route_table_private_zone_a.id,
                    subnet_id=vpc_subnet.id,
                    opts=ResourceOptions(parent=vpc_subnet),
                )
                self.private_subnets[zone["zone"]] = vpc_subnet.id
            else :
                route_table_private_zone_b_name = f"{self.stack}-rt-private-{zone['zone']}"
                self.route_table_private_zone_b = ec2.RouteTable(
                    route_table_private_zone_b_name,
                    vpc_id=self.vpc.id,
                    routes=[
                        ec2.RouteTableRouteArgs(
                            cidr_block="0.0.0.0/0",
                            nat_gateway_id=self.nat.id,
                        )
                    ],
                    tags={"Name": route_table_private_zone_b_name, "Stack": self.stack},
                    opts=ResourceOptions(parent=self.vpc, depends_on=[self.vpc, self.nat]),
                )
                ec2.RouteTableAssociation(
                    f"{self.stack}-rt-assoc-private-{subnet_az.replace('-', '')}",
                    route_table_id=self.route_table_private_zone_b.id,
                    subnet_id=vpc_subnet.id,
                    opts=ResourceOptions(parent=vpc_subnet),
                )
                self.private_subnets[zone["zone"]] = vpc_subnet.id
        

    def __set_vpc_details(self):
        self.id = self.__args.existing_vpc_details["id"]
        self.public_subnets = self.__args.existing_vpc_details["public_subnets"]
        self.private_subnets = self.__args.existing_vpc_details["private_subnets"]
        self.cidr_range = self.__args.existing_vpc_details["cidr-range"]

    def __exports(self):
        vpc_details = {
            "id": self.id,
            "cidr_range": self.cidr_range,
            "public_subnets": self.public_subnets,
            "private_subnets": self.private_subnets,
            "nat_id": self.nat,
            "route_table_1_id": self.route_table_private_zone_a.id,
            "routevmc":self.route_table_private_zone_b.id
        }
        export("vpc", vpc_details)
