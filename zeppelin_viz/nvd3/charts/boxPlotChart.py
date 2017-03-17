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


class BoxPlotChart(Nvd3Chart):
    valueAttributes = []

    def __init__(self, nvd3Functions):
        super(self.__class__, self).__init__(nvd3Functions)
        self.funcName = "boxPlotChart"
        self.funcBody = """
            function(session, object) {

                chart = nv.models.boxPlotChart()
                        .x(function(d) { return d.label })

                session.__functions.makeChart(session, object, chart);
            }      
        """

    def convert(self, df, boxStyle="iqr", config={}):
        nvd3data = Nvd3Data()

        valuesConfig, chartConfig = nvd3data.splitConfig(config, df.shape[1], self.valueAttributes)
        valuesConfig = valuesConfig[0]

        q1 = df.quantile(0.25)
        q2 = df.quantile(0.5)
        q3 = df.quantile(0.75)

        if boxStyle == "iqr":          # iqr
            iqr = q3 - q1
            low = q1 - 1.5 * iqr
            high = q3 + 1.5 * iqr
        else:                          # "min-max"
            low  = df.min()
            high = df.max()
            
        data =  [{"label":df.columns[i],
                  "values":{"whisker_low":low[i], "Q1":q1[i], "Q2":q2[i], "Q3": q3[i], "whisker_high":high[i]}}
                 for i in range(len(df.columns))] 
         
        # Add outliers
        if boxStyle == "iqr":
            for i in range(len(df.columns)):
                values = df.iloc[:,i]
                data[i]["values"]["outliers"] = list(values[(values < q1[i]-1.5*iqr[i]) | (values > q3[i]+1.5*iqr[i])])


        return {"data":data, "config":chartConfig}
    
    def append(self, dataConfig, chart=0):
        print("Not supported")

    def update(self, rowIndices, dataConfig, chart=0):
        print("Not supported")

    def delete(self, rowIndices, chart=0):
        print("Not supported")
