from dash import Dash, html, dash_table, dcc
import pandas as pd
import dash_cytoscape as cyto
from dash.dependencies import Input,Output,State
from style import stylesheet
from classes import Network
import plotly.express as px
import os
import datetime
# read CSV file for busses
w_security = Network(os.path.join('data', 'opt_w_security'))
w_security.load_csv()
w_security.automatic_plot()
data = w_security.all_nodes()

line_nodes = [
    {'id': 'xf1f', 'label': 'line', 'classes':'lines'},
    {'id': 'xf4t', 'label': 'line', 'classes':'lines'},
    {'id': 'xf2f', 'label': 'line', 'classes':'lines'},
    {'id': 'xf7t', 'label': 'line', 'classes':'lines'},
    {'id': 'xf9f', 'label': 'line', 'classes':'lines'},
    {'id': 'xf3t', 'label': 'line', 'classes':'lines'},
    
    {'id': 'ln4-5', 'label': 'line', 'classes':'lines'},
    {'id': 'ln6-4', 'label': 'line', 'classes':'lines'},
    {'id': 'ln6-9', 'label': 'line', 'classes':'lines'},
    {'id': 'ln5-7', 'label': 'line', 'classes':'lines'},
    {'id': 'ln7-8', 'label': 'line', 'classes':'lines'},
    {'id': 'ln8-9', 'label': 'line', 'classes':'lines'},
]

static_lines = [
    {'id': 'ln4-5a', 'source': '4', 'target': 'ln4-5'},
    {'id': 'ln0', 'source': 'ln4-5', 'target': '5'},

    {'id': 'ln6-4a', 'source': '6', 'target': 'ln6-4'},
    {'id': 'ln1', 'source': 'ln6-4', 'target': '4'},

    {'id': 'ln6-9a', 'source': '6', 'target': 'ln6-9'},
    {'id': 'ln2', 'source': 'ln6-9', 'target': '9'},

    {'id': 'ln5-7a', 'source': '5', 'target': 'ln5-7'},
    {'id': 'ln3', 'source': 'ln5-7', 'target': '7'},

    {'id': 'ln7-8a', 'source': '7', 'target': 'ln7-8'},
    {'id': 'ln4', 'source': 'ln7-8', 'target': '8'},

    {'id': 'ln8-9a', 'source': '8', 'target': 'ln8-9'},
    {'id': 'ln5', 'source': 'ln8-9', 'target': '9'},
]


for lineN in line_nodes:
    w_security.manual_plot(id=lineN['id'], label=lineN['label'], classes=lineN['classes'])

for line in static_lines:
    w_security.manual_line(id=line['id'], source=line['source'], target=line['target'])


# List of generator nodes
gen_nodes = [
    {'id': 'Gn2', 'label': 'Gas Generator', 'classes': 'gas gen'},
    {'id': 'Gn3', 'label': 'Wind Generator', 'classes': 'wind gen'},
    {'id': 'Gn1', 'label': 'Nuclear Generator', 'classes': 'nuclear gen'}
]

# List of connection lines
gen_lines = [
    {'id': 'gas_line', 'source': 'Gn2', 'target': '2', 'classes': 'gen_line'},
    {'id': 'wind_line', 'source': 'Gn3', 'target': '3', 'classes': 'gen_line'},
    {'id': 'nuclear_line', 'source': 'Gn1', 'target': '1', 'classes': 'gen_line'}
]


# Add generator nodes
for node in gen_nodes:
    w_security.manual_plot(id=node['id'], label=node['label'], classes=node['classes'])

# Add generator lines
for gen_line in gen_lines:
    w_security.manual_line(id=gen_line['id'], source=gen_line['source'], target=gen_line['target'], classes=gen_line['classes'])



# List of transformer connection lines
trans_lines = [
    {'id': 'xf1l', 'source': '1', 'target': 'xf1f'},
    {'id': 'line_node0', 'source': 'xf1f', 'target': 'xf1-4'},
    {'id': 'xf1-4l', 'source': 'xf1-4', 'target': 'xf4t'},
    {'id': 'line_node1', 'source': 'xf4t', 'target': '4'},
    
    {'id': 'xf2l', 'source': '2', 'target': 'xf2f'},
    {'id': 'line_node2', 'source': 'xf2f', 'target': 'xf2-7'},
    {'id': 'xf2-7l', 'source': 'xf2-7', 'target': 'xf7t'},
    {'id': 'line_node3', 'source': 'xf7t', 'target': '7'},
    
    {'id': 'xf9l', 'source': '9', 'target': 'xf9f'},
    {'id': 'line_node4', 'source': 'xf9f', 'target': 'xf9-3'},
    {'id': 'xf9-3l', 'source': 'xf9-3', 'target': 'xf3t'},
    {'id': 'line_node5', 'source': 'xf3t', 'target': '3'}

]

