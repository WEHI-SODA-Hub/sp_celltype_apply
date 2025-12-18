# Spatial Proteomics Celltype pipeline

This Nextflow pipeline is a sub-pipeline in the Spatial Proteomics Celltype suite. It is used to apply a trained XGBoost
model on preprocessed QuPath data or cell marker measurements in tabular format that the model hasn't been trained on.

## Introduction

This pipeline is a single-process pipeline, and is mostly used as an interface to Nextflow tower. It
feeds preprocessed QuPath data through an already trained XGBoost model.

## Usage

Note that this pipeline expects the input data to already have been preprocessed with the SODA-Classify-Preprocess-Data pipeline.

Parameters: 

```
  Usage:  nextflow run main.nf 
        --input <preprocessed-data.csv>
		--run_name <name>
		--model <bayes-cv-model.sav>
		--preprocess_scheme <scheme>
		--options_toml <preprocess-options.toml>
		--decoder_file <decoder.json>
		--images_list <images.csv>
		--output_path <output>
		--threshold <0.xxx>

  Required Arguments:

  --input			   Preprocessed input data file from QuPath (.csv or .parquet).
  --run_name 		   Run name used to label output files.
  --model              Final model saved from training.
  --preprocess_scheme  The scheme used to preprocess the model before application.
  --decoder_file       JSON file containing the decoder for the predicted cell types.
  --images_list        Path to images file (.csv or .parquet) produced during preprocessing.
  --validation_file    Path to preprocessed data used to train the model (.csv or .parquet).
  --output_path        Path to directory to store output files.

  Note: The pipeline automatically detects whether input files are CSV or Parquet format.
        Output results are always saved as CSV.

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
                        Preprocessed input data file from QuPath (.csv or .parquet).
  --model MODEL, -m MODEL
                        Path to final model file produced from training.
  --preprocess-scheme {null,logp1,poly}, -s {null,logp1,poly}
                        The scheme to use to transform the input data.
  --options OPTIONS, -x OPTIONS
                        Path to TOML file containing preprocessing scheme options.
  --decoder DECODER, -d DECODER
                        Path to decoder JSON file. Used to match predicted values to their cell names
  --images-file IMAGES_FILE, -f IMAGES_FILE
                        Path to images and coordinate columns file (.csv or .parquet). Used when converting predicted results back to QuPath-compatible format.
  --validation-file VALIDATION_FILE, -v VALIDATION_FILE
                        Path to preprocessed input data used to train the XGBoost model (.csv or .parquet). This is used to validate the input data.
  --output-path OUTPUT_PATH, -o OUTPUT_PATH
                        Path to directory to store output files.
  --threshold THRESHOLD, -t THRESHOLD
                        idk what this does yet

Note: The script automatically detects input file format (.csv or .parquet) by extension.
      Output results are always saved as CSV for QuPath compatibility.
```

### Example Usage

Following on from the examples in the [preprocessing step](https://github.com/BioimageAnalysisCoreWEHI/MIBI-preprocess-data/tree/main?tab=readme-ov-file#example-usage)
and in the [training step](https://github.com/BioimageAnalysisCoreWEHI/MIBI-train-model/tree/main?tab=readme-ov-file#example-usage), choose a model
produced by in the training step (look at one of the html reports in the output folder). Make sure to note the path to the model (`<path-to-model>/bayes_cv_model.sav`),
and the preprocessing scheme used to train that model.

```
# Using CSV input (default preprocessing output)
nextflow run main.nf \
    --run_name test-apply \
    --model <path-to-model>/bayes_cv_model.sav \
    --preprocess_scheme <preprocess-scheme> \
    --decoder_file /tmp/mibi-test-run-output/test_decoder.json \
    --images_list /tmp/mibi-test-run-output/test_images.csv \
    --validation_file /tmp/mibi-test-run-output/test_preprocessed_input_data.csv \
    --output_path /tmp/mibi-test-run-output \
    --input /tmp/mibi-test-run-output/test_preprocessed_input_data.csv \
    -profile gpu # use if wehi_gpu profile was used to train the model

# Using Parquet input (if preprocessing output was in Parquet format)
nextflow run main.nf \
    --run_name test-apply-parquet \
    --model <path-to-model>/bayes_cv_model.sav \
    --preprocess_scheme <preprocess-scheme> \
    --decoder_file /tmp/mibi-test-run-output/test_decoder.json \
    --images_list /tmp/mibi-test-run-output/test_images.parquet \
    --validation_file /tmp/mibi-test-run-output/test_preprocessed_input_data.parquet \
    --output_path /tmp/mibi-test-run-output \
    --input /tmp/mibi-test-run-output/test_preprocessed_input_data.parquet \
    -profile gpu
```

In the above example, the input is the output of the preprocessing step, which is also the same as the validation file.
In real usage, the input would be a new set of data (that has been preprocessed), whereas the validation file would be
the same preprocessed data used to train the model being used.

**Note:** The pipeline automatically detects the input file format based on the file extension (`.csv` or `.parquet`). Parquet input files provide faster loading times for large datasets. Output results are always saved as CSV for compatibility with QuPath.

## Pipeline Output

The result of this pipeline is a singular CSV file labelled as `<name>_applied_results.csv` located inside `--output_path`. The output is always in CSV format for compatibility with QuPath, regardless of input file format.

## Credits 

The core functionality of the Spatial Proteomics pipeline was developed by Kenta Yotoke (@yokotenka) under the supervision of Claire Marceaux 
(@ClaireMarceaux). The pipeline was adapted to Nextflow by Edward Yang (@edoyango) and maintained by Michael Mckay (@mikemcka) and Michael Milton (@multimeric).

## Citation

If you use WEHI-SODA-Hub/sp_celltype_apply for your analysis, please cite it using the following doi: 10.5281/zenodo.17970845

An extensive list of references for the tools used by the pipeline can be found in the CITATIONS.md file.

This pipeline was created using the nf-core template. You can cite the nf-core publication as follows:

  The nf-core framework for community-curated bioinformatics pipelines.

  Philip Ewels, Alexander Peltzer, Sven Fillinger, Harshil Patel, Johannes Alneberg, Andreas Wilm, Maxime Ulysse Garcia, Paolo Di Tommaso & Sven Nahnsen.

  Nat Biotechnol. 2020 Feb 13. doi: 10.1038/s41587-020-0439-x.
