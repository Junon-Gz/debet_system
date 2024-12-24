# USAGE

- linux

1.install miniconda
```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh
```

2.create conda environment
```bash
conda create -n debet-system python=3.11
```

3.activate conda environment
```bash
conda activate debet-system
```

4.clone project
```bash
git clone https://github.com/Junon_Gz/debet_system.git
cd debet-system
```

5.install dependencies
```bash
pip install -r requirements.txt
```

6.run project
```bash
python run.py
```
7.visit http://localhost:5000/register
