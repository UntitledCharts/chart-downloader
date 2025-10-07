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
        return "\033[39;49m"

    @staticmethod
    def apply_foreground(text, color_code):
        return f"{AnsiColors.fg(color_code)}{text}{AnsiColors.reset()}"

    @staticmethod
    def apply_background(text, color_code):
        return f"{AnsiColors.bg(color_code)}{text}{AnsiColors.reset()}"

    @staticmethod
    def apply(text, fg_color_code, bg_color_code):
        return f"{AnsiColors.fg(fg_color_code)}{AnsiColors.bg(bg_color_code)}{text}{AnsiColors.reset()}"


import colorama

colorama.just_fix_windows_console()

from locales.supported import SUPPORTED_LOCALES
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
    case_sensitive_choice_names: bool = False,
) -> str | None:
    def check_answer(
        ans: str,
        expected_ans: list,
        choice_names: list,
        case_sensitive_choice_names: bool,
    ):
        if ans in expected_ans:
            return True
        if case_sensitive_choice_names:
            return ans in choice_names
        else:
            return ans.lower() in [choice.lower() for choice in choice_names]

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
    print(
        AnsiColors.apply_foreground(
            locale.not_required if not required else locale.required, AnsiColors.YELLOW
        )
    )
    answer = input("> " + AnsiColors.fg(AnsiColors.YELLOW))
    print(AnsiColors.reset(), end=None)
    if answer.strip() == "" and not required:
        return None
    while not check_answer(
        answer, expected_answers, expected_answer_names, case_sensitive_choice_names
    ):
        print("-" * 50, "\n")
        print(AnsiColors.apply(locale.invalid_choice, AnsiColors.RED, AnsiColors.BLACK))
        print(AnsiColors.apply_foreground(prompt, AnsiColors.CYAN))
        for i, choice in enumerate(expected_answers):
            if expected_answer_names:
                print(
                    f"- {expected_answer_names[i]}",
                    AnsiColors.apply_foreground(f"({choice})", AnsiColors.GREEN),
                )
            else:
                print(AnsiColors.apply_foreground(f"- {choice}", AnsiColors.GREEN))
        print(
            AnsiColors.apply_foreground(
                locale.not_required if not required else locale.required,
                AnsiColors.YELLOW,
            )
        )
        answer = input("> " + AnsiColors.fg(AnsiColors.YELLOW))
        if answer.strip() == "" and not required:
            return None
        print(AnsiColors.reset(), end=None)
    if (answer in expected_answer_names) and case_sensitive_choice_names:
        answer_index = expected_answer_names.index(answer)
        return expected_answers[answer_index]
    elif (
        answer.lower() in [choice.lower() for choice in expected_answer_names]
    ) and not case_sensitive_choice_names:
        answer_index = [choice.lower() for choice in expected_answer_names].index(
            answer.lower()
        )
    return answer


if __name__ == "__main__":
    try:
        from downloaders.supported import SUPPORTED_DOWNLOADERS

        def get_param(data: dict, locale_keys: dict):
            required = data.get("required", False)
            choices = data.get("choices", None)
            choices_names = data.get("choices_names", None)
            prompt = data["prompt"]
            invalid = data.get("invalid", None)
            validation = data.get("validate", [])
            case_sensitive_choice_names = data.get("case_sensitive_choice_names", False)
            choices_names_literal = data.get("choices_names_literal", False)

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
                        [
                            apply_locale_keys(choice, locale_keys)
                            for choice in choices_names
                        ]
                        if choices_names and not choices_names_literal
                        else (
                            choices_names
                            if choices_names_literal and choices_names
                            else []
                        )
                    ),
                    required=required,
                    case_sensitive_choice_names=case_sensitive_choice_names,
                )
            print(
                AnsiColors.apply_foreground(
                    apply_locale_keys(prompt, locale_keys), AnsiColors.CYAN
                )
            )
            print(
                AnsiColors.apply_foreground(
                    locale.not_required if not required else locale.required,
                    AnsiColors.YELLOW,
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
                print(
                    AnsiColors.apply_foreground(
                        locale.not_required if not required else locale.required,
                        AnsiColors.YELLOW,
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
        out_path = Path("out")
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
        input()
    except Exception as e:
        print(AnsiColors.reset())
        raise e
    except KeyboardInterrupt as e:
        print(AnsiColors.reset())
        raise e
