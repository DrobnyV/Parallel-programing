# Parallel Programming Simulation - Windows Edition

Tento projekt demonstruje základy paralelního programování v Pythonu pomocí vláken a multiprocessing. Nyní je zkompilován do spustitelného souboru pro Windows.

## Instalace

1. **Stáhněte si repozitář jako ZIP archiv:**
   - Stáhněte si release z https://github.com/DrobnyV/Parallel-programing.

2. **Závislosti:**
   - **Není třeba instalovat Python**, protože `.exe` soubor už obsahuje všechny potřebné knihovny.

## Spuštění

- Spusťte hlavní spustitelný soubor:

main.exe

Použití
Po spuštění aplikace se dostanete do interaktivního menu, kde můžete:

Spustit jednotlivé simulace (run).
Zobrazit kód simulací (show).
Upravit konfiguraci (config).
Ukončit aplikaci (exit).

Konfigurace
Můžete upravit konfiguraci v souboru config.json nebo přímo v aplikaci pomocí příkazu config. Konfigurační volby zahrnují:

message_count: Počet zpráv v simulaci Messages.
delay_between_messages: Zpoždění mezi operacemi.
max_threads: Maximální počet vláken pro simulaci SharedMemory.
use_colors: Zapnutí/vypnutí barevného výstupu.
num_threads, num_processes: Počet vláken nebo procesů pro různé simulace.
array_size, num_arrays: Nastavení pro simulaci s polemi.
words_to_count, file_prefix: Nastavení pro WordCount simulaci.

Testování
Testování je stále možné provádět na Python verzi, ale .exe soubor testy neobsahuje. Pro spuštění testů na Python verzi musíte stáhnout celý repositář jako zip extrahovat a potom nainstalovat numpy:
python -m unittest discover test

Poznámky
.exe soubor byl vytvořen pomocí PyInstaller, což znamená, že obsahuje všechny potřebné knihovny pro běh aplikace na Windows bez nutnosti instalace Pythonu.
Pro optimalizaci, může být nutné znovu vytvořit .exe pokud dojde ke změnám v kódu nebo konfiguraci.
