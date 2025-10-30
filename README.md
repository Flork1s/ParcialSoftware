este proyecto es acerca de la gestion entre 
estudiante y los cursos, cada uno con sus 
respectivos datos.
1. Se tendra que crear como minimo un curso
ya que sin este curso no se podran agregar estudiantes 
ya que es mandatorio el id del curso
2. Ya despues de haber creado un curso
se puede adicionar los estudiantes que
se necesite
3. Los cursos podran tener tantos estudiantes como se necesite pero los estudiantes solo pueden estar matriculados a un solo curso no pueden estar dos al mismo tiempo
4. Ya despues se pueden los otros metodos ya seria para eliminar o editar un curso o estudiante
5. Si se elimina un curso los estudiantes que estan ahi seran desmatriculados del curso y podran ser matriculados a otro diferente


Primero

ve a la terminar y crea un directorio
mkdir <nombre>
cd <nombre>
ya al estar en la carpeta ejecuta
git clone <link repo> .

abre visual studio

crea el virtual enviroment 
py -m venv <nombre>

activalo 
venv\Scripts\Activate.ps1 (windows)

instala los requerimientos

pip install -r requirements.txt

ejecuta el servidor
fastapi devn main.py

