FROM centos:centos7

ENV HOME /root
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/bin:$PATH
RUN yum update -y \
    && yum install -y which \
    && yum install -y gcc zlib-devel bzip2 bzip2-devel readline readline-devel sqlite sqlite-devel openssl openssl-devel git libffi-devel \
    && curl https://bootstrap.pypa.io/get-pip.py | python \
    && git clone https://github.com/pyenv/pyenv.git ~/.pyenv \
    && echo 'eval "$(pyenv init -)"' >> ~/.bashrc

WORKDIR $HOME

# Anaconda install
RUN pyenv install anaconda3-4.3.0 \
    && pyenv rehash \
    && pyenv global anaconda3-4.3.0 \
    && echo 'export PATH="$PYENV_ROOT/versions/anaconda3-4.3.0/bin/:$PATH"' >> ~/.bashrc \
    && source ~/.bashrc

# TensorFlow install
ENV PATH $PYENV_ROOT/versions/anaconda3-4.3.0/bin:$PATH
ENV TF_BINARY_URL https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.0.1-cp36-cp36m-linux_x86_64.whl
RUN conda update -y conda
# RUN  conda create -n tensorflow python=3.6.0 \
#     && source activate tensorflow \
#     && pip install --upgrade pip \
#     && pip install --ignore-installed --upgrade $TF_BINARY_URL

RUN pip install --upgrade pip \
    && pip install astroid \
    && pip install pyqt5==5.12.0 \
    && pip install PyQtWebEngine==5.12
RUN pip install --ignore-installed --upgrade tensorflow==1.* ; exit 0

RUN pip uninstall -y numpy \
    && pip uninstall -y numpy \
    && pip install numpy

# Pipenv install
# ADD Pipfile $HOME/Pipfile
# ADD Pipfile.lock $HOME/Pipfile.lock
# RUN pip install --upgrade pip \
#     && pip install pipenv \
#     && pipenv install --system

# add to application
ADD ./src $HOME/src
ADD ./img $HOME/img

# CMD uvicorn app:app --host 0.0.0.0 --port $PORT --reload


