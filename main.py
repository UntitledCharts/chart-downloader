class AnsiColors:
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    RESET = 39

    @staticmethod
    def fg(color_code):
        return f"\033[{color_code}m"

    @staticmethod
    def bg(color_code):
        return f"\033[{color_code + 10}m"

    @staticmethod
    def reset():
        return f"\033[39m"

    @staticmethod
    def apply_foreground(text, color_code):
        return f"{AnsiColors.fg(color_code)}{text}{AnsiColors.reset()}"

    @staticmethod
    def apply_background(text, color_code):
        return f"{AnsiColors.bg(color_code)}{text}{AnsiColors.reset()}"

    @staticmethod
    def apply(text, fg_color_code, bg_color_code):
        return f"{AnsiColors.fg(fg_color_code)}{AnsiColors.bg(bg_color_code)}{text}{AnsiColors.reset()}"


if __name__ == "__main__":
    try:
        from locales.supported import SUPPORTED_LOCALES
        from downloaders.supported import SUPPORTED_DOWNLOADERS
        from locales import en
        from pathlib import Path

        locale = en

        def apply_locale_keys(loc: str | list, locale_keys: dict) -> str:
            if type(loc) == str:
                return eval(f"locale.{locale_keys[loc]}")
            else:
                loc_string = eval(f"locale.{locale_keys[loc[0]]}")
                for i, key in enumerate(loc):
                    if i == 0:
                        continue
                    loc_string = loc_string.format(eval(f"locale.{locale_keys[key]}"))
                return loc_string

        def ask(
            prompt: str,
            expected_answers: list,
            expected_answer_names: list = [],
            required: bool = True,
        ) -> str | None:
            expected_answers = list(expected_answers)
            expected_answer_names = list(expected_answer_names)
            if expected_answer_names:
                if len(expected_answers) != len(expected_answer_names):
                    raise ValueError(
                        "Expected answer names list must be in same order and length as expected answers."
                    )
            print(AnsiColors.apply_foreground(prompt, AnsiColors.CYAN))
            for i, choice in enumerate(expected_answers):
                if expected_answer_names:
                    print(
                        f"- {expected_answer_names[i]}",
                        AnsiColors.apply_foreground(f"({choice})", AnsiColors.GREEN),
                    )
                else:
                    print(AnsiColors.apply_foreground(f"- {choice}", AnsiColors.GREEN))
            answer = input("> " + AnsiColors.fg(AnsiColors.YELLOW))
            print(AnsiColors.reset(), end=None)
            if answer.strip() == "" and not required:
                return None
            while answer not in (expected_answers + expected_answer_names):
                print("-" * 50, "\n")
                print(
                    AnsiColors.apply(
                        locale.invalid_choice, AnsiColors.RED, AnsiColors.BLACK
                    )
                )
                print(AnsiColors.apply_foreground(prompt, AnsiColors.CYAN))
                for i, choice in enumerate(expected_answers):
                    if expected_answer_names:
                        print(
                            f"- {expected_answer_names[i]}",
                            AnsiColors.apply_foreground(
                                f"({choice})", AnsiColors.GREEN
                            ),
                        )
                    else:
                        print(
                            AnsiColors.apply_foreground(f"- {choice}", AnsiColors.GREEN)
                        )
                answer = input("> " + AnsiColors.fg(AnsiColors.YELLOW))
                if answer.strip() == "" and not required:
                    return None
                print(AnsiColors.reset(), end=None)
            if answer in expected_answer_names:
                answer_index = expected_answer_names.index(answer)
                return expected_answers[answer_index]
            return answer

        def get_param(data: dict, locale_keys: dict):
            required = data.get("required", False)
            choices = data.get("choices", None)
            choices_names = data.get("choices_names", None)
            prompt = data["prompt"]
            invalid = data.get("invalid", None)
            validation = data.get("validate", [])

            def validate(arg: str, validation: list) -> bool:
                try:
                    for code in validation:
                        is_valid = eval(code)
                        if not is_valid:
                            return is_valid
                except:
                    return False
                return True

            if choices:
                return ask(
                    apply_locale_keys(prompt, locale_keys),
                    choices,
                    (
                        [apply_locale_keys(choice) for choice in choices_names]
                        if choices_names
                        else []
                    ),
                    required=required,
                )
            print(
                AnsiColors.apply_foreground(
                    apply_locale_keys(prompt, locale_keys), AnsiColors.CYAN
                )
            )
            answer = input("> " + AnsiColors.fg(AnsiColors.YELLOW))
            print(AnsiColors.reset(), end=None)
            if answer.strip() == "" and not required:
                return None
            while not validate(answer, validation):
                print("-" * 50, "\n")
                print(
                    AnsiColors.apply(
                        (
                            apply_locale_keys(invalid, locale_keys)
                            if invalid
                            else locale.invalid_answer
                        ),
                        AnsiColors.RED,
                        AnsiColors.BLACK,
                    )
                )
                print(
                    AnsiColors.apply_foreground(
                        apply_locale_keys(prompt, locale_keys), AnsiColors.CYAN
                    )
                )
                answer = input("> " + AnsiColors.fg(AnsiColors.YELLOW))
                print(AnsiColors.reset(), end=None)
                if answer.strip() == "" and not required:
                    return None
            return answer

        locale_answer = ask(
            "What language do you want to use?",
            SUPPORTED_LOCALES.keys(),
            [l.name for l in SUPPORTED_LOCALES.values()],
        )
        locale: en = SUPPORTED_LOCALES[locale_answer]
        # haha use en for typehinting

        server_answer = ask(
            locale.what_server,
            SUPPORTED_DOWNLOADERS.keys(),
            [eval(f"locale.{d[2]['name']}") for d in SUPPORTED_DOWNLOADERS.values()],
        )
        exporter, arguments, locale_keys = (
            SUPPORTED_DOWNLOADERS[server_answer][0],
            SUPPORTED_DOWNLOADERS[server_answer][1],
            SUPPORTED_DOWNLOADERS[server_answer][2],
        )
        finished_arguments = {}
        for param, data in arguments.items():
            finished_arguments[param] = get_param(data, locale_keys)
        out_path = Path("out") / server_answer
        try:
            resp = exporter(locale, out_path, **finished_arguments)
            if resp == True:
                print(AnsiColors.apply_foreground(locale.done, AnsiColors.GREEN))
            else:
                print(AnsiColors.apply(resp, AnsiColors.RED, AnsiColors.BLACK))
        except Exception as e:
            print(
                AnsiColors.apply(locale.unknown_error, AnsiColors.RED, AnsiColors.BLACK)
            )
            raise e
    except Exception as e:
        print(AnsiColors.reset())
        raise e
    except KeyboardInterrupt as e:
        print(AnsiColors.reset())
        raise e
