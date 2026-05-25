import re
from typing import Tuple

# Regex oficial SEP para CURP
CURP_REGEX = re.compile(
    r'^[A-Z]{1}[AEIOU]{1}[A-Z]{2}'    # 4 iniciales
    r'\d{2}(0[1-9]|1[0-2])'            # año y mes de nacimiento
    r'(0[1-9]|[12]\d|3[01])'           # día de nacimiento
    r'[HM]{1}'                          # sexo
    r'(AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)'  # estados
    r'[B-DF-HJ-NP-TV-Z]{3}'            # consonantes
    r'[A-Z0-9]{2}$',                   # dígito(s) verificador
    re.IGNORECASE
)

def validate_curp(curp: str) -> Tuple[bool, str]:
    """
    Valida una CURP mexicana.
    Returns:
        (True, "")          si es válida
        (False, "mensaje")  si es inválida, con descripción del error
    """
    if not curp:
        return False, "La CURP no puede estar vacía."
    curp = curp.upper().strip()
    if len(curp) != 18:
        return False, f"La CURP debe tener 18 caracteres (tiene {len(curp)})."
    if not CURP_REGEX.match(curp):
        return False, "El formato de la CURP no es válido. Ejemplo: PETD800714HCLRNV02"
    return True, ""
