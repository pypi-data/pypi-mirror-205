# pylama-to-codelimate

Convert pylama output to codelimate format to be loaded by Gitlab

## Usage

```bash
pylama -o json > pylama.json
pylama_to_codelimate -i pylama.json -o codelimate.json
```
