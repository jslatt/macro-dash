from vizro import Vizro
import vizro.models as vm
import vizro.plotly.express as px
import pandas as pd
from openbb import obb
from dotenv import load_dotenv
import os

patK = os.getenv('PAT')
obb.account.login(pat=patK)

spy_price = obb.equity.price.historical(
    "SPY", start_date="2018-01-01", provider="fmp", interval="1d"
).to_df()


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

us_markets = vm.Page(
    title="US Markets",
    components=[
        vm.Graph(
            id="scatter_iris",
            figure=px.line(spy_price, x=spy_price.index, y="close",
            ),
        ),
    ],
    controls=[
    ],
)

dashboard = vm.Dashboard(pages=[home_page, global_macro, us_markets])
Vizro().build(dashboard).run()