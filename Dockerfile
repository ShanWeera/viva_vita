FROM centos:latest

# Update image
RUN yum update -y && yum upgrade -y

# Install dependancies
RUN yum install -y python3.8 python3-pip wget perl tcsh

# Install Perl requirement for IEDB
RUN dnf --enablerepo=powertools install -y perl-List-MoreUtils

# Download Blast
RUN wget -nv --show-progress --progress=bar:force https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.12.0+-1.x86_64.rpm

# Install Blast
RUN yum localinstall -y *.rpm && rm *.rpm

# Add Blast to the envar (installing puts blastp to path)
ENV BLAST_INSTALL_PATH=blastp

# Install Poetry
ENV POETRY_HOME=/poetry
ENV PATH=$POETRY_HOME/bin:$PATH
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3.8 - -p

# Download & Extract IEDB MHC II Tools
RUN wget -nd -nv --show-progress --progress=bar:force https://downloads.iedb.org/tools/mhcii/3.1.5/IEDB_MHC_II-3.1.5.tar.gz
RUN tar -xvf *.tar.gz
RUN rm *.gz

# Download & Extract IEDB MHC II Tools
RUN wget -nd -nv --show-progress --progress=bar:force https://downloads.iedb.org/tools/mhci/3.1.2/IEDB_MHC_I-3.1.2.tar.gz
RUN tar -xvf *.tar.gz
RUN rm *.gz

# Download Prosite binary and DB
# Binary first
WORKDIR /prosite
RUN wget -nv --show-progress --progress=bar:force https://ftp.expasy.org/databases/prosite/ps_scan/ps_scan_linux_x86_elf.tar.gz
RUN tar -xvf *.tar.gz
RUN rm *.gz

# Then DB
WORKDIR /prosite/db
RUN wget -nv --show-progress --progress=bar:force https://ftp.expasy.org/databases/prosite/prosite.dat

# Set the environment variables
ENV PROSITE_INSTALL_PATH=/prosite/ps_scan/pfscan
ENV PROSITE_DB_PATH=/prosite/db/prosite.dat

# Fix the Zipsafe issue for MHC II
RUN \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_ii/methods/allele-info/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_ii/methods/iedbtools-utilities/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_ii/methods/mhcii-comblib-percentile-data/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_ii/methods/mhcii-comblib-predictor/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_ii/methods/mhcii-netmhcii-2.3-percentile-data/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_ii/methods/mhcii-netmhciipan-3.2-percentile-data/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_ii/methods/mhcii-netmhciipan-4.0-ba-percentile-data/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_ii/methods/mhcii-netmhciipan-4.0-el-percentile-data/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_ii/methods/mhcii-predictor-data/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_ii/methods/mhcii-smmalign-percentile-data/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_ii/methods/mhcii-tepitope-percentile-data/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_ii/methods/mhcii-tepitope-predictor/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_ii/methods/netmhcii-1.1-executable/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_ii/methods/netmhcii-2.3-executable/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_ii/methods/netmhciipan-3.2-executable/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_ii/methods/netmhciipan-4.0-executable/setup.py

# Now we install MHC I tools
WORKDIR /mhc_ii/methods/allele-info/
RUN python3.8 setup.py install

WORKDIR /mhc_ii/methods/iedbtools-utilities/
RUN python3.8 setup.py install

WORKDIR /mhc_ii/methods/mhcii-comblib-percentile-data/
RUN python3.8 setup.py install

WORKDIR /mhc_ii/methods/mhcii-comblib-predictor/
RUN python3.8 setup.py install

WORKDIR /mhc_ii/methods/mhcii-netmhcii-2.3-percentile-data/
RUN python3.8 setup.py install

WORKDIR /mhc_ii/methods/mhcii-netmhciipan-3.2-percentile-data/
RUN python3.8 setup.py install

WORKDIR /mhc_ii/methods/mhcii-netmhciipan-4.0-ba-percentile-data/
RUN python3.8 setup.py install

WORKDIR /mhc_ii/methods/mhcii-netmhciipan-4.0-el-percentile-data/
RUN python3.8 setup.py install

WORKDIR /mhc_ii/methods/mhcii-predictor-data/
RUN python3.8 setup.py install

WORKDIR /mhc_ii/methods/mhcii-smmalign-percentile-data/
RUN python3.8 setup.py install

WORKDIR /mhc_ii/methods/mhcii-tepitope-percentile-data/
RUN python3.8 setup.py install

WORKDIR /mhc_ii/methods/mhcii-tepitope-predictor/
RUN python3.8 setup.py install

WORKDIR /mhc_ii/methods/netmhcii-1.1-executable/
RUN python3.8 setup.py install

WORKDIR /mhc_ii/methods/netmhcii-2.3-executable/
RUN python3.8 setup.py install

WORKDIR /mhc_ii/methods/netmhciipan-3.2-executable/
RUN python3.8 setup.py install

WORKDIR /mhc_ii/methods/netmhciipan-4.0-executable/
RUN python3.8 setup.py install

