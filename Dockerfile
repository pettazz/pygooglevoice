FROM centos:7

MAINTAINER https://github.com/pettazz/pygooglevoice

ARG user_home=/home/pygooglevoice
ARG user_name=pygooglevoice
ARG user_uid=808
ARG user_group=pygooglevoice
ARG user_gid=808

RUN /sbin/groupadd -g "${user_gid:-unset}" "${user_group:-unset}"
RUN /sbin/useradd -c "user" -d "${user_home:-unset}" -g "${user_gid:-unset}" -m "${user_name:-unset}"

RUN yum --noplugins install -y \
      python \
      python-setuptools \
      && yum clean all

RUN mkdir -p "${user_home:-unset}"/pygooglevoice

COPY . "${user_home:-unset}"/pygooglevoice

WORKDIR "${user_home:-unset}"/pygooglevoice

RUN python setup.py install

VOLUME "${user_home:-unset}"
USER "${user_name:-unset}"
