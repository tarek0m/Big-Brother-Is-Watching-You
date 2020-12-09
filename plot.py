from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource
import pandas


def plot(motion_df):
    motion_df["Start"] = pandas.to_datetime(motion_df["Start"], errors='coerce')
    motion_df["End"] = pandas.to_datetime(motion_df["End"], errors='coerce')

    motion_df["Start_str"] = motion_df["Start"].dt.strftime(r"%Y-%m-%d %H:%M:%S")
    motion_df["End_str"] = motion_df["End"].dt.strftime(r"%Y-%m-%d %H:%M:%S")

    cds = ColumnDataSource(motion_df)

    p = figure(x_axis_type= 'datetime', height= 100, width= 500, sizing_mode="stretch_width", title= 'Motoin Graph')
    p.yaxis.minor_tick_line_color = None
    p.yaxis.ticker.desired_num_ticks = 1

    # bokeh adds 'colomn-space'
    hover = HoverTool(tooltips= [("Start", "@Start_str"), ("End", "@End_str")])
    p.add_tools(hover)

    q = p.quad(left= "Start", right= "End", bottom= 0, top= 1, color= "green", source= cds)

    output_file("out\\plots\\motiongraph.html")
    show(p)