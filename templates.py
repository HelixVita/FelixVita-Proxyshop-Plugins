"""
FELIXVITA's TEMPLATES
"""
import proxyshop.templates as temp
from proxyshop.constants import con
from proxyshop.settings import cfg
import proxyshop.helpers as psd
import photoshop.api as ps
app = ps.Application()


class AncientTemplate (temp.NormalClassicTemplate):
    """
    FelixVita's template
    """
    template_file_name = "normal-classic.psd"
    template_suffix = "Ancient"

    def __init__(self, layout):
        super().__init__(layout)

    def enable_frame_layers(self):
        super().enable_frame_layers()


