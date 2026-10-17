ARG VER=1.9.14

FROM --platform=$BUILDPLATFORM golang:alpine AS build
ARG VER
ARG TARGETARCH
RUN apk add --no-cache git python3
WORKDIR /src
RUN git clone --depth 1 --branch v${VER} https://github.com/AlexxIT/go2rtc.git .
COPY patch.py /patch.py
RUN python3 /patch.py
RUN CGO_ENABLED=0 GOOS=linux GOARCH=${TARGETARCH} go build -ldflags "-s -w" -trimpath -o /go2rtc

FROM alexxit/go2rtc:${VER}
COPY --from=build /go2rtc /usr/local/bin/go2rtc
