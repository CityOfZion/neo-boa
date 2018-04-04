FROM ubuntu:16.04

RUN apt-get update && apt-get -y install python3-dev python3-pip

RUN pip3 install astor logzero coz-bytecode neo-boa

COPY compiler.py /compiler.py

CMD python3 compiler.py
