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


class LineChart(Nvd3Chart):
    valueAttributes = ["area", "fillOpacity", "style"]

    def __init__(self, nvd3Functions):
        super(self.__class__, self).__init__(nvd3Functions)
        self.funcName = "lineChart"
        self.funcBody = """
            function(session, object) {
                session.__functions.makeChart(session, object, function() {
                    console.log(session, object)
                    chart = nv.models.lineChart()
                              .useInteractiveGuideline(true)

                    chart.margin({right:  40});
                    chart.margin({bottom: 30});
                    
                    chart.xAxis
                        .axisLabel("X")
                         .tickFormat(d3.format(',.2f'))
                        .staggerLabels(false)
                    chart.x2Axis.tickFormat(d3.format(',f'))
                    
                    chart.yAxis
                         .axisLabel('Voltage (v)')
                         .tickFormat(d3.format(',.2f'));

                   return chart
                })
            }        
        """

        print("%html")
        print("<style>.dashed { stroke-dasharray: 7,7; }\n .dotted { stroke-dasharray: 3,3; } </style>")

    def convert(self, df, group, series, config={}):
        nvd3data = Nvd3Data()
        valuesConfig, chartConfig = nvd3data.splitConfig(config, len(series), self.valueAttributes)

        data = [nvd3data.convert(df, group, series[i], config=valuesConfig[i]) for i in range(len(series))]
        return {"data": data, "config": chartConfig} 
