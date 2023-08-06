def save_macro_file(macros, filepath):
    with open(filepath, "w") as f:
        for macro in macros:
            f.write("\n".join(macro.echo()))
