from tethys_sdk.base import TethysAppBase, url_map_maker


class Jhumapper(TethysAppBase):
    name = 'Schigella Risk Assessment Tool'
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
        )