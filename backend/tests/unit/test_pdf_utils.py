import io
from datetime import datetime
from app import pdf_utils

def test_generate_pdf_minimal(tmp_path):
    # Fichiers temporaires
    out_pdf = tmp_path / "rapport.pdf"
    csv = tmp_path / "zoll.csv"

    # En-têtes attendues par pdf_utils (_read_csv_resilient / _sample_every_3_minutes)
    csv.write_text(
        "Heure (HH:MM),FC/FP (BPM),SpO2 (%),PNI (mm Hg) (Sys),PNI (mm Hg) (Dia)\n",
        encoding="utf-8"
    )

    # Appel réel suivant ta signature
    pdf_utils.generate_pdf(
        str(out_pdf),
        "Patient Test",
        datetime(2025, 1, 1),
        str(csv),
        patient=None
    )

    content = out_pdf.read_bytes()
    assert len(content) > 100
    assert content.startswith(b"%PDF")
