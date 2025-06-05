import pytest
from unittest.mock import patch, MagicMock
from alibaba_cloud_ops_mcp_server.tools import cms_tools

def get_tool_func(name):
    return [f for f in cms_tools.tools if f.__name__ == name][0]

def fake_client(*args, **kwargs):
    class FakeResp:
        class Body:
            datapoints = [{"value": 1}]
        body = Body()
        def __init__(self):
            pass
    class FakeClient:
        def describe_metric_last(self, req):
            return FakeResp()
    return FakeClient()

@patch('alibaba_cloud_ops_mcp_server.tools.cms_tools.create_client', fake_client)
def test_CMS_GetCpuUsageData():
    func = get_tool_func("CMS_GetCpuUsageData")
    result = func(RegionId='cn-test', InstanceIds=['i-1'])
    assert isinstance(result, list)
    assert result[0]["value"] == 1

@patch('alibaba_cloud_ops_mcp_server.tools.cms_tools.create_client', fake_client)
def test_CMS_GetCpuLoadavgData():
    func = get_tool_func("CMS_GetCpuLoadavgData")
    result = func(RegionId='cn-test', InstanceIds=['i-1'])
    assert isinstance(result, list)

@patch('alibaba_cloud_ops_mcp_server.tools.cms_tools.create_client', fake_client)
def test_CMS_GetCpuloadavg5mData():
    func = get_tool_func("CMS_GetCpuloadavg5mData")
    result = func(RegionId='cn-test', InstanceIds=['i-1'])
    assert isinstance(result, list)

@patch('alibaba_cloud_ops_mcp_server.tools.cms_tools.create_client', fake_client)
def test_CMS_GetCpuloadavg15mData():
    func = get_tool_func("CMS_GetCpuloadavg15mData")
    result = func(RegionId='cn-test', InstanceIds=['i-1'])
    assert isinstance(result, list)

@patch('alibaba_cloud_ops_mcp_server.tools.cms_tools.create_client', fake_client)
def test_CMS_GetMemUsedData():
    func = get_tool_func("CMS_GetMemUsedData")
    result = func(RegionId='cn-test', InstanceIds=['i-1'])
    assert isinstance(result, list)

@patch('alibaba_cloud_ops_mcp_server.tools.cms_tools.create_client', fake_client)
def test_CMS_GetMemUsageData():
    func = get_tool_func("CMS_GetMemUsageData")
    result = func(RegionId='cn-test', InstanceIds=['i-1'])
    assert isinstance(result, list)

@patch('alibaba_cloud_ops_mcp_server.tools.cms_tools.create_client', fake_client)
def test_CMS_GetDiskUsageData():
    func = get_tool_func("CMS_GetDiskUsageData")
    result = func(RegionId='cn-test', InstanceIds=['i-1'])
    assert isinstance(result, list)

@patch('alibaba_cloud_ops_mcp_server.tools.cms_tools.create_client', fake_client)
def test_CMS_GetDiskTotalData():
    func = get_tool_func("CMS_GetDiskTotalData")
    result = func(RegionId='cn-test', InstanceIds=['i-1'])
    assert isinstance(result, list)

@patch('alibaba_cloud_ops_mcp_server.tools.cms_tools.create_client', fake_client)
def test_CMS_GetDiskUsedData():
    func = get_tool_func("CMS_GetDiskUsedData")
    result = func(RegionId='cn-test', InstanceIds=['i-1'])
    assert isinstance(result, list) 