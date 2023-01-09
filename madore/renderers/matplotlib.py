import base64
import io
import madore
import matplotlib.pyplot


@madore.register(matplotlib.pyplot.Figure)
def render(fig):
    f = io.BytesIO()
    fig.savefig(f, format="png")
    data = base64.b64encode(f.getvalue()).decode()
    return f"<figure><img src=\"data:image/png;base64,{data}\" /></figure>"
