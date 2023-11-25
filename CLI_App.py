from rich.prompt import Prompt
from rich.console import Console
from rich.panel import Panel
import inquirer
from rich.traceback import install
from MeanReversion import MeanReversion_strategy

install(show_locals=True)

console = Console()

#CLI application
console.print((Panel("[bold magenta]This program produces trade signals based on a mean reversion trading stratedgy :chart_with_upwards_trend: (Please visit the Github for a more in depth explanation). Important to note that this program is [bold bright_red]NOT FINANCIAL ADIVICE [bold bright_red]:bangbang:[/bold magenta]", title="[bold light_green]Welcome[/bold light_green] :smiley:", subtitle=":star2: [bold yellow]Hope you like it[/bold yellow] :star2:")))
first_ticker = Prompt.ask("Enter the ticker symbol of the first stock (e.g. AAPL): ", default="AAPL")
secound_ticker = Prompt.ask("Enter the ticker symbol of the secound stock (e.g. MSFT): " , default="MSFT")

console.print(f"[bold magenta]:clock1: TimeFrame:[/bold magenta]")

console.print("    :rotating_light: [bold red]Important Information:[/bold red] [bold green]Start Year[/bold green] < [bold yellow]End Year[/bold yellow].[bold red] For best results keep time frame between 1-2 years[/bold red]")

Time_Frame_start, Time_Frame_end = Prompt.ask("      :diamond_shape_with_a_dot_inside: Start Year (e.g. [bold green]2013[/bold green])") , Prompt.ask("      :diamond_shape_with_a_dot_inside: End Year (e.g. [bold yellow]2014[/bold yellow])") 

options = [
    inquirer.List(
        "Coint",
        message="Do you want to test conintegration of this pair",
        choices=["Yes", "No <--(Recomendad for first try)"],
    ),
    inquirer.List(
        "spread?",
        message="Do you want to show the spread",
        choices=["Yes", "No"],
    ),
]

response = inquirer.prompt(options)

def user_reponse (choice, message):
    if (choice == "Yes"):
        console.print(f"{message}: :white_check_mark:[bold bright_green]{choice}[/bold bright_green]")
        return True
    else:
        #hard coded No instead of using choice so that I don't print (<--(Recomendad for first try))
        console.print(f"{message}: :X:[bold bright_red]No[/bold bright_red]")
        return False


cointegration = user_reponse (response["Coint"], "[bold magenta1]Cointegration[/bold magenta1] :chart_with_upwards_trend:")
show_spread = user_reponse(response["spread?"], "[bold orange_red1]Show Spread[/bold orange_red1] :bar_chart:")

start_year , end_year= (str(Time_Frame_start+"-01-01")), (str(Time_Frame_end)+"-01-01")

MeanReversion_strategy(
    first_ticker, secound_ticker, start_year, end_year, cointegration, show_spread
)