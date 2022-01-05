FROM binaryanalysisplatform/bap:latest

COPY ./add_site_cert.sh /bin/add_site_cert.sh
RUN add_site_cert.sh github.com 443

RUN git clone https://github.com/draperlaboratory/cbat_tools.git

RUN cd cbat_tools/wp; \
    opam config exec -- make

RUN cd cbat_tools/bildb; \
    opam config exec -- make

WORKDIR /home/opam/cbat_tools

