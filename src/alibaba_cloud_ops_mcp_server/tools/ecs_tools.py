from pydantic import Field
from typing import List, Optional
import json

from alibabacloud_ecs20140526.client import Client as ecs20140526Client
from alibabacloud_ecs20140526 import models as ecs_20140526_models
from alibaba_cloud_ops_mcp_server.alibabacloud.utils import create_config

tools = []

def create_client(region_id: str) -> ecs20140526Client:
    config = create_config()
    config.endpoint = f'ecs.{region_id}.aliyuncs.com'
    return ecs20140526Client(config)

@tools.append
def ECS_DescribeInstances(
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou'),
    instance_ids: Optional[List[str]] = Field(description='实例ID列表，最多100个实例ID，使用JSON数组格式 (The IDs of instances. The value can be a JSON array that consists of up to 100 instance IDs)', default=None),
    instance_name: str = Field(description='实例名称 (The name of the instance)', default=None),
    status: str = Field(description='实例状态：运行中(Running)、启动中(Starting)、停止中(Stopping)、已停止(Stopped) (The status of the instance)', default=None),
    instance_type: str = Field(description='实例规格类型 (The instance type)', default=None),
    vpc_id: str = Field(description='专有网络VPC ID (The ID of the virtual private cloud)', default=None),
    v_switch_id: str = Field(description='虚拟交换机vSwitch ID (The ID of the vSwitch)', default=None),
    security_group_id: str = Field(description='安全组ID (The ID of the security group)', default=None),
    zone_id: str = Field(description='可用区ID (The ID of the zone)', default=None),
    page_number: int = Field(description='页码，从1开始 (The page number. Pages start from page 1)', default=1),
    page_size: int = Field(description='每页数量，最大100 (The number of entries per page. Maximum value: 100)', default=10)
):
    """查询一个或多个弹性计算服务(ECS)实例的详细信息 (Queries details of one or more Elastic Compute Service instances)"""
    client = create_client(region_id=region_id)

    # Prepare parameters
    params = {
        'region_id': region_id,
        'page_number': page_number,
        'page_size': page_size
    }

    if instance_ids:
        # 如果传入的是字符串，尝试解析为JSON数组
        if isinstance(instance_ids, str):
            try:
                instance_ids = json.loads(instance_ids)
            except json.JSONDecodeError:
                # 如果不是JSON格式，当作单个实例ID处理
                instance_ids = [instance_ids]
        params['instance_ids'] = json.dumps(instance_ids)
    if instance_name:
        params['instance_name'] = instance_name
    if status:
        params['status'] = status
    if instance_type:
        params['instance_type'] = instance_type
    if vpc_id:
        params['vpc_id'] = vpc_id
    if v_switch_id:
        params['v_switch_id'] = v_switch_id
    if security_group_id:
        params['security_group_id'] = security_group_id
    if zone_id:
        params['zone_id'] = zone_id

    describe_instances_request = ecs_20140526_models.DescribeInstancesRequest(**params)
    return client.describe_instances(describe_instances_request)

@tools.append
def ECS_DescribeInstanceTypes(
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou'),
    instance_type_family: str = Field(description='实例规格族 (The instance family)', default=None),
    instance_type: str = Field(description='实例规格类型 (The instance type)', default=None),
    cpu_architecture: str = Field(description='CPU架构：X86、ARM (The CPU architecture)', default=None)
):
    """查询地域中可用的实例规格类型 (Queries the instance types that are available in a region)"""
    client = create_client(region_id=region_id)

    params = {'region_id': region_id}
    if instance_type_family:
        params['instance_type_family'] = instance_type_family
    if instance_type:
        params['instance_type'] = instance_type
    if cpu_architecture:
        params['cpu_architecture'] = cpu_architecture

    describe_instance_types_request = ecs_20140526_models.DescribeInstanceTypesRequest(**params)
    return client.describe_instance_types(describe_instance_types_request)

