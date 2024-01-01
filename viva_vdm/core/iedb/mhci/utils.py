import subprocess
import tempfile

from viva_vdm.core.settings import AppConfig

app_config = AppConfig()


def run_mhci_prediction_process(method: str, allele: str, length: int, sequence: str):
    with tempfile.NamedTemporaryFile('w', delete=False) as f:
        f.write(sequence)

    process = subprocess.run(
        args=['src/predict_binding.py', method, allele, str(length), f.name],
        cwd=app_config.iedb_mhci_install_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    output = process.stdout
    errors = process.stderr

    return output, errors


def run_mhcii_prediction_process(method: str, allele: str, length: int, sequence: str):
    with tempfile.NamedTemporaryFile('w', delete=False) as f:
        f.write(sequence)

    process = subprocess.run(
        args=['./mhc_II_binding.py', method, allele, f.name, str(length)],
        cwd=app_config.iedb_mhcii_install_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    output = process.stdout
    errors = process.stderr

    return output, errors
