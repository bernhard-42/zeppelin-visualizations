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
    valueAttributes = ["slope", "intercept"]

    def __init__(self, nvd3Functions):
        super(self.__class__, self).__init__(nvd3Functions)
        self.funcName = "scatterPlusLineChart"
        self.funcBody = """
            function(session, object) {

                var chart = nv.models.scatterChart()
                              .showDistX(true)
                              .showDistY(true)

                chart.xAxis.showMaxMin(false)
                           .tickFormat(d3.format('.1f'));
                           
                chart.yAxis.showMaxMin(false)
                           .tickFormat(d3.format('.1f'));
              
                chart.scatter.onlyCircles = false;

                session.__functions.makeChart(session, object, chart);
            }        
        """


    def convert(self, df, key, value, shape=None, size=None, config={}):
        nvd3data = Nvd3Data()
        valuesConfig, chartConfig = nvd3data.splitConfig(config, len(df), self.valueAttributes)

        if size is None:
            size = [None] * len(df)

        if shape is None:
            shape = [None] * len(df)

        data = [nvd3data.convert(df[i], key[i], value[i], size[i], shape[i], config=valuesConfig[i]) for i in range(len(df))]
        return {"data": data, "config": chartConfig} 