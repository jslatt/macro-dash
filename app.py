from vizro import Vizro
import vizro.models as vm
import vizro.plotly.express as px

home_page = vm.Page(
    title="Index",
    components=[
        vm.Card(
            text="""
            ### Global Macro

            Global Macro
            """,
            href="/global-macro",
        ),
        vm.Card(
            text="""
            ### US Market

            Indicies
            """,
            href="/second-page",
        ),
    ],
)

df = px.data.gapminder()
gapminder_data = (
        df.groupby(by=["continent", "year"]).
            agg({"lifeExp": "mean", "pop": "sum", "gdpPercap": "mean"}).reset_index()
    )
global_macro = vm.Page(
    title="Global Macro",
    layout=vm.Layout(grid=[[0, 0], [1, 2], [1, 2], [1, 2]]),
    components=[
        vm.Card(
            text="""
                # Global Macro
                This pages shows the inclusion of markdown text in a page and how components
                can be structured using Layout.
            """,
        ),
        vm.Graph(
            id="box_cont",
            figure=px.box(gapminder_data, x="continent", y="lifeExp", color="continent",
                            labels={"lifeExp": "Life Expectancy", "continent":"Continent"}),
        ),
        vm.Graph(
            id="line_gdp",
            figure=px.line(gapminder_data, x="year", y="gdpPercap", color="continent",
                            labels={"year": "Year", "continent": "Continent",
                            "gdpPercap":"GDP Per Cap"}),
            ),
    ],
    controls=[
        vm.Filter(column="continent", targets=["box_cont", "line_gdp"]),
    ],
)

iris_data = px.data.iris()
us_markets = vm.Page(
    title="US Markets",
    components=[
        vm.Graph(
            id="scatter_iris",
            figure=px.scatter(iris_data, x="sepal_width", y="sepal_length", color="species",
                color_discrete_map={"setosa": "#00b4ff", "versicolor": "#ff9222"},
                labels={"sepal_width": "Sepal Width", "sepal_length": "Sepal Length",
                        "species": "Species"},
            ),
        ),
        vm.Graph(
            id="hist_iris",
            figure=px.histogram(iris_data, x="sepal_width", color="species",
                color_discrete_map={"setosa": "#00b4ff", "versicolor": "#ff9222"},
                labels={"sepal_width": "Sepal Width", "count": "Count",
                        "species": "Species"},
            ),
        ),
    ],
    controls=[
        vm.Parameter(
            targets=["scatter_iris.color_discrete_map.virginica",
                        "hist_iris.color_discrete_map.virginica"],
            selector=vm.Dropdown(
                options=["#ff5267", "#3949ab"], multi=False, value="#3949ab", title="Color Virginica"),
            ),
        vm.Parameter(
            targets=["scatter_iris.opacity", "hist_iris.opacity"],
            selector=vm.Slider(min=0, max=1, value=0.8, title="Opacity"),
        ),
    ],
)

dashboard = vm.Dashboard(pages=[home_page, global_macro, us_markets])
Vizro().build(dashboard).run()