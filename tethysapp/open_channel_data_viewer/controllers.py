from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .model import SessionMaker, OpenChannelData
from sqlalchemy import func
from tethys_sdk.gizmos import LinePlot, ScatterPlot


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    # Create a session
    session = SessionMaker()

    # Query DB for gage objects
    sites_query = session.query(OpenChannelData.name, func.Min(OpenChannelData.record_date).label("min_date"),
                          func.Max(OpenChannelData.record_date).label("max_date")).\
        distinct().\
        group_by(OpenChannelData.name).\
        all()
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

    session.close()

    context = {"sites": sites}

    return render(request, 'open_channel_data_viewer/home.html', context)


@login_required()
def site_details(request, site_name):
    """
    """
    # Create the connection to db
    session = SessionMaker()

    site_name = site_name.replace('-', ' ')

    sediment_transport_data_query = session.query(OpenChannelData.tot_bedload_rate,
                                                  OpenChannelData.avg_flow).\
        filter(OpenChannelData.name == site_name).\
        all()

    sediment_transport_data = []

    for row in sediment_transport_data_query:
        sediment_transport_data.append([row.avg_flow, row.tot_bedload_rate])

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

    session.close()

    context = {"scatter_plot_view": scatter_plot_view}

    return render(request, 'open_channel_data_viewer/site_details.html', context)