# Fix the Zipsafe issue for MHC I
RUN \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_i/method/netmhc-3.4-executable/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_i/method/netmhcpan-4.0-executable/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_i/method/netmhc-4.0-executable/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_i/method/mhci-ann-predictor-percentile-data/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_i/method/mhci-netmhccons-percentile-data/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_i/method/mhci-netmhcpan-4.0-el-percentile-data-/setup.py &&\
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_i/method/mhci-netmhcpan-4.0-percentile-data/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_i/method/mhci-netmhcpan-4.1-ba-percentile-data/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_i/method/mhci-netmhcpan-4.1-el-percentile-data/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_i/method/mhci-netmhcstabpan-percentile-data/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_i/method/pickpocket-1.1-executable/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_i/method/netmhcpan-2.8-executable/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_i/method/netmhcpan-4.1-executable/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_i/method/netmhccons-1.1-executable/setup.py && \
      sed -i 's/^setup(/replace=setup(\nzip_safe=False,/g' /mhc_i/method/netmhcstabpan-1.0-executable/setup.py

WORKDIR /mhc_i/method/netmhcpan-4.0-executable/
RUN python3.8 setup.py install

WORKDIR /mhc_i/method/netmhc-3.4-executable/
RUN python3.8 setup.py install

WORKDIR /mhc_i/method/netmhc-4.0-executable/
RUN python3.8 setup.py install

WORKDIR /mhc_i/method/mhci-ann-predictor-percentile-data/
RUN python3.8 setup.py install

WORKDIR /mhc_i/method/mhci-netmhccons-percentile-data/
RUN python3.8 setup.py install

WORKDIR /mhc_i/method/mhci-netmhcpan-4.0-el-percentile-data-/
RUN python3.8 setup.py install

WORKDIR /mhc_i/method/mhci-netmhcpan-4.0-percentile-data/
RUN python3.8 setup.py install

WORKDIR /mhc_i/method/mhci-netmhcpan-4.1-ba-percentile-data/
RUN python3.8 setup.py install

WORKDIR /mhc_i/method/mhci-netmhcpan-4.1-el-percentile-data/
RUN python3.8 setup.py install

WORKDIR /mhc_i/method/mhci-netmhcstabpan-percentile-data/
RUN python3.8 setup.py install

WORKDIR /mhc_i/method/pickpocket-1.1-executable/
RUN python3.8 setup.py install

WORKDIR /mhc_i/method/netmhcpan-2.8-executable/
RUN python3.8 setup.py install

WORKDIR /mhc_i/method/netmhcpan-4.1-executable/
RUN python3.8 setup.py install

WORKDIR /mhc_i/method/netmhccons-1.1-executable/
RUN python3.8 setup.py install

WORKDIR /mhc_i/method/netmhcstabpan-1.0-executable/
RUN python3.8 setup.py install

WORKDIR /mhc_ii
RUN rm -rf methods/

# Run tests
RUN python3.8 mhc_II_binding.py consensus3 HLA-DRB1*03:01 test.fasta
RUN python3.8 mhc_II_binding.py comblib HLA-DPA1*01/DPB1*04:01 test.fasta
RUN python3.8 mhc_II_binding.py IEDB_recommended HLA-DRB1*03:01 test.fasta
RUN python3.8 mhc_II_binding.py netmhciipan_el HLA-DRB1*03:01 test.fasta
RUN python3.8 mhc_II_binding.py netmhciipan_ba HLA-DRB1*03:01 test.fasta
RUN python3.8 mhc_II_binding.py nn_align HLA-DPA1*01:03/DPB1*02:01 test.fasta
RUN python3.8 mhc_II_binding.py smm_align HLA-DPA1*01/DPB1*04:01 test.fasta
RUN python3.8 mhc_II_binding.py sturniolo HLA-DRB1*04:21 test.fasta

# Configure MHC I
WORKDIR /mhc_i
RUN python3.8 src/configure.py
RUN rm -rf method/

# Add both IEDB tools to Python path
ENV PYTHONPATH=/mhc_i/src:/mhc_ii

# Run MHCI tests
#RUN python3.8 src/predict_binding.py consensus HLA-A*02:01 9 ./examples/input_sequence.fasta
RUN python3.8 src/predict_binding.py netmhcpan_el HLA-A*02:01 9 ./examples/input_sequence.fasta
RUN python3.8 src/predict_binding.py ann HLA-A*02:01 9 ./examples/input_sequence.fasta
RUN python3.8 src/predict_binding.py IEDB_recommended HLA-A*02:01 9 ./examples/input_sequence.fasta
RUN python3.8 src/predict_binding.py netmhcpan_ba HLA-A*02:01 9 ./examples/input_sequence.fasta
RUN python3.8 src/predict_binding.py pickpocket HLA-A*02:01 9 ./examples/input_sequence.fasta
RUN python3.8 src/predict_binding.py smm HLA-A*02:01 9 ./examples/input_sequence.fasta
RUN python3.8 src/predict_binding.py smmpmbec HLA-A*02:01 9 ./examples/input_sequence.fasta

# Installing NCBI TaxDB and add path to env
WORKDIR /blastdb
RUN wget -nv --show-progress --progress=bar:force https://ftp.ncbi.nlm.nih.gov/blast/db/taxdb.tar.gz
RUN tar -xvf taxdb.tar.gz
RUN rm *.gz
ENV BLASTDB=/blastdb

# Copy project files
COPY pyproject.toml /viva_vdm/
COPY viva_vdm /viva_vdm/viva_vdm/

# Install project dependancies
WORKDIR /viva_vdm
RUN poetry export -f requirements.txt --output requirements.txt
RUN python3.8 -m pip install -r requirements.txt
