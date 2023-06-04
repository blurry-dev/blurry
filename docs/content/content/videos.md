+++
"@type" = "WebPage"
name = "Content: videos"
abstract = "Documentation for Blurry's video handling"
datePublished = 2023-06-04
+++

# Content: videos

Blurry handles videos a little differently from some other static site generators by overloading the regular Markdown image syntax to support videos, too.
Video files whose extensions are listed in the `VIDEO_EXTENSIONS` [setting](../configuration/settings.md) will be embedded using a [`<video>` embed element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video).

## Example

For example, this Markdown:

```markdown
![My Video](./videos/my-video.mp4)
```

Will result in this HTML:

```html
<video controls="" width="1920" height="1080">
    <source src="/videos/my-video.mp4" type="video/mp4">
</video>
```

See the width and height?
That helps guard against [cumulative layout shifts](https://web.dev/cls/), which can cause a poor page experience for visitors, especially on smaller devices, when content shifts down as more content finishes loading above it.

## Styling

Adding a bit of CSS can make a video responsive:

```css
video {
    max-width: 100%;
    height: auto;
}
```
