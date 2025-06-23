import pytest
from unittest.mock import patch, MagicMock

@patch('alibaba_cloud_ops_mcp_server.server.FastMCP')
@patch('alibaba_cloud_ops_mcp_server.server.api_tools.create_api_tools')
def test_main_run(mock_create_api_tools, mock_FastMCP):
    # 创建具有name属性的mock函数
    mock_tool1 = MagicMock()
    mock_tool1.__name__ = 'mock_oss_tool'
    mock_tool2 = MagicMock()
    mock_tool2.__name__ = 'mock_oos_tool'
    mock_tool3 = MagicMock()
    mock_tool3.__name__ = 'mock_cms_tool'
    
    # 创建common_api_tools的mock
    mock_tool4 = MagicMock()
    mock_tool4.__name__ = 'mock_common_tool1'
    mock_tool5 = MagicMock()
    mock_tool5.__name__ = 'mock_common_tool2'
    mock_tool6 = MagicMock()
    mock_tool6.__name__ = 'mock_common_tool3'
    mock_tool7 = MagicMock()
    mock_tool7.__name__ = 'mock_common_tool4'
    
    with patch('alibaba_cloud_ops_mcp_server.server.oss_tools.tools', [mock_tool1]), \
         patch('alibaba_cloud_ops_mcp_server.server.oos_tools.tools', [mock_tool2]), \
         patch('alibaba_cloud_ops_mcp_server.server.cms_tools.tools', [mock_tool3]), \
         patch('alibaba_cloud_ops_mcp_server.server.common_api_tools.tools', [mock_tool4, mock_tool5, mock_tool6, mock_tool7]):
        from alibaba_cloud_ops_mcp_server import server
        mcp = MagicMock()
        mock_FastMCP.return_value = mcp
        # 调用main函数
        server.main.callback(transport='stdio', port=12345, host='127.0.0.1', services='ecs')
        mock_FastMCP.assert_called_once_with(
            name='alibaba-cloud-ops-mcp-server',
            port=12345, host='127.0.0.1')
        assert mcp.add_tool.call_count == 7  # common_api_tools 4 + oss/oos/cms 各1
        mock_create_api_tools.assert_called_once()
        mcp.run.assert_called_once_with(transport='stdio')

def test_run_as_main(monkeypatch):
    import runpy, sys
    from alibaba_cloud_ops_mcp_server import server
    monkeypatch.setattr(server, 'main', lambda *a, **kw: None)
    monkeypatch.setattr(sys, 'argv', ['server.py'])
    import mcp.server.fastmcp
    monkeypatch.setattr(mcp.server.fastmcp.FastMCP, 'run', lambda self, **kwargs: None)
    import pytest
    with pytest.raises(SystemExit) as e:
        runpy.run_path('src/alibaba_cloud_ops_mcp_server/server.py', run_name='__main__')
    assert e.value.code == 0 