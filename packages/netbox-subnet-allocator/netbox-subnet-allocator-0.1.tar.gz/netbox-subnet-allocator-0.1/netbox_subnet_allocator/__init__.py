from extras.plugins import PluginConfig

class NetBoxManagedSubnets(PluginConfig):
    name = 'netbox_subnet_allocator'
    verbose_name = ' NetBox Subnet Allocator'
    description = 'Managed subnet allocation in NetBox using the Buddy algorithm'
    version = '0.1'
    base_url = 'subnet-allocator'

config = NetBoxSubnetAllocator

