FROM xxxx
RUN rm -rf /export/*
RUN mkdir -p /export/openapi-test
COPY . /export/openapi-test
WORKDIR /export/openapi-test
CMD ["/bin/bash"]