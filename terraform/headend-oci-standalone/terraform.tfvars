#Tenancy and Key Details
tenancy_ocid = " "
user_ocid = " "
fingerprint = " "
private_key_path = " "
par_compartment_id = " "

#Image ID's
analytics_image_id = " "
director_image_id = " "
vos_image_id = " "

#Deployment variables
ssh_public_key_file = " "
regions = ["us-sanjose-1", "us-phoenix-1"]
region = "us-sanjose-1"
availability_domain = " "
vcn_display_name1 = "ALS-VCN-1"
vcn_display_name2 = "ALS-VCN-2"
vcn_cidr_block = "10.140.0.0/16"
northbound_cidr_block = "10.140.0.0/24"
southbound_cidr_block = "10.140.1.0/24"
wan_cidr_block = "10.140.2.0/24"
director_mem_in_gbs = "16"
director_ocpus = "8"
analytics_mem_in_gbs = "16"
analytics_ocpus = "8"
logforwarder_mem_in_gbs = "4"
logforwarder_ocpus = "2"
analytics_nodes_number = "1"
search_nodes_number = "1"
logforwarders_nodes_number = "1"
analytics_instance_shape = "VM.Standard.E4.Flex"
director_instance_shape = "VM.Standard.E4.Flex"
director_instance_name = "ALS-Director"
monitoring_instance_shape = "VM.Standard.E4.Flex"
monitoring_instance_name = "ALS-Director"
controller_instance_shape = "VM.Standard2.4"