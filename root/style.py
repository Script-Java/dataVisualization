stylesheet = [
    # Style for nodes
    {
        'selector': 'node',
        'style': {
            'width': 'mapData(degree, 0, 20, 10, 50)',  # Dynamic node sizing based on degree
            'height': 'mapData(degree, 0, 20, 10, 50)',
            'content': 'data(label)',  # Display node label as content
            'font-size': '12px',
            'background-color': 'white',  # Node color changed to white
            'color': 'black',  # Text color changed to black for visibility
            'overlay-padding': '6px',
            'z-index': '5000'
        }
    },
    # Style for edges
    {
        'selector': 'edge',
        'style': {
            'width': 5,
            'line-color': '#ccc',  # Edge color changed to light gray for subtle contrast
            'curve-style': 'bezier'
        }
    },
    # Style for node hover
    {
        'selector': 'node:hover',
        'style': {
            'background-color': 'lightblue',  # Hover background color for high visibility
            'color': 'black',  # Ensuring text color remains black for readability
            'line-color': 'black',
            'target-arrow-color': 'black',
            'source-arrow-color': 'black',
            'text-outline-color': 'black',
            'z-index': '9999'
        }
    },
    # Style for selected node
    {
        'selector': ':selected',
        'style': {
            'border-width': 3,
            'border-color': 'black'  # Selected border color changed to black for visibility
        }
    },
    {
        'selector': '.loads',
        'style': {
            'background-image': 'url(assets/home.jpg)',
            'background-fit': 'cover'
        }
    },
    {
        'selector':'.trans',
        'style': {
            'background-image': 'url(assets/transformer.jpg)',
            'background-fit': 'cover',
            'width': '60px',
            'height': '60px'
            
        }
    },
    {
        'selector': '.gas',
        'style': {
            'background-image': 'url(assets/gas.jpg)',
            'background-fit': 'cover'

        }
    },
    {
        'selector': '.wind',
        'style': {
            'background-image': 'url(assets/wind.jpg)',
            'background-fit': 'cover'

        }
    },
    {
        'selector': '.nuclear',
        'style': {
            'background-image': 'url(assets/nuclear.jpg)',
            'background-fit': 'cover'

        }
    },
    {
        'selector': '.gen',
        'style': {
            'width': '40px',
            'height': '40px'
        }
    },
    {
        'selector': '.bus',
        'style': {
            'background-image': 'url(assets/util_line.jpg)',
            'background-fit': 'cover'

        }
    },
    {
        'selector': '.gen_line',
        'style': {
            'width': 1,
            'line-style': 'dashed',
            'line-color': '#bbb',  # Edge color changed to light gray for subtle contrast
            'curve-style': 'bezier'
            
        }
    },
    {
        'selector': '.lines',
        'style': {
            'background-image': 'url(assets/line.jpg)',
            'background-fit': 'cover'
        }
    }
]