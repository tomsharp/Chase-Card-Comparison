import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from util import card_infos, calculate_net_value, calculate_breakeven



app = dash.Dash(__name__)


app.layout = html.Div([
    html.Div([
        html.H2("Calculate the Net Value of your Points"),
        html.Div([
            html.H3("Which card do you have?"),
            dcc.Dropdown(
                id='card',
                options=[
                    {'label': 'Chase Sapphire Preferred', 'value': 'preferred'},
                    {'label': 'Chase Sapphire Reserve', 'value': 'reserve'},
                ],
            ),
        ]),
        html.Div([
            html.H3("How much do you spend on each of these categories per year?"),
            dcc.Input(
                id='lyft',
                placeholder='Lyft',
                type='number',
            ),  
            dcc.Input(
                id='dining_travel',
                placeholder='Dining and Travel',
                type='number',
            ), 
            dcc.Input(
                id='everything_else',
                placeholder='Everything Else',
                type='number',
            ), 
        ]),
        html.Div([
            html.H3("Do you redeem your points in the Chase Portal?"),
            dcc.Checklist(
                id='portal_redemption',
                options=[
                    {'label': 'Chase Portal', 'value': 'portal_redemption'},
                ],
            ),
        ]),
        html.Div([
            html.Button('Calculate', id='button'),
        ]),
        html.Div(id='dummy')
    ])
])


@app.callback(
    Output('dummy', 'children'),
    [Input('button', 'n_clicks')],
    [State('dining_travel', 'value'), 
     State('lyft', 'value'),
     State('everything_else', 'value'), 
     State('portal_redemption', 'value'),
     State('card', 'value')]
)
def net_value(n_clicks, dining_travel, lyft, everything_else, portal_redemption, card):
    if n_clicks is not None:
        spending = {
            'lyft': lyft,
            'travel_dining': dining_travel,
            'everything_else': everything_else,
        }
        nv = calculate_net_value(card_infos[card], portal_redemption=len(portal_redemption), spending=spending)
        if nv>0:
            nv_str = "With your current spending, you gain ${:,.2f} for owning this card".format(abs(nv))
        else:
            nv_str = "With your current spending, you lose ${:,.2f} for owning this card".format(abs(nv))
        return nv_str
    else: 
        pass


if __name__=='__main__':
    app.run_server(debug=True)