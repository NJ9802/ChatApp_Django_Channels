const $imagen = document.querySelector("#profile_picture"),
		$calidad = 10,
		$imagenPrevisualizar = document.querySelector("#imagenPrevisualizar");
	const comprimirImagen = (imagenComoArchivo, porcentajeCalidad) => {
		/*
			https://parzibyte.me/blog
		*/
		return new Promise((resolve, reject) => {
			const $canvas = document.createElement("canvas");
			const imagen = new Image();
			imagen.onload = () => {
				$canvas.width = imagen.width;
				$canvas.height = imagen.height;
				$canvas.getContext("2d").drawImage(imagen, 0, 0);
				$canvas.toBlob(
					(blob) => {
						if (blob === null) {
							return reject(blob);
						} else {
							resolve(blob);
						}
					},
					"image/jpeg",
					porcentajeCalidad / 100
				);
			};
			imagen.src = URL.createObjectURL(imagenComoArchivo);
		});
	};

	document.querySelector("#profile_picture").addEventListener("change", async () => {
        const archivo = $imagen.files[0];
        const blob = await comprimirImagen(archivo, parseInt($calidad));
        $imagenPrevisualizar.src = URL.createObjectURL(blob);
        $imagenPrevisualizar.hidden = false;
        

        if ($imagen.files[0].size > 400000) {
            if ($imagen.files.length <= 0) {
                return;
            }
            // Ya puedes subir este archivo con FormData por ejemplo:
            //https://parzibyte.me/blog/2018/11/06/cargar-archivo-php-javascript-formdata/ 
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(new File ([blob], archivo.name, {
                type: archivo.type,
            }));
            $imagen.files = dataTransfer.files
        };
	});

