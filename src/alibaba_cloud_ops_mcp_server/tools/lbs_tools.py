from pydantic import Field
from typing import List
import os
import json

from alibabacloud_slb20140515.client import Client as slb20140515Client
from alibabacloud_slb20140515 import models as slb_20140515_models
from alibaba_cloud_ops_mcp_server.alibabacloud.utils import create_config

tools = []

def create_client(region_id: str) -> slb20140515Client:
    config = create_config()
    config.endpoint = f'slb.{region_id}.aliyuncs.com'
    return slb20140515Client(config)

@tools.append
def SLB_DescribeLoadBalancers(
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou'),
    load_balancer_name: str = Field(description='负载均衡器名称 (The name of the load balancer)', default=None),
    address: str = Field(description='负载均衡器服务地址 (The service address of the load balancer)', default=None)
):
    """查询已创建的负载均衡器(SLB)实例 (Queries created Server Load Balancer instances)"""
    client = create_client(region_id=region_id)
    describe_load_balancers_request = slb_20140515_models.DescribeLoadBalancersRequest(
        region_id=region_id,
        load_balancer_name=load_balancer_name,
        address=address
    )
    return client.describe_load_balancers(describe_load_balancers_request)

@tools.append
def SLB_DescribeLoadBalancerAttribute(
    load_balancer_id: str = Field(..., description='负载均衡器实例ID (The ID of the SLB instance)'),
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou')
):
    """查询负载均衡器实例的详细信息 (Queries the details of a Classic Load Balancer instance)"""
    client = create_client(region_id=region_id)
    describe_load_balancer_attribute_request = slb_20140515_models.DescribeLoadBalancerAttributeRequest(
        region_id=region_id,
        load_balancer_id=load_balancer_id
    )
    return client.describe_load_balancer_attribute(describe_load_balancer_attribute_request)

@tools.append
def SLB_DeleteLoadBalancer(
    load_balancer_id: str = Field(..., description='负载均衡器实例ID (The ID of the CLB instance)'),
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou')
):
    """删除负载均衡器实例 (Deletes a Classic Load Balancer instance)"""
    client = create_client(region_id=region_id)
    delete_load_balancer_request = slb_20140515_models.DeleteLoadBalancerRequest(
        region_id=region_id,
        load_balancer_id=load_balancer_id
    )
    return client.delete_load_balancer(delete_load_balancer_request)

@tools.append
def SLB_DescribeLoadBalancerListeners(
    load_balancer_id: str = Field(..., description='负载均衡器实例ID (The ID of the SLB instance)'),
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou'),
    listener_port: int = Field(description='监听端口 (The listener port)', default=None),
    protocol: str = Field(description='监听协议：TCP、UDP、HTTP、HTTPS (The listener protocol)', default=None),
    page_number: int = Field(description='页码，从1开始 (The page number. Pages start from page 1)', default=1),
    page_size: int = Field(description='每页数量，最大100 (The number of entries per page. Maximum value: 100)', default=10)
):
    """查询负载均衡器的监听器配置 (Queries the listeners of a Server Load Balancer instance)"""
    client = create_client(region_id=region_id)

    params = {
        'region_id': region_id,
        'load_balancer_id': load_balancer_id,
        'page_number': page_number,
        'page_size': page_size
    }

    if listener_port:
        params['listener_port'] = listener_port
    if protocol:
        params['protocol'] = protocol

    describe_load_balancer_listeners_request = slb_20140515_models.DescribeLoadBalancerListenersRequest(**params)
    return client.describe_load_balancer_listeners(describe_load_balancer_listeners_request)

@tools.append
def SLB_DescribeBackendServers(
    load_balancer_id: str = Field(..., description='负载均衡器实例ID (The ID of the SLB instance)'),
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou')
):
    """查询负载均衡器的后端服务器列表 (Queries the backend servers of a Server Load Balancer instance)"""
    client = create_client(region_id=region_id)

    describe_load_balancer_attribute_request = slb_20140515_models.DescribeLoadBalancerAttributeRequest(
        region_id=region_id,
        load_balancer_id=load_balancer_id
    )
    return client.describe_load_balancer_attribute(describe_load_balancer_attribute_request)

@tools.append
def SLB_DescribeHealthStatus(
    load_balancer_id: str = Field(..., description='负载均衡器实例ID (The ID of the SLB instance)'),
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou'),
    listener_port: int = Field(description='监听端口 (The listener port)', default=None)
):
    """查询负载均衡器的健康检查状态 (Queries the health check status of a Server Load Balancer instance)"""
    client = create_client(region_id=region_id)

    params = {
        'region_id': region_id,
        'load_balancer_id': load_balancer_id
    }

    if listener_port:
        params['listener_port'] = listener_port

    describe_health_status_request = slb_20140515_models.DescribeHealthStatusRequest(**params)
    return client.describe_health_status(describe_health_status_request)

