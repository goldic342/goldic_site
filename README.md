<p align="center">
  <a href="https://goldic.xyz"><img src="images/demo.png" alt="Goldic"></a>
</p>
<p align="center">
    Personal lightweight website with markdown blog&nbsp;
</p>

# Migration
This repository has been migrated to [codeberg](https://codeberg.org/goldic/goldic_site)_

## Features

- Works entirely without JavaScript.
- Markdown based blog
- SEO optimizations

## Setup

Clone the repo

```bash
git clone git@github.com:goldic342/goldic_site.git
```

Generate password hash and salt

```bash
python src/setup.py
```

Create `data` directory and `.env`

```bash
cp .example.env .env
mkdir -p data
```

Build the docker image

```bash
docker build -t goldic_site .
```

Run

```bash
docker run -p 8000:8000 -v ./data:/app/data goldic_site
```

### Docker compose

Uses an external Docker network by default.
For `localhost` deployment, disable networks and enable port mapping.
