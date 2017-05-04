FROM debian:jessie


# Use fast mirrors
RUN echo "deb http://debian.mirror.neology.co.za/debian jessie main\n"\
         "deb http://security.debian.org/ jessie/updates main contrib non-free\n"\
         "deb http://debian.mirror.neology.co.za/debian jessie-updates main \n"> /etc/apt/sources.list

#libncurses5-dev \
#libncurses5-dev \
#libpq-dev \
#libreadline-dev \
#llvm \
#zlib1g-dev \
#odbcinst1debian2 \

# Install apt deps
RUN apt-get update && apt-get install -y  \
  curl \
  git \
  less \
  libbz2-dev \
  libpng12-dev \
  silversearcher-ag \
  htop \
  iotop \
  vim \
  wget \
  zsh \
  nodejs \
  build-essential
# install from nodesource using apt-get
# https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-an-ubuntu-14-04-server

# fix npm - not the latest version installed by apt-get

# ODBC
#COPY odbcinst.ini /etc/odbcinst.ini

# Non-root user set up
RUN useradd -Um -s /bin/zsh craig

# Zsh
USER root
WORKDIR /home/craig
COPY .zshrc .zshrc
RUN chown craig:craig .zshrc
RUN chsh -s /bin/zsh craig


# Vim
USER root
WORKDIR /home/craig
COPY .vimrc .vimrc
COPY solarized.vim .vim/colors/
RUN mkdir -p .vim/autoload .vim/bundle
RUN curl -LSso .vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim
RUN git clone https://github.com/rking/ag.vim .vim/bundle/ag
RUN chown -R craig:craig .vim


# Pyenv
# TODO: Checkout specific releases.
RUN curl -sL https://deb.nodesource.com/setup_6.x -o nodesource_setup.sh
USER root
RUN bash nodesource_setup.sh
RUN apt-get install nodejs
RUN npm install -g npm

WORKDIR /server
COPY server.py server.py

CMD python server.py
#CMD ./node_modules/.bin/webpack-dev-server -p --config ./webpack.production.config.js --host 0.0.0.0 --port 8080
