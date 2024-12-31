from selectolax.lexbor import LexborNode, create_tag, parse_fragment


def body_to_cards(html: str):
    tree = parse_fragment(html)
    elements_for_sections: list[list[LexborNode]] = []
    current_section_index = 0
    html_before_card_elements = ""

    for node in tree:
        # Skip newlines or text out of tags
        if node.tag == "-text":
            continue

        # Split remaining elements by h2s
        if node.tag == "h2":
            try:
                len(elements_for_sections[current_section_index])
                current_section_index += 1
                elements_for_sections.append([node])
                continue
            except IndexError:
                elements_for_sections.append([node])
        else:
            # Sections will be empty until we start gathering elements for cards, so
            # we'll get an IndexError for pre-card elements
            try:
                elements_for_sections[current_section_index].append((node))
            except IndexError:
                html_before_card_elements += node.html or ""

    # Build cards
    cards_container = create_tag("div")
    cards_container.attrs["class"] = "flex-grid"

    for elements in elements_for_sections:
        article = create_tag("article")
        section = create_tag("section")

        for element in elements:
            if element.tag == "h2":
                header = create_tag("header")
                header.insert_child(element.text())
                article.insert_child(header)
                continue
            if elements[-1] == element:
                article.insert_child(section)
                footer = create_tag("footer")
                a = element.child
                if a:
                    a.attrs["class"] = "right-arrow"
                    a.attrs["role"] = "button"
                    footer.insert_child(a)
                article.insert_child(footer)
                continue
            section.insert_child(element)
        cards_container.insert_child(article)

    return html_before_card_elements + (cards_container.html or "")
