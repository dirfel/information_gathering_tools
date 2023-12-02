#!/bin/bash
function icmp_scan() {
  ip_address="$1"
  # Realiza um ping com um único pacote e um tempo limite de 1 segundo
  ipc=$(ping -c1 $ip_address | grep ttl | cut -d ":" -f 1 | cut -d " " -f 4)
  if [[ $ipc  ]]; then
    echo "[*] $ip_address ativo"
  else
    echo "[ ] $ip_address inativo"
  fi
}
# Verifica se o usuário forneceu um parâmetro
if [ -z "$1" ]; then
  echo "Uso: $0 <endereço IP ou range>"
  exit 1
fi

# Obtém o endereço IP ou range
ip="$1"

# Verifica se o endereço IP é válido
if [[ "$ip" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
  # O endereço IP é válido
  target="$ip"
elif [[ "$ip" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}-[0-9]{1,3}$ ]]; then
  start=$(echo $ip | cut -d '.' -f 4 | cut -d '-' -f1)
  stop=$(echo $ip | cut -d '.' -f 4 | cut -d '-' -f2)
  base=$(echo $ip | cut -d '.' -f 1,2,3)
  target=$(for (( i=${start}; i<=${stop}; i++ )); do echo $base.$i; done)
else
  # O endereço IP não é válido
  echo "Endereço IP inválido"
  exit 1
fi

# Realiza o icmpscan
for ip in $target; do
  icmp_scan "$ip"
done
