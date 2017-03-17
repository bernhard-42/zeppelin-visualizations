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


class Nvd3Data(object):
    
    def __init__(self):
        pass
        
                                         # NVD3 data attributes:
    def convert(self, df,
                      key,               # name as "key" and values as "values.x"
                      value,             # "values.y"
                      size=None,         # "values.size"
                      shape=None,        # "values.shape"
                      config = {}        # values configs
                ):

        columns = [key, value]
        rowIndices = [0,1]
        attributes = ["x", "y"]

        if size is not None:
            columns.append(size)
            rowIndices.append(max(rowIndices) + 1)
            attributes.append("size")

        if shape is not None:
            columns.append(shape)
            rowIndices.append(max(rowIndices) + 1)
            attributes.append("shape")

        values = list({attributes[i]:row[1][rowIndices[i]] for i in rowIndices} for row in df[columns].iterrows())
 
        data = {
            "key": value,
            "values": values
        }
        mapping = {"style": "classed"}
        
        for k,v in config.items():
            if k not in ["key", "values"]:
                if mapping.get(k):
                    k = mapping[k]
                if v is not None:
                    data[k] = v
                
        return data 


    def splitConfig(self, config, seriesLen, locals):
        chartConfig = {}
        valuesConfig = {}
    
        for k, v in config.items():
            if k in locals:
                if isinstance(v, (list, tuple)):
                    valuesConfig[k] = v
                else:
                    valuesConfig[k] = [v]
            else:
                if k == "color":
                    if seriesLen > 0:
                        chartConfig[k] = v # v[0:seriesLen]
                    else:
                        chartConfig[k] = v # v[0:1]
                else:
                    chartConfig[k] = v

        if valuesConfig == {}:
            valuesConfig = [{} for i in range(1 if seriesLen == 0 else seriesLen)] 

        else:
            if seriesLen > 0:
                res = [{} for i in range(seriesLen)]
                for k,v in valuesConfig.items():
                    for i in range(len(v)):
                        res[i][k] = v[i]
                valuesConfig = res

        return (valuesConfig, chartConfig)
        