
```python
%pyspark

sc.version
```


## Pretty print RDDs and DataFrames as with sql
A little convenience function to 

- collect random samples of RDDs and DataFrames
- print RDDs and DataFrames in table form without switching to %sql by leveraging Zeppelin Display capabilities


```python
%pyspark

def pprint(data, num=8, asTable=False, columns=None, sampleRatio=None, seed=42):

    # If a sampleRatio is given, a random sample with given seed is selected
    subset = data.sample(False, fraction=sampleRatio, seed=seed) if sampleRatio else data

    # If it is a DataFrame, convert rows to arras and extract headers
    if "rdd" in dir(data): 
        columns = subset.columns
        subset = subset.map(lambda row: row.asDict().values())
        
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


"Pretty print" an RDD without conversion and sql


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


```python
%pyspark

pprint(iris, num=-1, columns=["sepal-length", "sepal-width", "petal-length", "petal-width", "name", "species"])

```


### Integrate MatplotLib via HTML and SVG into Zeppelin


```python
%pyspark

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import StringIO

def zshow(plot):
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

zshow(plt)
```


## Below experiments are not working 


### Note: Seaborn currently not working


```python
%pyspark

import seaborn as sns; 
sns.set(style="ticks", color_codes=True)


```


```python
%pyspark

irisDF = sqlContext.createDataFrame(iris, ["sepal-length", "sepal-width", "petal-length", "petal-width", "species", "name"])
pprint(irisDf, sampleRatio=0.1)

```


```python
%pyspark

iris2 = irisDF.select(["sepal-length", "sepal-width", "petal-length", "petal-width", "species"]).toPandas()

```


```python
%pyspark
# iris2 = sns.load_dataset("iris")
g = sns.pairplot(iris2, size=2, hue="species")
zshow(plt)
```


### Note: Vega (embed) not working currently


```python
%pyspark

html = """
<script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
<script src="http://vega.github.io/vega-editor/vendor/vega.js" charset="utf-8"></script>
<script src="http://vega.github.io/vega-editor/vendor/vega-embed.js" charset="utf-8"></script>
"""

print "%html " + html
```


```python
%pyspark

desc = """
<script>
vg_spec = {
  "parameters": [
    { 
      "signal": "rotate", "type": "range",
      "value": 0, "min": -360, "max": 360,
      "rewrite": ["data[0].transform[0].rotate"]
    }
  ],
  "spec": {
    "width": 800,
    "height": 500,
    "padding": 0,
    "data": [
      {
        "name": "world",
        "url": "data/world-110m.json",
        "format": {"type": "topojson", "feature": "countries"},
        "transform": [{
          "type": "geopath",
          "projection": "winkel3",
          "scale": 170,
          "translate": [400, 250]
        }]
      }
    ],
    "marks": [
      {
        "type": "path",
        "from": {"data": "world"},
        "properties": {
          "enter": {
            "stroke": {"value": "#fff"}
          },
          "update": {
            "path": {"field": "layout_path"},
            "fill": {"value": "#ccc"}
          },
          "hover": {
            "fill": {"value": "pink"}
          }
        }
      }
    ]
  }
};
</script>
"""


print "%html " + desc

```


```python
%pyspark

embed = """
<script>
vg.embed('#vis', spec, function(error, result) {
    alert(result);
});
</script>
<div id='vis'></div>
"""

print "%html " + embed
```

