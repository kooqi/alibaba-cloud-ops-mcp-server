import pytest
from unittest.mock import patch, MagicMock
from alibaba_cloud_ops_mcp_server.tools import oos_tools

def get_tool_func(name):
    return [f for f in oos_tools.tools if f.__name__ == name][0]

def fake_client(*args, **kwargs):
    class FakeExecution:
        execution_id = 'exec-1'
        status = 'Success'
        status_message = 'ok'
    class FakeBody:
        executions = [FakeExecution()]
    class FakeListResp:
        body = FakeBody()
    class FakeStartResp:
        class Body:
            class Execution:
                execution_id = 'exec-1'
            execution = Execution()
        body = Body()
    class FakeClient:
        def start_execution(self, req):
            return FakeStartResp()
        def list_executions(self, req):
            return FakeListResp()
    return FakeClient()

@patch('alibaba_cloud_ops_mcp_server.tools.oos_tools.create_client', fake_client)
def test_OOS_RunCommand():
    func = get_tool_func("OOS_RunCommand")
    result = func(RegionId='cn-test', InstanceIds=['i-1'], CommandType='RunShellScript', Command='echo hello')
    assert hasattr(result, 'executions')

@patch('alibaba_cloud_ops_mcp_server.tools.oos_tools.create_client', fake_client)
def test_OOS_StartInstances():
    func = get_tool_func("OOS_StartInstances")
    result = func(RegionId='cn-test', InstanceIds=['i-1'])
    assert hasattr(result, 'executions')

@patch('alibaba_cloud_ops_mcp_server.tools.oos_tools.create_client', fake_client)
def test_OOS_StopInstances():
    func = get_tool_func("OOS_StopInstances")
    result = func(RegionId='cn-test', InstanceIds=['i-1'], ForeceStop=True)
    assert hasattr(result, 'executions')

@patch('alibaba_cloud_ops_mcp_server.tools.oos_tools.create_client', fake_client)
def test_OOS_RebootInstances():
    func = get_tool_func("OOS_RebootInstances")
    result = func(RegionId='cn-test', InstanceIds=['i-1'], ForeceStop=True)
    assert hasattr(result, 'executions')

@patch('alibaba_cloud_ops_mcp_server.tools.oos_tools.create_client', fake_client)
def test_OOS_RunInstances():
    func = get_tool_func("OOS_RunInstances")
    result = func(RegionId='cn-test', ImageId='img', InstanceType='ecs.t1', SecurityGroupId='sg', VSwitchId='vsw', Amount=1, InstanceName='test')
    assert hasattr(result, 'executions')

@patch('alibaba_cloud_ops_mcp_server.tools.oos_tools.create_client', fake_client)
def test_OOS_ResetPassword():
    func = get_tool_func("OOS_ResetPassword")
    result = func(RegionId='cn-test', InstanceIds=['i-1'], Password='Abcd1234!')
    assert hasattr(result, 'executions')

@patch('alibaba_cloud_ops_mcp_server.tools.oos_tools.create_client', fake_client)
def test_OOS_ReplaceSystemDisk():
    func = get_tool_func("OOS_ReplaceSystemDisk")
    result = func(RegionId='cn-test', InstanceIds=['i-1'], ImageId='img')
    assert hasattr(result, 'executions')

@patch('alibaba_cloud_ops_mcp_server.tools.oos_tools.create_client', fake_client)
def test_OOS_StartRDSInstances():
    func = get_tool_func("OOS_StartRDSInstances")
    result = func(RegionId='cn-test', InstanceIds=['rds-1'])
    assert hasattr(result, 'executions')

@patch('alibaba_cloud_ops_mcp_server.tools.oos_tools.create_client', fake_client)
def test_OOS_StopRDSInstances():
    func = get_tool_func("OOS_StopRDSInstances")
    result = func(RegionId='cn-test', InstanceIds=['rds-1'])
    assert hasattr(result, 'executions')

@patch('alibaba_cloud_ops_mcp_server.tools.oos_tools.create_client', fake_client)
def test_OOS_RebootRDSInstances():
    func = get_tool_func("OOS_RebootRDSInstances")
    result = func(RegionId='cn-test', InstanceIds=['rds-1'])
    assert hasattr(result, 'executions') 