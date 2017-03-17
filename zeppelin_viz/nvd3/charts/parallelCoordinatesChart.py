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

from zeppelin_viz.nvd3.nvd3_chart import Nvd3Chart
from zeppelin_viz.nvd3.nvd3_data import Nvd3Data


class ParallelCoordinatesChart(Nvd3Chart):
    valueAttributes = ["color", "strokeWidth"]
    
    def __init__(self, nvd3Functions, height=400, width=1024):
        super(self.__class__, self).__init__(nvd3Functions)
        self.height = height
        self.width = width
        self.funcName = "parallelCoordinatesChart"
        self.funcBody = """
            function(session, object) {
                for(i in object.data.dim) {
                    object.data.dim[i].format = d3.format(object.data.dim[i].format)
                }

                chart = nv.models.parallelCoordinatesChart()
                        .dimensionData(object.data.dim)
                        .displayBrush(true)
                        .lineTension(0.85);

                session.__functions.makeChart(session, object, chart);
            }
        """

    def convert(self, df, group, series, dimFormat=None, dimTooltip=None, color=None, strokeWidth=None, config={}):
        nvd3data = Nvd3Data()

        if color is not None:
            config["color"] = df[color].tolist()
            
        if strokeWidth is not None:
            config["strokeWidth"] = df[strokeWidth].tolist()
            
        valuesConfig, chartConfig = nvd3data.splitConfig(config, df.shape[0], self.valueAttributes)

        data = [{"name":row[group], "values": {k:v for k,v in row.items() if k != group}} for row in df.to_dict("records")]
        for i in range(df.shape[0]):
            for k,v in valuesConfig[i].items():
                data[i][k] = v
            
        dim = [{"key":col} for col in series]
        for i in range(len(dim)):
            if dimFormat is not None:
                dim[i]["format"] = dimFormat[i]
            if dimTooltip is not None:
                dim[i]["tooltip"] = dimTooltip[i]
                
        return {"data": data, "dim":dim, "config": chartConfig} 

    def append(self, dataConfig, chart=0):
        print("Not supported")

    def update(self, rowIndices, dataConfig, chart=0):
        print("Not supported")

    def delete(self, rowIndices, chart=0):
        print("Not supported")
