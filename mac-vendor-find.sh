#!/bin/bash
# script usado para imprimir o nome do fabricante de um macaddress
# modo de uso:
# 1. baixe o arquivo com os endereços Mac no url: https://maclookup.app/downloads/csv-database
# execute o comando: cat mac-vendor.txt | rev | cut -d, -f4-9 | rev > mac-vendor2.txt # onde mac-vendor.txt é o arquivo baixado
# execute da seguinte forma: bash mac-vendor-find.sh mac_alvo
# obs importante: precisa ter o arquivo mac-vendor2.sh para funcionar

mac=$1

end=17
while [[ $end -ge 2 ]]
do
    macstart=$(echo $mac | cut -c 1-$end)
    cat mac-vendor2.txt | grep -i ^$macstart > vendorlist
    vendorlistlen=$(cat vendorlist | wc -l)
    if [[ $vendorlistlen -eq 1  ]]
    then
        cat vendorlist | cut -d "," -f 2-9
        break
    else
        end=$(($end - 1))
    fi
done