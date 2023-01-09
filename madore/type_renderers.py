import html

from .render import register


try:
    import pandas

    @register(pandas.DataFrame)
    def render(df):
        s = '<table>\n<thead>\n<tr>\n'

        for column in df.columns:
            v = html.escape(str(column))
            s += f'<th title="{v}">{v}</th>\n'

        s += '</tr>\n</thead>\n<tbody>\n'

        for row in df.itertuples(index=False, name=None):
            s += '<tr>\n'
            for cell in row:
                v = html.escape(str(cell))
                s += f'<td title="{v}">{v}</td>\n'
            s += '</tr>\n'

        s += '</tbody>\n</table>\n'
        return s

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
