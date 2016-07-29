#!/bin/bash
VMS="$(VBoxManage list vms)"
IFS=$'\n'
i=0
for vm in $VMS;do
    i=$((i+1))
    name="$(echo $vm | grep -o '"[^"]\+"' | sed 's/\"//g')"
    id[i]="$(echo $vm | grep -o '{[^}]\+}' | sed 's/[{}]//g')"
    echo "No.${i} - ${name}" 
done
#echo "Please input the number of VM to start"

while [[ ! $NO =~ ^-?[0-9]+$ ]] || [ "$NO" -gt "$i" -o "$NO" -le "0" ];do
    read -p "$(echo -e 'Please input the number of VM to start: \n\b')" NO
done
chosenID=${id[${NO}]}
VBoxManage startvm --type headless ${chosenID}
