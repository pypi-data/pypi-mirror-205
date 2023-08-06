1. bajar el repositorio
      - git clone https://github.com/soypedroamaya/docker-ubuntu-python-pkgs.git    
2. nos metemos dentro del repo
      - cd docker-ubuntu-python-pkgs
3. construimos la imagen
      - docker build -t img-docker-ubuntu-python-pkgs .

4. construimos el contenedor basado en la imagen, con interaccion en la terminal y pegada a nuestro directorio local 
      - docker run --name cnt-docker-ubuntu-python-pkgs -it -v $(pwd):/docker-ubuntu-python-pkgs img-docker-ubuntu-python-pkgs bash

4.1 nos conectamos desde visual studio y con la extension "dev containers" a nuestro contenedor corriendo

5. nos movemos a la rama que necesitemos:
    - git checkout exp

6. creamos el entorno virtual de la rama
    - python3.10 -m venv exp

7. activamos el entorno virtual anterior
    - source exp/bin/activate

8. bajamos las librerias necesarias y que estan segun la rama
    - pip install --no-cache-dir -r requirements.txt

    - (opcional) => pip freeze > requirements.txt
    nota: para sacar una lista con las versiones exactas de las librerias que ocupa ese entorno.

9. creamos las librerias externas
    - npm install

------- conf de sphinx ----
mkdir docs -> en la raiz del proyecto
cd docs
sphinx-quickstart -> llenar las preguntas (aqui me quede...)
cd .. -> te salis hasta el directorio raiz
sphinx-apidoc -o docs .
cd docs

-- agregar la palabra "modules" en el archivo index.rst, en el area del toctree

make html
meter en un browser:
file:///Volumes/MicroSD4GB/Codigo/public/soypedroamaya/docker-ubuntu-python-pkgs/docs/_build/html/index.html


-- commitizen
primera vez
    cz bump --yes --changelog  

python setup.py bdist_wheel sdist

pip install . (para probarlo localmente en un env)

twine check dist/* (para probar que todo este bien)
twine upload -r testpypi dist/*


twine upload dist/*