# Lattice-based Sign and Verify on Raspberry Pi  

This project contains an implementation of **Dilithium**, a post-quantum digital signature scheme, running on a **Raspberry Pi**. The project measures **signing and verification times** in a real-world embedded environment, aiming to evaluate the feasibility of lattice-based cryptography for quantum-resistant security.  

## Features  
- **Dilithium Implementation**: Based on the CRYSTALS-Dilithium signature scheme. 
- **Post-Quantum Security**: Uses lattice-based cryptography to resist quantum attacks.  
- **Lightweight Application**: Designed to run efficiently on Raspberry Pi hardware.  

## Installation  

### Prerequisites  
Ensure your Raspberry Pi is set up with the necessary dependencies:  
- **Raspberry Pi 4 or 5 (any model with SSD support recommended)**  
- **Raspberry Pi OS (or a compatible Linux distribution)**  
- **4 GB ram for Raspberry Pi (recommended)**

### Clone the Repository  
```bash
git clone https://github.com/ahmed-ghadban/Dilithium.git
cd Dilithium
pip3 install -r requirements.txt
```

## Usage

After setting up the project, run the program with this command:
```bash
python3 Dilithium-Signature.py
```

![image](https://github.com/user-attachments/assets/45b6ac8f-9b80-47f3-9644-670a00ff42e0)


This is the interface of the app

## Performance Evaluation

This test made on:
1. Raspberry Pi 4
2. 4 GB ram
3. ssd m.2 256GB
4. Kali Linux OS

![image](https://github.com/user-attachments/assets/c6a71637-4bbe-4151-86b5-a0d1b42353a8)


| Metrics | Dilithium 2 | Dilithium 3 | Dilithium 5 |
|:------------|:--------|:--------|:--------:|
| KeyGen Time   | 31.017065 mS   | 48.992872 mS | 74.997425 mS |
| Sign Time      | 57.479382 mS   | 172.993898 mS | 185.995817 mS |
| Verify Time    | 29.039383 mS   | 46.033621 mS | 67.035675 mS |



## References  

Refer to the [Dilithium Specification][dilithium] and [NIST PQC Project][nist] for more information.  

[dilithium]: https://pq-crystals.org/dilithium/  
[nist]: https://csrc.nist.gov/Projects/post-quantum-cryptography