@tools.append
def ECS_DescribeImages(
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou'),
    image_id: str = Field(description='镜像ID (The ID of the image)', default=None),
    image_name: str = Field(description='镜像名称 (The name of the image)', default=None),
    image_family: str = Field(description='镜像族系 (The image family)', default=None),
    status: str = Field(description='镜像状态：创建中(Creating)、可用(Available)、不可用(UnAvailable)、创建失败(CreateFailed)、等待中(Waiting) (The status of the image)', default=None),
    image_owner_alias: str = Field(description='镜像来源：系统(system)、自定义(self)、他人(others)、市场(marketplace) (The image source)', default=None),
    page_number: int = Field(description='页码，从1开始 (The page number. Pages start from page 1)', default=1),
    page_size: int = Field(description='每页数量，最大100 (The number of entries per page. Maximum value: 100)', default=10)
):
    """查询地域中可用的镜像信息 (Queries available images in a region)"""
    client = create_client(region_id=region_id)

    params = {
        'region_id': region_id,
        'page_number': page_number,
        'page_size': page_size
    }

    if image_id:
        params['image_id'] = image_id
    if image_name:
        params['image_name'] = image_name
    if image_family:
        params['image_family'] = image_family
    if status:
        params['status'] = status
    if image_owner_alias:
        params['image_owner_alias'] = image_owner_alias

    describe_images_request = ecs_20140526_models.DescribeImagesRequest(**params)
    return client.describe_images(describe_images_request)

@tools.append
def ECS_DescribeInstanceStatus(
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou'),
    zone_id: str = Field(description='可用区ID (The ID of the zone)', default=None),
    instance_id: Optional[List[str]] = Field(description='实例ID列表 (The IDs of instances)', default=None),
    page_number: int = Field(description='页码，从1开始 (The page number. Pages start from page 1)', default=1),
    page_size: int = Field(description='每页数量，最大100 (The number of entries per page. Maximum value: 100)', default=10)
):
    """查询一个或多个ECS实例的状态信息 (Queries the status of one or more ECS instances)"""
    client = create_client(region_id=region_id)

    params = {
        'region_id': region_id,
        'page_number': page_number,
        'page_size': page_size
    }

    if zone_id:
        params['zone_id'] = zone_id
    if instance_id:
        params['instance_id'] = json.dumps(instance_id)

    describe_instance_status_request = ecs_20140526_models.DescribeInstanceStatusRequest(**params)
    return client.describe_instance_status(describe_instance_status_request)

@tools.append
def ECS_DescribeInstanceVncUrl(
    instance_id: str = Field(..., description='实例ID (The ID of the instance)'),
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou')
):
    """查询实例的VNC远程连接地址 (Queries the VNC connection address of an instance)"""
    client = create_client(region_id=region_id)

    describe_instance_vnc_url_request = ecs_20140526_models.DescribeInstanceVncUrlRequest(
        region_id=region_id,
        instance_id=instance_id
    )
    return client.describe_instance_vnc_url(describe_instance_vnc_url_request)

@tools.append
def ECS_DescribeInstanceAttribute(
    instance_id: str = Field(..., description='实例ID (The ID of the instance)'),
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou')
):
    """查询实例的详细属性信息 (Queries detailed attribute information of an instance)"""
    client = create_client(region_id=region_id)

    describe_instance_attribute_request = ecs_20140526_models.DescribeInstanceAttributeRequest(
        instance_id=instance_id
    )
    return client.describe_instance_attribute(describe_instance_attribute_request)

