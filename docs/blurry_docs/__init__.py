from selectolax.lexbor import parse_fragment


def body_to_cards(html: str):
    """Creates grids of h3s and their contents using <article> tags"""
    tree = parse_fragment(html)
    is_in_card = False
    html = ""

    for index, node in enumerate(tree):
        if node.tag == "h2":
            if is_in_card:
                html += "</article></div>"
                is_in_card = False
            # The next index is a text node (whitespace), so look two ahead
            if tree[index + 2].tag == "h3":
                html += node.html or ""
                html += '<div class="flex-grid">'
                continue

        if node.tag == "h3":
            if is_in_card:
                html += "</article>"
            html += "<article>"
            is_in_card = True

        html += node.html or ""

        # This assumes that the Markdown content ends with a card
        if node == tree[-1]:
            html += "</article></div>"

    return html
