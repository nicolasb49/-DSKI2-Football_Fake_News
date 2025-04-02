import pandas as pd
from spellchecker import SpellChecker
import os

def load_csv(file_path, text_column):
    df = pd.read_csv(file_path)
    if text_column not in df.columns:
        raise ValueError(f"Spalte '{text_column}' nicht in CSV gefunden.")
    return df

def check_spelling(df, text_column):
    spell = SpellChecker(language='en')
    df['misspelled_words'] = df[text_column].astype(str).apply(lambda x: list(spell.unknown(x.split())))
    df['has_errors'] = df['misspelled_words'].apply(lambda x: 1 if x else 0)
    return df

def save_results(df, output_path):
    df.to_csv(output_path, index=False)
    print(f"Ergebnisse gespeichert unter: {output_path}")

def analyze_dataset(input_file, output_file, text_column):
    df = load_csv(input_file, text_column)
    df_checked = check_spelling(df, text_column)
    save_results(df_checked, output_file)

    total_with_errors = df_checked['has_errors'].sum()
    total_without_errors = len(df_checked) - total_with_errors

    return total_with_errors, total_without_errors

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    text_column = "tweet"

    fake_input = os.path.join(base_dir, "assets", "fake.csv")
    fake_output = os.path.join(base_dir, "assets", "output_fake.csv")
    fake_errors, fake_no_errors = analyze_dataset(fake_input, fake_output, text_column)

    real_input = os.path.join(base_dir, "assets", "real.csv")
    real_output = os.path.join(base_dir, "assets", "output_real.csv")
    real_errors, real_no_errors = analyze_dataset(real_input, real_output, text_column)

    print("\n--- Zusammenfassung ---")
    print(f"Fake News - Gesamtanzahl mit Fehlern: {fake_errors}")
    print(f"Fake News - Gesamtanzahl ohne Fehler: {fake_no_errors}")
    print(f"Real News - Gesamtanzahl mit Fehlern: {real_errors}")
    print(f"Real News - Gesamtanzahl ohne Fehler: {real_no_errors}")