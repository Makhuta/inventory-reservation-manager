from django import template

register = template.Library()

@register.filter
def mysplit(string:str, args:str="_"):
    try:
        parts = args.split(",")
        sep, maxsplit = (parts[0] if parts else "_", int(parts[1]) if len(parts) > 1 and parts[1] != "None" else None)

        print(sep, maxsplit)

        if maxsplit is None or maxsplit == 0:
            return string.split(sep)
        if maxsplit < 0:
            return string.rsplit(sep, abs(maxsplit))
        return string.plit(sep, abs(maxsplit))

    except Exception as e:
        print(f'Error: {e}')
        return string