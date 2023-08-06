# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['experiment_results_manager']

package_data = \
{'': ['*']}

install_requires = \
['fsspec>=2021.4', 'pydantic>=1.6,<2.0']

setup_kwargs = {
    'name': 'experiment-results-manager',
    'version': '0.1.2',
    'description': 'Light-weight experiment tracker',
    'long_description': '# 🔬 ERM: Experiment Results Manager\n\nLight-weight alternative to `mlflow` experiment tracking that doesn\'t require kubernetes. Useful tool to compare metrics between training attempts in your model training workflow\n\n## ✨ Features\n\n- 📈 Track plots, metrics, & other data\n- 👀 Side-by-side comparison \n- 💾 Experiment registry \n- ⛅️ Supports S3, GCS, Azure and others (via `fsspec`)\n\n## 🚀 Examples & Demos\n- Quick and easy: [serialize_and_deserialize.ipynb](examples/serialize_and_deserialize.ipynb)\n- Practical but more involved: [compare_runs.ipynb](examples/compare_runs.ipynb)\n- Browse the registry: [browse_registry.ipynb](examples/browse_registry.ipynb)\n\n<p align="center">\n<img src="https://user-images.githubusercontent.com/1297369/233723764-c52cf948-ec4d-4b94-916d-77cadababae8.png" height="400">\n</p>\n\n## ✅ Get Started\n#### Installation\n```sh\n\npip install experiment-results-manager \\\n  gcsfs \\\n  s3fs\n# install s3fs if you plan to store data in s3\n# install gcsfs if you plan to store data in google cloud storage\n```\n\n#### Basic Usage\n```python\nimport experiment_results_manager as erm\n\n# Create an experiment run\ner = erm.ExperimentRun(\n    experiment_id="my_experiment",\n    variant_id="main"\n)\n\n# Log relevant data\ner.log_param("objective", "rmse")\ner.log_metric("rmse", "0.9")\ner.log_figure(mpl_fig, "ROC Curve")\ner.log_text("lorem ipsum...", "text")\n\n# Display the report (if you are in a notebook)\nhtml = erm.compare_runs(er)\ndisplay(HTML(html))\n\n# Save to registry\nsaved_path = erm.save_run_to_registry(er, "s3://erm-registry")\n\n```\n<hr>\n<p align="center" style="text-align: center; color: gray; font-size: 10px;">\nMade with ❤️ in Berlin\n</p>\n',
    'author': 'sa-',
    'author_email': 'name@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ml-cyclops/experiment-results-manager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
