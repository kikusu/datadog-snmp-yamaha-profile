#!/bin/bash
cd `dirname $0`
cd src
wget http://www.rtpro.yamaha.co.jp/RT/docs/mib/yamaha-private-mib.tar.gz -O yamaha-private-mib.tar.gz
rm -rf yamaha-private-mib
tar xvf yamaha-private-mib.tar.gz
