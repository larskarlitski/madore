import html
import madore
import pandas


@madore.register(pandas.DataFrame)
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
