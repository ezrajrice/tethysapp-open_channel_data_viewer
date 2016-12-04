from datetime import datetime
from suds.client import Client
from pandas import Series
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .model import SessionMaker, OpenChannelData
from tethys_sdk.gizmos import ScatterPlot, TimeSeries


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    # Create the inputs needed for the web service call
    wsdl_url = 'http://hydroportal.cuahsi.org/nwisuv/cuahsi_1_1.asmx?WSDL'
    site_code = 'NWISUV:10109000'
    variable_code = 'NWISUV:00060'
    begin_date = '2016-08-01'
    end_date = '2016-11-28'

    # Create a new object named "NWIS" for calling the web service methods
    NWIS = Client(wsdl_url).service

    # Call the GetValuesObject method to return datavalues
    response = NWIS.GetValuesObject(site_code, variable_code, begin_date, end_date)

    # Get the site's name from the response
    site_name = response.timeSeries[0].sourceInfo.siteName
    sites_query = []
    sites = []
    for site in sites_query:
        site_id = site.name.replace(' ', '-')
        site_obj = {
            'id': site_id,
            'name': site.name,
            'min_date': site.min_date,
            'max_date': site.max_date
        }
        sites.append(site_obj)

    context = {"sites": sites}

    return render(request, 'open_channel_data_viewer/home.html', context)


@login_required()
def site_details(request, site_name):
    """
    """
    # Create the connection to db
    session = SessionMaker()

    site_name = site_name.replace('-', ' ')
    metadata_query = session.query(OpenChannelData.drainage_area,
                                   OpenChannelData.sampling_method).\
        filter(OpenChannelData.name == site_name).\
        distinct().\
        first()

    data_query = session.query(OpenChannelData.tot_bedload_rate,
                               OpenChannelData.avg_flow,
                               OpenChannelData.avg_velocity,
                               OpenChannelData.avg_depth,
                               OpenChannelData.record_date). \
        filter(OpenChannelData.name == site_name). \
        all()

    sediment_transport_data = []
    velocity_data = []
    depth_data = []
    flow_data = []

    for row in data_query:
        date_list = []
        sediment_transport_data.append([row.avg_flow, row.tot_bedload_rate])
        date_res = row.record_date.split('/')
        for x in date_res:
            date_list.append(int(x))
        row_date = datetime(date_list[2], date_list[0], date_list[1])
        velocity_data.append([row_date, row.avg_velocity])
        depth_data.append([row_date, row.avg_depth])
        flow_data.append([row_date, row.avg_flow])

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

    velocity_timeseries = TimeSeries(
        width='900px',
        engine='highcharts',
        title='Velocity Timeseries Plot',
        y_axis_title='Velocity',
        y_axis_units='m/s',
        series=[{'data': velocity_data}],
        legend=False
    )

    depth_timeseries = TimeSeries(
        width='900px',
        engine='highcharts',
        title='Depth Timeseries Plot',
        y_axis_title='Depth',
        y_axis_units='m',
        series=[{'data': depth_data}],
        legend=False
    )

    flow_timeseries = TimeSeries(
        width='900px',
        engine='highcharts',
        title='Flow Timeseries Plot',
        y_axis_title='Flow',
        y_axis_units='cms',
        series=[{'data': flow_data}],
        legend=False
    )

    session.close()

    context = {"scatter_plot_view": scatter_plot_view,
               "velocity_timeseries": velocity_timeseries,
               "depth_timeseries": depth_timeseries,
               "flow_timeseries": flow_timeseries,
               "site_name": site_name,
               "meta_data": metadata_query}

    return render(request, 'open_channel_data_viewer/site_details.html', context)
