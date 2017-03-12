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
    
    def __init__(self, df):
        self.df = df
        
                                         # NVD3 data attributes:
    def convert(self, key,               # name as "key" and values as "values.x"
                      value,             # "values.y"
                      size=None,         # "values.size"
                      shape=None,        # "values.shape"
                      asBar=False,       # "bar"
                      asArea=False,      # "area"
                      color=None,        # "color"
                      slope=None,        # for withLine charts
                      intercept=None     # for withLine charts
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
            
        values = list({attributes[i]:row[1][rowIndices[i]] for i in rowIndices} for row in self.df[columns].iterrows())
        
        data = {
            "key": value,
            "values": values
        }
        
        if asBar:
            data["bar"] = True
        if asArea:
            data["area"] = True
        if color:
            data["color"] = color
        if slope:
            data["slope"] = slope
        if intercept:
            data["intercept"] = intercept
            
        return data 
