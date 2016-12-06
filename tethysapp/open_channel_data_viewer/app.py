from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.stores import PersistentStore


class OpenChannelDataViewer(TethysAppBase):
    """
    Tethys app class for Open Channel Data Viewer.
    """

    name = 'Open Channel Data Viewer'
    index = 'open_channel_data_viewer:home'
    icon = 'open_channel_data_viewer/images/icon.gif'
    package = 'open_channel_data_viewer'
    root_url = 'open-channel-data-viewer'
    color = '#29a3a3'
    description = ''
    enable_feedback = False
    feedback_emails = ['ezra.j.rice@gmail.com']

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='open-channel-data-viewer',
                           controller='open_channel_data_viewer.controllers.home'),
                    UrlMap(name='site_details',
                           url='open-channel-data-viewer/{site_code}/site-details',
                           regex='[0-9A-Za-z_ .-]+',
                           controller='open_channel_data_viewer.controllers.site_details'),
                    )

        return url_maps
