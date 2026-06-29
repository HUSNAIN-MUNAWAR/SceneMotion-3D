from vision_core.depth.provider_registry import DepthProviderRegistry


def test_depth_provider_registry_fallback():
    reg = DepthProviderRegistry()
    assert 'fallback' in reg.available()
    provider = reg.create('fallback')
    assert hasattr(provider, 'estimate')
