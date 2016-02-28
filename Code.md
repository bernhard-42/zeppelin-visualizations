
```python
%pyspark

print sc.version
```


## Table of Contents

### 1 Pretty print RDDs and DataFrames as with %sql Interpreter
#### 1.1 A little convenience function 
#### 1.2 "Pretty print" an RDD without conversion and %sql Interpreter
#### 1.3 Visualize an RDD without conversion and %sql Interpreter

### 2 Integration of Visualization libraries into Zeppelin
#### 2.1 Integratíon of Bokeh via HTML and Javascript
#### 2.2 Integration of Vega via HTML and Javascript
#### 2.3 Integratíon of MatplotLib via HTML and SVG



## 1 Pretty print RDDs and DataFrames as with %sql Interpreter

### 1.1 A little convenience function 

- Collect random samples of RDDs and DataFrames
- Print RDDs and DataFrames in table form without switching to %sql by leveraging Zeppelin Display capabilities


```python
%pyspark

def pprint(data, num=8, asTable=False, columns=None, sampleRatio=None, seed=42):

    # If a sampleRatio is given, a random sample with given seed is selected
    subset = data.sample(False, fraction=sampleRatio, seed=seed) if sampleRatio else data

    # If it is a DataFrame, convert rows to arras and extract headers
    if "rdd" in dir(data): 
        columns = subset.columns
        subset = subset.map(lambda row: list(row))
        
    # If num is -1 all records should be collected - avoid for big data ...
    array = subset.collect() if num == -1 else subset.take(num)
    
    # If asTable is True, sql format with columns c0, c1, ... as output
    # If columns is array of column names, sql format with given columns as output
    if asTable or columns:
        output = ""
        for d in array:
            l = len(d)
            output += "\t".join([str(x) for x in d]) + "\n"
        if columns:
            header = "\t".join([h for h in columns]) + "\n" 
        else:
            header = "\t".join(["c%0d" %i for i in range(l) ]) + "\n"
        print "%table " + header + output
    else:
        for d in array:
            print d
```


## 1.2 "Pretty print" an RDD without conversion and %sql Interpreter


```python
%pyspark

def parse(line):
    m = {u'Iris-virginica':0, u'Iris-setosa':1, u'Iris-versicolor':2}
    if len(line.strip()) > 0:
        parts = line.split(",")
        return [float(f) for f in parts[0:4]] + [parts[4], m[parts[4]]]
    
iris = sc.textFile("/tmp/iris.data").filter(lambda line: len(line.strip()) > 0).map(parse)

pprint(iris, num=10, sampleRatio=0.06, seed=123, columns=["sepal-length", "sepal-width", "petal-length", "petal-width", "name", "species"])

```


## 1.3 Visualize an RDD without conversion and %sql Interpreter


```python
%pyspark

pprint(iris, num=-1, columns=["sepal-length", "sepal-width", "petal-length", "petal-width", "name", "species"])

```


## 2 Integration of Visualization libraries into Zeppelin




```python
%pyspark

irisDf = sqlContext.createDataFrame(iris, ["sepal-length", "sepal-width", "petal-length", "petal-width", "name", "species"])

```


### 2.1 Integration of Bokeh via HTML and javascript

