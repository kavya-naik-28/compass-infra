from json import dumps


def check_key_in_list(search_word, search_list):
    return any( keyword in search_word for keyword in search_list )


CONST_CLOUD = ["gcp", "aws"]
CONST_AWS_REGIONS = ["use1", "use2", "usw1", "usw2", "eun1", "euw1",
                     "euw3", "euw2", "eus1", "euc1", "as1", "ane1", "ane2", "ane3",
                     "ae1", "ase1", "ase2", "ase3", "afs1", "mes1", "sae1", "cac1"
                     ]
CONST_GCP_REGIONS = ["ae1", "ae2", "ane1", "ane2", "ane3", "as1", "as2", "ase1", "ase2",
                     "aus1", "aus2", "euc2", "eun1", "euw1", "euw2", "euw3", "euw4", "euw6",
                     "nan1", "nan2", "sae1", "saw1", "usc1", "use1", "use4", "usw1", "usw2",
                     "usw3", "usw4"
                     ]


def pre_setup_checks(pulumi_stack):
    REGEX_ERRORS = []
    if len(pulumi_stack.split('-')) < 4:
        REGEX_ERRORS.append(f"ERROR: Pulumi stack is not in format of '<cloud>-<shorthand_region>-<project_alias>-<unique_identifier>'. Exiting ...")
        print(dumps(REGEX_ERRORS,indent=2))
        return False

    cloud_provider, region, project_alias, unique_identifier = pulumi_stack.split('-')
    # Cloud provider check
    if cloud_provider.lower() not in CONST_CLOUD:
        REGEX_ERRORS.append(f"ERROR: Cloud Provider in stack name is not in 'gcp' or 'aws' Exiting ...")
    # region check
    if (len(region) < 3 or len(region) > 4) or not region.isalnum():
        REGEX_ERRORS.append(f"ERROR: Region in Stack name should be in range min:3 max:4 characters WITH only alpha-numeric characters, Exiting ...")
    else:
        if check_key_in_list(cloud_provider.lower(), ["gcp"]) and not check_key_in_list(region, CONST_GCP_REGIONS):
            REGEX_ERRORS.append(f"ERROR: Region in Stack name, not following GCP Region mapping convention as said in docs. Exiting ...")
        elif check_key_in_list(cloud_provider.lower(), ["aws"]) and not check_key_in_list(region, CONST_AWS_REGIONS):
            REGEX_ERRORS.append(f"ERROR: Region in Stack name, not following AWS Region mapping convention as said in docs. Exiting ...")
    # Project Alias check
    if (len(project_alias) < 3 or len(project_alias) > 5) or not project_alias.isalnum():
        REGEX_ERRORS.append(f"ERROR: Project Alias not in Character range min:3 max:5 characters WITH only alpha-numeric characters, Exiting")

    # unique_identifier
    if (len(unique_identifier) < 3 or len(unique_identifier) > 5) or not unique_identifier.isalnum():
        REGEX_ERRORS.append(f"ERROR: Unique Identifier not in Character range min:3 max:5 characters WITH only alpha-numeric characters, Exiting")

    if REGEX_ERRORS:
        print(dumps(REGEX_ERRORS,indent=2))
        return False
    else:
        return True

