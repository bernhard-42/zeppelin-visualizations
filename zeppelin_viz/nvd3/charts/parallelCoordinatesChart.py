from zeppelin_viz.nvd3.nvd3_chart import Nvd3Chart
from zeppelin_viz.nvd3.nvd3_data import Nvd3Data


class ParallelCoordinatesChart(Nvd3Chart):
    valueAttributes = ["strokeWidth", "color"]
    
    def __init__(self, nvd3Functions, height=400, width=1024):
        super(self.__class__, self).__init__(nvd3Functions)
        self.height = height
        self.width = width
        self.funcName = "parallelCoordinatesChart"
        self.funcBody = """
            function(session, object) {
                console.log(1, object.data);
                for(i in object.data.dim) {
                    console.log(3, object.data.dim[i].format)
                    object.data.dim[i].format = d3.format(object.data.dim[i].format)
                }
                console.log(2, object.data);
                chart = nv.models.parallelCoordinatesChart()
                        .dimensionData(object.data.dim)
                        .displayBrush(true)
                        .lineTension(0.85);

                session.__functions.makeChart(session, object, chart);
            }
        """

    def convert(self, df, group, series, dimFormat=None, dimTooltip=None, config={}):
        nvd3data = Nvd3Data()
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
