import pytest
from unittest.mock import patch, MagicMock
from alibaba_cloud_ops_mcp_server.tools import api_tools

def fake_api_meta(post=False, no_summary=False):
    meta = {
        'parameters': [
            {'name': 'InstanceId', 'schema': {'type': 'string', 'description': '实例ID', 'example': 'i-123', 'required': True}},
            {'name': 'RegionId', 'schema': {'type': 'string', 'description': '地域ID', 'example': 'cn-hangzhou', 'required': False}},
            {'name': 'Ids', 'schema': {'type': 'array', 'description': 'ID列表', 'example': '"[\"a\",\"b\"]"', 'required': False}},
        ],
        'methods': ['post'] if post else ['get'],
        'path': '/test',
    }
    if not no_summary:
        meta['summary'] = '测试API'
    return meta, '2023-01-01'

class DummyMCP:
    def tool(self, name):
        def decorator(fn):
            return fn
        return decorator

def test_create_function_schemas():
    api_meta, _ = fake_api_meta()
    schemas = api_tools._create_function_schemas('ecs', 'DescribeInstances', api_meta)
    assert 'DescribeInstances' in schemas
    assert 'InstanceId' in schemas['DescribeInstances']
    assert schemas['DescribeInstances']['InstanceId'][0] == str
    assert schemas['DescribeInstances']['Ids'][0] == list

def test_create_parameter_schema():
    fields = {
        'foo': (str, MagicMock()),
        'bar': (int, MagicMock())
    }
    schema_cls = api_tools._create_parameter_schema(fields)
    inst = schema_cls(foo='a', bar=1)
    assert inst.foo == 'a' and inst.bar == 1

def test_create_tool_function_with_signature_required():
    api_meta, _ = fake_api_meta()
    schemas = api_tools._create_function_schemas('ecs', 'DescribeInstances', api_meta)
    fields = schemas['DescribeInstances']
    func = api_tools._create_tool_function_with_signature('ecs', 'DescribeInstances', fields, 'desc')
    # 检查参数名、类型、注释和default存在
    for name, (typ, field_info) in fields.items():
        param = func.__signature__.parameters[name]
        assert param.name == name
        assert param.annotation == typ
        assert hasattr(param, 'default')

def test_create_client_non_str_service():
    with patch('alibaba_cloud_ops_mcp_server.tools.api_tools.OpenApiClient') as mock_client, \
         patch('alibaba_cloud_ops_mcp_server.tools.api_tools.create_config') as mock_cfg:
        mock_cfg.return_value = MagicMock()
        client = api_tools.create_client(service=MagicMock(__str__=lambda self: 'ecs'), region_id='cn-test')
        assert mock_client.called
        assert mock_cfg.return_value.endpoint == 'ecs.cn-test.aliyuncs.com'

def test_tools_api_call_post():
    with patch('alibaba_cloud_ops_mcp_server.tools.api_tools.ApiMetaClient') as mock_ApiMetaClient, \
         patch('alibaba_cloud_ops_mcp_server.tools.api_tools.create_client') as mock_create_client, \
         patch('alibaba_cloud_ops_mcp_server.tools.api_tools.open_api_models') as mock_open_api_models, \
         patch('alibaba_cloud_ops_mcp_server.tools.api_tools.OpenApiUtilClient') as mock_OpenApiUtilClient, \
         patch('alibaba_cloud_ops_mcp_server.tools.api_tools.util_models') as mock_util_models:
        mock_ApiMetaClient.get_api_meta.return_value = fake_api_meta(post=True)
        mock_ApiMetaClient.get_service_version.return_value = '2023-01-01'
        mock_ApiMetaClient.get_service_style.return_value = 'RPC'
        mock_open_api_models.OpenApiRequest.return_value = MagicMock()
        mock_open_api_models.Params.return_value = MagicMock()
        mock_create_client.return_value.call_api.return_value = {'result': 'ok'}
        mock_OpenApiUtilClient.query.return_value = {}
        mock_util_models.RuntimeOptions.return_value = MagicMock()
        params = {'InstanceId': 'i-123', 'RegionId': 'cn-hangzhou'}
        result = api_tools._tools_api_call('ecs', 'DescribeInstances', params, None)
        assert result == {'result': 'ok'}

def test_create_and_decorate_tool_no_summary():
    with patch('alibaba_cloud_ops_mcp_server.tools.api_tools.ApiMetaClient.get_api_meta', return_value=fake_api_meta(no_summary=True)):
        mcp = DummyMCP()
        fn = api_tools._create_and_decorate_tool(mcp, 'ecs', 'DescribeInstances')
        assert callable(fn)

def test_create_api_tools():
    with patch('alibaba_cloud_ops_mcp_server.tools.api_tools._create_and_decorate_tool') as mock_create:
        mcp = DummyMCP()
        config = {'ecs': ['DescribeInstances', 'StartInstance'], 'rds': ['DescribeDBInstances']}
        api_tools.create_api_tools(mcp, config)
        assert mock_create.call_count == 3

def test_create_function_schemas_ignore_dot():
    api_meta = {
        'parameters': [
            {'name': 'foo.bar', 'schema': {'type': 'string'}},
            {'name': 'baz', 'schema': {'type': 'string'}},
        ]
    }
    schemas = api_tools._create_function_schemas('ecs', 'TestApi', api_meta)
    assert 'foo.bar' not in schemas['TestApi']
    assert 'baz' in schemas['TestApi']

def test_create_function_schemas_no_regionid():
    api_meta = {
        'parameters': [
            {'name': 'foo', 'schema': {'type': 'string'}},
        ]
    }
    schemas = api_tools._create_function_schemas('ecs', 'TestApi', api_meta)
    assert 'RegionId' in schemas['TestApi']

# 说明：由于 _create_tool_function_with_signature 生成的参数总有默认值，signature.bind 不会因缺参数抛 TypeError，故无法覆盖该异常分支。

def test_create_client_str_service():
    with patch('alibaba_cloud_ops_mcp_server.tools.api_tools.OpenApiClient') as mock_client, \
         patch('alibaba_cloud_ops_mcp_server.tools.api_tools.create_config') as mock_cfg:
        mock_cfg.return_value = MagicMock()
        client = api_tools.create_client(service='ecs', region_id='cn-test')
        assert mock_client.called
        assert mock_cfg.return_value.endpoint == 'ecs.cn-test.aliyuncs.com'

def test_create_and_decorate_tool_api_meta_exception():
    # 覆盖 _create_and_decorate_tool 的异常分支
    with patch('alibaba_cloud_ops_mcp_server.tools.api_tools.ApiMetaClient.get_api_meta', side_effect=Exception('meta-fail')):
        mcp = DummyMCP()
        with pytest.raises(Exception) as e:
            api_tools._create_and_decorate_tool(mcp, 'ecs', 'DescribeInstances')
        assert 'meta-fail' in str(e.value)
