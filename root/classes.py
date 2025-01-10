import pandas as pd
import os
import json

class Network:
    def __init__(self, path):
        self.nodes = []
        self.path = path
        self.data = {}
        
    def load_csv(self):
        filenames = [
            'static_buses', 'static_lines', 'static_generators',
            'static_loads', 'static_transformers'
        ]
        try:
            for filename in filenames:
                # Load csv then convert to json
                df = pd.read_csv(os.path.join(self.path, f'{filename}.csv'))
                self.data[filename] = json.loads(df.to_json(orient='records'))
        
        except Exception as e:
            print(f'Failed to load static fixtures: {e}')

    def automatic_plot(self):
        if 'static_buses' in self.data:
            for bus in self.data['static_buses']:
                self.manual_plot(
                    id=bus['Bus'],
                    # .get() gets a value from the parent element and the second value is the default outcome
                    x=bus.get('x',0),
                    y=bus.get('y',0),
                    label=str(bus['Bus']),
                    classes='bus'
                )
                
        #if 'static_lines' in self.data:
        #    for line in self.data['static_lines']:
        #        self.manual_line(
        #            id=f"ln{line['bus0']}-{line['bus1']}",
        #            source=line['bus0'],
        #            target=line['bus1']
        #        )
        #
        if 'static_loads' in self.data:
            for load in self.data['static_loads']:
                self.manual_plot(
                    id=str(load['Load']),
                    label=str(load['Load']),
                    classes='loads'
                )
                self.manual_line(
                    id=f'{str(load["Load"])}_line',
                    source=str(load['Load']),
                    target=str(load['bus'])
                )
        
        if 'static_transformers' in self.data:
            for transformer in self.data['static_transformers']:
                self.manual_plot(
                    id=str(transformer['Transformer']),
                    label=str(transformer['Transformer']),
                    classes='trans'
                )
                self.manual_line(
                    id=str(transformer['Transformer']),
                    source=str(transformer['bus0']),
                    target=str(transformer['bus1'])
                )
                
    def manual_plot(self,id,x=0,y=0,label=None,classes='default-classes'):
        node_dict = {
            'data': {
                'id': str(id),
                'label': str(label),
                'position': {'x': x, 'y': y}
            },
            'classes': classes
        }
        self.nodes.append(node_dict)
    
    def manual_line(self,id,source,target, classes='default-classes'):
        line_dict = {
            'data': {
                'id': str(id),
                'source': str(source),
                'target': str(target)
            },
            'classes': classes
        }
        self.nodes.append(line_dict)
    
    def all_nodes(self):
        return self.nodes
    
    def create_plot(self):
        pass
    
    def test_data(self):
        print(self.data)




















