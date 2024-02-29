# MIBI Apply Model Pipeline

This Nextflow pipeline is a sub-pipeline in the MIBI suite. It is used to apply a trained XGBoost
model on preprocessed QuPath data that the model hasn't been trained on.

## Introduction

This pipeline is a single-process pipeline, and is mostly used as an interface to Nextflow tower. It
feeds preprocessed QuPath data through an already trained XGBoost model.

## Usage

Note that this pipeline expects the input data to already have been preprocessed with the MIBI 
Preprocess Data pipeline.

Parameters: 

```
  Usage:  nextflow run main.nf 
        --input <preprocessed-data.csv>
		--run_name <name>
		--model <final_model.json>
		--preprocess_scheme <scheme>
		--options_toml <preprocess-options.toml>
		--decoder_file <decoder.json>
		--images_list <images.csv>
		--output_path <output>
		--threshold <0.xxx>

  Required Arguments:

  --input			   Preprocessed input data file from QuPath.
  --run_name 		   Run name used to label output files.
  --model              Final model saved from training (either in JSON or Pickle).
  --preprocess_scheme  The scheme used to preprocess the model before application.
  --decoder_file       JSON file containing the decoder for the predicted cell types.
  --output_path        Path to directory to store output files.

  Optional Arguments:

  --options_toml       TOML file containing preprocessing scheme and model classifier options. Only needed if --preprocess_scheme=poly. 
  --threshold	       Not sure what this does yet	
```

If you feel comfortable with the command line, you can run the preprocessing Python script directly.

```
$ conda env create -f envs/environment.yml   # or envs/environment-gpu.yml
$ conda activate xgboost-cell-classification # or xgboost-cell-classification-gpu
$ python scripts/apply_final_classifier.py --help
usage: MIBI-apply [-h] --name NAME --input INPUT --model MODEL --preprocess-scheme {null,logp1,poly} [--options OPTIONS] --decoder DECODER --images-file IMAGES_FILE
                  --output-path OUTPUT_PATH [--threshold THRESHOLD]

This takes an XGBoost classifier model and applies it on unlabelled cell data.

optional arguments:
  -h, --help            show this help message and exit
  --name NAME, -n NAME  Run name used to label output files.
  --input INPUT, -i INPUT
                        Preprocessed input data file from QuPath.
  --model MODEL, -m MODEL
                        Path to final model file produced from training.
  --preprocess-scheme {null,logp1,poly}, -s {null,logp1,poly}
                        The scheme to use to transform the input data.
  --options OPTIONS, -x OPTIONS
                        Path to TOML file containing preprocessing scheme options.
  --decoder DECODER, -d DECODER
                        Path to decoder JSON file. Used to match predicted values to their cell names
  --images-file IMAGES_FILE, -f IMAGES_FILE
                        Path to images and coordinate columns CSV file. Used when converting predicted results back to QuPath-compatible format.
  --output-path OUTPUT_PATH, -o OUTPUT_PATH
                        Path to directory to store output files.
  --threshold THRESHOLD, -t THRESHOLD
                        idk what this does yet
```

## Pipeline Output

The result of this pipeline is a singular CSV file labelled as `<name>_applied_results.csv` located inside `--output_path`.

## Credits 

The core functionality of the MIBI pipeline was developed by Kenta Yotoke (@yokotenka) under the supervision of Claire Marceaux 
(@ClaireMarceaux). The pipeline was adapted to Nextflow by Edward Yang (@edoyango).

## Citation

TBC