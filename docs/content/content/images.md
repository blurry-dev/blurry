+++
"@type" = "WebPage"
name = "Content: images"
abstract = "Documentation for Blurry's image handling"
datePublished = 2023-04-09
+++

# Content: images

Image handling is one of Blurry's strengths, and under the hood, Blurry doesn't sleep on image processing by making good use of [Pillow](https://pillow.readthedocs.io/en/stable/).

## Blurry image handling improvements

### Absolute paths

Blurry converts relative paths in Markdown to absolute paths in the build folder.
This enables autocomplete in code editors, which makes for a pleasant writing experience.

### `srcset` and `sizes`

Blurry generates images of various sizes, specified by the `IMAGE_WIDTHS` and `THUMBNAIL_WIDTH` [settings](../configuration/settings.md).
These enable [responsive images](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images), using an appropriately sized image for each device.

This improves page speed by ensuring that devices aren't loading larger images than they can display.

### AVIF

Rather than rendering images as plain `<img>` elements, Blurry uses [the `<picture>` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture) to support [AVIF](https://en.wikipedia.org/wiki/AVIF), while providing a fallback for browsers that do not yet support AVIF.

Blurry automatically generates AVIF versions of your images, including the resized images mentioned above.

This improves page speed because AVIF provides excellent image quality at smaller file sizes than other image codecs.

### Width & height

Blurry grabs the original image's width and height and includes those values in their corresponding HTML attributes.
This tells the browser the image's aspect ratio, so there is enough vertical for the image in the browser DOM.

This protects against layout shifts, which are disruptive for website visitors, especially on mobile devices.

For more information, see [the Lighthouse documentation on image aspect ratios](https://developer.chrome.com/docs/lighthouse/best-practices/image-aspect-ratio/).

### Lazy loading

Blurry adds lazy loading (`loading="lazy"`) to all images in body content.

This provides a page speed boost by waiting to load most images on a page until they're needed.

## Example

Given the following Markdown syntax for an image with dimensions of 2160x1620 and with a `MAXIMUM_IMAGE_WIDTH` [setting](../configuration/settings.md) of 750px:

```markdown
![Screenshot of Black's playground](./images/black-playground.png)
```

standard Markdown processing might output:

```html
<img alt="Screenshot of Black's playground" src="./images/black-playground.png">
```

When configured with a maximum image width of 750px, Blurry's image plugin, by contrast, outputs:

```html
<figure>
    <picture>
        <source srcset="/images/black-playground-285.avif 285w, /images/black-playground-360.avif 360w, /images/black-playground-640.avif 640w, /images/black-playground-750.avif 750w"
            sizes="(max-width: 285px) 285px, (max-width: 360px) 360px, (max-width: 640px) 640px, 750px">
        <img alt="Screenshot of Black's playground"
            loading="lazy"
            src="/images/black-playground.png"
            sizes="(max-width: 285px) 285px, (max-width: 360px) 360px, (max-width: 640px) 640px, 750px"
            srcset="/images/black-playground-285.png 285w, /images/black-playground-360.png 360w, /images/black-playground-640.png 640w, /images/black-playground-750.png 750w"
            width="2160"
            height="1620">
    </picture>
</figure>
```