@tools.append
def SLB_DescribeServerCertificates(
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou'),
    server_certificate_id: str = Field(description='服务器证书ID (The ID of the server certificate)', default=None),
    server_certificate_name: str = Field(description='服务器证书名称 (The name of the server certificate)', default=None),
    page_number: int = Field(description='页码，从1开始 (The page number. Pages start from page 1)', default=1),
    page_size: int = Field(description='每页数量，最大100 (The number of entries per page. Maximum value: 100)', default=10)
):
    """查询服务器证书列表 (Queries the server certificates)"""
    client = create_client(region_id=region_id)

    params = {
        'region_id': region_id,
        'page_number': page_number,
        'page_size': page_size
    }

    if server_certificate_id:
        params['server_certificate_id'] = server_certificate_id
    if server_certificate_name:
        params['server_certificate_name'] = server_certificate_name

    describe_server_certificates_request = slb_20140515_models.DescribeServerCertificatesRequest(**params)
    return client.describe_server_certificates(describe_server_certificates_request)

@tools.append
def SLB_DescribeCACertificates(
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou'),
    ca_certificate_id: str = Field(description='CA证书ID (The ID of the CA certificate)', default=None),
    ca_certificate_name: str = Field(description='CA证书名称 (The name of the CA certificate)', default=None),
    page_number: int = Field(description='页码，从1开始 (The page number. Pages start from page 1)', default=1),
    page_size: int = Field(description='每页数量，最大100 (The number of entries per page. Maximum value: 100)', default=10)
):
    """查询CA证书列表 (Queries the CA certificates)"""
    client = create_client(region_id=region_id)

    params = {
        'region_id': region_id,
        'page_number': page_number,
        'page_size': page_size
    }

    if ca_certificate_id:
        params['ca_certificate_id'] = ca_certificate_id
    if ca_certificate_name:
        params['ca_certificate_name'] = ca_certificate_name

    describe_ca_certificates_request = slb_20140515_models.DescribeCACertificatesRequest(**params)
    return client.describe_ca_certificates(describe_ca_certificates_request)

@tools.append
def SLB_DescribeVServerGroups(
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou'),
    load_balancer_id: str = Field(description='负载均衡器实例ID (The ID of the SLB instance)', default=None),
    v_server_group_id: str = Field(description='虚拟服务器组ID (The ID of the VServer group)', default=None),
    v_server_group_name: str = Field(description='虚拟服务器组名称 (The name of the VServer group)', default=None),
    page_number: int = Field(description='页码，从1开始 (The page number. Pages start from page 1)', default=1),
    page_size: int = Field(description='每页数量，最大100 (The number of entries per page. Maximum value: 100)', default=10)
):
    """查询虚拟服务器组列表 (Queries the VServer groups)"""
    client = create_client(region_id=region_id)

    params = {
        'region_id': region_id,
        'page_number': page_number,
        'page_size': page_size
    }

    if load_balancer_id:
        params['load_balancer_id'] = load_balancer_id
    if v_server_group_id:
        params['v_server_group_id'] = v_server_group_id
    if v_server_group_name:
        params['v_server_group_name'] = v_server_group_name

    describe_v_server_groups_request = slb_20140515_models.DescribeVServerGroupsRequest(**params)
    return client.describe_v_server_groups(describe_v_server_groups_request)

@tools.append
def SLB_DescribeMasterSlaveServerGroups(
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou'),
    load_balancer_id: str = Field(description='负载均衡器实例ID (The ID of the SLB instance)', default=None),
    master_slave_server_group_id: str = Field(description='主备服务器组ID (The ID of the master-slave server group)', default=None),
    master_slave_server_group_name: str = Field(description='主备服务器组名称 (The name of the master-slave server group)', default=None),
    page_number: int = Field(description='页码，从1开始 (The page number. Pages start from page 1)', default=1),
    page_size: int = Field(description='每页数量，最大100 (The number of entries per page. Maximum value: 100)', default=10)
):
    """查询主备服务器组列表 (Queries the master-slave server groups)"""
    client = create_client(region_id=region_id)

    params = {
        'region_id': region_id,
        'page_number': page_number,
        'page_size': page_size
    }

    if load_balancer_id:
        params['load_balancer_id'] = load_balancer_id
    if master_slave_server_group_id:
        params['master_slave_server_group_id'] = master_slave_server_group_id
    if master_slave_server_group_name:
        params['master_slave_server_group_name'] = master_slave_server_group_name

    describe_master_slave_server_groups_request = slb_20140515_models.DescribeMasterSlaveServerGroupsRequest(**params)
    return client.describe_master_slave_server_groups(describe_master_slave_server_groups_request)

@tools.append
def SLB_DescribeRegions(
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default=None)
):
    """查询阿里云支持的地域列表 (Queries the regions that are supported by Alibaba Cloud)"""
    client = create_client(region_id='cn-hangzhou')  # Use default region for this API

    params = {}
    if region_id:
        params['region_id'] = region_id

    describe_regions_request = slb_20140515_models.DescribeRegionsRequest(**params)
    return client.describe_regions(describe_regions_request)

@tools.append
def SLB_DescribeZones(
    region_id: str = Field(description='阿里云地域ID (AlibabaCloud region ID)', default='cn-hangzhou')
):
    """查询指定地域下的可用区列表 (Queries the zones that are available in the specified region)"""
    client = create_client(region_id=region_id)

    describe_zones_request = slb_20140515_models.DescribeZonesRequest(region_id=region_id)
    return client.describe_zones(describe_zones_request)
