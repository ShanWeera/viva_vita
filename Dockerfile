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

# Install Poetry
ENV POETRY_HOME=/poetry
ENV PATH=$POETRY_HOME/bin:$PATH
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3.8 -

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

# Now we install MHC I tools
WORKDIR /mhc_ii/methods/allele-info/
RUN python3.8 setup.py install

