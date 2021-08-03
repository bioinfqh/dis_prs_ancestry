infile=$1
sample_id=$2
customer_id=$3

infile_dir="XGMIX_infiles"
model_file_path="XGMIX_model_files"
output_prefix_path="demo_data/demo"

echo "start running local ancestry"
mkdir -p vcf_temp_dir
bash dis_calc/partition_vcf.sh $infile vcf_temp_dir
echo dis_calc/run_xgmix.py vcf_temp_dir $sample_id $model_file_path $output_prefix_path $customer_id
#outfile=$(python3 dis_calc/run_xgmix.py vcf_temp_dir $sample_id $model_file_path $output_prefix_path $customer_id)
python3 dis_calc/run_xgmix.py vcf_temp_dir $sample_id $model_file_path $output_prefix_path $customer_id
