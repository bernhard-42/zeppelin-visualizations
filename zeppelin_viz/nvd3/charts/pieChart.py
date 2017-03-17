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


class PieChart(Nvd3Chart):
    valueAttributes = []
    
    def __init__(self, nvd3Functions):
        super(self.__class__, self).__init__(nvd3Functions)
        self.funcName = "pieChart"
        self.funcBody = """
            function(session, object) {
                var chart = nv.models.pieChart()
                    .showLabels(true)
                    .growOnHover(true)
                    .labelType('value')
                    .legendPosition('top')
                    .showTooltipPercent(true)

               session.__functions.makeChart(session, object, chart);
            }        
        """

    def convert(self, data, group, series, config={}):
        df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
        
        nvd3data = Nvd3Data()
        series = [series]
        valuesConfig, chartConfig = nvd3data.splitConfig(config, df.shape[0], self.valueAttributes)

        data = [nvd3data.convert(df, group, series[i], config=valuesConfig[i])["values"] for i in range(len(series))]
        return {"data": data[0], "config": chartConfig} 