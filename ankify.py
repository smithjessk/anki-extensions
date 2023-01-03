#!/Users/jesssmith/opt/anaconda3/bin/python3


if __name__ == "__main__":
    import argparse

    import ankify_library_functions

    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="path to file to ankify")
    parser.add_argument("--debug", help="print debug info", action="store_true")
    args = parser.parse_args()
    filepath = args.filepath
    with open(filepath, "r") as file:
        lines_as_list = file.readlines()
        cleaned_lines = ankify_library_functions.clean_input_lines(lines_as_list)
        print(
            ankify_library_functions.ankify_via_openai(
                cleaned_lines, is_debug_mode=args.debug
            )
        )
