import click


@click.command()
@click.argument("type")
@click.argument("first_number", type=int)
@click.argument("second_number", type=int)
def main(type, first_number, second_number):
    if type == "add":
        result = first_number + second_number
    elif type == "sub":
        result = first_number - second_number
    elif type == "mul":
        result = first_number * second_number
    elif type == "div":
        result = first_number / second_number
    else:
        result = "Invalid type"

    print(result)


if __name__ == "__main__":
    main()
