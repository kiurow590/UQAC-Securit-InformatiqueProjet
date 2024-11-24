FROM alpine:latest

# Install the necessary packages including musl-dev and procps
RUN apk add --no-cache vim curl nano git gcc musl-dev linux-headers procps

COPY CMakeLists.txt /app/CMakeLists.txt
COPY main.c /app/main.c
COPY modifier.c /app/modifier.c
COPY /Test /app/Test
WORKDIR /app
RUN gcc -o main main.c
RUN gcc -o modifier modifier.c

CMD ["/bin/sh"]
