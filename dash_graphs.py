from re import M
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import plotly.figure_factory as ff
import dash_bootstrap_components as dbc
import dataservice
from flask import request


def create_modal_button(name):
    button = dbc.Button(
        name.title(),
        id="add-" + name,
        className="m1-auto",
        n_clicks=None,
    )
    if name == "close-modal":
        button = dbc.Button(
            "Close",
            id="close-body-scroll",
            className="ml-auto",
        )
    return button


class Linechart:
    def __init__(self, graph_counter, data):
        self.graph_counter = graph_counter
        self.data = data
        investments = pd.melt(self.data, id_vars=['anio_corte', 'municipio'],
                              value_vars=['inversion_transformacion', 'inversion_conectividad', 'inversion'])
        self.municipalities = list(investments["municipio"].unique())

    def create_graph(self):
        linechart = [
            dcc.Dropdown(
                id="linechart-input-" + str(self.graph_counter),
                options=[{"label": x, "value": x} for x in self.municipalities],
                placeholder='Municipio',
                value="medellin",
            ),
            dcc.Graph(id="line-chart-" + str(self.graph_counter))
        ]
        return linechart

    def update_graph(self, app):
        @app.callback(
            Output("line-chart-" + str(self.graph_counter), "figure"),
            Input("linechart-input-" + str(self.graph_counter), "value"))
        def update_linechart(value="medellin"):
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Scatter(x=self.data[self.data['municipio'] == value]["anio_corte"],
                           y=self.data[self.data['municipio'] == value]["inversion_transformacion"],
                           name="Inversión MinTC - Transformación"),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=self.data[self.data['municipio'] == value]["anio_corte"],
                           y=self.data[self.data['municipio'] == value]["inversion_conectividad"],
                           name="Inversión MinTC - Conectividad"),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=self.data[self.data['municipio'] == value]["anio_corte"],
                           y=self.data[self.data['municipio'] == value]["inversion"], name="Inversión MinTC - Total"),
                secondary_y=False,
            )

            fig.add_trace(
                go.Scatter(x=self.data[self.data['municipio'] == value]["anio_corte"],
                           y=self.data[self.data['municipio'] == value]["componente_de_resultados"],
                           name="Índice Calidad de Vida"),
                secondary_y=True,
            )
            return fig


class Stripplot:
    def __init__(self, graph_counter, data):
        self.graph_counter = graph_counter
        self.data = data
        self.x_options = [
            {"label": "Año Corte", "value": "anio_corte"},
            {"label": "Municipio", "value": "municipio"},
            {"label": "Departamento", "value": "departamento"},
            {"label": "Grupo Dotaciones", "value": "grupo_dotaciones"},
            {"label": "Categoria de Ruralidad", "value": "categoria_de_ruralidad"}]
        self.y_options = []
        for column_name in list(data.columns)[6:]:
            cleaned_column_name = column_name.replace("_", " ")
            label_dict = {"label": cleaned_column_name.title(), "value": column_name}
            self.y_options.append(label_dict)

    def create_graph(self):
        stripplot = [

            dcc.Dropdown(
                id="x-stripplot-" + str(self.graph_counter),
                options=self.x_options,
                value="anio_corte",
                placeholder="Eje X",
            ),
            dcc.Dropdown(
                id="y-stripplot-" + str(self.graph_counter),
                options=self.y_options,
                value="cobertura_neta_en_educacion_media",
                placeholder="Eje Y",
            ),
            dcc.Graph(id="stripplot-" + str(self.graph_counter))
        ]
        return stripplot

    def update_graph(self, app):
        @app.callback(
            Output("stripplot-" + str(self.graph_counter), "figure"),
            Input("x-stripplot-" + str(self.graph_counter), "value"),
            Input("y-stripplot-" + str(self.graph_counter), "value"))
        def update_stripplot(x_option_name="anio_corte", y_option_name="cobertura_neta_en_educacion_media"):
            fig = px.strip(self.data, x=x_option_name, y=y_option_name)
            fig.update_xaxes(title=x_option_name)
            fig.update_yaxes(title=y_option_name)
            return fig


