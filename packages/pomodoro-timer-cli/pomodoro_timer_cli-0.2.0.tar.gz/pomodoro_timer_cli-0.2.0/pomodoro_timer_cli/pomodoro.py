import time
import typer
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
import miniaudio


def play_sound_effect():
    duration = miniaudio.wav_get_file_info("complete.wav").duration
    stream = miniaudio.stream_file("complete.wav")
    with miniaudio.PlaybackDevice() as device:
        device.start(stream)
        time.sleep(duration)

def pomodoro(
    pomodoro: int = typer.Option(4, "--pomodoro", "-p", help="Numbers of pomodoros"),
    focus_min: int = typer.Option(25, "--focus", "-f", help="Numbers of minutes for focus"),
    break_min: int = typer.Option(5, "--break", "-b", help="Numbers of minutes for break"),
):
    with Progress(SpinnerColumn(),TextColumn("[progress.description]{task.description}"),BarColumn(),TimeElapsedColumn()) as progress:
        for ith in range(1, pomodoro+1):
            focus = progress.add_task(f"{ith}. Focus", total=60*focus_min)
            while not progress.finished:
                time.sleep(1)
                progress.update(focus, advance=10)
            play_sound_effect()
            _break = progress.add_task(f"{ith}. Break", total=60*break_min)
            while not progress.finished:
                time.sleep(1)
                progress.update(_break, advance=1)
            play_sound_effect()
    print("WELL DONE! Take a long break. :party_popper:")

def cli():
    typer.run(pomodoro)

if __name__ == "__main__":
    cli()
