FROM ubuntu

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
 build-essential \
 curl \
 python3 \
 python3-setuptools \
 python3-dev \
 zlib1g-dev \
 libbz2-dev \
 libcurl4-openssl-dev \
 && rm -rf /var/lib/apt/lists/*

RUN curl -O https://research.wand.net.nz/software/wandio/wandio-4.0.0.tar.gz \
 && tar zxf wandio-4.0.0.tar.gz \
 && cd wandio-4.0.0/ \
 && ./configure \
 && make \
 && make install \
 && ldconfig

RUN curl -O http://bgpstream.caida.org/bundles/caidabgpstreamwebhomepage/dists/bgpstream-1.2.1.tar.gz \
 && tar zxf bgpstream-1.2.1.tar.gz \
 && cd bgpstream-1.2.1/ \
 && ./configure \
 && make \
 && make install \
 && ldconfig

COPY bgpwatch.py bgpwatch.py
COPY setup.py setup.py
RUN python3 setup.py install

ENTRYPOINT ["bgpwatch"]
