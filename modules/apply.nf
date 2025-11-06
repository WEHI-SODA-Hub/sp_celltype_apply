#!/bin/env nextflow 

// Enable DSL-2 syntax
nextflow.enable.dsl=2

process APPLY {	
	cpus 1
	memory "${params.memory}"
	publishDir "${params.output_path}", mode: 'copy'
	label "apply"
	time "1h"
	container "oras://ghcr.io/wehi-researchcomputing/mibi:0.1"

	input:
	path(apply_script_ch)
	path(input_data_ch)
	path(model_ch)
	path(options_ch)
	path(decoder_ch)
	path(images_ch)
	path(validation_ch)
	val(threshold_ch)

	output:
	path("*_applied_results.csv", type: "file")
	
	script:
	def options = options_ch.name != "NO_FILE" ? "--options ${options_ch}" : ''
	def threshold = threshold_ch != "" ? "--threshold ${threshold_ch}" : ''
	"""
	python3 -B ${apply_script_ch} \\
		--input ${input_data_ch} \\
		--name ${params.run_name} \\
		--model ${model_ch} \\
		--preprocess-scheme ${params.preprocess_scheme} \\
		--decoder ${decoder_ch} \\
		--images-file ${images_ch} \\
		--validation-file ${validation_ch} \\
		--output-path . \\
		${threshold} ${options}
	"""
}
