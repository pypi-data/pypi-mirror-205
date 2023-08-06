import click
import pandas as pd

@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--verbose', '-v', is_flag=True, help='list details')
def main(filename, verbose):
	if verbose:
		click.echo('in verbose mode')
	df = pd.read_csv(filename)
	click.echo(df.iloc[[0]])

if __name__ == '__main__':
	main()
