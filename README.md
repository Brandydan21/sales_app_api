Run db:
'''podman run --name postgres_sales -e POSTGRES_USER=devuser -e POSTGRES_PASSWORD=password -p 5432:5432 -v $PWD/database:/var/lib/postgresql/data -d postgres:17.3'''