class Geograph:
    def __init__(self, graph_counter, maps_path):
        self.graph_counter = graph_counter
        self.maps_path = maps_path
        self.init_map = open(maps_path + '/map_foliumTotal2016.html', 'r').read()

    def create_graph(self):
        geograph = [
            dcc.Dropdown(
                id="year-" + str(self.graph_counter),
                options=[{"label": x, "value": x} for x in [2016, 2017, 2018, 2019]],
                placeholder="Select a year",
            ),
            dcc.Dropdown(
                id="type-of-investment-" + str(self.graph_counter),
                options=[{"label": x, "value": x} for x in
                         ['Inversión Total', 'Inversión en Conectividad', 'Inversión en Transformación']],
                placeholder="Select a type of investment",
            ),
            html.Iframe(
                id='geo-graph-' + str(self.graph_counter),
                srcDoc=self.init_map,
                width='100%',
                height='600'),
        ]
        return geograph

    def update_graph(self, app):
        @app.callback(
            Output("geo-graph-" + str(self.graph_counter), "srcDoc"),
            Input("year-" + str(self.graph_counter), "value"),
            Input("type-of-investment-" + str(self.graph_counter), "value"),
        )
        def update_geo_graph(year, type_of_investment):
            if type_of_investment == 'Inversión Total':
                if (year == 2016):
                    return open(str(self.maps_path) + '/map_foliumTotal2016.html', 'r').read()
                elif (year == 2017):
                    return open(str(self.maps_path) + '/map_foliumTotal2017.html', 'r').read()
                elif (year == 2018):
                    return open(str(self.maps_path) + '/map_foliumTotal2018.html', 'r').read()
                elif (year == 2019):
                    return open(str(self.maps_path) + '/map_foliumTotal2019.html', 'r').read()
            elif type_of_investment == 'Inversión en Conectividad':
                if (year == 2016):
                    return open(str(self.maps_path) + '/map_foliumConectividad2016.html', 'r').read()
                elif (year == 2017):
                    return open(str(self.maps_path) + '/map_foliumConectividad2017.html', 'r').read()
                elif (year == 2018):
                    return open(str(self.maps_path) + '/map_foliumConectividad2018.html', 'r').read()
                elif (year == 2019):
                    return open(str(self.maps_path) + '/map_foliumConectividad2019.html', 'r').read()
            elif type_of_investment == 'Inversión en Transformación':
                if (year == 2016):
                    return open(str(self.maps_path) + '/map_foliumTransformación2016.html', 'r').read()
                elif (year == 2017):
                    return open(str(self.maps_path) + '/map_foliumTransformación2017.html', 'r').read()
                elif (year == 2018):
                    return open(str(self.maps_path) + '/map_foliumTransformación2018.html', 'r').read()
                elif (year == 2019):
                    return open(str(self.maps_path) + '/map_foliumTransformación2019.html', 'r').read()


class Bargraph:
    def __init__(self, graph_counter, data):
        self.graph_counter = graph_counter
        self.data = data
        self.x_options = [
            {"label": "Año Corte", "value": "anio_corte"},
            {"label": "Municipio", "value": "municipio"},
            {"label": "Departamento", "value": "departamento"},
            {"label": "Grupo Dotaciones", "value": "grupo_dotaciones"},
            {"label": "Categoria de Ruralidad", "value": "categoria_de_ruralidad"}]
        self.y_options = []
        for column_name in list(data.columns)[6:]:
            cleaned_column_name = column_name.replace("_", " ")
            label_dict = {"label": cleaned_column_name.title(), "value": column_name}
            self.y_options.append(label_dict)

    def create_graph(self):
        bargraph = [
            dcc.Dropdown(
                id="x-bargraph-" + str(self.graph_counter),
                options=self.x_options,
                placeholder="Variable Categorica"
            ),
            dcc.Dropdown(
                id="y-bargraph-" + str(self.graph_counter),
                options=self.y_options,
                placeholder="Variable Numerica"
            ),
            dcc.Graph(id="bargraph-" + str(self.graph_counter))
        ]
        return bargraph

    def update_graph(self, app):
        @app.callback(
            Output("bargraph-" + str(self.graph_counter), "figure"),
            Input("x-bargraph-" + str(self.graph_counter), "value"),
            Input("y-bargraph-" + str(self.graph_counter), "value"))
        def update_bargraph(x_option_name="anio_corte", y_option_name="cobertura_neta_en_educacion_media"):
            data_grouped = (self.data.groupby([x_option_name]).sum()).reset_index()
            fig = px.bar(data_grouped, x=x_option_name, y=y_option_name)
            fig.update_xaxes(title=x_option_name)
            fig.update_yaxes(title=y_option_name)
            return fig


