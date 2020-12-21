import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, State

import pyamp1394

port = pyamp1394.FirewirePort(0)
board = pyamp1394.AmpIO(0, 10)
port.add_board(board)

adc_count_from_amp = (2 ** 16 / 4.5) * (20 / 1) * (1 / 50)

import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children=[

    dcc.Interval(
        id='interval-component',
        interval=200, # in milliseconds
        n_intervals=0
    ),

    dbc.FormGroup([
        dbc.Label('channel'),
        dbc.Input(id='channel', type='number', value=1)
    ]),

    dbc.FormGroup([
        dbc.Label('kp'),
        dbc.Input(id='kp', type='number', value=0.01, step=0.001)
    ]),

    dbc.FormGroup([
        dbc.Label('ki'),
        dbc.Input(id='ki', type='number', value=0.01, step=0.001)
    ]),
    dbc.FormGroup([
        dbc.Label('I term limit'),
        dbc.Input(id='i_term_limit', type='number', value=1023)
    ]),
    dbc.FormGroup([
        dbc.Label('output limit'),
        dbc.Input(id='output_limit', type='number', value=1023)
    ]),


    dbc.Button('write', id='write_pi'),
    dbc.FormGroup([
        dbc.Label('Current setpoint (A)'),
        dbc.Input(id='current_setpoint', type='number', value=0.0, step=0.01)
    ]),
    dbc.Button('write', id='write_current'),

    html.Div(id='live-update-text'),
    html.Div(id='placeholder'),
    html.Div(id='placeholder2')


], style={'width': '20rem', 'padding': '2rem'})

@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'),
              State('channel', 'value'),
              State('current_setpoint', 'value'))
def update_metrics(n, channel, current_setpoint):
    port.read_all_boards()
    index = channel - 1
    current_measured = board.get_motor_current(index)
    error = current_measured - int(current_setpoint * adc_count_from_amp) - 0x8000
    return [
        html.Span(f'Current ADC = 0x{current_measured:04x} = {(current_measured - 0x8000)/adc_count_from_amp:.3f} A. error = {error} = {error/adc_count_from_amp:.3f} A'),
    ]

def float_to_fixed(f, decimal_bits):
    scaled = f * (2 ** decimal_bits)
    return int(round(scaled))

@app.callback(
    Output('placeholder', 'children'),
    Input('write_pi', 'n_clicks'),
    State('channel', 'value'),
    State('kp', 'value'),
    State('ki', 'value'),
    State('i_term_limit', 'value'),
    State('output_limit', 'value'))
def write_current_loop_parameters(n_clicks, channel, kp, ki, i_term_limit, output_limit):
    index = channel - 1
    board.write_motor_control_mode(index, pyamp1394.AmpIO.MotorControlMode.CURRENT)
    decimal_bits = 12
    kp_fixed = float_to_fixed(float(kp), decimal_bits)
    ki_fixed = float_to_fixed(float(ki), decimal_bits)
    board.write_current_loop_parameters(index,kp_fixed , ki_fixed, int(i_term_limit), int(output_limit))
    return f'write #{n_clicks}'

@app.callback(
    Output('placeholder2', 'children'),
    Input('write_current', 'n_clicks'),
    State('channel', 'value'),
    State('current_setpoint', 'value'))
def write_current_loop_parameters(n_clicks, channel, current_setpoint):
    index = channel - 1
    setpoint_raw = int(current_setpoint * adc_count_from_amp) + 0x8000
    print(hex(setpoint_raw))
    board.set_motor_current(index, setpoint_raw)
    port.write_all_boards()
    return f'write #{n_clicks}'

if __name__ == '__main__':
    app.run_server(debug=True)