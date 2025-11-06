def escape_text_from_admin_panel(text: str) -> str:
    return (
        text
        .replace('<p>', '\n\n')
        .replace('</p>', '')
        .replace('<br>', '\n')
        .strip('\n')
    )
