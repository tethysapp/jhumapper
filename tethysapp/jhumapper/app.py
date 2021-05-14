from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting


class Jhumapper(TethysAppBase):
    name = 'Shigella Risk Assessment Tool'
    index = 'jhumapper:home'
    icon = 'jhumapper/images/icon.gif'
    package = 'jhumapper'
    root_url = 'jhumapper'
    color = '#c0392b'
    description = ''
    tags = ''
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        UrlMap = url_map_maker(self.root_url)
        return (
            UrlMap(
                name='home',
                url='jhumapper',
                controller='jhumapper.controllers.home'
            ),
            # App API
            UrlMap(
                name='queryValues',
                url='jhumapper/queryValues',
                controller='jhumapper.controllers.query_values'
            ),
        )

    def custom_settings(self):
        return (
            CustomSetting(
                name='thredds_wms_base',
                type=CustomSetting.TYPE_STRING,
                description="WMS URL to the THREDDS directory containing the Schigella data",
                required=True,
                default='http://0.0.0.0:7000/thredds/wms/data/jhudata/',
            ),
        )
