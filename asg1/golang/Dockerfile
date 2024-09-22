FROM golang:1.22.2 AS builder

WORKDIR /app

COPY go.mod ./

COPY main.go .

RUN go build -o hello-app

FROM alpine:latest

WORKDIR /app

COPY --from=builder /app/hello-app .

CMD ["./hello-app"]
