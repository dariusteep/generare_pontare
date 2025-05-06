# TODO: input the month and year via glider online (gradio or streamlit) and host this on huggingface

# Generare Pontaj

Acest proiect generează automat pontaje lunare în formatele CSV, Excel și PDF, folosind fonturi compatibile cu diacriticele românești.

## Cerințe

- Python 3.8 sau o versiune mai nouă
- [pip](https://pip.pypa.io/en/stable/installation/)

## Instalare

1. Clonează acest repository sau descarcă fișierele proiectului.
2. Instalează dependențele necesare:

    ```sh
    pip install -r requirements.txt
    ```

## Fonturi

Fonturile DejaVu Sans sunt incluse în directorul `fonts/dejavu-sans/`. Nu șterge acest director, deoarece este necesar pentru generarea PDF-urilor cu diacritice.

## Utilizare

Pentru a genera pontajul pentru o anumită lună și an, rulează scriptul principal:

```sh
python generare_pontare.py
```

Poți modifica luna și anul în fișierul [`generare_pontare.py`](generare_pontare.py), la finalul fișierului, în linia:

```python main(4, 2025)
```

Înlocuiește `4` și `2025` cu luna și anul dorite.

## Output

Vor fi generate următoarele fișiere:

- `pontaj_MM_YYYY.csv`
- `pontaj_MM_YYYY.xlsx`
- `pontaj_MM_YYYY.pdf`
