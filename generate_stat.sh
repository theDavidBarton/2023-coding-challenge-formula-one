#!/bin/bash

number_of_drivers=$1
number_of_engine_suppliers=$2
number_of_images=$3
number_of_identified_images=$4
number_of_not_identified_images=$5
size_of_all_images=$6
average_size_of_images=$7
highest_resolution=$8
lowest_resolution=$9

echo "1. number of drivers in the championship: $number_of_drivers" > stat.txt
echo "2. number of engine suppliers: $number_of_engine_suppliers" >> stat.txt
echo "3. number of images: $number_of_images" >> stat.txt
echo "4. number of identified images: $number_of_identified_images" >> stat.txt
echo "5. number of not identified images: $number_of_not_identified_images" >> stat.txt
echo "6. size of all images: $size_of_all_images" >> stat.txt
echo "7. average size of images: $average_size_of_images" >> stat.txt
echo "8. highest resolution: $highest_resolution" >> stat.txt
echo "9. lowest resolution: $lowest_resolution" >> stat.txt

echo "stat.txt created successfully (Linux)"
