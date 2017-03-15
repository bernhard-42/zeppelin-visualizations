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
    valueAttributes = ["bar"]
    
    def __init__(self, nvd3Functions):
        super(self.__class__, self).__init__(nvd3Functions)
        self.funcName = "linePlusBarChart"
        self.funcBody = """
            function(session, object) {
                session.__functions.makeChart(session, object, function() {

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
                    
                    return chart;
                })
            }
        """
 

    def convert(self, df, key, lineCol, barCol, config={}):
        nvd3data = Nvd3Data()
        columns =       [barCol, lineCol] # same order
        config["bar"] = [True,   False]   # same order
        valuesConfig, chartConfig = nvd3data.splitConfig(config, 2, self.valueAttributes)

        data = [nvd3data.convert(df, key, columns[i], config=valuesConfig[i]) for i in range(2)]
        return {"data": data, "config": chartConfig} 