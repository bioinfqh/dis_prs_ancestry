

legend="false"

if [ $# -ge 3 ]; then
    if [[ $3 == "true" ]]; then
        legend="true"
    fi
fi
perc=$2
perc_even=${perc%.*}
echo $perc_even

python3 dis_calc/make_scale_with_data.py $1 $2 $legend
python3 dis_calc/make_scale_2.py $1 dis_calc/yourscale_$perc_even.png
rm -f dis_calc/out_temp_2.png
