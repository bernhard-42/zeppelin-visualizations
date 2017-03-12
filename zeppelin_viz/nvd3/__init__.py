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
		if downloadAsPng:
			print("%html")
			print("""<script src="http://cdn.rawgit.com/exupero/saveSvgAsPng/gh-pages/saveSvgAsPng.js" type="text/javascript"></script>""")
			print("""<div>Downloaded http://cdn.rawgit.com/exupero/saveSvgAsPng/gh-pages/saveSvgAsPng.js to allow saving charts to PNG</div>""")

	def linePlusBarChart(self):
		self.nvd3Functions.register("linePlusBarChart", LinePlusBarChart.JS_linePlusBarChart)
		return LinePlusBarChart(self.nvd3Functions)

	def scatterPlusLineChart(self):
		self.nvd3Functions.register("scatterPlusLineChart", ScatterPlusLineChart.JS_scatterPlusLineChart)
		return ScatterPlusLineChart(self.nvd3Functions)

	def reloadNVD3(self, version="1.7.1"):
		print("%html")
		print("""
		<link href="https://cdnjs.cloudflare.com/ajax/libs/nvd3/%s/nv.d3.min.css" rel="stylesheet">
		<script src="https://cdnjs.cloudflare.com/ajax/libs/nvd3/%s/nv.d3.js"></script>
		""" % (version, version))

