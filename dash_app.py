import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Данные Gapminder
df = px.data.gapminder()

measures = {
    'Population': 'pop',
    'GDP per Capita': 'gdpPercap',
    'Life Expectancy': 'lifeExp'
}

app = dash.Dash(__name__, assets_folder='assets')

app.layout = html.Div([
    html.Img(src='/assets/logo.png', style={'height':'60px', 'display':'block', 'margin':'0 auto'}),
    html.H1("Сравнение стран и континентов (Gapminder)"),

    html.Div([
        html.Label("Выберите страны"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': c, 'value': c} for c in df['country'].unique()],
            value=['United States', 'China'],
            multi=True
        ),
        html.Label("Мера по оси Y"),
        dcc.Dropdown(
            id='yaxis-dropdown',
            options=[{'label': k, 'value': v} for k, v in measures.items()],
            value='gdpPercap'
        )
    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),

    html.Div([
        html.Label("Мера для X (bubble)"),
        dcc.Dropdown(
            id='bubble-x',
            options=[{'label': k, 'value': v} for k, v in measures.items()],
            value='gdpPercap'
        ),
        html.Label("Мера для Y (bubble)"),
        dcc.Dropdown(
            id='bubble-y',
            options=[{'label': k, 'value': v} for k, v in measures.items()],
            value='lifeExp'
        ),
        html.Label("Мера для размера (bubble)"),
        dcc.Dropdown(
            id='bubble-size',
            options=[{'label': k, 'value': v} for k, v in measures.items()],
            value='pop'
        ),
        html.Label("Выберите год"),
        dcc.Slider(
            id='year-slider',
            min=int(df['year'].min()),
            max=int(df['year'].max()),
            step=5,
            marks={int(year): str(year) for year in df['year'].unique()},
            value=int(df['year'].min())
        )
    ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),

    html.Div([
        dcc.Graph(id='line-chart')
    ], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='bubble-chart')
    ], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='bar-chart')
    ], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='pie-chart')
    ], style={'width': '48%', 'display': 'inline-block'})
])

@app.callback(
    Output('line-chart', 'figure'),
    Input('country-dropdown', 'value'),
    Input('yaxis-dropdown', 'value')
)
def update_line(countries, yaxis):
    if not countries:
        return {}
    dff = df[df['country'].isin(countries)]
    return px.line(
        dff, x='year', y=yaxis, color='country',
        title=f"Динамика {yaxis} по странам"
    )

@app.callback(
    Output('bubble-chart', 'figure'),
    Output('bar-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Input('year-slider', 'value'),
    Input('bubble-x', 'value'),
    Input('bubble-y', 'value'),
    Input('bubble-size', 'value')
)
def update_others(year, x, y, size):
    dff = df[df['year'] == year]
    bubble = px.scatter(
        dff, x=x, y=y, size=size, hover_name='country',
        title=f"Пузырьковая диаграмма за {year}"
    )
    top15 = dff.nlargest(15, 'pop')
    bar = px.bar(
        top15, x='country', y='pop',
        title=f"Топ-15 стран по населению в {year}"
    )
    cont = dff.groupby('continent', as_index=False)['pop'].sum()
    pie = px.pie(
        cont, names='continent', values='pop',
        title=f"Распределение населения по континентам в {year}"
    )
    return bubble, bar, pie

if __name__ == '__main__':
    app.run(debug=True)