@tools.append
def ECS_DescribeDisks(
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou'),
    disk_ids: Optional[List[str]] = Field(description='磁盘ID列表 (The IDs of disks)', default=None),
    instance_id: str = Field(description='实例ID (The ID of the instance)', default=None),
    disk_type: str = Field(description='磁盘类型：system、data (The type of the disk)', default=None),
    category: str = Field(description='磁盘种类：cloud、cloud_essd、cloud_ssd、cloud_efficiency (The category of the disk)', default=None),
    status: str = Field(description='磁盘状态：In_use、Available、Attaching、Detaching、Creating、ReIniting (The status of the disk)', default=None),
    page_number: int = Field(description='页码，从1开始 (The page number. Pages start from page 1)', default=1),
    page_size: int = Field(description='每页数量，最大100 (The number of entries per page. Maximum value: 100)', default=10)
):
    """查询一个或多个块存储(云盘)的详细信息 (Queries details of one or more block storage devices)"""
    client = create_client(region_id=region_id)

    params = {
        'region_id': region_id,
        'page_number': page_number,
        'page_size': page_size
    }

    if disk_ids:
        params['disk_ids'] = json.dumps(disk_ids)
    if instance_id:
        params['instance_id'] = instance_id
    if disk_type:
        params['disk_type'] = disk_type
    if category:
        params['category'] = category
    if status:
        params['status'] = status

    describe_disks_request = ecs_20140526_models.DescribeDisksRequest(**params)
    return client.describe_disks(describe_disks_request)

@tools.append
def ECS_DescribeSecurityGroups(
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou'),
    security_group_ids: Optional[List[str]] = Field(description='安全组ID列表 (The IDs of security groups)', default=None),
    security_group_name: str = Field(description='安全组名称 (The name of the security group)', default=None),
    vpc_id: str = Field(description='专有网络VPC ID (The ID of the virtual private cloud)', default=None),
    page_number: int = Field(description='页码，从1开始 (The page number. Pages start from page 1)', default=1),
    page_size: int = Field(description='每页数量，最大100 (The number of entries per page. Maximum value: 100)', default=10)
):
    """查询一个或多个安全组的详细信息 (Queries details of one or more security groups)"""
    client = create_client(region_id=region_id)

    params = {
        'region_id': region_id,
        'page_number': page_number,
        'page_size': page_size
    }

    if security_group_ids:
        params['security_group_ids'] = json.dumps(security_group_ids)
    if security_group_name:
        params['security_group_name'] = security_group_name
    if vpc_id:
        params['vpc_id'] = vpc_id

    describe_security_groups_request = ecs_20140526_models.DescribeSecurityGroupsRequest(**params)
    return client.describe_security_groups(describe_security_groups_request)

@tools.append
def ECS_DescribeVpcs(
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou'),
    vpc_id: str = Field(description='专有网络VPC ID (The ID of the virtual private cloud)', default=None),
    vpc_name: str = Field(description='专有网络VPC名称 (The name of the virtual private cloud)', default=None),
    page_number: int = Field(description='页码，从1开始 (The page number. Pages start from page 1)', default=1),
    page_size: int = Field(description='每页数量，最大100 (The number of entries per page. Maximum value: 100)', default=10)
):
    """查询一个或多个专有网络(VPC)的详细信息 (Queries details of one or more virtual private clouds)"""
    client = create_client(region_id=region_id)

    params = {
        'region_id': region_id,
        'page_number': page_number,
        'page_size': page_size
    }

    if vpc_id:
        params['vpc_id'] = vpc_id
    if vpc_name:
        params['vpc_name'] = vpc_name

    describe_vpcs_request = ecs_20140526_models.DescribeVpcsRequest(**params)
    return client.describe_vpcs(describe_vpcs_request)

@tools.append
def ECS_DescribeVSwitches(
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou'),
    v_switch_id: str = Field(description='虚拟交换机vSwitch ID (The ID of the vSwitch)', default=None),
    vpc_id: str = Field(description='专有网络VPC ID (The ID of the virtual private cloud)', default=None),
    zone_id: str = Field(description='可用区ID (The ID of the zone)', default=None),
    page_number: int = Field(description='页码，从1开始 (The page number. Pages start from page 1)', default=1),
    page_size: int = Field(description='每页数量，最大100 (The number of entries per page. Maximum value: 100)', default=10)
):
    """查询一个或多个虚拟交换机(vSwitch)的详细信息 (Queries details of one or more vSwitches)"""
    client = create_client(region_id=region_id)

    params = {
        'region_id': region_id,
        'page_number': page_number,
        'page_size': page_size
    }

    if v_switch_id:
        params['v_switch_id'] = v_switch_id
    if vpc_id:
        params['vpc_id'] = vpc_id
    if zone_id:
        params['zone_id'] = zone_id

    describe_v_switches_request = ecs_20140526_models.DescribeVSwitchesRequest(**params)
    return client.describe_v_switches(describe_v_switches_request)