class Treemap:
    def __init__(self, graph_counter, data):
        self.graph_counter = graph_counter
        self.data = data
        self.x_options = [
            {"label": "Año Corte", "value": "anio_corte"},
            {"label": "Municipio", "value": "municipio"},
            {"label": "Departamento", "value": "departamento"},
            {"label": "Grupo Dotaciones", "value": "grupo_dotaciones"},
            {"label": "Categoria de Ruralidad", "value": "categoria_de_ruralidad"}]
        self.y_options = []
        for column_name in list(data.columns)[6:]:
            cleaned_column_name = column_name.replace("_", " ")
            label_dict = {"label": cleaned_column_name.title(), "value": column_name}
            self.y_options.append(label_dict)

    def create_graph(self):
        treemap = [
            dcc.Dropdown(
                id="x-treemap-" + str(self.graph_counter),
                options=self.x_options,
                placeholder="Selecciona Categoria",
                value="anio_corte"),
            dcc.Dropdown(
                id="y-treemap-" + str(self.graph_counter),
                options=self.y_options,
                placeholder="Selecciona Valor Numérico",
                value="inversion"),
            dcc.Graph(id="treemap-" + str(self.graph_counter))
        ]
        return treemap

    def update_graph(self, app):
        @app.callback(
            Output("treemap-" + str(self.graph_counter), "figure"),
            Input("x-treemap-" + str(self.graph_counter), "value"),
            Input("y-treemap-" + str(self.graph_counter), "value")
        )
        def update_treemap(x_option, y_option):
            fig = px.treemap(self.data, path=[px.Constant("Datos"), x_option], values=y_option, color=x_option)
            fig.update_xaxes(title=x_option)
            fig.update_yaxes(title=y_option)
            fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
            return fig


class Piechart:
    def __init__(self, graph_counter, data):
        self.graph_counter = graph_counter
        self.data = data
        self.x_options = [
            {"label": "Año Corte", "value": "anio_corte"},
            {"label": "Municipio", "value": "municipio"},
            {"label": "Departamento", "value": "departamento"},
            {"label": "Grupo Dotaciones", "value": "grupo_dotaciones"},
            {"label": "Categoria de Ruralidad", "value": "categoria_de_ruralidad"}]
        self.y_options = []
        for column_name in list(data.columns)[6:]:
            cleaned_column_name = column_name.replace("_", " ")
            label_dict = {"label": cleaned_column_name.title(), "value": column_name}
            self.y_options.append(label_dict)

    def create_graph(self):
        piechart = [
            dcc.Dropdown(
                id="x-piechart-" + str(self.graph_counter),
                options=self.x_options,
                placeholder="Variable Categorica",
                value="anio_corte"
            ),
            dcc.Dropdown(
                id="y-piechart-" + str(self.graph_counter),
                options=self.y_options,
                placeholder="Variable Numerica",
                value="inversion"
            ),
            dcc.Graph(id="piechart-" + str(self.graph_counter))]
        return piechart

    def update_graph(self, app):
        @app.callback(
            Output("piechart-" + str(self.graph_counter), "figure"),
            Input("x-piechart-" + str(self.graph_counter), "value"),
            Input("y-piechart-" + str(self.graph_counter), "value"))
        def update_piechart(x_option_name="anio_corte", y_option_name="inversion"):
            fig = px.pie(self.data, values=y_option_name, names=x_option_name)
            return fig


class Distplot:
    def __init__(self, graph_counter, data):
        self.graph_counter = graph_counter
        self.data = data
        self.x_options = [
            {"label": "Año Corte", "value": "anio_corte"},
            {"label": "Municipio", "value": "municipio"},
            {"label": "Departamento", "value": "departamento"},
            {"label": "Grupo Dotaciones", "value": "grupo_dotaciones"},
            {"label": "Categoria de Ruralidad", "value": "categoria_de_ruralidad"}]
        self.y_options = []
        for column_name in list(data.columns)[6:]:
            cleaned_column_name = column_name.replace("_", " ")
            label_dict = {"label": cleaned_column_name.title(), "value": column_name}
            self.y_options.append(label_dict)

    def create_graph(self):
        distplot = [
            dcc.Dropdown(
                id="x-distplot-" + str(self.graph_counter),
                options=self.y_options,
                value="anio_corte",
                placeholder="Variable X"
            ),
            dcc.Dropdown(
                id="y-distplot-" + str(self.graph_counter),
                options=self.y_options,
                value="inversion",
                placeholder="Variable Y"
            ),
            dcc.Graph(id="distplot-" + str(self.graph_counter))]
        return distplot

    def update_graph(self, app):
        @app.callback(
            Output("distplot-" + str(self.graph_counter), "figure"),
            Input("x-distplot-" + str(self.graph_counter), "value"),
            Input("y-distplot-" + str(self.graph_counter), "value"))
        def update_distplot(x_option, y_option):
            fig = px.histogram(self.data, x=x_option, y=y_option, marginal="box", )
            fig.update_xaxes(title=x_option)
            fig.update_yaxes(title=y_option)
            return fig