# Assuming `network` is an instance of your Network class
# Add transformer connection lines
for line in trans_lines:
    w_security.manual_line(id=line['id'], source=line['source'], target=line['target'])

app = Dash(__name__)
app.title = 'Network Visualization'

app.layout = html.Div([
    html.H1('Network Visualization', style={'text-align': 'center', 'padding':'10px'}),
    
    html.P('Contingency:'),
    dcc.Dropdown(
    id='data-dropdown',
    options=[
        {'label': 'ln7-8', 'value': 'ln7-8'},
        {'label': 'None', 'value': 'None'}
    ],
    value='None'
    ),

    html.Div(id='security-d'),
    
    cyto.Cytoscape(
        id='cytoscape',
        layout={'name':'cose'},
        style={'width':'100%', 'height':'800px'},
        elements=data,
        stylesheet=stylesheet
    ),
    html.P("Click on a node or edge to see its data here:", style={'text-align':'center'}),
    html.Div(id='output-info', style={'text-align': 'center'}),
    dcc.Graph(id='graph-output'),
    dcc.Graph(id='postctg-graph')
])

@app.callback(
    [
        Output('data-d', 'children'),
    ],
    [
        Input('data-dropdown', 'value')
    ]
)

def dropdownFunc(dataValue, securityValue):
    if securityValue == 'w_security':
        w_security = Network(os.path.join('data', 'opt_w_security'))
    else:
        w_security = Network(os.path.join('data', 'opt_wo_security'))

    return f'You have selected {dataValue}, {securityValue}'


@app.callback(
    [
        Output('output-info', 'children'),  # Output for the DataTable
        Output('graph-output', 'figure')    # Output for the Graph
    ],
    [
        Input('cytoscape', 'tapNodeData')
    ])

