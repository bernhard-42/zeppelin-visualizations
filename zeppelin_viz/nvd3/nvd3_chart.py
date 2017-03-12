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

from .nvd3_functions import Nvd3Functions

class Nvd3Chart(object):
    _plotId = 0

    def __init__(self, nvd3Functions, funcName, height=400, width=1024):
        self.funcName = funcName
        self.height = height
        self.width = width

        self.id = 0
        self.data = None
        self.nvd3Functions = nvd3Functions
        

    def _divId(self):
        return "%s-%03d" % (self.funcName, Nvd3Chart._plotId) 
        

    def _send(self, event, delay, data):
        self.nvd3Functions.send(self.funcName, event, data, "%s" % self._divId(), delay)

    def plot(self, data):
        Nvd3Chart._plotId = Nvd3Chart._plotId + 1
        
        print("%html")
        print("""
        <div id="%s"  class='with-3d-shadow with-transitions' style="height:%dpx; width:%dpx">
            <svg></svg>
        </div>
        """ % (self._divId(), self.height, self.width))
        
        self.data = data
        self._send("plot", 200, data)


    def replace(self, data):
        self.data = data
        self._send("replace", 0, data)
    
        
    def append(self, newData):                              # needs to do the same as the javascript part

        def _appendData(data, newData):
            data["values"] = data["values"] + newData["values"]
            for key in newData.keys():
                if key not in ["key", "values"]:
                    data[key] = newData[key]

        if type(self.data) == list and type(newData) == list:
            for i in range(len(self.data)):
                _appendData(self.data[i], newData[i])
        else:
            _appendData(self.data, newData)
            
        self._send("append", 0, newData)
    
            
    def update(self, rowIndices, changedData):              # needs to do the same as the javascript part

        def _updateData(data, rowIndices, changedData):
            for i in range(len(rowIndices)):
                data["values"][rowIndices[i]] = changedData["values"][i]
    
            for key in changedData.keys():
                if key not in ["key", "values"]:
                    data[key] = changedData[key]

        if type(self.data) == list and type(changedData) == list:
            for i in range(len(self.data)):
                _updateData(self.data[i], rowIndices, changedData[i])
        else:
            _updateData(self.data, rowIndices, changedData)
            
        self._send("update", 0, {"rowIndices":rowIndices, "changedData":changedData})

        
    def delete(self, rowIndices):              # needs to do the same as the javascript part

        sortedIndices = sorted(rowIndices, reverse=True)
        def _deleteData(data, rowIndices):
            for i in sortedIndices:
                data["values"].pop(i)
    
        if type(self.data) == list:
            for i in range(len(self.data)):
                _deleteData(self.data[i], rowIndices)
        else:
            _deleteData(self.data, rowIndices)
            
        self._send("delete", 0, {"rowIndices":sortedIndices})
        
    def saveAsPng(self, filename=None):
        if filename is None:
            filename = self._divId
        self._send("saveAsPng", 0, {"filename":filename})

