# Simple Search Engine

This is a simple version of a search engine.  Users can enter
a url and the search engine will index all the words on that
page and follow outgoing links and index those pages as well.
Max depth is limited to 3.  The search function will return
all pages that have a particular word as well as the number of
occurrences.

I built this mainly as an exercise to understand how we can
deploy services using Docker, Flask, and React.

## Setting up the services

Make sure Docker is installed on your local machine and run the
following:

```
export REACT_APP_BACKEND_URL=http:://localhost:5000
docker-compose -f docker-compose-dev.yml up -d --build
```

This will expose the web client app on port 3007 and the
 backend on port 5000.
 
 Not intended for production.