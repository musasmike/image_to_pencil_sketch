# Import packages
import cv2
import datetime
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

# Initialize the application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# APPLICATION LAYOUT
app.layout = html.Div(children=[
    # The title section
    dbc.Row(
        dbc.Col(
            html.Div('Image to Pencil Sketch',
                     style={'font-size': '60px', 'font-family': 'Merriweather', 'font-weight': 'bold',
                            'margin-top': '50px', 'color': 'white'}),
            width={'size': 10, 'offset': 1},
            style={'background-color': '#A63F03', 'padding': '0 0 0 50px'},
            xs=8, sm=8, md=8, lg=10, xl=10
        ), justify='center'
    ),
    html.Br(),
    # Instruction Section
    dbc.Row([
        # Instructions
        dbc.Col([
            html.Div('Instructions'),
            html.Br(),
            html.Div("The instructions goes here."),
            html.Br(),
            html.Br(),
            html.Div("Select the operation"),
            html.Div([
                dcc.Dropdown(["Pencil Sketch"],
                             id="pencil-sketch-dropdown",
                             searchable=False)
            ])
        ],
            width={'size': 10, 'offset': 1},
            xs=8, sm=8, md=8, lg=10, xl=10
        )
    ], justify='center'),
    html.Br(),
    # UPLOAD an image
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Upload(
                    id='upload-image',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    # Allow multiple files to be uploaded
                    multiple=True
                )
            ])
        ],
            width={'size': 10, 'offset': 1},
            xs=8, sm=8, md=8, lg=10, xl=10
        )
    ], justify='center'),
    html.Br(),

    # DISPLAY THE IMAGE
    dbc.Row([
        # Original image
        dbc.Col([
            # Image display
            html.Div(id='output-image-upload')
        ],
            width={'size': 5, 'offset': 1},
            xs=4, sm=4, md=4, lg=5, xl=5
        ),

        # Pencil Sketch Image
        dbc.Col([
            # Image display
            html.Div(id='output-pencil-image')
        ],
            width={'size': 5, 'offset': 1},
            xs=4, sm=4, md=4, lg=5, xl=5
        )

    ], justify="center")

])


def parse_contents(contents, filename, date):
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents),
        html.Hr(),
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


# Define the function image_to_pencil_sketch
# Reads original image
def image_to_pencil_sketch():
    image = cv2.imread("images/car.png")

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Invert the image
    inverted_image = 255 - gray_image
    # Blurring the image
    blurred_image = cv2.GaussianBlur(inverted_image, ksize=(151, 151), sigmaX=0, sigmaY=0)
    # Inverting the blurred image
    inv_blur = 255 - blurred_image
    # Sketch the image
    sketched_image = cv2.divide(gray_image, inv_blur, scale=285.0)

    # Save the image
    # cv2.imwrite(filename, sketch_img)

    cv2.imshow('RGB', sketched_image)
    cv2.waitKey(0)

    # Window shown waits for any key pressing event
    cv2.destroyAllWindows()


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
