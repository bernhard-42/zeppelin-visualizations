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


class LinePlusBarChart(Nvd3Chart):

    JS_linePlusBarChart = """

    linePlusBarChart = function(session, object) {                                                  // add to example 
        session.__functions.makeChart(session, object, function(session, divId, data, cache) {      // add to example 

            // see https://github.com/nvd3-community/nvd3/blob/gh-pages/examples/linePlusBarChart.html
            
            nv.addGraph(function() {
                chart = nv.models.linePlusBarChart()
                    .margin({top: 50, right: 80, bottom: 30, left: 80})
                    .legendRightAxisHint(' [Using Right Axis]')
                    .color(d3.scale.category10().range());
                
                chart.xAxis.tickFormat(function(d) {
                    return d3.time.format('%x')(new Date(d))
                }).showMaxMin(false);
                
                chart.y2Axis.tickFormat(function(d) { return '$' + d3.format(',f')(d) });
                chart.bars.forceY([0]).padData(false);
                
                chart.x2Axis.tickFormat(function(d) {
                    return d3.time.format('%x')(new Date(d))
                }).showMaxMin(false);
                
                chartData = d3.select(divId).datum(data)                                            // replace with "divId" and "data" and assign to "chartD
                chartData.transition().duration(500).call(chart);
                
                chart.dispatch.on('stateChange', function(e) { 
                    console.log('New State:', JSON.stringify(e)); 
                });
                
                cache.chart = chart;                                                                // add to example to allow updates
                cache.chartData = chartData;                                                        // add to example to allow updates
                
                return chart;
            });
        })                                                                                          // add to example 
    }

    """
    
    def __init__(self, nvd3Functions, height=400, width=1024):
        super(self.__class__, self).__init__(nvd3Functions, "linePlusBarChart", height, width)
    
    def convert(self, df, key, bar, line):
        nvd3data = Nvd3Data(df)
        return [nvd3data.convert(key, bar, asBar=True), nvd3data.convert(key, line)] 

