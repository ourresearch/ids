unsub-ids
=========

Command line tools for looking up various Unsub identifiers.

Why? 

- To help quickly find what users/institutions/etc. are linked to various package/scenario ids
- To get a JWT token to e.g., pop into a curl request for debugging purposes

## installation

In the `unsub-ids` directory, run `pip install .`


## Examples

### ids

```
ids
```

```
Usage: ids [OPTIONS] COMMAND [ARGS]...

  Lookup Unsub identifiers

Options:
  --help  Show this message and exit.

Commands:
  i  lookup a institution id
  p  lookup a package id
  s  lookup a scenario id
```

### token

```
tokens
```

```
Usage: tokens [OPTIONS] COMMAND [ARGS]...

  Get Unsub JWT Tokens

Options:
  --help  Show this message and exit.

Commands:
  e  get a JWT token by email address
```

To do a curl request with this:

```
curl https://unpaywall-jump-api.herokuapp.com/<some-route>?jwt=$(tokens e hello@world.org)
```
