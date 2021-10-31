import altair as alt

def plotTimeSeries1(resultsdf,BandName):
  minYaxis=min(resultsdf[BandName])-(0.1*min(resultsdf[BandName]))
  maxYaxis=1.1* max(resultsdf[BandName])
  highlight = alt.selection(
      type='single', on='mouseover', fields=['Year'], nearest=True)
  base = alt.Chart(resultsdf).encode(
    x=alt.X('DOY:Q', scale=alt.Scale(domain=[0, 353], clamp=True)),
    y=alt.Y(BandName, scale=alt.Scale(domain=[minYaxis, maxYaxis])),
    color=alt.Color('Year:O', scale=alt.Scale(scheme='magma')))
  points = base.mark_circle().encode(
    opacity=alt.value(0),
    tooltip=[
        alt.Tooltip('Year:O', title='Year'),
        alt.Tooltip('DOY:Q', title='DOY'),
        alt.Tooltip('NDVI:Q', title='NDVI')
    ]).add_selection(highlight)
  lines = base.mark_line().encode(
    size=alt.condition(~highlight, alt.value(1), alt.value(3)))
  plotresult=(points + lines).properties(width=600, height=350).interactive()
  return (plotresult)
