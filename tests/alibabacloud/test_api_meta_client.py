import pytest
from unittest.mock import patch, MagicMock
from alibaba_cloud_ops_mcp_server.alibabacloud import api_meta_client

@patch('alibaba_cloud_ops_mcp_server.alibabacloud.api_meta_client.requests.get')
def test_get_response_from_pop_api_success(mock_get):
    mock_get.return_value.json.return_value = [{"code": "ecs", "defaultVersion": "2014-05-26", "style": "RPC"}]
    data = api_meta_client.ApiMetaClient.get_response_from_pop_api('GetProductList')
    assert isinstance(data, list)
    assert data[0]["code"] == "ecs"

@patch('alibaba_cloud_ops_mcp_server.alibabacloud.api_meta_client.requests.get')
def test_get_response_from_pop_api_exception(mock_get):
    mock_get.side_effect = Exception('fail')
    with pytest.raises(Exception) as e:
        api_meta_client.ApiMetaClient.get_response_from_pop_api('GetProductList')
    assert 'Failed to get response' in str(e.value)

@patch('alibaba_cloud_ops_mcp_server.alibabacloud.api_meta_client.requests.get')
def test_get_service_version_and_style(mock_get):
    mock_get.return_value.json.return_value = [{"code": "ecs", "defaultVersion": "2014-05-26", "style": "RPC"}]
    v = api_meta_client.ApiMetaClient.get_service_version('ecs')
    s = api_meta_client.ApiMetaClient.get_service_style('ecs')
    assert v == "2014-05-26"
    assert s == "RPC"

@patch('alibaba_cloud_ops_mcp_server.alibabacloud.api_meta_client.requests.get')
def test_get_standard_service_and_api(mock_get):
    # 1st call: GetProductList, 2nd call: GetApiOverview
    mock_get.return_value.json.side_effect = [
        [{"code": "ecs", "defaultVersion": "2014-05-26"}],
        {"apis": {"DescribeInstances": {}}}
    ]
    service, api = api_meta_client.ApiMetaClient.get_standard_service_and_api('ecs', 'DescribeInstances', '2014-05-26')
    assert service == 'ecs'
    assert api == 'DescribeInstances'

@patch('alibaba_cloud_ops_mcp_server.alibabacloud.api_meta_client.requests.get')
def test_get_api_meta_invalid(mock_get):
    # 1st call: GetProductList returns empty list
    mock_get.return_value.json.return_value = []
    with pytest.raises(Exception) as e:
        api_meta_client.ApiMetaClient.get_api_meta('notexist', 'api')
    assert 'InvalidServiceName' in str(e.value) or 'object has no attribute' in str(e.value)

@patch('alibaba_cloud_ops_mcp_server.alibabacloud.api_meta_client.ApiMetaClient.get_service_version', return_value='2014-05-26')
@patch('alibaba_cloud_ops_mcp_server.alibabacloud.api_meta_client.ApiMetaClient.get_standard_service_and_api', return_value=(None, 'api'))
def test_get_api_meta_service_none(mock_get_std, mock_get_ver):
    with pytest.raises(Exception) as e:
        api_meta_client.ApiMetaClient.get_api_meta('ecs', 'DescribeInstances')
    assert 'InvalidServiceName' in str(e.value)

@patch('alibaba_cloud_ops_mcp_server.alibabacloud.api_meta_client.ApiMetaClient.get_service_version', return_value='2014-05-26')
@patch('alibaba_cloud_ops_mcp_server.alibabacloud.api_meta_client.ApiMetaClient.get_standard_service_and_api', return_value=('ecs', None))
def test_get_api_meta_api_none(mock_get_std, mock_get_ver):
    with pytest.raises(Exception) as e:
        api_meta_client.ApiMetaClient.get_api_meta('ecs', 'DescribeInstances')
    assert 'InvalidAPIName' in str(e.value)

@patch('alibaba_cloud_ops_mcp_server.alibabacloud.api_meta_client.ApiMetaClient.get_api_meta', return_value=({}, '2014-05-26'))
def test_get_response_from_api_meta_empty(mock_get_meta):
    prop, ver = api_meta_client.ApiMetaClient.get_response_from_api_meta('ecs', 'DescribeInstances')
    assert prop == {}
    assert ver == '2014-05-26'