@tools.append
def ECS_DescribeRegions(
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default=None)
):
    """查询阿里云支持的地域列表 (Queries the regions that are supported by Alibaba Cloud)"""
    client = create_client(region_id='cn-hangzhou')  # Use default region for this API

    params = {}
    if region_id:
        params['region_id'] = region_id

    describe_regions_request = ecs_20140526_models.DescribeRegionsRequest(**params)
    return client.describe_regions(describe_regions_request)

@tools.append
def ECS_DescribeZones(
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou')
):
    """查询指定地域下的可用区列表 (Queries the zones that are available in the specified region)"""
    client = create_client(region_id=region_id)

    describe_zones_request = ecs_20140526_models.DescribeZonesRequest(region_id=region_id)
    return client.describe_zones(describe_zones_request)

@tools.append
def ECS_DescribeKeyPairs(
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou'),
    key_pair_name: str = Field(description='密钥对名称 (The name of the key pair)', default=None),
    key_pair_ids: Optional[List[str]] = Field(description='密钥对ID列表 (The IDs of key pairs)', default=None),
    page_number: int = Field(description='页码，从1开始 (The page number. Pages start from page 1)', default=1),
    page_size: int = Field(description='每页数量，最大100 (The number of entries per page. Maximum value: 100)', default=10)
):
    """查询一个或多个密钥对的详细信息 (Queries details of one or more key pairs)"""
    client = create_client(region_id=region_id)

    params = {
        'region_id': region_id,
        'page_number': page_number,
        'page_size': page_size
    }

    if key_pair_name:
        params['key_pair_name'] = key_pair_name
    if key_pair_ids:
        params['key_pair_ids'] = json.dumps(key_pair_ids)

    describe_key_pairs_request = ecs_20140526_models.DescribeKeyPairsRequest(**params)
    return client.describe_key_pairs(describe_key_pairs_request)

@tools.append
def ECS_DescribeSnapshots(
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou'),
    snapshot_ids: Optional[List[str]] = Field(description='快照ID列表 (The IDs of snapshots)', default=None),
    disk_id: str = Field(description='磁盘ID (The ID of the disk)', default=None),
    snapshot_name: str = Field(description='快照名称 (The name of the snapshot)', default=None),
    status: str = Field(description='快照状态：progressing、accomplished、failed (The status of the snapshot)', default=None),
    usage: str = Field(description='快照用途：image、disk、none (The usage of the snapshot)', default=None),
    page_number: int = Field(description='页码，从1开始 (The page number. Pages start from page 1)', default=1),
    page_size: int = Field(description='每页数量，最大100 (The number of entries per page. Maximum value: 100)', default=10)
):
    """查询一个或多个快照的详细信息 (Queries details of one or more snapshots)"""
    client = create_client(region_id=region_id)

    params = {
        'region_id': region_id,
        'page_number': page_number,
        'page_size': page_size
    }

    if snapshot_ids:
        params['snapshot_ids'] = json.dumps(snapshot_ids)
    if disk_id:
        params['disk_id'] = disk_id
    if snapshot_name:
        params['snapshot_name'] = snapshot_name
    if status:
        params['status'] = status
    if usage:
        params['usage'] = usage

    describe_snapshots_request = ecs_20140526_models.DescribeSnapshotsRequest(**params)
    return client.describe_snapshots(describe_snapshots_request)