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

from ..nvd3_chart import Nvd3Chart
from ..nvd3_data import Nvd3Data


class ScatterPlusLineChart(Nvd3Chart):
    
    JS_scatterPlusLineChart = """linePlusBarChart = function(session, object) {                     // add to example 
        session.__functions.makeChart(session, object, function(session, divId, data, cache) {      // add to example 

            // see http://nvd3.org/examples/scatter.html
            
            nv.addGraph(function() {
              var chart = nv.models.scatterChart()
                            .showDistX(true)
                            .showDistY(true)
                            .color(d3.scale.category10().range());
            
              //Configure how the tooltip looks.
              chart.tooltipContent(function(key) {
                  return '<h3>' + key + '</h3>';
              });
            
              //Axis settings
              chart.xAxis.tickFormat(d3.format('.02f'));
              chart.yAxis.tickFormat(d3.format('.02f'));
            
              //We want to show shapes other than circles.
              chart.scatter.onlyCircles = false;
                
              chartData = d3.select(divId).datum(data)                                              // replace with "divId" and "data" and assign to "chartData"
              chartData.transition().duration(350).call(chart);
            
              cache.chart = chart;                                                                  // add to example to allow updates
              cache.chartData = chartData;                                                          // add to example to allow updates

              return chart;
            });
        })                                                                                          // add to example 
    }
    """

    def __init__(self, nvd3Functions, height=400, width=1024):
        super(self.__class__, self).__init__(nvd3Functions, "scatterPlusLineChart", height, width)
        self
    
    def convert(self, df, key, bar, line):
        nvd3data = Nvd3Data(df)
        return [nvd3data.convert(key, bar), nvd3data.convert(key, line)]

