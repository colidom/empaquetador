"""
Autor: colidom
Versión: 1.0
Desc: Empaqueta contenido de carpeta expluyendo todo lo especificado en el set (ignore),
añade automáticamente versión en el nombre del zip
"""
import os, shutil, logging, tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


def get_version(file: Path) -> str | None:
    """Función para coger la versión del fichero config.xml"""
    tree = ET.parse(file)
    root = tree.getroot()
    version = root[2].text

    return version if version else None


def make_package(suffix=None):
    """
    Empaqueta el contenido de la ruta desde donde es llamado el script,
    guarda el zip final en el directorio releases.
    Recibe un string como parámetro(suffix) para añadirlo al nombre del
    fichero comprimido (resultado 'package_1.0.0-sufix.zip).
    """
    # Obtenemos el directorio actual
    this_dir = os.getcwd()

    with tempfile.TemporaryDirectory() as tmpdir:
        shutil.copytree(
            os.path.join(this_dir, os.getcwd()),
            os.path.join(tmpdir, 'package'),
            # Metemos en una tupla los directorios a ignorar
            ignore=shutil.ignore_patterns(
                # Files
                '.gitignore',
                'package.log',
                'secret.hash.php',
                'secret.iv.php',
                '.prettierrc',
                '*.code-workspace',
                # Folders
                '.git',
                '.vscode',
                '.mypy_cache',
                '.scannerwork',
                'phpdoc',
                'releases',
                'documentation',
                'empaquetador',
                'testing',
                'bin',
            ),
        )
        # Añadimos un parámetro(string) al nombre del zip cuando llamamos a make_package()
        # Resultado 'package_1.0.0-sufix.zip
        zip_name = 'package' + get_version('config.xml')
        if suffix:
            zip_name += '-' + suffix

        # Iniciamos logs
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s : %(levelname)s : %(message)s',
            filename='package.log',
            filemode='w',
        )
        logging.info("Inicio del proceso")

        releases_dir = os.path.join(os.getcwd(), 'releases')

        # Empaquetamos
        print("Espere, estamos empaquetando...")
        shutil.make_archive(
            os.path.join(releases_dir, zip_name),
            'zip',
            tmpdir,
            base_dir="empaquetador",
            logger=logging,
        )

        # Finalizamos logs
        logging.info(f"Generado paquete '{zip_name}.zip' en la ruta {releases_dir}")
        logging.info("Fin del proceso.")

        print(
            f"""
       ------------------------------------------------------------------
        Generado paquete '{zip_name}.zip' en la ruta:
        {releases_dir}
       ------------------------------------------------------------------
       """
        )


# Llamamos a la función empaquetadora
make_package()
