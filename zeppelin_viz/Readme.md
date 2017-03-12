# Visualizations in Apache Zeppelin

## Overview

The projects

- [ZeppelinSession](https://github.com/bernhard-42/advanced-angular-for-pyspark)
- [ZeppelinCommLayer](https://github.com/bernhard-42/zeppelin-ipython-shim)

allow to use python and javascript visualization libraries in Apache [Zeppelin](https://zeppelin.apache.org/)

Currently supported are

- [Bokeh](http://bokeh.pydata.org) (using ZeppelinCommLayer)
- [NVD3](http://nvd3.org/) currently only LinePlusBarChart and ScatterPlusLineChart* (more toi come, using ZeppelinSession)


Look at [Zeppelin-Viz.md](notebooks/Zeppelin-Viz.md) or import [Zeppelin-Viz.json](notebooks/Zeppelin-Viz.json) into Zeppelin.

To run the Zeppelin Notebook, first install the python libraries:

```bash
git clone https://github.com/bernhard-42/advanced-angular-for-pyspark.git
cd advanced-angular-for-pyspark
pip install .

git clone https://github.com/bernhard-42/zeppelin-ipython-shim.git
cd zeppelin-ipython-shim
pip install .

git clone https://github.com/bernhard-42/zeppelin-visualizations.git
cd zeppelin-visualizations
pip install .
```


## License

Copyright 2017 Bernhard Walter

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.