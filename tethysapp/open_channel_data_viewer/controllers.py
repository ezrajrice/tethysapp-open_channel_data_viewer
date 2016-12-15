from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import ScatterPlot, TimeSeries
from suds.client import Client
# from pandas import Series


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    # Create the inputs needed for the web service call
    wsdl_url = 'http://worldwater.byu.edu/app/index.php/sediment/services/cuahsi_1_1.asmx?WSDL'

    # Create a new object named "NWIS" for calling the web service methods
    NWIS = Client(wsdl_url).service
    sites_response = NWIS.GetSitesObject()[1]
    sites = []
    for site in sites_response:
        if site.siteInfo.siteProperty[0].value != 'NULL':
            state = site.siteInfo.siteProperty[0].value
        else:
            state = ''
        site_obj = {
            'name': site.siteInfo.siteName.lstrip(),
            'site_code': site.siteInfo.siteCode[0].value,  # Gets the value of siteCode
            'latitude': site.siteInfo.geoLocation.geogLocation.latitude,
            'longitude': site.siteInfo.geoLocation.geogLocation.longitude,
            'state': state
        }
        sites.append(site_obj)

    context = {"sites": sites}

    return render(request, 'open_channel_data_viewer/home.html', context)


@login_required()
def site_details(request, site_code):
    """
    """
    # Create the inputs needed for the web service call
    wsdl_url = 'http://worldwater.byu.edu/app/index.php/sediment/services/cuahsi_1_1.asmx?WSDL'

    site_lookup = 'sediment:' + site_code
    # Create a new object named "NWIS" for calling the web service methods
    NWIS = Client(wsdl_url).service
    site_info = NWIS.GetSiteInfoObject(site_lookup)[1][0]
    site_name = site_info.siteInfo.siteName.lstrip()
    latitude = site_info.siteInfo.geoLocation.geogLocation.latitude
    longitude = site_info.siteInfo.geoLocation.geogLocation.longitude
    site_location = site_info.siteInfo.siteProperty[0].value

    variables = []
    for site in site_info.seriesCatalog[0].series:
        variable = {
            'variable_code': site.variable.variableCode[0].value,
            'variable_name': site.variable.variableName,
            'variable_medium': site.variable.sampleMedium,
            'variable_category': site.variable.generalCategory,
            'variable_units': site.variable.unit.unitAbbreviation
        }
        variables.append(variable)

    # print(variables)

    # Call the GetValuesObject method to return datavalues
    # site_data = NWIS.GetValuesObject(site_lookup, variable_code, begin_date, end_date)

    # Get the site's name from the response
    # site_name = response.timeSeries[0].sourceInfo.siteName

    sediment_transport_data = []

    sediment_transport_dataset = {
        'data': sediment_transport_data
    }

    scatter_plot_view = ScatterPlot(
        width='900px',
        engine='highcharts',
        title='Sediment Transport',
        x_axis_title='Avg Flow',
        x_axis_units='cms',
        y_axis_title='Sediment Transport',
        y_axis_units='kg/s',
        series=[sediment_transport_dataset],
        legend=False
    )

    context = {"scatter_plot_view": scatter_plot_view,
               "site_name": site_name,
               "site_code": site_code,
               "latitude": latitude,
               "longitude": longitude,
               "site_location": site_location,
               "variables": variables}

    return render(request, 'open_channel_data_viewer/site_details.html', context)
