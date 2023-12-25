import os
from PIL import Image

def get_exif_data(filename):
    """
    Obtém os dados EXIF de um arquivo de imagem.

    Args:
        filename: O nome do arquivo de imagem.

    Returns:
        Um dicionário com os dados EXIF do arquivo.
    """

    with Image.open(filename) as img:
        exif = img.getexif()
    return exif

def main():
    """
    Programa principal.
    """

    geo_ref_folder = "geo_ref_folder"
    exif_datas = {}

    for filename in os.listdir(geo_ref_folder):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            exif = get_exif_data(os.path.join(geo_ref_folder, filename))
            if exif is not None:
                latitude = exif.get(2986)
                longitude = exif.get(2987)
                timestamp = exif.get(36867)
                if not latitude == None and not longitude == None:
                    exif_datas[filename] = {"latitude": latitude, "longitude": longitude, "timestamp": timestamp}

    for data in exif_datas:
        print(data)

if __name__ == "__main__":
    main()