See [Bokeh](http://bokeh.pydata.org/en/latest/)


```python
%pyspark

def loadBokeh():

    print """%html
    <link rel="stylesheet" href="https://cdn.pydata.org/bokeh/release/bokeh-0.11.0.min.css" type="text/css" />
    <script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-0.11.0.min.js"></script>
    <div>OK</div>
    """
    

def showBokeh(plot):
    from bokeh.embed import components

    script, div = components(plot)
    print "%html " + script + div
```


```python
%pyspark

loadBokeh()

```


```python
%pyspark

from bokeh.plotting import figure
from bokeh.sampledata.iris import flowers

colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
colors = [colormap[x] for x in flowers['species']]

p = figure(title = "Iris Morphology")
p.xaxis.axis_label = 'Petal Length'
p.yaxis.axis_label = 'Petal Width'

p.circle(flowers["petal_length"], flowers["petal_width"],
         color=colors, fill_alpha=0.2, size=10)

showBokeh(p)
```


```python
%pyspark

import bokeh

print "Note: Uncomment the download once if you have never accessed bokeh.sampledata!"

# bokeh.sampledata.download(False)  # progress doesn't work with Zeppelin
```


```python
%pyspark

from bokeh.models import HoverTool
from bokeh.plotting import figure, show, output_file, ColumnDataSource

from bokeh.sampledata.us_counties import data as counties
from bokeh.sampledata.unemployment import data as unemployment


counties = {
    code: county for code, county in counties.items() if county["state"] == "tx"
}

county_xs = [county["lons"] for county in counties.values()]
county_ys = [county["lats"] for county in counties.values()]

colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]

county_names = [county['name'] for county in counties.values()]
county_rates = [unemployment[county_id] for county_id in counties]
county_colors = [colors[int(rate/3)] for rate in county_rates]

source = ColumnDataSource(data=dict(
    x=county_xs,
    y=county_ys,
    color=county_colors,
    name=county_names,
    rate=county_rates,
))

TOOLS="pan,resize,wheel_zoom,box_zoom,reset,hover,save"

p = figure(title="Texas Unemployment 2009", tools=TOOLS)

p.patches('x', 'y', source=source,
          fill_color='color', fill_alpha=0.7,
          line_color="white", line_width=0.5)

hover = p.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Name", "@name"),
    ("Unemployment rate)", "@rate%"),
    ("(Long, Lat)", "($x, $y)"),
]

showBokeh(p)
```


## 2.2 Integration of Vega and Vega-Lite via HTML and Javascript

See [Vega](http://vega.github.io/vega/) and [Vega-Lite](https://vega.github.io/vega-lite/)

Samples: [Online Editor and Samples](http://vega.github.io/vega-editor/)


```python
%pyspark

def loadVega():
    html = """
        <script src="//d3js.org/d3.v3.min.js"></script>
        <script src="//vega.github.io/vega/vega.js"></script>
        <script src="//vega.github.io/vega-lite/vega-lite.js"></script>
        <div>OK</div>
    """
    
    print "%html " + html


def showVega(spec, mode="vega"):
    from uuid import uuid4
    import json
    
    if isinstance(spec, dict):
        spec = json.dumps(spec)
    
    id = "vega_%s" % uuid4().hex
    
    print """%html
<script>
  preprocessor = function(spec, mode) {
    return (mode == 'vega') ? spec : vl.compile(spec).spec
  }
  var spec = preprocessor(""" + spec + """ , '%s');
  vg.parse.spec(spec, function(error, chart) { chart({el:"#%s"}).update(); });
</script>
<div id='%s'></div>
""" % (mode, id, id)    # adding 'spec' as a format parameter here ends up in an error


```


```python
%pyspark

loadVega()

```


### 2.2.1 Vega

**Note**: Plots are interactive


```python
%pyspark

avg = irisDf.select("name", "sepal-length", "sepal-width", "petal-length", "petal-width").groupBy("name").mean()
pprint(avg)
```


```python
%pyspark

data = []
scales = []
marks = []

values = avg.select("avg(sepal-length)").collect()

data.append(
    { 
      "name": "table",
      "values": list(v[0] for v in values), # [12, 23, 45, 6, 52, 69],
      "transform": [{"type": "pie", "field": "data"}]
    }
)

scales.append(
    { 
      "name": "r",
      "type": "sqrt",
      "domain": {"data": "table", "field": "data"},
      "range": [20, 100]
    }
)

marks.append(
     {
      "type": "arc",
      "from": {"data": "table"},
      "properties": {
        "enter": {
          "x": {"field": {"group": "width"}, "mult": 0.5},
          "y": {"field": {"group": "height"}, "mult": 0.5},
          "startAngle": {"field": "layout_start"},
          "endAngle": {"field": "layout_end"},
          "innerRadius": {"value": 20},
          "outerRadius": {"scale": "r", "field": "data"},
          "stroke": {"value": "#fff"}
        },
        "update": {
          "fill": {"value": "#ccc"}
        },
        "hover": {
          "fill": {"value": "pink"}
        }
      }
    }
)

marks.append(
     {
      "type": "text",
      "from": {"data": "table"},
      "properties": {
        "enter": {
          "x": {"field": {"group": "width"}, "mult": 0.5},
          "y": {"field": {"group": "height"}, "mult": 0.5},
          "radius": {"scale": "r", "field": "data", "offset": 8},
          "theta": {"field": "layout_mid"},
          "fill": {"value": "#000"},
          "align": {"value": "center"},
          "baseline": {"value": "middle"},
          "text": {"field": "data"}
        }
      }
    }
)

spec = {
  "width": 400,
  "height": 400,
  "data": data,
  "scales": scales,
  "marks": marks
}

showVega(spec)

```


```python
%pyspark


us10m = "https://vega.github.io/vega-tutorials/airports/data/us-10m.json"
flightsAirport = "https://vega.github.io/vega-tutorials/airports/data/flights-airport.csv"
airports = "https://vega.github.io/vega-tutorials/airports/data/airports.csv"

data = []

data.append({
  "format": {"feature": "states", "type": "topojson"},
  "name": "states",
  "transform": [
    {
      "projection": "albersUsa",
      "scale": 1200,
      "translate": [450, 280],
      "type": "geopath"
    }
  ],
  "url": us10m
})

data.append({
  "format": {"parse": "auto", "type": "csv"},
  "name": "traffic",
  "transform": [
    {
      "groupby": ["origin"],
      "summarize": [
        {
          "as": ["flights"],
          "field": "count",
          "ops": ["sum"]
        }
      ],
      "type": "aggregate"
    }
  ],
  "url": flightsAirport
})

data.append({
  "format": {"parse": "auto", "type": "csv"},
  "name": "airports",
  "transform": [
    {
      "as": ["traffic"],
      "keys": ["iata"],
      "on": "traffic",
      "onKey": "origin",
      "type": "lookup"
    }, {
      "test": "datum.traffic != null", "type": "filter"
    }, {
      "lat": "latitude",
      "lon": "longitude",
      "projection": "albersUsa",
      "scale": 1200,
      "translate": [450, 280],
      "type": "geo"
    }, {
      "test": "datum.layout_x != null && datum.layout_y != null",
      "type": "filter"
    }, {
      "by": "-traffic.flights", "type": "sort"
    }, {
      "type": "voronoi", "x": "layout_x", "y": "layout_y"
    }
  ],
  "url": airports
})

data.append({
  "format": {"parse": "auto", "type": "csv"},
  "name": "routes",
  "transform": [
    {
      "test": "hover && hover.iata == datum.origin",
      "type": "filter"
    }, {
      "as": ["_source", "_target"],
      "keys": ["origin", "destination"],
      "on": "airports",
      "onKey": "iata",
      "type": "lookup"
    }, {
      "test": "datum._source && datum._target", "type": "filter"
    }, {
      "type": "linkpath"
    }
  ],
  "url": flightsAirport
})

scales = []
scales.append({
  "domain": {"data": "traffic", "field": "flights"},
  "name": "size",
  "range": [16, 1000],
  "type": "linear"
})

marks = []
marks.append({
  "from": {"data": "states"},
  "properties": {
    "enter": {
      "fill": {"value": "#dedede"},
      "stroke": {"value": "white"}
    },
    "update": {
      "path": {"field": "layout_path"}
    }
  },
  "type": "path"
})

marks.append({
  "from": {"data": "airports"},
  "properties": {
    "enter": {
      "fill": {"value": "steelblue"},
      "fillOpacity": {"value": 0.8},
      "size": {"field": "traffic.flights", "scale": "size"},
      "stroke": {"value": "white"},
      "strokeWidth": {"value": 1.5}
    },
    "update": {
      "x": {"field": "layout_x"},
      "y": {"field": "layout_y"}
    }
  },
  "type": "symbol"
})

marks.append({
  "from": {"data": "airports"},
  "name": "cell",
  "properties": {
    "enter": {
      "fill": {"value": "transparent"},
      "strokeWidth": {"value": 0.35}
    },
    "update": {
      "path": {"field": "layout_path"},
      "stroke": {"signal": "cell_stroke"}
    }
  },
  "type": "path"
})

marks.append({
  "from": {"data": "routes"},
  "interactive": False,
  "properties": {
    "enter": {
      "path": {"field": "layout_path"},
      "stroke": {"value": "black"},
      "strokeOpacity": {"value": 0.35}
    }
  },
  "type": "path"
})


marks.append({
  "interactive": False,
  "properties": {
    "enter": {
      "align": {"value": "right"},
      "fill": {"value": "black"},
      "fontSize": {"value": 20},
      "x": {"value": 895},
      "y": {"value": 0}
    },
    "update": {
      "text": {"signal": "title"}
    }
  },
  "type": "text"
})

signals = []

signals.append({
  "init": None,
  "name": "hover",
  "streams": [
    {
      "expr": "datum", "type": "@cell:mouseover"
    }, {
      "expr": "null", "type": "@cell:mouseout"
    }
  ]
})


signals.append({
  "init": "U.S. Airports, 2008",
  "name": "title",
  "streams": [
    {
      "expr": "hover ? hover.name + ' (' + hover.iata + ')' : 'U.S. Airports, 2008'",
      "type": "hover"
    }
  ]
})


signals.append({
  "init": None,
  "name": "cell_stroke",
  "streams": [
    {
      "expr": 'cell_stroke ? null : "brown"',
      "type": "dblclick"
    }
  ]
})

spec = {
  "width": 900,
  "height": 560,
  "data": data,
  "scales": scales,
  "marks": marks,
  "padding": {"bottom": 0, "left": 0, "right": 0, "top": 25},
  "signals": signals
}

showVega(spec)


```


### 2.2.2 Vega Lite


```python
%pyspark

irisDF = sqlContext.createDataFrame(iris, ["sepal-length", "sepal-width", "petal-length", "petal-width", "species", "name"])

stacked =   irisDf.select("name", irisDf["sepal-length"].alias("value")).withColumn("type", lit("sepal-length"))\
  .unionAll(irisDf.select("name", irisDf["sepal-width"].alias("value")).withColumn("type", lit("sepal-width")))\
  .unionAll(irisDf.select("name", irisDf["petal-length"].alias("value")).withColumn("type", lit("petal-length")))\
  .unionAll(irisDf.select("name", irisDf["petal-width"].alias("value")).withColumn("type", lit("petal-width")))

```


```python
%pyspark

values = stacked.map(lambda r: r.asDict())

data = {"values": values.collect()}

encoding = {
    "column": {"field": "type", "type": "ordinal"},
    "x":   {"aggregate": "mean", "field": "value", "type": "quantitative"},
    "y":   {"field": "name", "type": "ordinal"}
}

spec = {
    "data": data,
    "mark": "point",
    "encoding": encoding
}
    
showVega(spec, "vega-lite")
```


## 2.3 Integration of MatplotLib via HTML and SVG

See [Matplotlib](http://matplotlib.org/)


```python
%pyspark

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import StringIO

def showMPL(plot):
    img = StringIO.StringIO()
    plot.savefig(img, format='svg')
    img.seek(0)
    print "%html <div style='width:600px'>" + img.buf + "</div>"

```


```python
%pyspark

X = np.array(iris.map(lambda row: [row[i] for i in range(4)]).collect())
Y = np.array(iris.map(lambda row: row[5]).collect())

```


```python
%pyspark

from mpl_toolkits.mplot3d import Axes3D

x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5

plt.figure(2, figsize=(8, 6))
plt.clf()

# Plot the training points
plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=plt.cm.Paired)
plt.xlabel('Sepal length')
plt.ylabel('Sepal width')

plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())

showMPL(plt)
```

