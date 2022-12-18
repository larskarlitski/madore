from .render import register

try:
    import pandas

    @register(pandas.DataFrame)
    def render(df):
        return df.to_html()

except ImportError:
    pass


try:
    import base64
    import io
    import matplotlib.pyplot

    @register(matplotlib.pyplot.Figure)
    def render(fig):
        f = io.BytesIO()
        fig.savefig(f, format="png")
        data = base64.b64encode(f.getvalue()).decode()
        return f"<figure><img src=\"data:image/png;base64,{data}\" /></figure>"

except ImportError:
    pass
