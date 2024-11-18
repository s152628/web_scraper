import click


@click.command()
@click.argument("first_amount", type=float)
@click.option("--rate", type=float, default=1.0)
def main(first_amount, rate):
    result = first_amount * rate
    print(round(result, 2))


if __name__ == "__main__":
    main()
