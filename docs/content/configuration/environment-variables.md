+++
"@type" = "WebPage"
name = "Configuration: environment variables"
abstract = "Documentation for Blurry's settings configuration using environment variables"
datePublished = 2023-04-09
dateModified = 2024-01-03
+++

# Configuration: environment variables

Blurry settings can be overridden using environment variables.

For the setting you'd like to override, simply prefix the setting name with `BLURRY_`.
(This prefix can be customized in your [`blurry.toml` file](./blurry.toml.md)).

## Example

To build your site for a different domain, for instance, set the `BLURRY_DOMAIN` environment variable:

```bash
BLURRY_DOMAIN=differentdomain.com blurry build
```
