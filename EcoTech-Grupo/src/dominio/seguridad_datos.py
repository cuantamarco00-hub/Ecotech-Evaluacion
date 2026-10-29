import hashlib

class SeguridadDatos:

    def __init__(self, nivel_seguridad="medio"):
        self.nivel_seguridad = nivel_seguridad

    def cifrar_datos(self, texto):
        """Convierte el texto en un hash SHA-256."""
        return hashlib.sha256(texto.encode("utf-8")).hexdigest()

    def verificar_datos(self, texto, cifrado):
        """True si el hash del texto es igual al hash guardado."""
        return self.cifrar_datos(texto) == cifrado

    def validar_privacidad(self, contrasena):
        """True si tiene 8+ caracteres, al menos una letra y al menos un número."""
        tiene_letra = any(c.isalpha() for c in contrasena)
        tiene_numero = any(c.isdigit() for c in contrasena)
        return len(contrasena) >= 8 and tiene_letra and tiene_numero