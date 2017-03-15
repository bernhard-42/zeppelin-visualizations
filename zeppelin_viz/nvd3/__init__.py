# Copyright 2017 Bernhard Walter
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from .nvd3_functions import Nvd3Functions
from .nvd3_data import Nvd3Data
from .nvd3_chart import Nvd3Chart
from .charts.linePlusBarChart import LinePlusBarChart
from .charts.scatterPlusLineChart import ScatterPlusLineChart


class Nvd3(object):
    
    def __init__(self, downloadAsPng=True):
        self.nvd3Functions = Nvd3Functions()
        self.LPB = LinePlusBarChart
        self.SPL = ScatterPlusLineChart

        if downloadAsPng:
            print("%html")
            print("""<script src="http://cdn.rawgit.com/exupero/saveSvgAsPng/gh-pages/saveSvgAsPng.js" type="text/javascript"></script>""")
            print("""<div>Downloaded http://cdn.rawgit.com/exupero/saveSvgAsPng/gh-pages/saveSvgAsPng.js to allow saving charts to PNG</div>""")


    def reloadNVD3(self, version="1.7.1"):
        print("%html")
        print("""
        <link href="https://cdnjs.cloudflare.com/ajax/libs/nvd3/%s/nv.d3.min.css" rel="stylesheet">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/nvd3/%s/nv.d3.js"></script>
        """ % (version, version))


    def register(self, chart):
        self.nvd3Functions.register(chart.funcName, "%s = %s" % (chart.funcName, chart.funcBody))
        return chart


    def linePlusBarChart(self):
        return self.register(LinePlusBarChart(self.nvd3Functions))

    def scatterPlusLineChart(self):
        return self.register(ScatterPlusLineChart(self.nvd3Functions))

    def multiBarHorizontalChart(self):
        return self.register(MultiBarHorizontalChart(self.nvd3Functions))

    def boxPlotChart(self):
        return self.register(BoxPlotChart(self.nvd3Functions))

    def discreteBarChart(self):
        return self.register(DiscreteBarChart(self.nvd3Functions))

    def lineChart(self):
        return self.register(LineChart(self.nvd3Functions))

    def multiBarChart(self):
        return self.register(MultiBarChart(self.nvd3Functions))

    def parallelCoordinatesChart(self):
        return self.register(ParallelCoordinatesChart(self.nvd3Functions))

    def pieChart(self):
        return self.register(PieChart(self.nvd3Functions))

    def scatterChart(self):
        return self.register(ScatterChart(self.nvd3Functions))

    def stackedAreaChart(self):
        return self.register(StackedAreaChart(self.nvd3Functions))


    # Source: http://d3js.org
    def c10(self):
        return ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

    # Source: http://d3js.org
    def c20(self):
        return ["#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c", "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5", 
                "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f", "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5"]

    # Source: http://d3js.org
    def c20b(self):
        return ["#393b79", "#5254a3", "#6b6ecf", "#9c9ede", "#637939", "#8ca252", "#b5cf6b", "#cedb9c", "#8c6d31", "#bd9e39", 
                "#e7ba52", "#e7cb94", "#843c39", "#ad494a", "#d6616b", "#e7969c", "#7b4173", "#a55194", "#ce6dbd", "#de9ed6"]

    # Source: http://d3js.org
    def c20c(self):
        return ["#3182bd", "#6baed6", "#9ecae1", "#c6dbef", "#e6550d", "#fd8d3c", "#fdae6b", "#fdd0a2", "#31a354", "#74c476", 
                "#a1d99b", "#c7e9c0", "#756bb1", "#9e9ac8", "#bcbddc", "#dadaeb", "#636363", "#969696", "#bdbdbd", "#d9d9d9"]

    def grey(self):
        digits = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
        return ["#%s" % (d*3) for d in digits]
