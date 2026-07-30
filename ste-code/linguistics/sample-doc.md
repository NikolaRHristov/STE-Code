# Sample Document — STE-Code Linguistic Linter Demo

This file demonstrates violations the linguistic linter catches.

## Build and Deploy

The build takes five minutes. After the build, the deploy starts.
The deploy takes about three minutes in production.

The API is fast and handles high load well. It will retry failed
requests. The server should respond in under 100 ms in many cases.

Use the config to set the timeout. The config file is in the root
directory. The service listens on port 8080. The service endpoint
requires a token for authentication.

## Cache and Log

The cache stores results from database queries. It uses an LRU
eviction strategy. The log shows all incoming requests. It rotates
every hour.

This component is not uncommon to fail under significant load.
Approximately 5% of requests time out, but this is rarely a problem.

The deployment uses Kubernetes. The deployment artifact is a
Docker image. The token expires after one hour. The parser
consumes the token and produces an AST.
