# DeBEIR

A **De**nse **B**i-**E**ncoder for **I**nformation **R**etrieval library for experimenting and using neural models (with a particular emphasis on bi-encoder models) for end-to-end ranking of documents.

### Setup and installation
It is recommended to set up a virtual environment and install the requirements

```bash
python3 -m virtualenv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Usage

The library has an emphasis on reproducibility and experimentation. With this in mind, settings are placed into configuration files to be used to build the pipeline. 

```python3
from nir.interfaces.pipeline import NIRPipeline

p = NIRPipeline.build_from_config(config_fp="./tests/config.toml",
                                  engine="elasticsearch",
                                  nir_config_fp="./tests/nir_config.toml")

results = await p.run_pipeline(cosine_offset=5.0)
```

See examples/ for more use cases and where to get started.

Otherwise, html rendered documentation is available in docs/

### Development

If you use to help with development of the library, first verify the tests cases and set up a development environment. 
This will take approximately 30 minutes to complete on a mid-range system.

Requires: Docker and pip installation of requirements-dev.txt packages.

```bash
cd tests/

./build_test.env.sh

pytest tests_imports.py 
pytest test_pipeline.py
```

A helper script for removing the development environment is provided in ```tests/cleanup.sh```