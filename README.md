# craigbot

Bot for finding apartments on Craigslist.

## Installation

Start by creating a [Slack token](https://api.slack.com/docs/oauth-test-tokens). Put it in a new file, `.docker/env`. See `.docker/env.example` for an example. Other environment variables can be placed in this file to override default settings.

With Docker installed and running, start the bot:

```
$ make
```

If the image doesn't exist locally, Docker will pull it from [Docker Hub](https://hub.docker.com/r/rlucioni/craigbot/), create a container, and start it.

Tail a running container's logs:

```
$ make logs
```

Open a shell on a running container:

```
$ make shell
```

For information about additional Make targets:

```
$ make help
```

To deploy to DigitalOcean, see [this guide](https://docs.docker.com/machine/examples/ocean). To create a new Droplet, put your DigitalOcean access token in `~/.digitalocean-access-token`, then run:

```
$ make create
```

To stop and remove the Droplet:

```
$ make kill
```

## Development

Run quality checks:

```
$ make quality
```

Build a new image:

```
$ make image
```

Push it to Docker Hub:

```
$ make push
```
