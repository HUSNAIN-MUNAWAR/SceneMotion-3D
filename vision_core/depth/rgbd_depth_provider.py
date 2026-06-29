from .external_depth_provider import ExternalDepthProvider
class RGBDDepthProvider(ExternalDepthProvider):
    name = 'rgbd_depth_input'
    is_metric = True