@patch('alibaba_cloud_ops_mcp_server.alibabacloud.api_meta_client.ApiMetaClient.get_standard_service_and_api', return_value=('ecs', 'api'))
@patch('alibaba_cloud_ops_mcp_server.alibabacloud.api_meta_client.ApiMetaClient.get_response_from_pop_api')
def test_get_ref_api_meta_keyerror(mock_pop_api, mock_std):
    # ref_path指向不存在的key
    mock_pop_api.return_value = {'apis': {}}
    with pytest.raises(KeyError):
        api_meta_client.ApiMetaClient.get_ref_api_meta({'$ref': '#/notfound'}, 'ecs', '2014-05-26')

@patch('alibaba_cloud_ops_mcp_server.alibabacloud.api_meta_client.ApiMetaClient.get_api_meta')
def test_get_api_parameters_params_in_and_ref(mock_get_meta):
    # 测试params_in过滤和递归ref
    api_meta = {
        'parameters': [
            {'name': 'foo', 'in': 'query', 'schema': {'type': 'string'}},
            {'name': 'bar', 'in': 'body', 'schema': {'type': 'string', '$ref': '#/defs/bar'}}
        ]
    }
    # get_ref_api_meta返回递归结构
    with patch.object(api_meta_client.ApiMetaClient, 'get_ref_api_meta', return_value={'properties': {'baz': {}}}):
        mock_get_meta.return_value = (api_meta, '2014-05-26')
        params = api_meta_client.ApiMetaClient.get_api_parameters('ecs', 'DescribeInstances', params_in='query')
        assert params == ['foo']
        # 测试递归ref
        params2 = api_meta_client.ApiMetaClient.get_api_parameters('ecs', 'DescribeInstances')
        assert 'baz' in params2

@patch('alibaba_cloud_ops_mcp_server.alibabacloud.api_meta_client.ApiMetaClient.get_api_meta')
def test_get_api_parameters_circular_ref(mock_get_meta):
    # 测试循环引用
    api_meta = {
        'parameters': [
            {'name': 'foo', 'in': 'query', 'schema': {'type': 'string', '$ref': '#/defs/foo'}}
        ]
    }
    # get_ref_api_meta返回带$ref的结构，模拟循环
    def fake_get_ref(data, service, version):
        return {'$ref': '#/defs/foo'}
    with patch.object(api_meta_client.ApiMetaClient, 'get_ref_api_meta', side_effect=fake_get_ref):
        mock_get_meta.return_value = (api_meta, '2014-05-26')
        params = api_meta_client.ApiMetaClient.get_api_parameters('ecs', 'DescribeInstances')
        assert 'foo' in params

@patch('alibaba_cloud_ops_mcp_server.alibabacloud.api_meta_client.ApiMetaClient.get_api_meta', side_effect=Exception('fail'))
def test_get_api_field_exception(mock_get_meta):
    val = api_meta_client.ApiMetaClient.get_api_field('parameters', 'ecs', 'DescribeInstances', default='d')
    assert val == 'd'

def test_get_api_body_style_none():
    # get_api_field返回None
    with patch.object(api_meta_client.ApiMetaClient, 'get_api_field', return_value=None):
        val = api_meta_client.ApiMetaClient.get_api_body_style('ecs', 'DescribeInstances')
        assert val is None
    # get_api_field返回无STYLE参数
    with patch.object(api_meta_client.ApiMetaClient, 'get_api_field', return_value=[{'in': 'body'}]):
        val = api_meta_client.ApiMetaClient.get_api_body_style('ecs', 'DescribeInstances')
        assert val is None

@patch('alibaba_cloud_ops_mcp_server.alibabacloud.api_meta_client.requests.get')
def test_get_apis_in_service(mock_get):
    mock_get.return_value.json.return_value = {"apis": {"A": {}, "B": {}}}
    apis = api_meta_client.ApiMetaClient.get_apis_in_service('ecs', '2014-05-26')
    assert set(apis) == {"A", "B"} 