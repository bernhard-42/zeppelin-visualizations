from zeppelin_viz.nvd3.nvd3_chart import Nvd3Chart
from zeppelin_viz.nvd3.nvd3_data import Nvd3Data


class ParallelCoordinatesChart(Nvd3Chart):
    
    def __init__(self, nvd3Functions, height=400, width=1024):
        super(self.__class__, self).__init__(nvd3Functions)
        self.height = height
        self.width = width
        self.funcName = "parallelCoordinatesChart"
        self.funcBody = """
            function(session, object) {
                session.__functions.makeChart(session, object, function() {

                    var dim = dimensions();
                    chart = nv.models.parallelCoordinatesChart()
                        .dimensionData(dim)
                        .displayBrush(false)
                        .lineTension(0.85);

	                return chart
                })
            }        
        """

    def convert(self, df, group, series, colors):
        nvd3data = Nvd3Data(df)
        return [nvd3data.convert(group, series[i], color=colors[i]) for i in range(len(series))]
