FROM centos:centos7

ENV HOME /root
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/bin:$PATH
RUN yum update -y \
    && yum install -y which \
    && yum install -y gcc zlib-devel bzip2 bzip2-devel readline readline-devel sqlite sqlite-devel openssl openssl-devel git libffi-devel \
    && curl https://bootstrap.pypa.io/get-pip.py | python \
    && git clone https://github.com/pyenv/pyenv.git ~/.pyenv \
    && echo 'eval "$(pyenv init -)"' >> ~/.bashrc \
    && yum install -y libSM.x86_64 libXrender.x86_64 libXext.x86_64

WORKDIR $HOME

# Pythoon3.6
RUN pyenv install 3.6.10 \
    && pyenv rehash \
    && pyenv global 3.6.10
ENV PATH $PYENV_ROOT/versions/3.6.10/bin:$PATH

# TensorFlow install
RUN pip install --upgrade pip \
    && pip install astroid \
    && pip install pyqt5==5.12.0 \
    && pip install PyQtWebEngine==5.12
RUN pip install --ignore-installed --upgrade tensorflow==1.* ; exit 0

RUN pip uninstall -y numpy \
    && pip uninstall -y numpy \
    && pip install numpy

# Pipenv install
# export LC_ALL=en_US.UTF-8 # pipenvを動かすために必要
ENV LC_ALL en_US.UTF-8
ADD Pipfile $HOME/Pipfile
ADD Pipfile.lock $HOME/Pipfile.lock
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

# add to application
ADD ./src $HOME/src
ADD ./api $HOME/api
ADD ./img $HOME/img

WORKDIR $HOME/api

# CMD uvicorn main:app --host 0.0.0.0 --port $PORT --reload
CMD gunicorn -k uvicorn.workers.UvicornWorker -c $HOME/api/config/gunicorn_conf.py main:app