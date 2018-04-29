import altair as alt
import pandas as pd

def createChart(data, zipcode):
    color_expression    = "highlight._vgsid_==datum._vgsid_"
    color_condition     = alt.ConditionalPredicateValueDef(color_expression, "SteelBlue")
    highlight_selection = alt.selection_single(name="highlight", empty="all", on="mouseover")
    try:
        data = pd.concat([data['cuisine'], data['perZip'+zipcode]], axis=1).nlargest(20, 'perZip'+zipcode)
        maxCount = int(data['perZip'+zipcode].max())
    except KeyError:
        maxCount = 1
        data = pd.DataFrame([{"cuisine":"", 'perZip'+zipcode:0}])


    return alt.Chart(data) \
              .mark_bar(stroke="Black") \
              .encode(
                  alt.X('perZip'+zipcode+':Q', axis=alt.Axis(title="Restaurants"),
                    scale=alt.Scale(domain=(0,maxCount))),
                  alt.Y('cuisine:O', axis=alt.Axis(title="cuisine"),
                    sort=alt.SortField(field='perZip'+zipcode, op="argmax")),
                  alt.ColorValue("LightGrey", condition=color_condition),
              ).properties(
                selection = highlight_selection,
              )


def loadData():
    import urllib.request, json
    with urllib.request.urlopen("https://raw.githubusercontent.com/lingyielia/D3-visual/master/data/nyc_restaurants_by_cuisine.json") as url:
        cuisines = json.loads(url.read().decode())

    df = pd.io.json.json_normalize(cuisines)
    columnchange = df.columns[1:-1]
    df.columns = ["cuisine"] + ["".join(element.split(".")) for element in columnchange] + ['total']

    return df