def node_data(tapNodeData):
    
    if tapNodeData:
        base_path = w_security.path
        if tapNodeData['id'].startswith('xf'):
            node_id = tapNodeData['id']
            if node_id[-1] == 'f':
                column_mapping = {
                'xf1': 'xf1-4',
                'xf2': 'xf2-7',
                'xf9': 'xf9-3',
                'xf4': 'xf1-4',
                'xf3': 'xf9-3',
                'xf7': 'xf2-7'
                }
                num_part = node_id[2:-1]
                node_id = node_id[:-1]
                print(node_id)
                column_name = column_mapping.get(node_id)
                print(column_name)
                dff = pd.read_csv(os.path.join(base_path, 'static_transformers.csv'))
                graph_df_csv = pd.read_csv(os.path.join(base_path, 'transformers_from_timeseries.csv'))
                trans_x = graph_df_csv['snapshot']
                trans_y = graph_df_csv[column_name]
                graph_fig = px.line(x=trans_x, y=trans_y, labels={'x':'Injection Value', 'y':'Timestamp'}, title=f'Flow Profiles for Transformer {column_name}')
                output_data = dff[dff['Transformer'] == column_name].dropna(axis=1, how='all').to_dict('records')
                empty_table = 'No visual selected'
                return empty_table, graph_fig
                
            elif node_id[-1] == 't':
                column_mapping = {
                'xf1': 'xf1-4',
                'xf2': 'xf2-7',
                'xf9': 'xf9-3',
                'xf4': 'xf1-4',
                'xf3': 'xf9-3',
                'xf7': 'xf2-7'

                }
                num_part = node_id[2:-1]
                node_id = node_id[:-1]
                print(node_id)
                column_name = column_mapping.get(node_id)
                print(column_name)
                dff = pd.read_csv(os.path.join(base_path, 'static_transformers.csv'))
                graph_df_csv = pd.read_csv(os.path.join(base_path, 'transformers_to_timeseries.csv'))
                trans_x = graph_df_csv['snapshot']
                trans_y = graph_df_csv[column_name]
                graph_fig = px.line(x=trans_x, y=trans_y, labels={'x':'Injection Value', 'y':'Timestamp'}, title=f'Flow Profiles for Transformer {column_name}')
                output_data = dff[dff['Transformer'] == column_name].dropna(axis=1, how='all').to_dict('records')
                empty_table = 'No visual selected'
                return empty_table, graph_fig
        

        elif tapNodeData['id'].startswith('ld'):
            dff = pd.read_csv(os.path.join(base_path, 'static_loads.csv'))
            graph_df_csv = pd.read_csv(os.path.join(base_path, 'loads_timeseries.csv'))
            load_id = str(tapNodeData['id'])
            load_x = graph_df_csv['snapshot']
            load_y = graph_df_csv[load_id]
            graph_fig = px.line(x=load_x, y=load_y, labels={'x':'Injection Value', 'y':'Timestamp'}, title=f'Injection Profiles for Load {load_id}')
            output_data = dff[dff['Load'] == tapNodeData['id']].dropna(axis=1, how='all').to_dict('records')
            table = dash_table.DataTable(output_data)
            return table, graph_fig
        
        elif tapNodeData['id'].startswith('Gn'):
            dff = pd.read_csv(os.path.join(base_path, 'static_generators.csv'))
            graph_df_csv = pd.read_csv(os.path.join(base_path, 'generation_production_timeseries.csv'))
            gen_id = str(tapNodeData['id'])
            gen_x = graph_df_csv['snapshot']
            gen_y = graph_df_csv[gen_id]
            graph_fig = px.line(x=gen_x, y=gen_y, labels={'x':'Injection Value', 'y':'Timestamp'}, title=f'Injection Profiles for Generator {gen_id}')
            output_data = dff[dff['Generator'] == tapNodeData['id']].dropna(axis=1, how='all').to_dict('records')
            table = dash_table.DataTable(output_data)
            return table, graph_fig
        
        elif tapNodeData['id'].startswith('ln'):
            base_path = w_security.path
            node_id = tapNodeData['id']
            if node_id[-1] == 'l':
                node_id = node_id[:-1]
            graph_df_csv = pd.read_csv(os.path.join(base_path, 'lines_from_timeseries.csv'))
            lines_id = str(node_id)
            lines_x = graph_df_csv['snapshot']
            lines_y = graph_df_csv[lines_id]
            graph_fig = px.line(x=lines_x, y=lines_y, labels={'x':'Injection Value', 'y':'Timestamp'}, title=f'Injection Profiles for Line {lines_id}')
            empty_table = 'No visual selected'
            return empty_table, graph_fig
        
        else:
            if tapNodeData['id'].startswith('xf'):
                base_path = w_security.path
                dff = pd.read_csv(os.path.join(base_path, 'static_transformers.csv'))
                graph_df_csv = pd.read_csv(os.path.join(base_path, 'transformers_from_timeseries.csv'))
                trans_x = graph_df_csv['snapshot']
                trans_y = graph_df_csv[tapNodeData['id']]
                graph_fig = px.line(x=trans_x, y=trans_y, labels={'x':'Injection Value', 'y':'Timestamp'}, title=f'Flow Profiles for Transformer {tapNodeData["id"]}')
                output_data = dff[dff['Transformer'] == tapNodeData['id']].dropna(axis=1, how='all').to_dict('records')
                table = dash_table.DataTable(output_data)
                empty_graph = px.scatter(title='No Data Available')
                return table, empty_graph
            else:
                dff = pd.read_csv(os.path.join(base_path, 'static_buses.csv'))
                graph_df_csv = pd.read_csv(os.path.join(base_path, 'buses_injection_timeseries.csv'))
                bus_id = str(tapNodeData['id'])
                bus_x = graph_df_csv['snapshot']
                bus_y = graph_df_csv[bus_id]
                graph_fig = px.line(x=bus_x, y=bus_y, labels={'x':'Injection Value', 'y':'Timestamp'}, title=f'Injection Profiles for Bus {bus_id}')
                output_data = dff[dff['Bus'] == int(tapNodeData['id'])].dropna(axis=1, how='all').to_dict('records')
                table = dash_table.DataTable(output_data)
                return table, graph_fig
                
    else:
        # Return empty states for both outputs
        empty_table = 'No visual selected'
        empty_graph = px.scatter(title='No Data Available')
        return empty_table, empty_graph      

if __name__ == '__main__':
    app.run(debug=True)