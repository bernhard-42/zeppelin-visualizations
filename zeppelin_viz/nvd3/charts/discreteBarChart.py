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
import pandas as pd


class DiscreteBarChart(Nvd3Chart):
    valueAttributes = []

    def __init__(self, nvd3Functions):
        super(self.__class__, self).__init__(nvd3Functions)
        self.funcName = "discreteBarChart"
        self.funcBody = """
            function(session, object) {
                var chart = nv.models.discreteBarChart()
                    .staggerLabels(true)
                    .showValues(true)
                    .showLegend(false)
                    .margin({top:30})

                session.__functions.makeChart(session, object, chart);
            }        
        """

    def convert(self, data, group, series, config={}):
        df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
        
        nvd3data = Nvd3Data()
        valuesConfig, chartConfig = nvd3data.splitConfig(config, df.shape[0], self.valueAttributes)
        valuesConfig = valuesConfig[0]

        data = [nvd3data.convert(df, group, series, config=valuesConfig)]

        return {"data": data, "config": chartConfig} 

    def append(self, dataConfig, chart=0):
        print("Not supported")

    def update(self, rowIndices, dataConfig, chart=0):
        print("Not supported")

    def delete(self, rowIndices, chart=0):
        print("Not supported")
